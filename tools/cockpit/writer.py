"""Write the Product Owner's answers and decisions — TECHNICAL_V1 §8.1,
§8.2, §8.3, §8.4.

Every write goes back to the file it was read from. After writing, the
file is read again and the command's own test is run on it: if the entry
still reads as open, the write is undone and the error reported.
"""
import re
import threading
from dataclasses import dataclass, asdict

import blocking
import questions
import textfile

_lock = threading.Lock()

FORBIDDEN_LINE = re.compile(r"^(#|(Answer|Question|Options|Défaut):)")
NUMBERED_START = re.compile(r"^\s*\d+\.")


@dataclass
class Choice:
    """What she picked in the form for one entry.

    kind: "default" (keep `Défaut:`), "option" (one of the options),
          "free" (her own text), or "none" (left for later).
    """
    kind: str
    option: str | None = None
    text: str = ""


@dataclass
class Result:
    id: str
    status: str          # "saved", "unchanged", "skipped", "error"
    message: str = ""
    written: str = ""

    def to_dict(self):
        return asdict(self)


class WriteError(Exception):
    pass


# ------------------------------------------------------------ composing

def _clean(text: str) -> str:
    lines = [l.rstrip() for l in (text or "").replace("\r\n", "\n").split("\n")]
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    if lines:
        lines[0] = lines[0].lstrip()
    return "\n".join(lines)


def compose(choice: Choice, options: list[str], default: str | None = None) -> str | None:
    """The text that goes into the file, or None when nothing is written.

    §8.1: the default kept with no remark leaves `Answer:` empty; an option
    is written in full; an option and a remark is `<option> — <remark>`;
    free text is written as typed."""
    remark = _clean(choice.text)
    if choice.kind == "none":
        return None
    if choice.kind == "default":
        if default is None:
            raise WriteError("aucune valeur par défaut pour cette question")
        return None if not remark else f"{default} — {remark}"
    if choice.kind == "option":
        if choice.option not in options:
            raise WriteError("l'option choisie n'est plus dans le fichier")
        return choice.option if not remark else f"{choice.option} — {remark}"
    if choice.kind == "free":
        if not remark:
            raise WriteError("le texte libre est vide")
        return remark
    raise WriteError(f"choix inconnu : {choice.kind}")


def _check_lines(text: str):
    for line in text.split("\n"):
        if FORBIDDEN_LINE.match(line):
            raise WriteError(
                f"une ligne commence par « {line[:12]} » : elle serait lue comme un titre "
                "ou un champ du fichier — reformulez-la")


# ------------------------------------------------------------ questions

def write_question(entry: questions.Question, choice: Choice) -> Result:
    try:
        text = compose(choice, entry.options, entry.default)
    except WriteError as e:
        return Result(entry.id, "error", str(e))
    if text is None and choice.kind == "default" and entry.kind == "technique":
        # /6_convertit reads `technique-*.md` on `^Answer:\s*$` alone, with no
        # `Défaut:` exception: the kept default has to be written out.
        text = entry.default
    if text is None:
        if choice.kind == "default":
            return Result(entry.id, "unchanged",
                          "défaut gardé : « Answer: » reste vide, la chaîne le lit comme accepté")
        return Result(entry.id, "skipped")
    try:
        _check_lines(text)
    except WriteError as e:
        return Result(entry.id, "error", str(e))

    with _lock:
        try:
            original = textfile.read_bytes(entry.file)
        except OSError as e:
            return Result(entry.id, "error", f"lecture impossible : {e}")
        try:
            tf = textfile.decode(entry.file, original)
            current = _find_question(tf, entry)
            if not current.answer_empty:
                raise WriteError("déjà répondu dans le fichier depuis l'affichage — rechargez")
            first, *rest = text.split("\n")
            new = ["Answer: " + first] + rest
            tf.lines[current.answer_line:current.answer_end + 1] = new
            textfile.write_bytes(entry.file, tf.encode())
            _verify_question(entry, text)
        except (WriteError, textfile.UnreadableFile, OSError) as e:
            _restore(entry.file, original)
            return Result(entry.id, "error", str(e))
    return Result(entry.id, "saved", written=text)


def _find_question(tf, entry):
    parsed = questions.parse_lines(tf.lines, entry.file, entry.rel, entry.kind)
    if parsed.errors:
        raise WriteError("le fichier ne se lit plus : " + parsed.errors[0])
    for q in parsed.entries:
        if q.number == entry.number:
            if q.fingerprint != entry.fingerprint:
                raise WriteError(f"Q{entry.number} a changé dans le fichier depuis l'affichage — rechargez")
            return q
    raise WriteError(f"Q{entry.number} n'est plus dans le fichier")


def _verify_question(entry, text):
    """§8.4 — the command's own test, on the file as written."""
    tf = textfile.load(entry.file)
    parsed = questions.parse_lines(tf.lines, entry.file, entry.rel, entry.kind)
    if parsed.errors:
        raise WriteError("après écriture le fichier ne se lit plus : " + parsed.errors[0])
    for q in parsed.entries:
        if q.number == entry.number:
            if q.answer_empty or q.open:
                raise WriteError("après écriture la commande lirait encore la question comme ouverte")
            if q.answer != text.strip():
                raise WriteError("après écriture la réponse relue diffère de la réponse écrite")
            return
    raise WriteError(f"après écriture Q{entry.number} est introuvable")


# ------------------------------------------------------------ blocking

def write_blocking(entry: blocking.BlockingEntry, choice: Choice) -> Result:
    try:
        text = compose(choice, entry.options)
    except WriteError as e:
        return Result(entry.id, "error", str(e))
    if text is None:
        return Result(entry.id, "skipped")
    if entry.shape == 4:
        # One line `N. <text>` per entry: the command counts numbered lines.
        text = " ".join(text.split())
    try:
        _check_lines(text)
    except WriteError as e:
        return Result(entry.id, "error", str(e))

    with _lock:
        try:
            original = textfile.read_bytes(entry.file)
        except OSError as e:
            return Result(entry.id, "error", f"lecture impossible : {e}")
        try:
            tf = textfile.decode(entry.file, original)
            current = _find_blocking(tf, entry)
            lines = tf.lines
            d = current.decision_line
            end = _region_end(lines, d)
            if entry.shape == 4:
                last = d
                for j in range(d + 1, end):
                    if lines[j].strip():
                        last = j
                answer = f"{entry.number}. {text}"
                if last == d:
                    # Nothing under the heading yet: one blank line, then it.
                    lines[d + 1:end] = ["", answer] + ([""] if end < len(lines) else [])
                else:
                    lines[last + 1:last + 1] = [answer]
            else:
                region = lines[d + 1:end]
                if any(l.strip() for l in region):
                    raise WriteError("« ## Decision » n'est plus vide dans le fichier — rechargez")
                new = [""] + text.split("\n")
                if end < len(lines):
                    new.append("")
                lines[d + 1:end] = new
            textfile.write_bytes(entry.file, tf.encode())
            _verify_blocking(entry)
        except (WriteError, textfile.UnreadableFile, OSError) as e:
            _restore(entry.file, original)
            return Result(entry.id, "error", str(e))
    written = f"{entry.number}. {text}" if entry.shape == 4 else text
    return Result(entry.id, "saved", written=written)


def _region_end(lines, d):
    for j in range(d + 1, len(lines)):
        m = blocking.HEADING.match(lines[j])
        if m and len(m.group(1)) <= 2:
            return j
    return len(lines)


def _parse_blocking(tf, entry):
    return blocking.parse_lines(tf.lines, entry.file, entry.rel,
                                work_dir=entry.base or None, worktree=entry.worktree)


def _find_blocking(tf, entry):
    parsed = _parse_blocking(tf, entry)
    if parsed.notices:
        raise WriteError("le fichier ne se lit plus : " + parsed.notices[0])
    for b in parsed.entries:
        if b.id == entry.id:
            if b.fingerprint != entry.fingerprint:
                raise WriteError("l'entrée a changé dans le fichier depuis l'affichage — rechargez")
            if not b.waiting:
                raise WriteError("l'entrée n'attend plus de décision dans le fichier — rechargez")
            return b
    raise WriteError("l'entrée n'est plus dans le fichier — rechargez")


def _verify_blocking(entry):
    tf = textfile.load(entry.file)
    parsed = _parse_blocking(tf, entry)
    if parsed.notices:
        raise WriteError("après écriture le fichier ne se lit plus : " + parsed.notices[0])
    for b in parsed.entries:
        if b.id == entry.id:
            if b.waiting:
                raise WriteError("après écriture la commande lirait encore l'entrée comme en attente")
            return
    raise WriteError("après écriture l'entrée est introuvable")


# --------------------------------------------------------- redecoupage

def write_redecoupage(entry: blocking.Redecoupage, choice: Choice, work_dir: str) -> Result:
    text = _clean(choice.text) if choice.kind in ("free", "option") else ""
    if choice.kind == "none" or not text:
        return Result(entry.id, "skipped")
    try:
        _check_lines(text)
    except WriteError as e:
        return Result(entry.id, "error", str(e))
    with _lock:
        try:
            original = textfile.read_bytes(entry.file)
        except OSError as e:
            return Result(entry.id, "error", f"lecture impossible : {e}")
        try:
            tf = textfile.decode(entry.file, original)
            lines = tf.lines
            idx = blocking._has_po_decision(lines)
            if idx >= 0:
                end = _region_end(lines, idx)
                if any(l.strip() for l in lines[idx + 1:end]):
                    raise WriteError("« ## Décision du Product Owner » est déjà rempli — rechargez")
                new = [""] + text.split("\n") + ([""] if end < len(lines) else [])
                lines[idx + 1:end] = new
            else:
                while lines and not lines[-1].strip():
                    lines.pop()
                lines += ["", "## Décision du Product Owner", ""] + text.split("\n")
                tf.final_newline = True
            textfile.write_bytes(entry.file, tf.encode())
            again = textfile.load(entry.file).lines
            i = blocking._has_po_decision(again)
            if i < 0 or blocking.decision_empty_a2(again, i):
                raise WriteError("après écriture « ## Décision du Product Owner » se lit vide")
        except (WriteError, textfile.UnreadableFile, OSError) as e:
            _restore(entry.file, original)
            return Result(entry.id, "error", str(e))
    return Result(entry.id, "saved", written=text)


def _restore(path, original):
    try:
        textfile.write_bytes(path, original)
    except OSError:
        pass
