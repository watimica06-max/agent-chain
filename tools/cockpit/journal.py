"""Le journal de cycle — cockpit 1.20.

For a feature, and for each of its correction cycles, what happened step
by step: one line per command the cockpit ran — a click, a programme's,
« Continuer » —, appended to `docs/features/<feature>/journal.md` (the
`bugfix-NN/journal.md` of a correction cycle), committed `journal:
<command> — <outcome>` and pushed as the cockpit's other commits (1.12).
Kept in the application's repository: both computers see all of it.

The format is the cockpit's alone, written here and nowhere else — never in
`.claude/formats/`: no agent of the chain reads the journal, and none is
ever given it to read. A markdown table: readable on GitHub as it is, and
parsed back here row by row.

From the lines, the git history of the cycle's folder and, on this
computer, the stats and the run logs, the journal computes (§2): each
questions file — created, answered, how long she took —; each blocking
file — created, settled, and by whom when it can be told —; the
programmes; the « Lancer quand même ». Then the points à creuser (§3),
the reconstruction of the runs before 1.20, and the end-of-cycle report.
"""
import os
import re
import socket
import statistics
import subprocess
from datetime import datetime

import blocking as blocking_mod
import nextline
import questions as questions_mod
import sync as sync_mod

FILE = "journal.md"
REPORT = "rapport-cycle.md"
MESSAGE = "journal: {command} — {outcome}"
PENDING_MESSAGE = "journal: lignes en attente"
REBUILD_MESSAGE = "journal: reconstitution du passé ({n} lignes)"
REPORT_MESSAGE = "journal: rapport de fin de cycle"
UNKNOWN = "inconnu"
OVERRIDE_NOTE = "lancé quand même (seuil de blocage)"
NONE = "—"
COLUMNS = ("Quand", "Ordinateur", "Commande", "Durée", "Tokens", "5 h", "Semaine", "Issue", "Ensuite",
           "Créés", "Programme", "Note")
INTRO = ("Écrit par le cockpit : une ligne par commande lancée depuis lui — un clic, un programme, "
         "« Continuer ». Aucun agent de la chaîne ne le lit.")

# The outcomes, as the « Issue » column says them.
DONE, QUESTIONS, BLOCKING, BOTH, MANUAL, STOP, NO_NEXT, ERROR, STOPPED, NOT_LOGGED = (
    "fait", "questions", "blocage", "questions et blocage", "à la main", "arrêt de la chaîne", "sans Next",
    "erreur", "arrêté", "pas connecté")
FAILED = {ERROR, NOT_LOGGED}

# Paramètres → Journal (§3): the thresholds of the points à creuser.
DEFAULT_THRESHOLDS = {"cost_factor": 2.0, "repeat_runs": 3, "blocking_repeat": 2}
LIMITS = {"cost_factor": (1.1, 10.0), "repeat_runs": (2, 20), "blocking_repeat": (2, 20)}

# The cockpit's own commits, and the chain's commits before a worktree —
# what the Product Owner wrote, committed from the main checkout.
PO_PREFIXES = ("chore: answers", "chore: pre-", "donnees:")
COCKPIT_PREFIXES = ("journal:", "chain:", "deploy:", "donnees:", "chore:")
MERGE = re.compile(r"^Merge (/[A-Za-z0-9_]+)(?:\s+(.*))?$")
BUGFIX = re.compile(r"^bugfix-\d+$")


def clean_thresholds(raw):
    out = dict(DEFAULT_THRESHOLDS)
    for k, (lo, hi) in LIMITS.items():
        v = (raw or {}).get(k)
        if v is None or v == "":
            continue
        try:
            v = float(v)
        except (TypeError, ValueError):
            raise ValueError(f"{k} : un nombre est attendu")
        if not lo <= v <= hi:
            raise ValueError(f"{k} : entre {lo:g} et {hi:g}")
        out[k] = v if k == "cost_factor" else int(v)
    return out


def computer_name():
    return os.environ.get("COMPUTERNAME") or socket.gethostname() or UNKNOWN


# ------------------------------------------------------------ the cycle

def cycle_rel(feature, cycle="main"):
    """The cycle's folder, from the repository's root, with `/`."""
    base = f"docs/features/{feature}"
    return base if not cycle or cycle == "main" else f"{base}/{cycle}"


def journal_path(app, feature, cycle="main"):
    return os.path.join(app, *cycle_rel(feature, cycle).split("/"), FILE)


def report_path(app, feature, cycle="main"):
    return os.path.join(app, *cycle_rel(feature, cycle).split("/"), REPORT)


def cycles(app, feature):
    """« main », then each `bugfix-NN/`, in order."""
    d = os.path.join(app, "docs", "features", feature)
    try:
        names = sorted(n for n in os.listdir(d) if BUGFIX.match(n) and os.path.isdir(os.path.join(d, n)))
    except OSError:
        names = []
    return ["main", *names]


# ------------------------------------------------------------ formatting

def fmt_duration(s):
    if s is None:
        return UNKNOWN
    s = int(round(s))
    h, m, r = s // 3600, (s % 3600) // 60, s % 60
    if h:
        return f"{h} h {m:02d} min"
    if m:
        return f"{m} min {r:02d} s"
    return f"{r} s"


def parse_duration(text):
    t = (text or "").strip()
    m = re.fullmatch(r"(?:(\d+) h)?\s*(?:(\d+) min)?\s*(?:(\d+) s)?", t)
    if not t or t == UNKNOWN or not m or not any(m.groups()):
        return None
    h, mi, s = (int(x) if x else 0 for x in m.groups())
    return h * 3600 + mi * 60 + s


def _int(n):
    return f"{n:,}".replace(",", " ")


def fmt_tokens(read, wrote):
    if read is None and wrote is None:
        return UNKNOWN
    a = _int(read) if read is not None else UNKNOWN
    b = _int(wrote) if wrote is not None else UNKNOWN
    return f"{a} lus · {b} écrits"


def parse_tokens(text):
    m = re.fullmatch(r"\s*([\d ]+|inconnu) lus · ([\d ]+|inconnu) écrits\s*", text or "")
    if not m:
        return None, None
    conv = (lambda x: None if x == UNKNOWN else int(x.replace(" ", "")))
    return conv(m.group(1)), conv(m.group(2))


def fmt_share(x):
    if x is None:
        return UNKNOWN
    v = round(float(x), 1)
    return (f"{v:g}" if v != int(v) else str(int(v))).replace(".", ",") + " %"


def parse_share(text):
    m = re.fullmatch(r"\s*(-?\d+(?:,\d+)?) %\s*", text or "")
    return float(m.group(1).replace(",", ".")) if m else None


def _cell(text):
    t = str(text if text not in (None, "") else NONE)
    return t.replace("\r", " ").replace("\n", " ").replace("|", "\\|").strip() or NONE


def _split_row(line):
    cells, cur, i = [], "", 0
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|") and not body.endswith("\\|"):
        body = body[:-1]
    while i < len(body):
        ch = body[i]
        if ch == "\\" and i + 1 < len(body) and body[i + 1] == "|":
            cur += "|"
            i += 2
            continue
        if ch == "|":
            cells.append(cur.strip())
            cur = ""
        else:
            cur += ch
        i += 1
    cells.append(cur.strip())
    return cells


def _blank(x):
    return None if x in (None, "", NONE) else x


def format_row(e):
    created = ", ".join(e.get("created") or []) or NONE
    when = (e.get("at") or "")[:16].replace("T", " ")
    cells = [when, e.get("computer") or UNKNOWN, e.get("command") or UNKNOWN, fmt_duration(e.get("duration_s")),
             fmt_tokens(e.get("read_tokens"), e.get("output_tokens")), fmt_share(e.get("five_hour")),
             fmt_share(e.get("seven_day")), e.get("outcome") or UNKNOWN, e.get("next") or UNKNOWN, created,
             e.get("programme"), e.get("note")]
    return "| " + " | ".join(_cell(c) for c in cells) + " |"


ROW = re.compile(r"^\|\s*\d{4}-\d{2}-\d{2} \d{2}:\d{2}\s*\|")


def parse_row(line):
    """A row of the table, back into its entry; None for any other line."""
    if not ROW.match(line or ""):
        return None
    c = _split_row(line)
    c += [""] * (len(COLUMNS) - len(c))
    read, wrote = parse_tokens(c[4])
    return {"at": c[0].replace(" ", "T"), "computer": c[1], "command": c[2], "duration_s": parse_duration(c[3]),
            "read_tokens": read, "output_tokens": wrote, "five_hour": parse_share(c[5]),
            "seven_day": parse_share(c[6]), "outcome": c[7], "next": c[8],
            "created": [x.strip() for x in c[9].split(",") if x.strip() and x.strip() != NONE],
            "programme": _blank(c[10]), "note": _blank(c[11])}


def header(feature, cycle="main"):
    title = feature if cycle in (None, "", "main") else f"{feature} / {cycle}"
    return (f"# Journal de cycle — {title}\n\n{INTRO}\n\n"
            f"| {' | '.join(COLUMNS)} |\n|{'---|' * len(COLUMNS)}\n")


def read(path):
    """The journal's entries, in the file's order; [] when it is absent."""
    try:
        with open(path, encoding="utf-8") as f:
            lines = f.read().splitlines()
    except OSError:
        return []
    return [e for e in (parse_row(l) for l in lines) if e]


def append(path, entry, feature, cycle="main"):
    """One row at the end of the file — the file and its header first when
    it is new."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        text = header(feature, cycle)
    if text and not text.endswith("\n"):
        text += "\n"
    text += format_row(entry) + "\n"
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    return format_row(entry)


def rewrite(path, entries, feature, cycle="main"):
    """The whole table again, sorted by time — the reconstruction's lines
    go before the ones the cockpit wrote since."""
    rows = sorted(entries, key=lambda e: e.get("at") or "")
    text = header(feature, cycle) + "".join(format_row(e) + "\n" for e in rows)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


# ------------------------------------------------------------ a run's line

def outcome_of(outcome, nxt, api_error=""):
    """The « Issue » of a run, from how it ended and its `Next:`."""
    if outcome == "erreur":
        return NOT_LOGGED if api_error == "authentication_failed" else ERROR
    if outcome == "interrompu":
        return STOPPED
    kind = (nxt or {}).get("kind")
    if kind == "answer":
        return {"questions": QUESTIONS, "blocking": BLOCKING}.get((nxt or {}).get("what"), BOTH)
    if kind == "manual":
        return MANUAL
    if kind == "stop":
        return STOP
    if kind == "unknown" or not nxt:
        return NO_NEXT
    return DONE


def next_text(nxt, lots=None):
    """The « Ensuite » column: what the run's `Next:` proposes, short."""
    n = nxt or {}
    kind, cmd = n.get("kind"), n.get("command")
    if kind == "run":
        out = f"/{cmd}"
    elif kind == "answer":
        out = "répondre" + (f" → /{cmd}" if cmd else "")
    elif kind == "manual":
        out = "à la main" + (f" → /{cmd}" if cmd else "")
    elif kind == "done":
        out = "fini"
    elif kind == "stop":
        out = "arrêt"
    else:
        out = UNKNOWN
    if lots:
        out += f" ({lots[0]}/{lots[1]} lots)"
    return out


def run_entry(run, usage_shares, created, programme_name=None, lots=None, note=None, computer=None):
    """The line of a run that just ended (runner.Run)."""
    u = run.usage or {}
    notes = []
    if run.resume:
        notes.append("suite de session")
    if run.outcome == "erreur" and run.error:
        notes.append("erreur : " + run.error[:160])
    if note:
        notes.append(note)
    dur = u.get("duration_s")
    if dur is None and run.started_at and getattr(run, "ended_at", ""):
        a, b = _local(run.started_at), _local(run.ended_at)
        dur = (b - a).total_seconds() if a and b else None
    return {"at": (run.started_at or "")[:16], "computer": computer or computer_name(), "command": run.prompt,
            "duration_s": dur, "read_tokens": u.get("read_tokens"),
            "output_tokens": u.get("output_tokens"), "five_hour": usage_shares.get("five_hour"),
            "seven_day": usage_shares.get("seven_day"),
            "outcome": outcome_of(run.outcome, run.next, getattr(run, "api_error", "")),
            "next": next_text(run.next, lots), "created": created, "programme": programme_name,
            "note": " · ".join(notes) or None}


def is_answer_file(rel_in_cycle):
    name = rel_in_cycle.split("/")[-1]
    parts = rel_in_cycle.split("/")
    if len(parts) == 1 and questions_mod.ROOT_FILE.match(name):
        return True
    return len(parts) == 2 and parts[0] == "convertisseur" and bool(questions_mod.TECHNIQUE_FILE.match(name))


def is_blocking_file(rel_in_cycle):
    name = rel_in_cycle.split("/")[-1]
    return bool(blocking_mod.BLOCKED_FILE.match(name)) and not blocking_mod.ARCHIVED.search(name)


def _in_cycle(path, rel):
    """`path`'s part under the cycle's folder, or None — a main cycle's
    `bugfix-NN/` belong to their own cycles."""
    if not path.startswith(rel + "/"):
        return None
    inner = path[len(rel) + 1:]
    if not rel.count("/") > 2 and BUGFIX.match(inner.split("/")[0]):
        return None
    return inner


def created_files(app, feature, cycle, before, after):
    """The questions and blocking files the run created — those git added
    between the HEAD it started on and the one it ended on, and those still
    uncommitted on the disk."""
    rel = cycle_rel(feature, cycle)
    out = []
    if before and after and before != after:
        r = sync_mod.git(app, "diff", "--name-status", "--no-renames", before, after, "--", rel)
        if r.ok:
            for line in r.out.splitlines():
                parts = line.split("\t")
                if len(parts) >= 2 and parts[0].startswith("A"):
                    inner = _in_cycle(parts[-1], rel)
                    if inner and (is_answer_file(inner) or is_blocking_file(inner)):
                        out.append(inner)
    d = sync_mod.dirty_paths(app, [rel + "/"]) or []
    for code, p in d:
        inner = _in_cycle(p.rstrip("/"), rel)
        if code == "??" and inner and (is_answer_file(inner) or is_blocking_file(inner)) and inner not in out:
            out.append(inner)
    return sorted(out)


# ------------------------------------------------------------ git

def commit(app, paths, message):
    """Commits these paths alone. (old HEAD, new HEAD) — new None when
    nothing was left to commit; raises sync.SyncError."""
    old = sync_mod.git(app, "rev-parse", "HEAD").out.strip() or None
    a = sync_mod.git(app, "add", "--", *paths)
    if not a.ok:
        raise sync_mod.SyncError(f"git add : {a.text}")
    staged = sync_mod.git(app, "diff", "--cached", "--name-only", "--", *paths)
    if not staged.out.strip():
        return old, None
    c = sync_mod.git(app, "commit", "-q", "-m", message, "--only", "--", *paths)
    if not c.ok:
        raise sync_mod.SyncError(f"git commit : {c.text}")
    return old, sync_mod.git(app, "rev-parse", "HEAD").out.strip()


def dirty_journals(app):
    """The journal files git sees changed and not committed."""
    d = sync_mod.dirty_paths(app, [":(glob)docs/features/**/" + FILE]) or []
    return sorted(p for _, p in d)


def is_journal_path(p):
    return p.rstrip("/").split("/")[-1] == FILE


# ------------------------------------------------------------ the history (§2)

def _local(iso):
    try:
        d = datetime.fromisoformat(iso)
    except (TypeError, ValueError):
        return None
    if d.tzinfo is not None:
        d = d.astimezone().replace(tzinfo=None)
    return d


def _iso(d):
    return d.isoformat(timespec="seconds") if d else None


def git_log(app, rel):
    """Every commit that touched the cycle's folder, oldest first, with what
    it changed: [{sha, parents, at, subject, changes: [(status, old, new)]}]."""
    spec = ["--", rel]
    if rel.count("/") <= 2:
        spec.append(f":(exclude,glob){rel}/bugfix-*/**")
    r = sync_mod.git(app, "log", "--reverse", "--topo-order", "--full-history", "-M", "--name-status",
                     "--format=%x1e%H%x1f%P%x1f%aI%x1f%s", *spec, timeout=60)
    if not r.ok:
        return []
    out = []
    for chunk in r.out.split("\x1e")[1:]:
        lines = chunk.strip("\n").split("\n")
        head = lines[0].split("\x1f")
        if len(head) < 4:
            continue
        c = {"sha": head[0], "parents": head[1].split(), "at": _local(head[2]), "subject": head[3], "changes": []}
        for l in lines[1:]:
            parts = l.split("\t")
            if len(parts) >= 2:
                st = parts[0]
                c["changes"].append((st[0], parts[1], parts[2] if len(parts) > 2 else parts[1]))
        out.append(c)
    return out


def _cat(app, specs):
    """`git cat-file --batch` on `<sha>:<path>`: {spec: text or None}."""
    specs = list(dict.fromkeys(specs))
    if not specs:
        return {}
    try:
        p = subprocess.run(["git", "-C", app, "cat-file", "--batch"], input=("\n".join(specs) + "\n").encode("utf-8"),
                           capture_output=True, timeout=60, env=sync_mod.env())
    except (OSError, subprocess.SubprocessError):
        return {}
    data, out, i = p.stdout, {}, 0
    for s in specs:
        nl = data.find(b"\n", i)
        if nl < 0:
            break
        head = data[i:nl].decode("utf-8", "replace").split()
        if len(head) >= 2 and head[-1] == "missing":
            out[s] = None
            i = nl + 1
            continue
        size = int(head[2]) if len(head) >= 3 and head[2].isdigit() else 0
        out[s] = data[nl + 1: nl + 1 + size].decode("utf-8", "replace")
        i = nl + 1 + size + 1
    return out


def _q_state(text):
    """(questions, unanswered) of a questions file's text."""
    if text is None:
        return None
    lines = text.splitlines()
    n = sum(1 for l in lines if questions_mod.Q_HEADING.match(l))
    empty = sum(1 for l in lines if questions_mod.ANSWER_EMPTY.match(l))
    return n, empty


def _b_waiting(text, path):
    """True when a blocking file's text still waits on a decision."""
    if text is None:
        return None
    try:
        parsed = blocking_mod.parse_lines(text.splitlines(), path, os.path.basename(path))
    except Exception:
        return None
    if not parsed.entries:
        return None
    return any(e.waiting for e in parsed.entries)


def _agent_of_questions(name):
    m = re.match(r"^questions-(.+)-\d+\.md$", name)
    if m:
        return m.group(1)
    return "convertisseur" if name.startswith("technique-") else UNKNOWN


def who_wrote(subject):
    """Whose writing a commit holds: the Product Owner's, committed from the
    main checkout (« chore: answers », a command's « chore: pre-… »), or an
    agent's — the Arbitre's, for a decision."""
    s = subject or ""
    if s.startswith(PO_PREFIXES):
        return "Product Owner"
    if s.startswith(COCKPIT_PREFIXES) or MERGE.match(s):
        return None
    return "Arbitre"


def history(app, feature, cycle="main", log=None):
    """§2 — the questions and blocking files of the cycle, timed from git.
    {"questions": [...], "blocking": [...], "commits": [...]}."""
    rel = cycle_rel(feature, cycle)
    log = git_log(app, rel) if log is None else log
    qs, bs = {}, {}           # current path → entity
    done_q, done_b = [], []
    want = []                 # (sha, path) to read

    for c in log:
        for st, old, new in c["changes"]:
            for p in {old, new}:
                inner = _in_cycle(p, rel)
                if inner and (is_answer_file(inner) or blocking_mod.BLOCKED_FILE.match(p.split("/")[-1])):
                    if st != "D" or p == old:
                        want.append((c["sha"], new if st in "RA" else p))
    texts = _cat(app, [f"{s}:{p}" for s, p in want])

    def text(sha, path):
        return texts.get(f"{sha}:{path}")

    for c in log:
        for st, old, new in c["changes"]:
            o_in, n_in = _in_cycle(old, rel), _in_cycle(new, rel)
            # ------------------------------------------------ questions files
            if st == "A" and n_in and is_answer_file(n_in):
                qn = _q_state(text(c["sha"], new))
                qs[new] = {"file": n_in, "agent": _agent_of_questions(n_in.split("/")[-1]),
                           "created_at": _iso(c["at"]), "created_by": c["subject"], "created_sha": c["sha"][:7],
                           "questions": qn[0] if qn else None, "answered_at": None, "answered_by": None,
                           "answered_sha": None, "seconds": None, "moved_to": None,
                           "_open": bool(qn and qn[1])}
                if qn and qn[0] and not qn[1]:
                    qs[new]["answered_at"] = _iso(c["at"])
            elif st == "M" and new in qs:
                q = qs[new]
                qn = _q_state(text(c["sha"], new))
                if qn and q["questions"] is None:
                    q["questions"] = qn[0]
                if qn and qn[1]:
                    q["_open"] = True
                if qn and qn[0] and not qn[1] and q["_open"] and not q["answered_at"]:
                    q["answered_at"], q["answered_sha"] = _iso(c["at"]), c["sha"][:7]
                    q["answered_by"] = who_wrote(c["subject"]) or "Product Owner"
            elif st in ("R", "D") and old in qs:
                q = qs.pop(old)
                q["moved_to"] = (new.split(rel + "/", 1)[-1] if st == "R" else None)
                q["gone_at"] = _iso(c["at"])
                done_q.append(q)
            # ------------------------------------------------ blocking files
            name_new = new.split("/")[-1]
            if st in ("A", "R", "C") and n_in and is_blocking_file(n_in) and not (st == "R" and old in bs):
                w = _b_waiting(text(c["sha"], new), new)
                bs[new] = {"file": n_in, "agent": blocking_mod.agent_of(new), "created_at": _iso(c["at"]),
                           "created_sha": c["sha"][:7], "created_by": c["subject"], "decided_at": None,
                           "decided_sha": None, "settled_at": None, "settled_as": None, "by": None,
                           "seen_waiting": bool(w), "seconds": None}
                if w is False:
                    bs[new]["decided_at"], bs[new]["decided_sha"] = _iso(c["at"]), c["sha"][:7]
                    bs[new]["by"] = who_wrote(c["subject"])
            elif st == "M" and new in bs:
                b = bs[new]
                w = _b_waiting(text(c["sha"], new), new)
                if w:
                    b["seen_waiting"] = True
                    if b["decided_at"]:   # a new Blocking N appended: waiting again
                        b["decided_at"] = b["decided_sha"] = b["by"] = None
                elif w is False and not b["decided_at"]:
                    b["decided_at"], b["decided_sha"] = _iso(c["at"]), c["sha"][:7]
                    b["by"] = who_wrote(c["subject"])
            elif st in ("R", "D") and old in bs:
                b = bs.pop(old)
                if st == "R" and blocking_mod.ARCHIVED.search(name_new):
                    b["settled_at"], b["settled_as"] = _iso(c["at"]), n_in or new
                    if not b["decided_at"]:
                        w = _b_waiting(text(c["sha"], new), new)
                        if w is False:
                            b["decided_at"], b["decided_sha"] = _iso(c["at"]), c["sha"][:7]
                            b["by"] = who_wrote(c["subject"])
                elif st == "R":
                    bs[new] = b
                    b["file"] = n_in or new
                    continue
                else:
                    b["settled_at"], b["settled_as"] = _iso(c["at"]), "supprimé"
                done_b.append(b)
    all_q = done_q + list(qs.values())
    all_b = done_b + list(bs.values())
    for q in all_q:
        q.pop("_open", None)
        if q["answered_at"] and q["created_at"]:
            q["seconds"] = (_local(q["answered_at"]) - _local(q["created_at"])).total_seconds()
    for b in all_b:
        if not b["by"] and b["decided_at"]:
            b["by"] = UNKNOWN
        if b["decided_at"] and b["created_at"]:
            b["seconds"] = (_local(b["decided_at"]) - _local(b["created_at"])).total_seconds()
        if b["settled_at"] and not b["by"]:
            b["by"] = UNKNOWN
    all_q.sort(key=lambda q: q["created_at"] or "")
    all_b.sort(key=lambda b: b["created_at"] or "")
    return {"questions": all_q, "blocking": all_b, "commits": log}


# ------------------------------------------------------------ points à creuser (§3)

def _cmd(command):
    return (command or "").split()[0] if command else ""


def points(entries, hist, estimates, thresholds, programmes=()):
    """Raised by the journal itself, each with its reason. `estimates`:
    usage.estimates' {"/cmd": {window: {median}}}."""
    th = clean_thresholds(thresholds)
    out = []
    for e in entries:
        if e.get("outcome") in FAILED:
            what = "n'était pas connecté (Claude Code)" if e["outcome"] == NOT_LOGGED else "a fini en erreur"
            out.append({"kind": "erreur", "at": e.get("at"), "command": e.get("command"),
                        "text": f"{e.get('command')} {what} le {_human(e.get('at'))}"
                                + (f" — {e['note']}" if e.get("note") and e["outcome"] != NOT_LOGGED else "") + "."})
    by_agent = {}
    for b in (hist or {}).get("blocking", []):
        by_agent.setdefault(b["agent"], []).append(b)
    for agent, bl in sorted(by_agent.items()):
        if len(bl) >= th["blocking_repeat"]:
            out.append({"kind": "blocage", "at": bl[-1]["created_at"], "command": None,
                        "text": f"{len(bl)} fichiers de blocage de {agent} dans ce cycle : "
                                + ", ".join(b["file"] for b in bl) + "."})
    for e in entries:
        est = (estimates or {}).get(_cmd(e.get("command"))) or {}
        med = (est.get("five_hour") or {}).get("median")
        share = e.get("five_hour")
        if share is not None and med and share > th["cost_factor"] * med:
            out.append({"kind": "coût", "at": e.get("at"), "command": e.get("command"),
                        "text": f"{e.get('command')} le {_human(e.get('at'))} a pris {fmt_share(share)} de la fenêtre "
                                f"de 5 heures — plus de {th['cost_factor']:g} fois son habitude ({fmt_share(med)}, "
                                f"la médiane de {est['five_hour'].get('n')} runs)."})
    run = []
    for e in entries + [None]:
        same = e and run and _cmd(e.get("command")) == _cmd(run[-1].get("command")) \
            and e.get("next") == run[-1].get("next") and e.get("outcome") not in FAILED
        if same:
            run.append(e)
            continue
        if len(run) >= th["repeat_runs"]:
            out.append({"kind": "sur place", "at": run[-1].get("at"), "command": run[-1].get("command"),
                        "text": f"{_cmd(run[-1].get('command'))} lancée {len(run)} fois de suite sans que l'étape "
                                f"proposée bouge (« {run[-1].get('next')} »), du {_human(run[0].get('at'))} au "
                                f"{_human(run[-1].get('at'))}."})
        run = [e] if e and e.get("outcome") not in FAILED else []
    seen = set()
    for p in programmes or ():
        if p.get("reason_kind") == "erreur":
            seen.add(p.get("name"))
            out.append({"kind": "programme", "at": p.get("ended_at"), "command": None,
                        "text": f"Le programme « {p.get('name')} » s'est arrêté sur une erreur le "
                                f"{_human(p.get('ended_at'))} : {p.get('reason')}"})
    for e in entries:
        if e.get("programme") and e.get("outcome") in FAILED and e["programme"] not in seen:
            seen.add(e["programme"])
            out.append({"kind": "programme", "at": e.get("at"), "command": e.get("command"),
                        "text": f"Le programme « {e['programme']} » s'est arrêté sur une erreur : {e.get('command')} "
                                f"le {_human(e.get('at'))}."})
    out.sort(key=lambda p: p.get("at") or "")
    return out


def _human(at):
    d = _local((at or "").replace(" ", "T")) if at else None
    return d.strftime("%d/%m à %H:%M") if d else "?"


# ------------------------------------------------------------ the screen (§4)

def overrides(log_dir, app_name, feature):
    """« Lancer quand même » on this computer: consommation.log's lines for
    this application's feature."""
    out = []
    try:
        with open(os.path.join(log_dir, "consommation.log"), encoding="utf-8") as f:
            for line in f:
                if f"« {app_name} »" in line and re.search(rf"\s{re.escape(feature)}\b", line):
                    at, _, text = line.partition(" · ")
                    out.append({"at": at.strip(), "text": text.strip()})
    except OSError:
        pass
    return out


def totals(entries, hist):
    def s(key):
        vals = [e.get(key) for e in entries]
        known = [v for v in vals if v is not None]
        return (round(sum(known), 1) if known else None), len(vals) - len(known)
    dur, dur_u = s("duration_s")
    read, read_u = s("read_tokens")
    wrote, _ = s("output_tokens")
    fh, fh_u = s("five_hour")
    wk, wk_u = s("seven_day")
    qs = (hist or {}).get("questions", [])
    bl = (hist or {}).get("blocking", [])
    her = [q["seconds"] for q in qs if q.get("seconds") is not None] + \
          [b["seconds"] for b in bl if b.get("seconds") is not None and b.get("by") == "Product Owner"]
    return {"runs": len(entries), "duration_s": dur, "duration_unknown": dur_u, "read_tokens": read,
            "read_unknown": read_u, "output_tokens": wrote, "five_hour": fh, "five_hour_unknown": fh_u,
            "seven_day": wk, "seven_day_unknown": wk_u, "errors": sum(1 for e in entries if e.get("outcome") in FAILED),
            "questions_files": len([q for q in qs if q.get("questions")]),
            "questions": sum(q.get("questions") or 0 for q in qs),
            "blocking": len(bl), "her_seconds": round(sum(her)) if her else None,
            "her_median_s": round(statistics.median(her)) if her else None}


def by_step(entries, hist):
    """Per command: runs, time, cost, and the questions and blocking files
    its runs created."""
    out = {}
    for e in entries:
        c = _cmd(e.get("command")) or UNKNOWN
        x = out.setdefault(c, {"command": c, "runs": 0, "duration_s": 0, "duration_unknown": 0, "five_hour": 0.0,
                               "five_hour_unknown": 0, "questions": [], "blocking": [], "failed": 0})
        x["runs"] += 1
        if e.get("duration_s") is None:
            x["duration_unknown"] += 1
        else:
            x["duration_s"] += e["duration_s"]
        if e.get("five_hour") is None:
            x["five_hour_unknown"] += 1
        else:
            x["five_hour"] = round(x["five_hour"] + e["five_hour"], 1)
        for f in e.get("created") or []:
            (x["blocking"] if f.split("/")[-1].startswith("blocked_") else x["questions"]).append(f)
        if e.get("outcome") in FAILED:
            x["failed"] += 1
    return list(out.values())


def attach_steps(entries, hist):
    """Each questions and blocking file under the step that made it: the
    command of the line whose « Créés » names it, else the one its agent's
    file comes from (AGENT_COMMAND), else « inconnu »."""
    made = {}
    for e in entries:
        for f in e.get("created") or []:
            made.setdefault(f, _cmd(e.get("command")))
    for x in (hist or {}).get("questions", []) + (hist or {}).get("blocking", []):
        c = AGENT_COMMAND.get(x.get("agent"))
        x["step"] = made.get(x["file"]) or (f"/{c}" if c else UNKNOWN)
    return hist


# ------------------------------------------------------------ reconstruction (§2)

def _stats_runs(store_path, app, feature):
    import statsview
    runs, _passes, limits, err = statsview.read_store(store_path)
    if err:
        return [], {}, {}
    akey = statsview.app_key(app)
    mine = [r for r in runs if not r.get("kind") and r.get("feature") == feature
            and statsview.app_key(r.get("app")) == akey]
    by_run = {}
    for m in limits:
        by_run.setdefault(m.get("run_id"), []).append(m)
    progs = {}
    try:
        import sqlite3
        with sqlite3.connect(store_path) as db:
            for pid, name in db.execute("SELECT id, name FROM programmes"):
                progs[pid] = name
    except Exception:
        pass
    return mine, by_run, progs


def shares(measures):
    import statsview
    return {w: statsview.limit_delta([m for m in measures if m["window"] == w])["delta"]
            for w in ("five_hour", "seven_day")}


def _head_at(app, when):
    r = sync_mod.git(app, "rev-list", "-1", f"--before={when}", "HEAD")
    return r.out.strip() or None if r.ok else None


def cycle_of_command(command, at, bugfix_starts):
    """Which cycle a past run belonged to: /diagnostique and the downstream
    commands to the highest correction that existed then, the rest to the
    main cycle (decide.chain_of, at the time of the run)."""
    c = _cmd(command).lstrip("/")
    live = [name for name, start in sorted(bugfix_starts.items()) if start and start <= (at or "")]
    if live and c in ("diagnostique", "7_lots", "8_code", "9_controle"):
        return live[-1]
    return "main"


def bugfix_starts(log):
    """{bugfix-NN: when its folder first appeared}, from the feature's log."""
    out = {}
    for c in log:
        for _st, _o, new in c["changes"]:
            m = re.match(r"^docs/features/[^/]+/(bugfix-\d+)/", new)
            if m and m.group(1) not in out:
                out[m.group(1)] = _iso(c["at"])
    return out


def reconstruct(app, feature, store_path, log_dir, app_name=None, computer=None, now=None):
    """§2 — the lines of the runs before 1.20: this computer's stats and
    logs first, git alone for the rest (cost and duration « inconnu »).
    {cycle: [entries]} — nothing written. A run already in a journal is
    left out."""
    computer = computer or computer_name()
    feat_rel = cycle_rel(feature)
    flog = git_log(app, feat_rel) if os.path.isdir(os.path.join(app, *feat_rel.split("/"))) else []
    # The whole feature's log, the bugfix-NN/ included.
    r = sync_mod.git(app, "log", "--reverse", "--topo-order", "--full-history", "--name-only", "--format=%x1e%H%x1f%P%x1f%aI%x1f%s",
                     "--", feat_rel, timeout=60)
    whole = []
    if r.ok:
        for chunk in r.out.split("\x1e")[1:]:
            lines = chunk.strip("\n").split("\n")
            h = lines[0].split("\x1f")
            if len(h) >= 4:
                whole.append({"sha": h[0], "parents": h[1].split(), "at": _local(h[2]), "subject": h[3],
                              "changes": [("M", p, p) for p in lines[1:] if p.strip()]})
    starts = bugfix_starts(whole)
    existing = {cy: read(journal_path(app, feature, cy)) for cy in cycles(app, feature)}
    first_line = min((e["at"] for es in existing.values() for e in es if e.get("at")), default=None)
    have = {(e.get("at"), _cmd(e.get("command"))) for es in existing.values() for e in es}
    out = {}
    runs, limits, progs = _stats_runs(store_path, app, feature) if store_path else ([], {}, {})
    ovr = overrides(log_dir, app_name or os.path.basename(app), feature) if log_dir else []
    covered = []
    for run in sorted(runs, key=lambda x: x.get("started_at") or ""):
        at = (run.get("started_at") or "")[:16]
        if (first_line and at >= first_line) or (at, _cmd(run.get("command"))) in have:
            continue
        cy = cycle_of_command(run.get("command"), run.get("started_at"), starts)
        nxt = nextline.parse(run.get("next_line") or "").to_dict() if run.get("next_line") else None
        before = _head_at(app, run.get("started_at"))
        after = _head_at(app, (run.get("ended_at") or "")[:19])
        created = created_files(app, feature, cy, before, after) if before and after else []
        sh = shares(limits.get(run["id"], []))
        notes = ["reconstitué (stats et journal de run de cet ordinateur)"]
        if run.get("resumed"):
            notes.insert(0, "suite de session")
        for o in ovr:
            if o["at"][:16] <= at and _cmd(run.get("command")) in o["text"] \
                    and (_local(at) - _local(o["at"][:19])).total_seconds() < 600:
                notes.insert(0, OVERRIDE_NOTE)
                break
        read_t = None
        if run.get("input_tokens") is not None:
            read_t = (run.get("input_tokens") or 0) + (run.get("cache_read_tokens") or 0) + \
                     (run.get("cache_creation_tokens") or 0)
        e = {"at": at, "computer": computer, "command": run.get("command"), "duration_s": run.get("duration_s"),
             "read_tokens": read_t, "output_tokens": run.get("output_tokens"),
             "five_hour": sh.get("five_hour"), "seven_day": sh.get("seven_day"),
             "outcome": outcome_of(run.get("outcome") if run.get("outcome") in ("erreur", "interrompu") else "terminé",
                                   nxt),
             "next": next_text(nxt), "created": created, "programme": progs.get(run.get("programme")),
             "note": " · ".join(notes), "source": "stats"}
        covered.append((run.get("started_at"), run.get("ended_at"), _cmd(run.get("command"))))
        out.setdefault(cy, []).append(e)
    # Git alone: each `Merge /<command>` — the chain's merge of its worktree —
    # and each agent's commit outside a merge, not covered by a stored run.
    merged = set()
    for c in whole:
        if len(c["parents"]) > 1:
            merged.update(_side_commits(app, c))
    for c in whole:
        at = _iso(c["at"])
        if not at or (first_line and at[:16] >= first_line):
            continue
        m = MERGE.match(c["subject"])
        if m:
            command = f"{m.group(1)} {m.group(2) or ''}".strip()
        elif len(c["parents"]) <= 1 and c["sha"] not in merged and who_wrote(c["subject"]) == "Arbitre" \
                and not _cockpit_commit(c["subject"], feature):
            command = None
        else:
            continue
        if any(_within(at, s, e2) and (command is None or _cmd(command) == k) for s, e2, k in covered):
            continue
        if (at[:16], _cmd(command) if command else UNKNOWN) in have:
            continue
        cy = "main"
        for ch in c["changes"]:
            mm = re.match(r"^docs/features/[^/]+/(bugfix-\d+)/", ch[2])
            if mm:
                cy = mm.group(1)
        parent = c["parents"][0] if c["parents"] else None
        created = created_files(app, feature, cy, parent, c["sha"]) if parent else []
        note = f"reconstitué de git seul — commit {c['sha'][:7]} « {c['subject'][:80]} »"
        if command is None and not created:
            continue        # nothing tells it from a hand edit
        if command is None:
            guessed = {AGENT_COMMAND.get(_agent_of_file(f)) for f in created} - {None}
            if len(guessed) == 1:
                command = f"/{guessed.pop()} {feature}"
                note += f" ; commande déduite de {', '.join(created)}"
        out.setdefault(cy, []).append({
            "at": at[:16], "computer": UNKNOWN, "command": command or "commande inconnue",
            "duration_s": None, "read_tokens": None, "output_tokens": None, "five_hour": None, "seven_day": None,
            "outcome": UNKNOWN, "next": UNKNOWN, "created": created, "programme": None,
            "note": note, "source": "git"})
    for cy in out:
        out[cy].sort(key=lambda e: e["at"] or "")
    return out


# The command whose run leaves an agent's questions or blocking file — only
# where one command alone does (the commands' own files): what a commit with
# no `Merge /<command>` is read as, said in its note.
AGENT_COMMAND = {"lexicographe": "1_lexique", "redacteur": "2_structure", "decoupeur": "3_decoupe",
                 "qualifieur": "3a_genre", "classeur": "3b_nature", "sondeur": "4_grille", "assembleur": "4_grille",
                 "convertisseur": "6_convertit", "batisseur": "batir", "cadreur": "7_lots",
                 "verificateur": "7_lots", "detailleur": "8_code", "realisateur": "8_code", "relecteur": "8_code",
                 "controleur": "9_controle", "diagnostiqueur": "diagnostique"}


def _agent_of_file(rel):
    name = rel.split("/")[-1]
    if name.startswith("blocked_"):
        return blocking_mod.agent_of(name)
    return _agent_of_questions(name)


def _cockpit_commit(subject, feature):
    """A commit the cockpit made itself — the idea file of « Nouvelle
    application » (create.py), a data file — never a command's run."""
    return subject.startswith(f"feat: {feature} — ")


def _side_commits(app, merge):
    r = sync_mod.git(app, "rev-list", f"{merge['parents'][0]}..{merge['sha']}")
    return set(r.out.split()) - {merge["sha"]} if r.ok else set()


def _within(at, start, end):
    if not start:
        return False
    a, s = _local(at), _local(start)
    e = _local(end) if end else s
    if not a or not s:
        return False
    return (s - _pad()) <= a <= ((e or s) + _pad())


def _pad():
    from datetime import timedelta
    return timedelta(minutes=2)


# ------------------------------------------------------------ the report (§4)

def report_md(feature, cycle, entries, hist, pts, programmes=(), overrides_=(), now=None):
    """`rapport-cycle.md`: duration, cost, questions and blocking files per
    step, where her time went, what failed, the points à creuser."""
    now = now or datetime.now()
    t = totals(entries, hist)
    title = feature if cycle == "main" else f"{feature} / {cycle}"
    first = min((e["at"] for e in entries if e.get("at")), default=None)
    last = max((e["at"] for e in entries if e.get("at")), default=None)
    L = [f"# Rapport de fin de cycle — {title}", "",
         f"Écrit par le cockpit le {now.strftime('%d/%m/%Y à %H:%M')}, d'après le journal de cycle, l'historique git "
         "du dossier et, sur cet ordinateur, les statistiques. Aucun agent de la chaîne ne le lit.", ""]
    L += ["## En bref", "",
          f"- Du {_human(first)} au {_human(last)} : {t['runs']} commande(s) lancée(s) depuis le cockpit"
          + (f", dont {t['errors']} en erreur" if t["errors"] else "") + ".",
          f"- Temps des commandes : {fmt_duration(t['duration_s'])}"
          + (f" (dont {t['duration_unknown']} durée(s) inconnue(s), hors somme)" if t["duration_unknown"] else "") + ".",
          f"- Coût : {fmt_tokens(t['read_tokens'], t['output_tokens'])} ; ≈ {fmt_share(t['five_hour'])} de la fenêtre "
          f"de 5 heures et ≈ {fmt_share(t['seven_day'])} de la semaine, au total"
          + (f" ({t['five_hour_unknown']} run(s) sans mesure)" if t["five_hour_unknown"] else "") + ".",
          f"- Questions : {t['questions']} dans {t['questions_files']} fichier(s) ; fichiers de blocage : {t['blocking']}.",
          f"- Son temps de réponse : {fmt_duration(t['her_seconds'])} en tout"
          + (f", médiane {fmt_duration(t['her_median_s'])} par fichier" if t["her_median_s"] is not None else "") + ".",
          ""]
    L += ["## Par étape", "", "| Commande | Runs | Durée | ≈ 5 h | Questions créées | Blocages créés | En erreur |",
          "|---|---|---|---|---|---|---|"]
    for x in by_step(entries, hist):
        L.append(f"| {x['command']} | {x['runs']} | {fmt_duration(x['duration_s']) if x['runs'] > x['duration_unknown'] else UNKNOWN} "
                 f"| {fmt_share(x['five_hour']) if x['runs'] > x['five_hour_unknown'] else UNKNOWN} "
                 f"| {_cell(', '.join(x['questions']))} | {_cell(', '.join(x['blocking']))} | {x['failed']} |")
    L += ["", "## Où est passé son temps", "", "| Fichier | Agent | Questions | Créé | Répondu | Temps |",
          "|---|---|---|---|---|---|"]
    for q in hist.get("questions", []):
        if not q.get("questions"):
            continue
        L.append(f"| {q['file']} | {q['agent']} | {q['questions']} | {_human(q['created_at'])} | "
                 f"{_human(q['answered_at']) if q['answered_at'] else 'pas encore'} | {fmt_duration(q['seconds'])} |")
    L += ["", "| Blocage | Agent | Créé | Décidé | Par | Réglé | Temps |", "|---|---|---|---|---|---|---|"]
    for b in hist.get("blocking", []):
        L.append(f"| {b['file']} | {b['agent']} | {_human(b['created_at'])} | "
                 f"{_human(b['decided_at']) if b['decided_at'] else 'pas encore'} | {b.get('by') or NONE} | "
                 f"{_human(b['settled_at']) if b['settled_at'] else 'pas encore'} | {fmt_duration(b['seconds'])} |")
    failed = [e for e in entries if e.get("outcome") in FAILED or e.get("outcome") == STOPPED]
    L += ["", "## Ce qui a échoué", ""]
    L += [f"- {_human(e['at'])} — {e['command']} : {e['outcome']}" + (f" — {e['note']}" if e.get("note") else "")
          for e in failed] or ["- Rien."]
    if programmes or overrides_:
        L += ["", "## Pilote automatique et « Lancer quand même »", ""]
        L += [f"- Programme « {p.get('name')} » : {p.get('commands') or 0} commande(s), arrêté le "
              f"{_human(p.get('ended_at'))} — {p.get('reason') or '?'}" for p in programmes]
        L += [f"- {_human(o['at'][:16])} — {o['text']}" for o in overrides_]
    L += ["", "## Points à creuser", ""]
    L += [f"- {p['text']}" for p in pts] or ["- Aucun."]
    return "\n".join(L) + "\n"
