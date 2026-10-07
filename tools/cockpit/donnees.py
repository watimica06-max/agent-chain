"""« Données » (1.10) — the external data of `.claude/formats/donnees.md`:
the two `donnees/` folders, their index `donnees.md`, and the private section
of the application's `.gitignore` (§6).

The cockpit is the Product Owner's hand here, and writes as she would: the
files she joins, the index in the format, the `.gitignore` line of a private
file — `git rm --cached` when it was committed —, one commit,
`donnees: <what changed>`, and a push.
"""
import os
import re
import subprocess
import tempfile
from dataclasses import dataclass, asdict
from datetime import date

import chain as chain_mod
import textfile

INDEX = "donnees.md"
TITLE = "# Données"
FIELDS = ("What", "Source", "Date", "Private")
# §6: the section's opening line, exactly.
SECTION = "# Données privées — .claude/formats/donnees.md"
APP_FOLDER = "docs/donnees"
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
IMAGE_TYPES = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif",
               ".svg": "image/svg+xml", ".webp": "image/webp", ".bmp": "image/bmp", ".ico": "image/x-icon"}
PREVIEW_LINES = 20
PREVIEW_BYTES = 64 * 1024
# A name the folder holds as one file, its `.gitignore` line a path and never
# a pattern (§6): no folder, nothing Windows refuses, nothing `.gitignore`
# would read as a pattern or a comment.
BAD_CHARS = set('<>:"|?*\\/[]') | {chr(c) for c in range(32)}


class DataError(Exception):
    """Refused, and said why — nothing written."""


@dataclass
class Entry:
    name: str
    what: str = ""
    source: str = ""
    date: str = ""
    private: str = ""          # "yes", "no", or what the index holds

    def to_dict(self):
        return asdict(self)


# ------------------------------------------------------------ where

def folder_of(tab, feature):
    """`app` — `docs/donnees/`, embedded data; `feature` — the feature's
    `donnees/`, reference data (§1). Relative to the repository, with `/`."""
    if tab == "app":
        return APP_FOLDER
    if tab == "feature" and feature:
        return f"docs/features/{feature}/donnees"
    raise DataError("onglet inconnu")


def folder_of_marker(app, value):
    """The folder a question's `Folder:` line names (§5): one of the two of
    §1, the feature written out — or DataError."""
    v = (value or "").strip().replace("\\", "/")
    if v == APP_FOLDER + "/":
        return APP_FOLDER
    m = re.match(r"^docs/features/([^/]+)/donnees/$", v)
    if m and os.path.isdir(os.path.join(app, "docs", "features", m.group(1))):
        return v.rstrip("/")
    raise DataError(f"« Folder: {value} » ne nomme aucun des deux dossiers de données")


def _abs(app, rel):
    return os.path.join(app, *rel.split("/"))


def check_name(name):
    n = (name or "").strip()
    if not n:
        raise DataError("nom de fichier vide")
    if n != name:
        raise DataError(f"« {name} » : pas d'espace au début ni à la fin du nom")
    bad = sorted({c for c in n if c in BAD_CHARS})
    if bad:
        raise DataError(f"« {name} » : caractère refusé dans un nom de fichier ({' '.join(repr(c) for c in bad)})")
    if n.lower() == INDEX:
        raise DataError(f"« {INDEX} » est le nom de l'index")
    if n[0] in "#!" or n in (".", "..") or n.endswith("."):
        raise DataError(f"« {name} » : un nom qui ouvre sur # ou ! se lirait autrement dans .gitignore")
    return n


def _entry_path(folder, name):
    """An index name, relative to the folder — `images/fleche.svg` (§2)."""
    parts = name.replace("\\", "/").split("/")
    if any(p in ("", ".", "..") for p in parts):
        raise DataError(f"« {name} » : chemin refusé")
    return folder + "/" + "/".join(parts)


# ------------------------------------------------------------ the index

def parse_index(text):
    """(entries, errors): `# Données`, then `## <name>` and the four lines,
    in that order (§2). A line out of place is an error, never guessed."""
    entries, errors = [], []
    cur = None
    seen_title = False
    for i, raw in enumerate(text.splitlines(), 1):
        line = raw.rstrip()
        if not line.strip():
            continue
        if line == TITLE:
            if seen_title or entries:
                errors.append(f"ligne {i} : « {TITLE} » une seconde fois")
            seen_title = True
            continue
        if line.startswith("## "):
            cur = Entry(line[3:].strip())
            cur._got = []
            if any(e.name == cur.name for e in entries):
                errors.append(f"ligne {i} : « {cur.name} » deux fois dans l'index")
            entries.append(cur)
            continue
        m = re.match(r"^(What|Source|Date|Private):\s?(.*)$", line)
        if m and cur is not None:
            key, value = m.group(1), m.group(2).strip()
            expected = FIELDS[len(cur._got)] if len(cur._got) < len(FIELDS) else None
            if key != expected:
                errors.append(f"ligne {i} : « {key}: » sous « {cur.name} », où « {expected or 'rien'} » était attendu")
            cur._got.append(key)
            setattr(cur, key.lower(), value)
            continue
        errors.append(f"ligne {i} : hors du format — « {line[:60]} »")
    if entries and not seen_title:
        errors.insert(0, f"le titre « {TITLE} » manque")
    for e in entries:
        missing = [f for f in FIELDS if f not in e._got]
        if missing:
            errors.append(f"« {e.name} » : il manque {', '.join(m + ':' for m in missing)}")
        if e.private and e.private not in ("yes", "no"):
            errors.append(f"« {e.name} » : « Private: {e.private} » — yes ou no")
        del e._got
    return entries, errors


def index_text(entries):
    """The index in the format: its title, then five lines per file."""
    out = [TITLE]
    for e in entries:
        out += ["", f"## {e.name}", f"What: {e.what}", f"Source: {e.source}", f"Date: {e.date}",
                f"Private: {e.private}"]
    return "\n".join(out) + "\n"


def check_entry(e):
    """What keeps an entry from being written — every line written (§2)."""
    errs = []
    if not e.what.strip():
        errs.append("« What: » vide")
    if not e.source.strip():
        errs.append("« Source: » vide")
    if not DATE.match(e.date.strip()):
        errs.append("« Date: » attendue AAAA-MM-JJ")
    else:
        try:
            date.fromisoformat(e.date.strip())
        except ValueError:
            errs.append(f"« Date: {e.date} » n'est pas une date")
    if e.private not in ("yes", "no"):
        errs.append("« Private: » yes ou no")
    for f in (e.what, e.source):
        if "\n" in f or "\r" in f:
            errs.append("une ligne, pas plusieurs")
    return errs


def read_index(app, folder):
    p = _abs(app, folder + "/" + INDEX)
    if not os.path.exists(p):
        return [], [], False
    try:
        tf = textfile.load(p)
    except textfile.UnreadableFile as e:
        return [], [f"{INDEX} illisible : {e}"], True
    entries, errors = parse_index(tf.text())
    return entries, errors, True


# ------------------------------------------------------------ .gitignore, §6

def section_paths(text):
    """The paths of the private section: the lines after its opening line,
    to the first blank line or the end of the file."""
    lines = text.splitlines()
    out = []
    for i, l in enumerate(lines):
        if l.strip() == SECTION:
            for x in lines[i + 1:]:
                if not x.strip():
                    break
                out.append(x.strip())
            break
    return out


def with_section(text, add=(), drop=()):
    """`.gitignore`'s text with the paths added to its private section and
    `drop` taken out of it — the section created at the end when absent,
    never twice; every other line as it was."""
    nl = "\r\n" if "\r\n" in text else "\n"
    lines = text.splitlines()
    start = next((i for i, l in enumerate(lines) if l.strip() == SECTION), None)
    if start is None:
        cur = []
    else:
        end = start + 1
        while end < len(lines) and lines[end].strip():
            end += 1
        cur = [l.strip() for l in lines[start + 1:end]]
    keep = [p for p in cur if p not in set(drop)]
    for p in add:
        if p not in keep:
            keep.append(p)
    if keep == cur:
        return text
    if start is None:
        while lines and not lines[-1].strip():
            lines.pop()
        block = ([""] if lines else []) + [SECTION] + keep
        lines = lines + block
    else:
        lines = lines[:start + 1] + keep + lines[end:]
        if not keep:
            # An empty section is dropped with its opening line.
            del lines[start]
            if start > 0 and not lines[start - 1].strip() and (start >= len(lines) or not lines[start].strip()):
                del lines[start - 1]
    return nl.join(lines) + nl if lines else ""


# ------------------------------------------------------------ git

def _git(app, *args, env=None):
    e = dict(os.environ, GIT_TERMINAL_PROMPT="0", **(env or {}))
    p = subprocess.run(["git", "-C", app, "-c", "core.quotepath=off", *args], capture_output=True,
                       stdin=subprocess.DEVNULL, env=e, timeout=60)
    if p.returncode:
        msg = p.stderr.decode("utf-8", "replace").strip() or p.stdout.decode("utf-8", "replace").strip()
        raise DataError(f"git {args[0]} : {msg}")
    return p.stdout.decode("utf-8", "replace")


def tracked(app, paths):
    """The paths, among `paths`, git's index holds."""
    if not paths:
        return set()
    out = _git(app, "ls-files", "-z", "--", *paths)
    return {x for x in out.split("\0") if x}


# ------------------------------------------------------------ the folder

def kind_of(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in IMAGE_TYPES:
        return "image"
    try:
        with open(path, "rb") as f:
            head = f.read(4096)
    except OSError:
        return "other"
    if b"\0" in head:
        return "other"
    try:
        head.decode("utf-8")
        return "text"
    except UnicodeDecodeError as e:
        # A multi-byte character cut at the end of the sample is still text.
        return "text" if e.start >= len(head) - 3 else "other"


def _disk_files(app, folder):
    base = _abs(app, folder)
    out = []
    if not os.path.isdir(base):
        return out
    for dp, dn, fn in os.walk(base):
        dn[:] = [d for d in dn if not d.startswith(".")]
        for n in fn:
            rel = os.path.relpath(os.path.join(dp, n), base).replace(os.sep, "/")
            if rel != INDEX:
                out.append(rel)
    return sorted(out)


def listing(app, tab, feature):
    """The tab: the index's entries, each with its file's state; the files
    the folder holds that no entry names — joined, not yet indexed."""
    folder = folder_of(tab, feature)
    entries, errors, exists = read_index(app, folder)
    on_disk = _disk_files(app, folder)
    gi = _abs(app, ".gitignore")
    try:
        section = set(section_paths(textfile.load(gi).text())) if os.path.exists(gi) else set()
    except textfile.UnreadableFile:
        section = set()
    try:
        held = tracked(app, [folder])
    except DataError:
        held = set()
    rows = []
    for e in entries:
        p = _abs(app, folder + "/" + e.name)
        here = os.path.isfile(p)
        rel = folder + "/" + e.name
        rows.append({**e.to_dict(), "on_disk": here, "kind": kind_of(p) if here else None,
                     "size": os.path.getsize(p) if here else None, "path": rel,
                     "tracked": rel in held, "ignored": rel in section})
    named = {e.name for e in entries}
    loose = []
    for n in on_disk:
        if n in named:
            continue
        p = _abs(app, folder + "/" + n)
        rel = folder + "/" + n
        loose.append({"name": n, "kind": kind_of(p), "size": os.path.getsize(p), "path": rel,
                      "tracked": rel in held, "ignored": rel in section})
    return {"tab": tab, "folder": folder + "/", "index_exists": exists, "entries": rows, "loose": loose,
            "errors": errors, "today": date.today().isoformat()}


def file_path(app, tab, feature, name):
    folder = folder_of(tab, feature)
    p = _abs(app, _entry_path(folder, name))
    if not os.path.isfile(p):
        raise DataError(f"« {name} » n'est pas dans {folder}/")
    return p


def preview(app, tab, feature, name):
    p = file_path(app, tab, feature, name)
    kind = kind_of(p)
    out = {"name": name, "kind": kind, "size": os.path.getsize(p)}
    if kind == "text":
        with open(p, "rb") as f:
            raw = f.read(PREVIEW_BYTES)
        text = raw.decode("utf-8", "replace").lstrip("﻿")
        lines = text.splitlines()
        out["lines"] = lines[:PREVIEW_LINES]
        out["truncated"] = len(lines) > PREVIEW_LINES or os.path.getsize(p) > PREVIEW_BYTES
    elif kind == "image":
        out["type"] = IMAGE_TYPES[os.path.splitext(p)[1].lower()]
    return out


def join(app, folder, name, data, replace=False):
    """One file copied into the folder, as it came — §1: never retouched."""
    n = check_name(name)
    p = _abs(app, folder + "/" + n)
    if os.path.exists(p) and not replace:
        raise DataError(f"« {n} » est déjà dans {folder}/")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "wb") as f:
        f.write(data)
    return n


# ------------------------------------------------------------ saving

def _what_changed(before, after, removed, now_private, now_public):
    old = {e.name: e for e in before}
    new = {e.name: e for e in after}
    parts = []
    for n, e in new.items():
        if n not in old:
            parts.append(f"{n} joint" + (", privé" if e.private == "yes" else ""))
    for n in removed:
        parts.append(f"{n} retiré")
    for n, e in new.items():
        o = old.get(n)
        if o and n not in now_private and n not in now_public and o.to_dict() != e.to_dict():
            parts.append(f"{n} modifié")
    for n in now_private:
        if n in old and old[n].private != "yes":
            parts.append(f"{n} privé")
    for n in now_public:
        parts.append(f"{n} n'est plus privé")
    return ", ".join(parts) or "index réécrit"


def _write_text(app, rel, text):
    p = _abs(app, rel)
    crlf = chain_mod._crlf(app)
    data = (text.replace("\r\n", "\n").replace("\n", "\r\n") if crlf else text.replace("\r\n", "\n")).encode("utf-8")
    old = textfile.read_bytes(p) if os.path.exists(p) else None
    if old != data:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        textfile.write_bytes(p, data)


def save(app, folder, entries, removed=(), push=True, answer_for=None):
    """« Enregistrer »: the removed files and their entries go together; the
    index written in the format; each private file's path in `.gitignore`'s
    section — `git rm --cached` when git held it —, a file no longer private
    taken out of it; then one commit of the folder and `.gitignore`,
    `donnees: <what changed>`, and a push. Nothing changed: no commit.

    The commit goes through an index of its own: what the Product Owner
    staged stays staged and out of it, and `git commit --only` would put a
    file `git rm --cached` took out back in."""
    entries = [Entry(**{k: (v.strip() if isinstance(v, str) else v) for k, v in e.items()})
               if isinstance(e, dict) else e for e in entries]
    errs = {}
    names = set()
    for e in entries:
        _entry_path(folder, e.name)
        if e.name in names:
            errs.setdefault(e.name, []).append("deux fois dans l'index")
        names.add(e.name)
        bad = check_entry(e)
        if bad:
            errs.setdefault(e.name, []).extend(bad)
        if e.name not in removed and not os.path.isfile(_abs(app, folder + "/" + e.name)):
            errs.setdefault(e.name, []).append("le fichier n'est pas dans le dossier")
    if errs:
        raise DataError("; ".join(f"{n} : {', '.join(v)}" for n, v in errs.items()))
    removed = [r for r in removed if r not in names]
    for r in removed:
        _entry_path(folder, r)
    before, _, _ = read_index(app, folder)
    for r in removed:
        p = _abs(app, folder + "/" + r)
        if os.path.isfile(p):
            os.remove(p)
    _write_text(app, folder + "/" + INDEX, index_text(entries))

    gi_rel = ".gitignore"
    gi = _abs(app, gi_rel)
    gi_text = textfile.load(gi).text() if os.path.exists(gi) else ""
    private = [folder + "/" + e.name for e in entries if e.private == "yes"]
    public = [folder + "/" + e.name for e in entries if e.private == "no"]
    gone = [folder + "/" + r for r in removed]
    in_section = set(section_paths(gi_text))
    new_gi = with_section(gi_text, add=private, drop=[p for p in public + gone if p in in_section])
    if new_gi != gi_text:
        _write_text(app, gi_rel, new_gi)
    now_private = [e.name for e in entries if e.private == "yes" and folder + "/" + e.name not in in_section]
    now_public = [e.name for e in entries if e.private == "no" and folder + "/" + e.name in in_section]
    held = tracked(app, private)
    history = sorted(p[len(folder) + 1:] for p in held)

    res = {"commit": None, "pushed": False, "push_error": None, "history": history, "message": None}
    paths = [folder, gi_rel] if os.path.exists(gi) else [folder]
    fd, tmp_index = tempfile.mkstemp(prefix="cockpit-donnees-", suffix=".index")
    os.close(fd)
    os.remove(tmp_index)
    env = {"GIT_INDEX_FILE": tmp_index}
    try:
        _git(app, "read-tree", "HEAD", env=env)
        _git(app, "add", "-A", "--", *paths, env=env)
        if held:
            _git(app, "rm", "-q", "--cached", "--ignore-unmatch", "--", *sorted(held), env=env)
        changed = _git(app, "diff", "--cached", "--name-only", "HEAD", env=env).split()
        if changed:
            message = "donnees: " + _what_changed(before, entries, removed, now_private, now_public)
            if answer_for:
                message += f" — {answer_for}"
            _git(app, "commit", "-q", "-m", message, env=env)
            res["commit"] = _git(app, "rev-parse", "--short", "HEAD").strip()
            res["message"] = message
            # The real index catches up on these paths alone.
            _git(app, "reset", "-q", "--", *paths, *sorted(held))
    finally:
        if os.path.exists(tmp_index):
            os.remove(tmp_index)
    if res["commit"] and push:
        try:
            chain_mod.push_branch(app)
            res["pushed"] = True
        except chain_mod.InstallError as e:
            res["push_error"] = str(e)
    return res


def add_entry(app, folder, entry, push=True, answer_for=None):
    """« Joindre un fichier » from a question (§5): the index on disk, with
    this entry added — or replacing the one of the same name —, saved."""
    entries, errors, _ = read_index(app, folder)
    if errors:
        raise DataError(f"l'index de {folder}/ ne tient pas le format : {errors[0]}")
    e = Entry(**entry) if isinstance(entry, dict) else entry
    entries = [x for x in entries if x.name != e.name] + [e]
    return save(app, folder, entries, push=push, answer_for=answer_for)
