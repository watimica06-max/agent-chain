"""Every blocking entry waiting on the Product Owner — TECHNICAL_V1 §8.2,
§8.3.

Five shapes:
  1. one block, one `## Decision`;
  2. the same with `## Invocation` above (routing, never shown);
  3. `## Blocking N`, one `## Decision` each;
  4. `## Blocking N` with `###` sub-headings, one `## Decision` at the end
     holding `N. <text>` lines (detailleur, realisateur);
  5. one block appended several times, only the last `## Decision` live
     (cadreur).
What is waiting is decided by the commands' own tests, unchanged.
"""
import hashlib
import os
import re
from dataclasses import dataclass, field, asdict

import textfile

BLOCKED_FILE = re.compile(r"^blocked_[A-Za-z0-9_-]+\.md$")
ARCHIVED = re.compile(r"-\d+\.md$")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
BLOCKING = re.compile(r"^## Blocking (\d+)\b(.*)$")
LOT_IN_HEADING = re.compile(r"\b(lot-[A-Za-z0-9-]+)")
DECISION = re.compile(r"^## Decision\s*$")
INVOCATION = re.compile(r"^## Invocation\s*$")
OPTIONS = re.compile(r"^Options:\s*$")
OPTION_ITEM = re.compile(r"^\s*(?:[-*•])\s+(.*)$")
NUMBERED = re.compile(r"^(\d+)\.")
REQUEST_IN_WHERE = re.compile(r"architecte/cadreur\.md\s*[—–-]+\s*Request\s+(\d+)")
PO_DECISION = re.compile(r"^## Décision du Product Owner\s*$")
# What the relecteur's three act rows name missing (cmd/8_code.md:743-745):
# the act retires them; only « anything else » is hers.
# The relecteur blocks when one of its four inputs is missing: the act
# rows are a block naming one of them, and saying it is missing.
RELECTEUR_INPUT = re.compile(
    r"compte-rendu|fiche-executable|conception\.md|tests\.md|\breport\b|\bsheet\b",
    re.IGNORECASE)
RELECTEUR_MISSING = re.compile(
    r"\bmissing\b|\babsent\b|not found|does not exist|no such|introuvable|manquant|manque",
    re.IGNORECASE)
SKIP_DIRS = {"closed", ".git", "node_modules", "build"}


@dataclass
class BlockingEntry:
    id: str
    file: str
    rel: str
    shape: int                 # 1-5, or 0 for code/redecoupage.md
    agent: str
    number: int | None         # N of `## Blocking N`, shapes 3 and 4
    lot: str | None
    what_blocks: str
    where: str
    to_resume: str
    options: list[str]
    decision: str
    waiting: bool
    fingerprint: str
    worktree: str | None = None
    decision_line: int = -1
    base: str = ""             # the working folder it was read against

    def to_dict(self):
        d = asdict(self)
        d.pop("decision_line")
        d.pop("base")
        return d


@dataclass
class Notice:
    file: str
    rel: str
    message: str
    level: str = "error"       # "error" or "warning"

    def to_dict(self):
        return asdict(self)


@dataclass
class ParsedBlocking:
    entries: list[BlockingEntry] = field(default_factory=list)
    notices: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


# ---------------------------------------------------------------- tests

def decision_empty_a2(lines: list[str], idx: int) -> bool:
    """`grep -A2 '^## Decision$'`: nothing under the heading — a blank line
    and the next heading, or the end of the file — is empty."""
    for line in lines[idx + 1: idx + 3]:
        if line.startswith("#"):
            return True
        if line.strip():
            return False
    return True


def numbered_answers(lines: list[str], start: int, end: int) -> set[int]:
    """The `N.` lines under the single `## Decision` of shape 4."""
    found = set()
    for line in lines[start:end]:
        m = NUMBERED.match(line)
        if m:
            found.add(int(m.group(1)))
    return found


# --------------------------------------------------------------- parsing

def _headings(lines):
    out = []
    for i, line in enumerate(lines):
        m = HEADING.match(line)
        if m:
            out.append((i, len(m.group(1)), m.group(2)))
    return out


def _section(lines, heads, a, b, title):
    """Text under the first heading named `title` within [a, b)."""
    for k, (i, level, t) in enumerate(heads):
        if i < a or i >= b or level not in (2, 3):
            continue
        if t.strip().lower() == title:
            end = b
            for (j, lvl, _) in heads[k + 1:]:
                if j >= b:
                    break
                end = j
                break
            return "\n".join(lines[i + 1:end]).strip()
    return ""


def _split_options(text):
    lines = text.split("\n")
    for k, line in enumerate(lines):
        if OPTIONS.match(line):
            opts = []
            for l in lines[k + 1:]:
                m = OPTION_ITEM.match(l)
                if m:
                    opts.append(m.group(1).strip())
                elif l.strip() and opts:
                    opts[-1] += " " + l.strip()
            return "\n".join(lines[:k]).strip(), opts
    return text, []


def _decision_text(lines, idx, heads):
    end = len(lines)
    for (j, level, _) in heads:
        if j > idx and level <= 2:
            end = j
            break
    return "\n".join(lines[idx + 1:end]).strip(), end


def _fingerprint(*parts):
    h = hashlib.sha1()
    for p in parts:
        h.update((p or "").encode("utf-8"))
        h.update(b"\0")
    return h.hexdigest()[:16]


def agent_of(path):
    return os.path.basename(path)[len("blocked_"):-len(".md")]


def parse_lines(lines, path, rel, work_dir=None, worktree=None) -> ParsedBlocking:
    out = ParsedBlocking()
    name = os.path.basename(path)
    agent = agent_of(path)

    if name == "blocked_verificateur.md":
        return out          # no `## Decision`: never a form (§8.2)
    if not any(l.strip() for l in lines):
        out.warnings.append("fichier vide — rien à décider ; il attend d'être supprimé ou renommé")
        return out

    heads = _headings(lines)
    blockings = [(i, int(BLOCKING.match(lines[i]).group(1)), lines[i])
                 for (i, lvl, _) in heads if BLOCKING.match(lines[i])]
    decisions = [i for (i, lvl, _) in heads if DECISION.match(lines[i])]

    if not decisions:
        out.notices.append("aucun « ## Decision » : rien que la chaîne lirait comme une "
                           "décision — fichier à vérifier")
        return out

    def make(shape, a, b, number, lot, decision_idx, waiting, decision):
        what = _section(lines, heads, a, b, "what blocks")
        where = _section(lines, heads, a, b, "where")
        resume, options = _split_options(_section(lines, heads, a, b, "to resume"))
        key = f"{number}" if number is not None else f"L{a}"
        loc = f"{worktree}::" if worktree else ""
        return BlockingEntry(
            id=f"b:{loc}{rel}#{key}", file=path, rel=rel, shape=shape, agent=agent,
            number=number, lot=lot, what_blocks=what, where=where, to_resume=resume,
            options=options, decision=decision, waiting=waiting,
            fingerprint=_fingerprint(str(shape), key, what, where, resume),
            worktree=worktree, decision_line=decision_idx, base=work_dir or "")

    if blockings:
        sub3 = any(lvl == 3 for (i, lvl, _) in heads if i > blockings[0][0])
        nums = [n for (_, n, _) in blockings]
        if len(set(nums)) != len(nums):
            out.notices.append("deux « ## Blocking N » portent le même numéro")
            return out
        if len(decisions) == 1 and decisions[0] > blockings[-1][0] and (
                sub3 or len(blockings) > 1):
            # Shape 4 — one `## Decision` at the end, answered by number.
            d = decisions[0]
            text, end = _decision_text(lines, d, heads)
            answered = numbered_answers(lines, d + 1, end)
            for k, (i, n, h) in enumerate(blockings):
                b = blockings[k + 1][0] if k + 1 < len(blockings) else d
                m = LOT_IN_HEADING.search(h)
                out.entries.append(make(4, i, b, n, m.group(1) if m else None, d,
                                        n not in answered, text))
            return out
        if len(decisions) == len(blockings):
            # Shape 3 — one `## Decision` per entry.
            for k, (i, n, h) in enumerate(blockings):
                b = blockings[k + 1][0] if k + 1 < len(blockings) else len(lines)
                ds = [d for d in decisions if i < d < b]
                if len(ds) != 1:
                    out.notices.append(f"« ## Blocking {n} » sans « ## Decision » à lui")
                    return out
                text, _ = _decision_text(lines, ds[0], heads)
                m = LOT_IN_HEADING.search(h)
                out.entries.append(make(3, i, b, n, m.group(1) if m else None, ds[0],
                                        decision_empty_a2(lines, ds[0]), text))
            return out
        out.notices.append(
            f"{len(blockings)} « ## Blocking N » pour {len(decisions)} « ## Decision » : "
            "forme non reconnue")
        return out

    if name == "blocked_cadreur.md" or len(decisions) > 1:
        if name != "blocked_cadreur.md":
            out.notices.append(
                f"{len(decisions)} « ## Decision » sans « ## Blocking N » : "
                "forme réservée au cadreur")
            return out
        # Shape 5 — the last block alone is live.
        starts = [i for (i, lvl, t) in heads if lvl == 2 and t.strip().lower() == "what blocks"]
        a = max([s for s in starts if s < decisions[-1]], default=0)
        d = decisions[-1]
        text, _ = _decision_text(lines, d, heads)
        entry = make(5, a, len(lines), None, None, d, decision_empty_a2(lines, d), text)
        if entry.waiting and work_dir and _waits_on_architecte(entry.where, work_dir):
            entry.waiting = False
        out.entries.append(entry)
        return out

    d = decisions[0]
    text, _ = _decision_text(lines, d, heads)
    shape = 2 if any(INVOCATION.match(l) for l in lines) else 1
    entry = make(shape, 0, len(lines), None, None, d, decision_empty_a2(lines, d), text)
    if (name == "blocked_relecteur.md" and entry.waiting
            and RELECTEUR_INPUT.search(entry.what_blocks)
            and RELECTEUR_MISSING.search(entry.what_blocks)):
        entry.waiting = False   # retired by an act of /8_code, not by her
    out.entries.append(entry)
    return out


def _waits_on_architecte(where, work_dir):
    """cmd/7_lots.md:209-210 — a block whose `## Where` names a request in
    `architecte/cadreur.md` is lifted by the Architecte's verdict."""
    m = REQUEST_IN_WHERE.search(where or "")
    if not m:
        return False
    req = os.path.join(work_dir, "architecte", "cadreur.md")
    try:
        lines = textfile.load(req).lines
    except textfile.UnreadableFile:
        return False
    pat = re.compile(rf"^# Request {m.group(1)}\b")
    return any(pat.match(l) for l in lines)


def parse_file(path, work_dir, worktree=None) -> ParsedBlocking:
    base = work_dir
    rel = os.path.relpath(path, base).replace(os.sep, "/")
    tf = textfile.load(path)
    return parse_lines(tf.lines, path, rel, work_dir=base, worktree=worktree)


# ----------------------------------------------------------- discovery

def find_files(work_dir: str) -> list[str]:
    """Every unnumbered `blocked_*.md` of the working folder. A feature
    root's `bugfix-NN/` are working folders of their own: not walked."""
    found = []
    is_feature_root = os.path.basename(os.path.dirname(os.path.abspath(work_dir))) == "features"
    for root, dirs, files in os.walk(work_dir):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not (
            is_feature_root and root == work_dir and re.match(r"^bugfix-\d+$", d)))
        for name in sorted(files):
            if BLOCKED_FILE.match(name) and not ARCHIVED.search(name):
                found.append(os.path.join(root, name))
    return found


def shape4_files(work_dir: str) -> list[str]:
    """In a live worktree, only shape 4 is answered there (§8.2)."""
    found = []
    p = os.path.join(work_dir, "code", "blocked_detailleur.md")
    if os.path.isfile(p):
        found.append(p)
    code = os.path.join(work_dir, "code")
    if os.path.isdir(code):
        for lot in sorted(os.listdir(code)):
            q = os.path.join(code, lot, "blocked_realisateur.md")
            if os.path.isfile(q):
                found.append(q)
    return found


# ------------------------------------------------------ redecoupage.md

@dataclass
class Redecoupage:
    id: str
    file: str
    rel: str
    count: int
    ce_qui_revient: str
    ce_que_jen_fais: str
    decision: str
    waiting: bool
    fingerprint: str
    shape: int = 0
    agent: str = "redecoupage"

    def to_dict(self):
        return asdict(self)


def _has_po_decision(lines):
    for i, l in enumerate(lines):
        if PO_DECISION.match(l):
            return i
    return -1


def redecoupage_count(work_dir: str) -> int:
    """cmd/8_code.md:634-640 — archived returns numbered above the highest
    one carrying `## Décision du Product Owner`, plus the current one."""
    code = os.path.join(work_dir, "code")
    archived = []
    for name in os.listdir(code) if os.path.isdir(code) else []:
        m = re.match(r"^redecoupage-(\d+)\.md$", name)
        if m:
            archived.append((int(m.group(1)), os.path.join(code, name)))
    archived.sort()
    floor = 0
    for n, p in archived:
        try:
            if _has_po_decision(textfile.load(p).lines) >= 0:
                floor = n
        except textfile.UnreadableFile:
            pass
    current = 1 if os.path.isfile(os.path.join(code, "redecoupage.md")) else 0
    return sum(1 for n, _ in archived if n > floor) + current


def read_redecoupage(work_dir: str):
    path = os.path.join(work_dir, "code", "redecoupage.md")
    if not os.path.isfile(path):
        return None
    lines = textfile.load(path).lines
    heads = _headings(lines)
    count = redecoupage_count(work_dir)
    idx = _has_po_decision(lines)
    if idx >= 0:
        decision, _ = _decision_text(lines, idx, heads)
        empty = decision_empty_a2(lines, idx)
    else:
        decision, empty = "", True
    revient = _section(lines, heads, 0, len(lines), "ce qui revient")
    fais = _section(lines, heads, 0, len(lines), "ce que j'en fais")
    return Redecoupage(
        id="r:code/redecoupage.md", file=path, rel="code/redecoupage.md", count=count,
        ce_qui_revient=revient, ce_que_jen_fais=fais, decision=decision,
        waiting=empty and count >= 3,
        fingerprint=_fingerprint(revient, fais))


# ---------------------------------------------------------------- scan

def scan(work_dir: str, worktree_dirs: list[tuple[str, str]] = ()):
    """Entries waiting on her, and notices for files that could not be read.

    `worktree_dirs`: (worktree path, the working folder inside it), for the
    worktrees live during a run."""
    shown, notices = [], []

    def take(path, base, worktree=None):
        rel = os.path.relpath(path, base).replace(os.sep, "/")
        try:
            parsed = parse_file(path, base, worktree=worktree)
        except textfile.UnreadableFile as e:
            notices.append(Notice(path, rel, str(e)))
            return
        for m in parsed.notices:
            notices.append(Notice(path, rel, m))
        for m in parsed.warnings:
            notices.append(Notice(path, rel, m, level="warning"))
        if parsed.notices:
            return
        shown.extend(e for e in parsed.entries if e.waiting)

    for path in find_files(work_dir):
        take(path, work_dir)
    for wt, wt_work in worktree_dirs:
        for path in shape4_files(wt_work):
            take(path, wt_work, worktree=wt)
    try:
        r = read_redecoupage(work_dir)
    except textfile.UnreadableFile as e:
        notices.append(Notice(os.path.join(work_dir, "code", "redecoupage.md"),
                              "code/redecoupage.md", str(e)))
        r = None
    return shown, notices, (r if r and r.waiting else None)
