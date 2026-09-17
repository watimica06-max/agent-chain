#!/usr/bin/env python3
"""Mechanical coherence check for .claude/agents/ and .claude/commands/.

Catches the defect class an edit introduces and a reading rarely sees:
unclosed bold, dead cross-references, announced counts that no longer
match, colliding move numbers, orphan fragments, repeated lines, tools
no gesture names.

    python3 .claude/scripts/coherence.py            # the whole chain
    python3 .claude/scripts/coherence.py agents/x.md   # one file

Exit code 1 when anything is found, so it can gate a commit.
"""
import glob
import re
import sys

NUM_WORDS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11,
    "twelve": 12,
}
# words this chain has got wrong before, and their fix
TYPOS = {"tshe": "the", "teh": "the", "adn": "and"}


def paragraphs(text):
    for p in text.split("\n\n"):
        if not p.strip():
            continue
        if all(l.startswith("    ") or not l.strip()
               for l in p.split("\n")):
            continue        # an indented block is code, not prose
        yield p


def headings(text):
    return [h.strip() for h in re.findall(r"(?m)^#+ (.+)$", text)]


def bold_titles(text):
    """Bold-only lines act as headings in these files."""
    return [m.strip() for m in re.findall(r"(?m)^\*\*(.+?)\*\*$", text)]


def check(path):
    text = open(path, encoding="utf-8").read()
    body = text.split("---\n", 2)[-1] if text.startswith("---") else text
    out = []

    # 0. frontmatter: a value carrying `: ` must be quoted
    if text.startswith("---"):
        for line in text.split("---", 2)[1].split("\n"):
            if not re.match(r"^\w+: ", line):
                continue
            value = line.split(": ", 1)[1]
            if ": " in value and not value.startswith(('"', "'")):
                out.append(("frontmatter", "%s: value holds `: ` unquoted"
                            % line.split(":")[0]))

    # 0b. a table row that does not end on a pipe
    for n, line in enumerate(body.split("\n"), 1):
        if line.startswith("|") and not line.rstrip().endswith("|"):
            out.append(("table row", "line %d does not close on a pipe" % n))

    # 1. unclosed bold, per paragraph — code spans stripped first
    for p in paragraphs(body):
        bare = re.sub(r"`[^`]*`", "", p)
        if bare.count("**") % 2:
            out.append(("unclosed bold", p.split("\n")[0][:70]))

    # 2. dead cross-references
    targets = [t.lower() for t in headings(text) + bold_titles(text)]
    for m in re.finditer(r"see \*([^*\n]{4,60})\*", body):
        ref = m.group(1).strip().lower()
        if ref in ("below", "there", "above"):
            continue
        if not any(ref in t for t in targets):
            out.append(("dead reference", "see *%s*" % m.group(1)[:50]))

    # 3. announced counts against what follows
    for m in re.finditer(
        r"\*\*(%s) (moves|passes|fields|headings|questions|filters|"
        r"shapes|sources|parts|invocations|places|greps|reads|lines)\b"
        % "|".join(NUM_WORDS), body, re.I):
        said = NUM_WORDS[m.group(1).lower()]
        what = m.group(2).lower()
        tail = body[m.end():]
        nxt = re.search(r"(?m)^#+ ", tail)      # stop at the next heading
        if nxt:
            tail = tail[:nxt.start()]
        if what in ("moves", "passes"):
            found = len(set(re.findall(r"(?m)^\*\*(\d+[a-z]?)\.", tail)))
        elif what == "headings":
            found = len(re.findall(r"(?m)^    ## ", tail))
        else:
            continue
        if found and found != said:
            out.append(("count", "%s %s announced, %d found"
                        % (m.group(1), what, found)))

    # 4. move numbers: collisions and gaps, per numbered run
    runs, current = [], []
    for line in body.split("\n"):
        m = re.match(r"^\*\*(\d+)([a-z]?)\.", line)
        if m:
            if m.group(2):      # 2b, 4b — an insertion, not a new number
                continue
            current.append(int(m.group(1)))
        elif line.startswith("#") and current:
            runs.append(current)
            current = []
    if current:
        runs.append(current)
    for run in runs:
        if len(run) != len(set(run)):
            out.append(("move numbers", "repeated in %s" % run))
        elif run and run != list(range(run[0], run[0] + len(run))):
            out.append(("move numbers", "gap in %s" % run))

    # 5. orphan fragments — a paragraph opening mid-sentence
    for p in paragraphs(body):
        first = p.lstrip()
        if re.match(r"^(and|or|but|which|that|so)\b", first, re.I):
            out.append(("orphan fragment", first[:70]))
        # a marker followed by a lowercase continuation
        if re.match(r"^[🔴⚠️📌]+\s*\*\*[a-z]", first) and not re.match(
                r"^[🔴⚠️📌]+\s*\*\*[a-z]\.", first) and not re.match(
                r"^[🔴⚠️📌]+\s*\*\*(a|an|the|you|it|its|one|two|three|no|not|"
                r"never|every|each|when|where|what|which|write|read|say|"
                r"name|take|give|leave|stop|ask)\b", first, re.I):
            out.append(("lowercase opening", first[:70]))

    # 6. empty separators — a `---` with nothing between it and the next
    for m in re.finditer(r"\n---\n\s*\n---", body):
        out.append(("empty separator", "two rules, nothing between"))

    # 6b. a trailing rule at the end of the file
    if re.search(r"\n---\n?\s*$", body):
        out.append(("trailing rule", "the file ends on a separator"))

    # 7. a line repeated back to back
    lines = [l.strip() for l in body.split("\n")]
    for a, b in zip(lines, lines[1:]):
        if a and a == b and len(a) > 20:
            out.append(("repeated line", a[:70]))

    # 8. known typos
    for bad, good in TYPOS.items():
        if re.search(r"\b%s\b" % bad, body):
            out.append(("typo", "%s → %s" % (bad, good)))

    return out


def main():
    args = sys.argv[1:]
    if args:
        files = [a if a.startswith(".claude") else ".claude/" + a
                 for a in args]
    else:
        files = sorted(glob.glob(".claude/agents/*.md")
                       + glob.glob(".claude/commands/*.md"))

    total = 0
    for f in files:
        found = check(f)
        if found:
            print("\n%s" % f)
            for kind, detail in found:
                print("  %-18s %s" % (kind, detail))
            total += len(found)

    print("\n%d finding%s across %d files."
          % (total, "" if total == 1 else "s", len(files)))
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
