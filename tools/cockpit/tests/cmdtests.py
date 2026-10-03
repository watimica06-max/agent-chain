r"""The commands' own tests, written from the command files and nothing
else — independent of the cockpit's parsers, so that a parser bug cannot
hide itself.

- /1_lexique, /2_structure, /4_grille: an entry is unanswered when it
  holds `^Answer:\s*$` with no `Défaut:` above it in the same entry.
- /6_convertit: `technique-*.md` is answered when it holds a `### Q` and
  no `^Answer:\s*$` line.
- shapes 1-3: `grep -A2 '^## Decision$'` — nothing under the heading.
- shape 4: an entry is open when its number has no `N.` line under
  `## Decision` (cmd/8_code.md:330-335).
- shape 5: read on the last `## Decision`.
"""
import re


def _lines(path):
    with open(path, encoding="utf-8-sig") as f:
        return f.read().splitlines()


def unanswered_questions(path):
    """Numbers of the `### Q` entries the command still reads as open."""
    out, cur, has_default, empty = [], None, False, False

    def close():
        if cur is not None and empty and not has_default:
            out.append(cur)

    for line in _lines(path):
        m = re.match(r"^### Q(\d+)", line)
        if m:
            close()
            cur, has_default, empty = int(m.group(1)), False, False
            continue
        if re.match(r"^Défaut:", line):
            has_default = True
        if re.match(r"^Answer:\s*$", line):
            empty = True
    close()
    return out


def technique_answered(path):
    lines = _lines(path)
    return any(l.startswith("### Q") for l in lines) and not any(
        re.match(r"^Answer:\s*$", l) for l in lines)


def a2_empty(path):
    """One boolean per `^## Decision$`, as `grep -A2` shows it."""
    lines = _lines(path)
    out = []
    for i, l in enumerate(lines):
        if l == "## Decision":
            after = lines[i + 1:i + 3]
            filled = False
            for a in after:
                if a.startswith("#"):
                    break
                if a.strip():
                    filled = True
                    break
            out.append(not filled)
    return out


def shape4_open(path):
    lines = _lines(path)
    heads = [int(m.group(1)) for m in (re.match(r"^## Blocking (\d+)", l) for l in lines) if m]
    d = max(i for i, l in enumerate(lines) if l == "## Decision")
    numbered = {int(m.group(1)) for m in (re.match(r"^(\d+)\.", l) for l in lines[d + 1:]) if m}
    return [n for n in heads if n not in numbered]


def numbered_count(path):
    lines = _lines(path)
    d = max(i for i, l in enumerate(lines) if l == "## Decision")
    return sum(1 for l in lines[d + 1:] if re.match(r"^\d+\.", l))
