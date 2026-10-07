"""Every open question of a working folder — TECHNICAL_V1 §8.1.

Reads the root `questions-<agent>-NN.md` and `convertisseur/technique-*.md`,
in the shape the writers' templates give: `### Q<n>`, `Key: value` lines
(`Block:`, `Terms:`, `Entries:`, `Kind:`, `Folder:`), `Question:`, an optional
`Options:` list of `- ` items, an optional `Défaut:`, `Answer:`. What a
current template produces besides, and is read: a `Question:` over several
lines (agents/lexicographe.md:348-350), a title on the `Block:` line
(agents/architecte.md:579), and the file's own title above the first `### Q`
(the lexicographe's, premiere-app-3). Anything else is an error, and a file
it cannot read is an error, never a file with no questions.
"""
import hashlib
import os
import re
from dataclasses import dataclass, field, asdict

import textfile

ROOT_FILE = re.compile(r"^questions-[A-Za-z0-9_-]+-\d+\.md$")
TECHNIQUE_FILE = re.compile(r"^technique-[A-Za-z0-9_-]+\.md$")

Q_HEADING = re.compile(r"^### Q(\d+)\b")
# A question heading in any other shape: `## Q1 — …`, `#### Q2`, `### Q 3`.
OTHER_Q_HEADING = re.compile(r"^#{1,6}\s*Q\s*\d+\b")
ANY_HEADING = re.compile(r"^#{1,6}\s")
ANSWER = re.compile(r"^Answer:(.*)$")
ANSWER_EMPTY = re.compile(r"^Answer:\s*$")          # the commands' own test
QUESTION = re.compile(r"^Question:(.*)$")
OPTIONS = re.compile(r"^Options:\s*$")
DEFAUT = re.compile(r"^Défaut:(.*)$")
OPTION_ITEM = re.compile(r"^- (.*)$")                 # `- <a proposal…>`, every template
CONTEXT_KEY = re.compile(r"^[A-Z][A-Za-z]*:\s")       # `Block:`, `Terms:`, `Entries:`, `Kind:`, `Folder:`


@dataclass
class Question:
    id: str
    file: str            # absolute path, where the answer is written back
    rel: str             # path relative to the working folder, for display
    kind: str            # "questions" or "technique"
    number: int
    context: list[str]   # the `Key: value` lines above `Question:`
    question: str
    options: list[str]
    default: str | None  # the option `Défaut:` repeats
    default_source: str | None
    answer: str          # what sits in `Answer:` now
    open: bool           # the command's test reads it as waiting
    answer_empty: bool   # `^Answer:\s*$`
    fingerprint: str
    heading_line: int = 0
    answer_line: int = 0
    answer_end: int = 0  # last line of the answer text, inclusive

    def to_dict(self):
        d = asdict(self)
        for k in ("heading_line", "answer_line", "answer_end"):
            d.pop(k)
        return d


@dataclass
class FileError:
    file: str
    rel: str
    message: str

    def to_dict(self):
        return asdict(self)


@dataclass
class ParsedFile:
    entries: list[Question] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def find_files(work_dir: str) -> list[str]:
    """The files the Product Owner answers: root questions files, and the
    convertisseur's technical files, answered in place."""
    found = []
    try:
        names = sorted(os.listdir(work_dir))
    except OSError:
        return found
    for name in names:
        p = os.path.join(work_dir, name)
        if ROOT_FILE.match(name) and os.path.isfile(p):
            found.append(p)
    conv = os.path.join(work_dir, "convertisseur")
    if os.path.isdir(conv):
        for name in sorted(os.listdir(conv)):
            p = os.path.join(conv, name)
            if TECHNIQUE_FILE.match(name) and os.path.isfile(p):
                found.append(p)
    return found


def file_kind(path: str) -> str:
    return "technique" if TECHNIQUE_FILE.match(os.path.basename(path)) else "questions"


def _fingerprint(question: str, options: list[str], default_line: str | None) -> str:
    h = hashlib.sha1()
    for part in [question, *options, default_line or ""]:
        h.update(part.encode("utf-8"))
        h.update(b"\0")
    return h.hexdigest()[:16]


def _split_default(value: str, options: list[str]) -> tuple[str, str | None]:
    value = value.strip()
    # The text before ` — ` repeats one option verbatim; match the option
    # first, in case an option itself holds a dash.
    for opt in sorted(options, key=len, reverse=True):
        if value == opt:
            return opt, None
        if value.startswith(opt + " — "):
            return opt, value[len(opt) + 3:].strip() or None
    if " — " in value:
        text, source = value.split(" — ", 1)
        return text.strip(), source.strip() or None
    return value, None


def parse_lines(lines: list[str], path: str, rel: str, kind: str) -> ParsedFile:
    out = ParsedFile()
    starts = []
    for i, line in enumerate(lines):
        if Q_HEADING.match(line):
            starts.append(i)
        elif OTHER_Q_HEADING.match(line):
            out.errors.append(
                f"ligne {i + 1} : titre de question non reconnu « {line.strip()} » "
                "— attendu « ### Q<n> »")
    if not starts:
        stray = [i for i, l in enumerate(lines) if ANSWER.match(l) or QUESTION.match(l)]
        if stray and not out.errors:
            out.errors.append(
                f"ligne {stray[0] + 1} : « Question: » ou « Answer: » hors de tout "
                "« ### Q<n> »")
        return out

    seen = {}
    for k, start in enumerate(starts):
        end = starts[k + 1] if k + 1 < len(starts) else len(lines)
        # An entry also stops at any other heading.
        for j in range(start + 1, end):
            if ANY_HEADING.match(lines[j]):
                end = j
                break
        number = int(Q_HEADING.match(lines[start]).group(1))
        if number in seen:
            out.errors.append(f"ligne {start + 1} : Q{number} apparaît deux fois")
            continue
        seen[number] = start
        entry, err = _parse_entry(lines, start, end, number, path, rel, kind)
        if err:
            out.errors.append(err)
        else:
            out.entries.append(entry)
    return out


def _parse_entry(lines, start, end, number, path, rel, kind):
    context, question_lines, options = [], [], []
    default_line = None
    answer_line = None
    mode = "context"
    for j in range(start + 1, end):
        line = lines[j]
        m_ans = ANSWER.match(line)
        if m_ans:
            if answer_line is not None:
                return None, f"ligne {j + 1} : Q{number} porte deux lignes « Answer: »"
            answer_line = j
            mode = "answer"
            continue
        if mode == "answer":
            if QUESTION.match(line) or OPTIONS.match(line) or DEFAUT.match(line):
                return None, (f"ligne {j + 1} : Q{number}, « {line.split(':')[0]}: » "
                              "sous « Answer: »")
            continue
        m = QUESTION.match(line)
        if m:
            mode = "question"
            question_lines.append(m.group(1).strip())
            continue
        if OPTIONS.match(line):
            mode = "options"
            continue
        m = DEFAUT.match(line)
        if m:
            default_line = m.group(1).strip()
            mode = "defaut"
            continue
        if mode == "context":
            if not line.strip():
                continue
            if not CONTEXT_KEY.match(line):
                return None, (f"ligne {j + 1} : Q{number}, ligne hors gabarit avant « Question: » "
                              "— attendu « Block: », « Terms: », « Entries: » ou « Kind: »")
            context.append(line.strip())
        elif mode == "question":
            question_lines.append(line.rstrip())
        elif mode == "options":
            m = OPTION_ITEM.match(line)
            if m:
                options.append(m.group(1).strip())
            elif line.strip():
                return None, f"ligne {j + 1} : Q{number}, sous « Options: », une ligne qui n'ouvre pas sur « - »"
        elif mode == "defaut":
            if line.strip():
                return None, f"ligne {j + 1} : Q{number}, « Défaut: » tient sur une ligne"

    if answer_line is None:
        return None, f"ligne {start + 1} : Q{number} n'a pas de ligne « Answer: »"

    # The answer runs to the end of the entry, less trailing blanks.
    answer_end = answer_line
    for j in range(end - 1, answer_line, -1):
        if lines[j].strip():
            answer_end = j
            break
    first = ANSWER.match(lines[answer_line]).group(1)
    body = [first.strip()] + lines[answer_line + 1:answer_end + 1]
    answer = "\n".join(body).strip()

    question = "\n".join(question_lines).strip()
    if not question:
        return None, f"ligne {start + 1} : Q{number} n'a pas de « Question: »"
    default = default_source = None
    if default_line is not None:
        default, default_source = _split_default(default_line, options)

    empty = bool(ANSWER_EMPTY.match(lines[answer_line]))
    if kind == "technique":
        # /6_convertit: answered when no `^Answer:\s*$` line is left.
        is_open = empty
    else:
        # /1_lexique, /2_structure, /4_grille: `^Answer:\s*$` with no
        # `Défaut:` above it in the same entry.
        is_open = empty and default_line is None
    q = Question(
        id=f"q:{rel}#{number}",
        file=path, rel=rel, kind=kind, number=number,
        context=context, question=question, options=options,
        default=default, default_source=default_source,
        answer=answer,
        open=is_open,
        answer_empty=empty,
        fingerprint=_fingerprint(question, options, default_line),
        heading_line=start, answer_line=answer_line, answer_end=answer_end,
    )
    return q, None


def parse_file(path: str, work_dir: str) -> ParsedFile:
    rel = os.path.relpath(path, work_dir).replace(os.sep, "/")
    tf = textfile.load(path)
    return parse_lines(tf.lines, path, rel, file_kind(path))


def scan(work_dir: str):
    """Every entry to show, and every file that could not be read."""
    shown, errors = [], []
    for path in find_files(work_dir):
        rel = os.path.relpath(path, work_dir).replace(os.sep, "/")
        try:
            parsed = parse_file(path, work_dir)
        except textfile.UnreadableFile as e:
            errors.append(FileError(path, rel, str(e)))
            continue
        if parsed.errors:
            more = len(parsed.errors) - 1
            msg = parsed.errors[0] + (f" (et {more} autre{'s' if more > 1 else ''})" if more else "")
            errors.append(FileError(path, rel, msg))
            # A file half read is not shown half: its answers would be
            # written against a shape the cockpit did not understand.
            continue
        for e in parsed.entries:
            if is_shown(e):
                shown.append(e)
    return shown, errors


def is_shown(e: Question) -> bool:
    """The `Answer:` line is empty: open, or a default waiting to be kept."""
    return e.open or (e.default is not None and e.answer_empty)
