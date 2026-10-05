"""The last `Next:` line of a relay — the grammar of `.claude/CLAUDE.md`:

    Next: run /<command> <arguments>
    Next: answer <questions | blocking | questions and blocking>[, then run /<command> <arguments>]
    Next: manual <what the Product Owner does>[, then run /<command> <arguments>]
    Next: stop <reason>
    Next: done

No line, or a line outside the grammar → « unknown ». The cockpit never
fills that gap.
"""
import re
from dataclasses import dataclass, asdict

LINE = re.compile(r"^\s*[*_`>\s]*Next:\s*(.*?)[*_`\s]*$")
RUN = re.compile(r"^run\s+/([A-Za-z0-9_-]+)(?:\s+(.*))?$")
THEN = re.compile(r",\s*then run\s+/([A-Za-z0-9_-]+)(?:\s+(.*))?$")
ANSWER_WHAT = ("questions and blocking", "questions", "blocking")


@dataclass
class Next:
    kind: str                    # run, answer, manual, stop, done, unknown
    raw: str = ""                # the line as printed, "" when there is none
    command: str | None = None   # run: the command; answer/manual: the one after
    args: str = ""
    what: str | None = None      # answer: questions, blocking, questions and blocking
    text: str = ""               # manual: the instruction; stop: the reason

    def to_dict(self):
        d = asdict(self)
        d["french"] = describe_fr(self)
        return d


def find_line(relay: str) -> str | None:
    last = None
    for line in (relay or "").splitlines():
        m = LINE.match(line)
        if m:
            last = m.group(1).strip()
    return last


def _then(rest):
    m = THEN.search(rest)
    if not m:
        return rest.strip(), None, ""
    return rest[:m.start()].strip(), m.group(1), (m.group(2) or "").strip()


def parse(relay: str) -> Next:
    body = find_line(relay)
    if body is None:
        return Next("unknown")
    raw = "Next: " + body
    if body == "done":
        return Next("done", raw)
    m = RUN.match(body)
    if m:
        return Next("run", raw, command=m.group(1), args=(m.group(2) or "").strip())
    if body.startswith("answer "):
        what, cmd, args = _then(body[len("answer "):])
        if what not in ANSWER_WHAT:
            return Next("unknown", raw)
        return Next("answer", raw, command=cmd, args=args, what=what)
    if body.startswith("manual "):
        text, cmd, args = _then(body[len("manual "):])
        if not text:
            return Next("unknown", raw)
        return Next("manual", raw, command=cmd, args=args, text=text)
    if body == "stop" or body.startswith("stop "):
        reason = body[len("stop"):].strip()
        return Next("stop", raw, text=reason)
    return Next("unknown", raw)


WHAT_FR = {
    "questions": "aux questions",
    "blocking": "aux fichiers de blocage",
    "questions and blocking": "aux questions et aux fichiers de blocage",
}


def describe_fr(n: Next) -> str:
    then = f", puis lancer /{n.command} {n.args}".rstrip() if n.command else ""
    if n.kind == "run":
        return f"Lancer /{n.command} {n.args}".rstrip() + "."
    if n.kind == "answer":
        return f"Répondre {WHAT_FR[n.what]}{then}."
    if n.kind == "manual":
        return f"À faire à la main : {n.text}{then}."
    if n.kind == "stop":
        return f"Arrêt : {n.text}." if n.text else "Arrêt."
    if n.kind == "done":
        return "Étape terminée."
    if n.raw:
        return f"Prochaine étape inconnue : la ligne « {n.raw} » sort de la grammaire."
    return "Prochaine étape inconnue : le relais ne porte pas de ligne « Next: »."
