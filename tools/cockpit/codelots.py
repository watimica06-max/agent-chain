"""The « Code » tab — cockpit 1.5: /8_code, lot by lot.

What a lot is, its state, its passes, its blocking files and its commits,
each read the way the command and its agents read or write them. Every rule
carries the id `code_rules.md` lists it under, with its lines; a test checks
that each cited line still says what the rule reads. A state or a field no
rule gives is « inconnu », never guessed.

Reads the files, the stats store (the agent passes), and git read-only
(`git log`). During a run the files live in the run's worktree: they are
read there (code_rules.md, `W-LIVE`).
"""
import os
import re
import sqlite3
import statistics
import subprocess
from pathlib import Path

import blocking
import scan as scan_mod
import textfile

PAS_COMMENCE, ENTAME, EN_COURS, PASSE, ECHOUE, TROIS, ANNULE, BLOQUE, REDECOUPE, INCONNU = (
    "pas commencé", "entamé", "en cours", "passé", "échoué", "échoué 3 fois", "annulé", "bloqué",
    "redécoupé", "inconnu")
CAP = 3                      # cmd/8_code.md:297-299 — three codings, the first included
FIELDS = ("Anchor", "Needs", "Produces", "Modifies", "Touches")
# Requests an agent of the lot writes to the Architecte, named by the lot.
REQUEST = re.compile(r"^(concepteur|testeur|realisateur|detailleur|arbitre)-(lot-[A-Za-z0-9]+?)"
                     r"(?:-blocking-\d+)?(?:-\d+)?\.md$")
BLOCKED = re.compile(r"^blocked_([A-Za-z0-9_]+?)(?:-(\d+))?\.md$")
DETAILLEUR_ENTRY = re.compile(r"^## Blocking (\d+)\s*[—–-]+\s*(lot-[A-Za-z0-9]+)\b")
GIT_TIMEOUT = 20

# Every rule, with the lines it comes from (code_rules.md is the same table).
RULES = {
    "L-ORDRE": "8_code.md:38-39 · agents/verificateur.md:107-115",
    "L-TITRE": "agents/cadreur.md:848-854",
    "E-PASSE": "8_code.md:80-82 · agents/relecteur.md:116",
    "E-ECHOUE": "8_code.md:262-264",
    "E-TROIS": "8_code.md:318-320",
    "E-ANNULE": "8_code.md:163-165 · agents/relecteur.md:183-186",
    "E-BLOQUE": "8_code.md:348-355 · 8_code.md:748-758",
    "E-REDEC": "8_code.md:630-633 · 8_code.md:667-670",
    "E-ENTAME": "8_code.md:158-159 · 8_code.md:174-176",
    "E-AFAIRE": "8_code.md:158-159",
    "E-ENCOURS": "8_code.md:605-606 · 8_code.md:80-82",
    "E-INCONNU": "aucune règle : un verdict sans « ## Status » lisible",
    "T-ESSAIS": "8_code.md:318-320 · 8_code.md:322-323 · 8_code.md:331-336 · agents/relecteur.md:173-175",
    "P-ORDRE": "8_code.md:158-159 · 8_code.md:174-176 · 8_code.md:190",
    "P-ECRIT": "agents/detailleur.md:55-56 · agents/relecteur.md:140 · agents/concepteur.md:301-304 · "
               "agents/realisateur.md:715",
    "P-ARBITRE": "8_code.md:760-763 · agents/realisateur.md:342-349 · agents/detailleur.md:381-388",
    "P-ARCHITECTE": "8_code.md:488-492 · agents/arbitre.md:476-486",
    "P-DEMANDES": "agents/concepteur.md:227-230 · agents/realisateur.md:466 · agents/detailleur.md:421 · "
                  "agents/detailleur.md:439-440 · agents/arbitre.md:451-460",
    "B-OU": "8_code.md:748-758 · agents/detailleur.md:328-331",
    "C-GREP": "8_code.md:198-201 · 8_code.md:217-220",
    "C-DOSSIER": "agents/concepteur.md:301-304 · agents/testeur.md:315-316 · agents/realisateur.md:715-718",
    "W-LIVE": "8_code.md:126-128 · 8_code.md:135-136 · 8_code.md:470-475",
    "A-LOT": "8_code.md:605-606 · 8_code.md:564 · 8_code.md:573 · 8_code.md:582 · 8_code.md:597 · 8_code.md:442",
    "A-DESC": "8_code.md:563 · 8_code.md:572 · 8_code.md:581 · 8_code.md:596 · agents/realisateur.md:346-348",
    "A-BLOC": "8_code.md:418-419 · 8_code.md:440-441 · agents/detailleur.md:385-387",
    "A-DOSSIER": "8_code.md:608-609",
    "A-AUCUN": "8_code.md:509-510",
    "A-IMBRIQUE": "agents/realisateur.md:342-349 · agents/arbitre.md:476-486",
    "D-ESTIME": "demande 1.5, §4 : la médiane des lots passés de la feature",
}

STATE_RULE = {PAS_COMMENCE: "E-AFAIRE", ENTAME: "E-ENTAME", EN_COURS: "E-ENCOURS", PASSE: "E-PASSE",
              ECHOUE: "E-ECHOUE", TROIS: "E-TROIS", ANNULE: "E-ANNULE", BLOQUE: "E-BLOQUE",
              REDECOUPE: "E-REDEC", INCONNU: "E-INCONNU"}


# ------------------------------------------------------------ the folder

def work_path(app, feature, folder):
    return os.path.join(app, "docs", "features", feature, *([folder] if folder else []))


def work_rel(feature, folder):
    return "/".join(["docs", "features", feature] + ([folder] if folder else []))


def live_folder(app, feature, folder, worktrees):
    """During a run, the working folder inside the run's worktree, where the
    agents write (`W-LIVE`): `.claude/worktrees/<feature>` first, then any
    live worktree holding it. (worktree, path) or (None, None)."""
    rel = work_rel(feature, folder).split("/")
    named = os.path.normcase(os.path.join(app, ".claude", "worktrees", feature))
    for wt in sorted(worktrees or [], key=lambda w: os.path.normcase(os.path.realpath(w)) != named):
        p = os.path.join(wt, *rel)
        if os.path.isdir(os.path.join(p, "code")):
            return wt, p
    return None, None


def decoupage(W):
    """`## lot-NN` sections of `code/decoupage.md`, their five fields (`L-TITRE`)."""
    out = {}
    p = W.p("code", "decoupage.md")
    if not os.path.isfile(p):
        return out
    cur = None
    for line in W.lines(p):
        m = re.match(r"^## (lot-[A-Za-z0-9]+)\s*$", line)
        if m:
            cur = out.setdefault(m.group(1), {})
            continue
        if line.startswith("## "):
            cur = None
            continue
        if cur is not None:
            m = re.match(r"^(Anchor|Needs|Produces|Modifies|Touches):\s*(.*)$", line)
            if m:
                cur[m.group(1)] = m.group(2).strip()
    return out


def blocks(W):
    """`## Blocks` of the sequence: block name → its lots (`L-ORDRE`)."""
    if not W.has("code", "sequence.md"):
        return []
    out = []
    for line in scan_mod.section(W.lines(W.p("code", "sequence.md")), "Blocks"):
        m = re.match(r"^\s*(block-[A-Za-z0-9]+)\s*:\s*(.*)$", line)
        if m:
            out.append({"name": m.group(1), "lots": scan_mod.LOT_ID.findall(m.group(2))})
    return out


def _files_of_lot(W, lot):
    d = W.p("code", lot)
    try:
        return sorted(os.listdir(d))
    except OSError:
        return []


def _blocking_history(W, lot, names):
    """Every blocking file of the lot, settled (`-NN`) or not, in its folder,
    and the Détailleur's entries naming it at the split's root (`B-OU`)."""
    out = []
    for n in names:
        m = BLOCKED.match(n)
        if m:
            out.append({"rel": f"code/{lot}/{n}", "agent": m.group(1), "archived": bool(m.group(2))})
    code = W.p("code")
    try:
        root = sorted(os.listdir(code))
    except OSError:
        root = []
    for n in root:
        m = BLOCKED.match(n)
        if not m or m.group(1) != "detailleur":
            continue
        try:
            lines = textfile.load(os.path.join(code, n)).lines
        except textfile.UnreadableFile:
            continue
        nums = [int(x.group(1)) for x in (DETAILLEUR_ENTRY.match(l) for l in lines) if x and x.group(2) == lot]
        if nums:
            out.append({"rel": f"code/{n}", "agent": "detailleur", "archived": bool(m.group(2)), "entries": nums})
    return out


def _requests(W, lot):
    """The requests to the Architecte named by the lot (`P-DEMANDES`), each
    with whether its `## Verdict` is written."""
    d = W.p("architecte")
    out = []
    try:
        names = sorted(os.listdir(d))
    except OSError:
        return out
    for n in names:
        m = REQUEST.match(n)
        if not m or m.group(2) != lot:
            continue
        p = os.path.join(d, n)
        lines = W.lines(p)
        idx = [i for i, l in enumerate(lines) if l.strip() == "## Verdict"]
        answered = bool(idx) and not blocking.decision_empty_a2(lines, idx[-1])
        out.append({"rel": f"architecte/{n}", "by": m.group(1), "answered": answered})
    return out


# ---------------------------------------------------------------- the lots

def read_lots(app, feature, folder="", worktrees=(), passes=None, run=None, opens=None):
    """Every lot of the sequence with its state. `passes`: the stored agent
    passes of the feature (store_passes). `run`: the run going, its snapshot.
    `opens`: the blocking entries waiting on her, as « À répondre » has them."""
    wt, live = live_folder(app, feature, folder, worktrees)
    base = live or work_path(app, feature, folder)
    W = scan_mod.Folder(base)
    out = {"folder": folder, "work": work_rel(feature, folder), "source": "worktree" if live else "dossier",
           "worktree": wt, "exists": W.has("code", "sequence.md"), "lots": [], "blocks": [],
           "rules": RULES}
    if not out["exists"]:
        out["why"] = "Pas de code/sequence.md : /7_lots n'a pas encore découpé ce dossier."
        return out
    order = scan_mod.lot_order(W)
    # `## Defects` carrying lines — `None.` is a line: /8_code stops and sends
    # to /7_lots (8_code.md:92-93, scan rule COD-2). The lots are shown all the same.
    out["defects"] = [l.strip() for l in scan_mod.section(W.lines(W.p("code", "sequence.md")), "Defects")
                      if l.strip()] or None
    split = decoupage(W)
    bl = blocks(W)
    block_of = {lot: b["name"] for b in bl for lot in b["lots"]}
    redec = W.has("code", "redecoupage.md")
    mine = [p for p in (passes or []) if (p.get("folder") or "") == folder and p.get("folder") is not None]
    current = _current(run, feature, folder, order, W)
    waiting = {}
    for e in opens or []:
        rel = e.get("rel", "")
        head = rel.split("/")[0]
        if (head if scan_mod.BUGFIX.match(head) else "") != folder:
            continue
        lot = e.get("lot") or _lot_of_rel(rel, folder)
        if lot:
            waiting.setdefault(lot, []).append(e["id"])
    passed = 0
    for i, lot in enumerate(order):
        names = _files_of_lot(W, lot)
        v = scan_mod.lot_verdict(W, lot)
        row = {"lot": lot, "index": i + 1, "block": block_of.get(lot),
               "fields": split.get(lot), "title": (split.get(lot) or {}).get("Anchor"),
               "files": [n for n in names if n.endswith(".md")],
               "verdict": None, "blocking": waiting.get(lot, [])}
        if v:
            row["verdict"] = {"status": v["status"] or None, "attempts": v["attempts"],
                              "attempts_written": v["attempts_written"], "cause": v["cause"] or None,
                              "causes_so_far": v["causes_so_far"] or None}
        state, detail = _state(lot, v, names, redec, row["blocking"], current)
        if v and v["pass"]:
            passed += 1
        row["state"], row["detail"], row["rule"] = state, detail, STATE_RULE[state]
        row["attempts"] = {"used": v["attempts"] if v else 0, "cap": CAP,
                           "note": None if not v else (None if v["attempts_written"] else
                                   "pas de ## Attempts dans le verdict : lu comme 1 (8_code.md:322-323)")}
        lp = [p for p in mine if p.get("lot") == lot]
        row["passes"] = [_pass_row(p) for p in lp]
        hist = _blocking_history(W, lot, names)
        reqs = _requests(W, lot)
        arb_files = [h for h in hist if h["agent"] in ("realisateur", "detailleur")]
        row["arbitre"] = {"passes": sum(1 for p in lp if p.get("agent") == "arbitre"), "files": arb_files} \
            if (arb_files or any(p.get("agent") == "arbitre" for p in lp)) else None
        row["architecte"] = {"passes": sum(1 for p in lp if p.get("agent") == "architecte"), "requests": reqs} \
            if (reqs or any(p.get("agent") == "architecte" for p in lp)) else None
        row["duration_s"] = _lot_duration(lp)
        out["lots"].append(row)
    out["blocks"] = bl
    out["total"], out["passed"] = len(order), passed
    out["current"] = current
    out["redecoupage"] = "code/redecoupage.md" if redec else None
    out["outside"] = sorted(n for n in _dirs(W.p("code")) if re.match(r"^lot-", n) and n not in order)
    out["block_passes"] = [_pass_row(p) for p in mine if not p.get("lot") and p.get("block")]
    out["unknown_passes"] = [_pass_row(p) for p in mine if not p.get("lot") and not p.get("block")]
    out["estimate"] = estimate(out["lots"], len(order) - passed)
    arch = W.p("blocked_architecte.md")
    out["architecte_blocked"] = "blocked_architecte.md" if os.path.isfile(arch) else None
    return out


def _dirs(p):
    try:
        return [n for n in os.listdir(p) if os.path.isdir(os.path.join(p, n))]
    except OSError:
        return []


def _lot_of_rel(rel, folder):
    parts = rel.split("/")
    if folder and parts and parts[0] == folder:
        parts = parts[1:]
    elif parts and scan_mod.BUGFIX.match(parts[0]):
        return None
    if len(parts) >= 3 and parts[0] == "code" and parts[1].startswith("lot-"):
        return parts[1]
    return None


def _state(lot, v, names, redec, waiting, current):
    """One lot's state, by the command's own tests, in this order."""
    if current and current.get("lot") == lot:
        how = "d'après le flux" if current.get("from") == "flux" else "d'après la règle de 8_code.md:80-82"
        return EN_COURS, f"{current.get('agent') or 'l’orchestrateur'} y travaille ({how})"
    if waiting:
        return BLOQUE, "une décision vous attend"
    if v and v["pass"]:
        return PASSE, "avec réserve" if "reservation" in v["status"].lower() else None
    if redec:
        return REDECOUPE, "code/redecoupage.md : le lot repart au découpage"
    if v:
        if not v["lines"] or not v["status"]:
            return INCONNU, "verdict.md sans « ## Status » lisible"
        if v["attempts"] >= CAP:
            return TROIS, f"{v['attempts']} codages : le lot est à vous"
        if v["cause"] == "sheet" and "fiche-executable.md" not in names:
            return ANNULE, "cause « sheet » : les commits sont annulés, la fiche est à réécrire"
        return ECHOUE, f"{v['status']}" + (f" · cause : {v['cause']}" if v["cause"] and v["cause"] != "—" else "")
    if "fiche-executable.md" not in names:
        if any(n in names for n in ("conception.md", "tests.md", "compte-rendu.md")):
            return ENTAME, "pas de fiche : le Détailleur la réécrit"
        return PAS_COMMENCE, None
    for f, who in (("conception.md", "concepteur"), ("tests.md", "testeur"), ("compte-rendu.md", "réalisateur")):
        if f not in names:
            return ENTAME, f"fiche écrite · reprend au {who}"
    return ENTAME, "codé, pas encore relu · reprend au relecteur"


def _current(run, feature, folder, order, W):
    """The lot a /8_code run going works on: the lot its running agents'
    input names (`A-LOT`), else, when none does, the next lot by the
    command's rule (`E-ENCOURS`). None when no /8_code runs on this folder."""
    if not run or run.get("status") == "ended" or run.get("command") != "8_code":
        return None
    if (run.get("work") or feature).split("/")[0] != feature:
        return None
    bfs = sorted((n for n in _dirs(work_path_from(W.path, folder)) if scan_mod.BUGFIX.match(n)),
                 key=lambda n: int(scan_mod.BUGFIX.match(n).group(1)))
    acts_on = bfs[-1] if bfs else ""
    if folder != acts_on:
        return None
    active = run.get("active") or []
    named = [a for a in active if a.get("lot")]
    if named:
        a = named[-1]
        chain = " → ".join(x["agent"] for x in active if x.get("lot") == a["lot"])
        return {"lot": a["lot"], "agent": chain or a["agent"], "from": "flux"}
    agent = active[-1]["agent"] if active else None
    for lot in order:
        v = scan_mod.lot_verdict(W, lot)
        if not (v and v["pass"]):
            return {"lot": lot, "agent": agent, "from": "regle"}
    return None


def work_path_from(path, folder):
    """The feature folder, from a working folder's path."""
    return os.path.dirname(path) if folder else path


def _pass_row(p):
    read = None
    if p.get("input_tokens") is not None:
        read = (p.get("input_tokens") or 0) + (p.get("cache_read_tokens") or 0) + (p.get("cache_creation_tokens") or 0)
    return {"id": p.get("id"), "run_id": p.get("run_id"), "agent": p.get("agent"),
            "description": p.get("description"), "model": p.get("model"), "parent": p.get("parent_tool_use_id"),
            "started_at": p.get("started_at"), "ended_at": p.get("ended_at"), "duration_s": p.get("duration_s"),
            "read_tokens": read, "output_tokens": p.get("output_tokens"), "lot": p.get("lot"),
            "block": p.get("block"), "run_command": p.get("run_command"), "live": bool(p.get("live"))}


def _lot_duration(passes):
    """A lot's time: the sum of its top-level passes — a nested one (the
    Arbitre in a Réalisateur) runs inside its caller's. None when one of
    them has no duration, or there is none."""
    top = [p for p in passes if not p.get("parent_tool_use_id")]
    if not top or any(p.get("duration_s") is None for p in top):
        return None
    return round(sum(p["duration_s"] for p in top), 3)


def estimate(lots, left):
    """« ≈ 40 min »: the median time of this folder's passed lots times the
    lots left — only once two passed lots have a known time (`D-ESTIME`)."""
    known = [r["duration_s"] for r in lots if r["state"] == PASSE and r["duration_s"] is not None]
    if len(known) < 2 or left <= 0:
        return {"shown": False, "lots_known": len(known), "left": left}
    med = statistics.median(known)
    return {"shown": True, "lots_known": len(known), "left": left, "median_s": med, "eta_s": med * left}


# --------------------------------------------------------------- a lot opened

def lot_detail(app, feature, folder, lot, worktrees=(), passes=None):
    wt, live = live_folder(app, feature, folder, worktrees)
    base = live or work_path(app, feature, folder)
    W = scan_mod.Folder(base)
    if lot not in scan_mod.lot_order(W):
        return None
    out = {"lot": lot, "folder": folder, "source": "worktree" if live else "dossier", "worktree": wt}
    sheet = W.p("code", lot, "fiche-executable.md")
    out["sheet"] = _doc(sheet)
    v = scan_mod.lot_verdict(W, lot)
    out["verdict"] = None
    if v:
        lines = v["lines"]
        out["verdict"] = {"lines": lines, "status": v["status"] or None, "attempts": v["attempts"],
                          "attempts_written": v["attempts_written"], "cause": v["cause"] or None,
                          "causes_so_far": v["causes_so_far"] or None,
                          "findings": _section_text(lines, "Findings"),
                          "verified": _section_text(lines, "Verified"),
                          "divergences": _section_text(lines, "Symbol divergences")}
    names = _files_of_lot(W, lot)
    out["reports"] = [n for n in ("conception.md", "tests.md", "compte-rendu.md") if n in names]
    out["blocking"] = _blocking_history(W, lot, names)
    out["requests"] = _requests(W, lot)
    out["commits"] = commits(wt or app, work_rel(feature, folder), lot)
    lp = [p for p in (passes or []) if p.get("lot") == lot and (p.get("folder") or "") == folder
          and p.get("folder") is not None]
    out["passes"] = sorted((_pass_row(p) for p in lp), key=lambda p: p["started_at"] or "")
    return out


def _doc(path):
    if not os.path.isfile(path):
        return {"exists": False, "lines": []}
    try:
        return {"exists": True, "lines": textfile.load(path).lines}
    except textfile.UnreadableFile as e:
        return {"exists": True, "lines": [], "error": str(e)}


def _section_text(lines, title):
    body = scan_mod.section(lines, title)
    text = "\n".join(body).strip()
    return text or None


def commits(repo, work, lot):
    """The lot's commits, read-only (`C-GREP`): `<lot>: ` and `Revert
    "<lot>: ` messages, newest first, each with the files it changed. A
    lot's name is reused by every split, so a commit is this folder's when it
    touches `<work>/code/<lot>/` (`C-DOSSIER`), another folder's when it
    touches another one — left out —, and « sans dossier » otherwise."""
    fmt = "%x1e%H%x1f%h%x1f%aI%x1f%s"
    try:
        out = subprocess.run(["git", "-C", repo, "log", "-E", f"--grep=^(Revert \")?{re.escape(lot)}: ",
                              f"--format={fmt}", "--name-only"],
                             capture_output=True, text=True, encoding="utf-8", errors="replace",
                             timeout=GIT_TIMEOUT, stdin=subprocess.DEVNULL)
    except (OSError, subprocess.SubprocessError) as e:
        return {"error": f"git log n'a pas répondu : {e}", "list": []}
    if out.returncode != 0:
        err = (out.stderr or "").strip()
        if "not a git repository" in err:
            err = "Ce dossier n'est pas dans un dépôt git : les commits ne se lisent pas."
        return {"error": err or f"git log : code {out.returncode}", "list": []}
    mine_prefix = f"{work}/code/{lot}/"
    other = re.compile(r"^docs/features/[^/]+(?:/bugfix-\d+)?/code/" + re.escape(lot) + "/")
    found, elsewhere = [], 0
    for chunk in out.stdout.split("\x1e"):
        chunk = chunk.strip("\n")
        if not chunk:
            continue
        head, _, rest = chunk.partition("\n")
        parts = head.split("\x1f")
        if len(parts) < 4:
            continue
        files = [f for f in rest.splitlines() if f.strip()]
        subject = parts[3]
        if not (subject.startswith(f"{lot}: ") or subject.startswith(f'Revert "{lot}: ')):
            continue
        here = any(f.startswith(mine_prefix) for f in files)
        there = any(other.match(f) and not f.startswith(mine_prefix) for f in files)
        if there and not here:
            elsewhere += 1
            continue
        found.append({"sha": parts[0], "short": parts[1], "at": parts[2], "subject": subject,
                      "revert": subject.startswith("Revert "), "files": files,
                      "where": "dossier" if here else "sans dossier"})
    reverted = {c["subject"][len('Revert "'):-1] for c in found if c["revert"] and c["subject"].endswith('"')}
    for c in found:
        c["reverted"] = (not c["revert"]) and c["subject"] in reverted
    return {"list": found, "elsewhere": elsewhere, "error": None}


# ------------------------------------------------------------ the passes

def store_passes(store_path, feature):
    """The agent passes of the feature's runs, from stats.sqlite, read-only."""
    if not store_path or not os.path.isfile(store_path):
        return []
    try:
        db = sqlite3.connect(Path(os.path.abspath(store_path)).as_uri() + "?mode=ro", uri=True, timeout=10)
    except sqlite3.Error:
        return []
    try:
        db.row_factory = sqlite3.Row
        cols = {r["name"] for r in db.execute("PRAGMA table_info(agent_passes)")}
        if "lot" not in cols:
            return []
        return [dict(r) for r in db.execute(
            "SELECT a.*, r.command AS run_command FROM agent_passes a JOIN runs r ON r.id = a.run_id"
            " WHERE r.feature = ? ORDER BY a.started_at, a.id", (feature,))]
    except sqlite3.Error:
        return []
    finally:
        db.close()
