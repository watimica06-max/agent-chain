"""What a question is about — cockpit 1.4, `context_rules.md`.

Each writer's entries point somewhere by their own instructions: `Terms:`
to words in the file the lexicographe sweeps, `Block:` to a `### B<n>`
heading, `Entries:` to `§n.m` headings. This module finds that place in
that document, read-only. A writer whose target the instructions do not
give resolves to no context, and says so — never a guess.
"""
import bisect
import os
import re

import questions as questions_mod
import textfile

ROOT_FILE = re.compile(r"^questions-(?P<agent>[A-Za-z0-9_]+(?:-[A-Za-z0-9_]+)*?)-\d+\.md$")
TECHNIQUE = re.compile(r"^technique-(?P<nature>[A-Za-z0-9_-]+)\.md$")
HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
BLOCK_ID = re.compile(r"\bB\d+\b")
ENTRY_ID = re.compile(r"§\d+(?:\.\d+)*")
BRACKET = re.compile(r"\[B\d+[^\]]*\]")

PRODUCT = "desc-produit.md"
FUSION_PRODUCT = "desc-produit-fusion.md"
TECHNICAL = "spec-technique.md"
IDEAS = "idees.md"

# Writer -> (key read, document, rule id in context_rules.md). The document
# is relative to the folder holding the root questions file.
BLOCK_WRITERS = {
    "redacteur": ("CTX-RED", PRODUCT),
    "qualifieur": ("CTX-GEN", PRODUCT),
    "classeur": ("CTX-NAT", PRODUCT),
    "sondeur": ("CTX-GRI", PRODUCT),       # the assembleur's merge, copied by /4_grille
    "existant": ("CTX-EXI", PRODUCT),      # the sondeur's invocation 3
    "convertisseur": ("CTX-CNV", PRODUCT),  # the product questions, merged by /6_convertit
    "fusionneur": ("CTX-FUS", FUSION_PRODUCT),
}


def writer_of(path: str) -> str | None:
    name = os.path.basename(path)
    if TECHNIQUE.match(name) and os.path.basename(os.path.dirname(path)) == "convertisseur":
        return "convertisseur-technique"
    m = ROOT_FILE.match(name)
    return m.group("agent") if m else None


def _key(entry, name):
    """The value of `<name>:` among the lines above `Question:`."""
    for line in entry.context:
        if line.lower().startswith(name.lower() + ":"):
            return line.split(":", 1)[1].strip()
    return None


def _load(path):
    try:
        return textfile.load(path).lines
    except (OSError, textfile.UnreadableFile):
        return None


def _rel(path, base):
    return os.path.relpath(path, base).replace(os.sep, "/")


def _section_end(lines, start, level):
    for j in range(start + 1, len(lines)):
        m = HEADING.match(lines[j])
        if m and len(m.group(1)) <= level:
            return j - 1
    return len(lines) - 1


def _trim(lines, start, end):
    while end > start and not lines[end].strip():
        end -= 1
    return end


def heading_ranges(lines, wanted, pattern):
    """The section of every heading whose first token is one of `wanted`
    (`B7`, `§3.2`), in document order: [{label, start, end}], 0-based,
    inclusive."""
    out = []
    for i, line in enumerate(lines):
        m = HEADING.match(line)
        if not m:
            continue
        tok = pattern.match(m.group(2).strip())
        if tok and tok.group(0) in wanted:
            end = _trim(lines, i, _section_end(lines, i, len(m.group(1))))
            out.append({"label": tok.group(0), "start": i, "end": end})
    return out


# Between two words of a term: a run of spaces, or one line break.
GAP = r"(?:[^\S\n]+|[^\S\n]*\n[^\S\n]*)"


def term_pattern(term):
    # A term as a whole, any case: its words in order, never one of them
    # alone; `atelier` never matches `ateliers`.
    words = term.split()
    return re.compile(r"(?<![\w])" + GAP.join(map(re.escape, words)) + r"(?![\w])", re.IGNORECASE)


def _parts(starts, lines, s, e):
    """The span [s, e) of the joined text, cut line by line."""
    first = bisect.bisect_right(starts, s) - 1
    out = []
    for i in range(first, len(lines)):
        if starts[i] >= e:
            break
        a = max(s, starts[i]) - starts[i]
        b = min(e, starts[i] + len(lines[i])) - starts[i]
        if b > a:
            out.append({"line": i, "start": a, "end": b})
    return out


def term_matches(lines, terms, allowed=None):
    """Every occurrence of every term: [{label, line, start, end, parts}],
    in document order. `line`, `start`, `end` are the first part; `parts`
    holds one span per line the occurrence covers. `allowed` limits the
    search to a set of line numbers."""
    text = "\n".join(lines)
    starts, pos = [], 0
    for line in lines:
        starts.append(pos)
        pos += len(line) + 1
    hits = []
    for t in terms:
        hits += [(m.start(), -m.end(), t) for m in term_pattern(t).finditer(text)]
    hits.sort()                        # in document order; at one place, the longest term first
    out, last = [], -1
    for s, neg_e, t in hits:
        if s < last:                   # overlapping terms: the first wins
            continue
        parts = _parts(starts, lines, s, -neg_e)
        if not parts or (allowed is not None and any(p["line"] not in allowed for p in parts)):
            continue
        out.append({"label": t, **parts[0], "parts": parts})
        last = -neg_e
    return out


def _answer_lines(path, base):
    """Lines of the `Answer:` fields, and of the `Défaut:` line of an entry
    whose `Answer:` is empty — what the lexicographe sweeps at invocations
    3 and 4 (agents/lexicographe.md:440, :450)."""
    lines = _load(path)
    if lines is None:
        return None, None
    parsed = questions_mod.parse_lines(lines, path, _rel(path, base), "questions")
    allowed = set()
    for e in parsed.entries:
        allowed.update(range(e.answer_line, e.answer_end + 1))
        if e.answer_empty:
            for j in range(e.heading_line, e.answer_line):
                if questions_mod.DEFAUT.match(lines[j]):
                    allowed.add(j)
    return lines, allowed


def _none(rule, reason):
    return {"status": "none", "rule": rule, "reason": reason}


def target(entry, work_dir):
    """Where an entry points: the document and what to find in it, without
    reading the document. `work_dir` is the folder the root questions file
    sits in (a technical file sits one level below, in `convertisseur/`)."""
    writer = writer_of(entry.file)
    folder = os.path.dirname(entry.file)
    if writer == "convertisseur-technique":
        folder = os.path.dirname(folder)
    if writer is None:
        return _none("CTX-?", "ce fichier n'est d'aucun rédacteur connu")

    if writer == "lexicographe":
        terms = [t.strip() for t in (_key(entry, "Terms") or "").split(",") if t.strip()]
        if not terms:
            return _none("CTX-LEX12", "l'entrée ne porte pas de ligne « Terms: »")
        others = [n for n in _root_files(folder) if writer_of(n) not in (None, "lexicographe")]
        if len(others) == 1:
            # Invocations 3 and 4: another agent's answered file beside it
            # (1_lexique.md:62-66) — its Answer: fields are what was swept.
            return {"status": "ok", "rule": "CTX-LEX34", "kind": "terms", "terms": terms,
                    "doc": os.path.join(folder, others[0]), "scope": "answers"}
        if len(others) > 1:
            return _none("CTX-LEX34", "deux fichiers d'autres agents à la racine : "
                                      "lequel a été balayé n'est pas dit")
        return {"status": "ok", "rule": "CTX-LEX12", "kind": "terms", "terms": terms,
                "doc": os.path.join(folder, IDEAS), "scope": "all"}

    if writer in BLOCK_WRITERS:
        rule, doc = BLOCK_WRITERS[writer]
        value = _key(entry, "Block")
        if value is None:
            return _none(rule, "l'entrée ne porte pas de ligne « Block: »")
        ids = BLOCK_ID.findall(value)
        if not ids:
            return _none(rule, "« Block: " + value + " » : la question porte sur la feature, "
                               "pas sur un bloc")
        return {"status": "ok", "rule": rule, "kind": "block", "ids": _unique(ids),
                "doc": os.path.join(folder, doc)}

    if writer == "architecte":
        value = _key(entry, "Block") or ""
        ids = ENTRY_ID.findall(value)
        if not ids:
            return _none("CTX-ARC", "« Block: " + value + " » ne nomme aucune entrée § "
                                    "(une entrée de la grille n'est pas lue ici)")
        return {"status": "ok", "rule": "CTX-ARC", "kind": "entries", "ids": _unique(ids),
                "doc": os.path.join(folder, TECHNICAL)}

    if writer == "convertisseur-technique":
        value = _key(entry, "Entries") or ""
        ids = ENTRY_ID.findall(BRACKET.sub("", value))
        outside = BRACKET.findall(value)
        nature = TECHNIQUE.match(os.path.basename(entry.file)).group("nature")
        # Invocation 1: its own section, its own numbers; invocation 2,
        # « transversal », any number of the document (convertisseur.md:436-439).
        doc = (os.path.join(folder, TECHNICAL) if nature == "transversal"
               else os.path.join(folder, "convertisseur", nature + ".md"))
        if not ids:
            return _none("CTX-TEC", "« Entries: " + value + " » ne nomme aucune entrée § de la section"
                         + (" — " + ", ".join(outside) + " est hors de la section" if outside else ""))
        return {"status": "ok", "rule": "CTX-TEC", "kind": "entries", "ids": _unique(ids),
                "doc": doc, "outside": outside}

    return _none("CTX-?", f"aucune règle ne dit où pointe une entrée de « {writer} »")


def _unique(xs):
    seen, out = set(), []
    for x in xs:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def _root_files(folder):
    try:
        return sorted(n for n in os.listdir(folder) if ROOT_FILE.match(n))
    except OSError:
        return []


def resolve(entry, base):
    """The document and the passages, for the page. `base` is the feature
    folder: paths are shown relative to it. Never writes."""
    t = target(entry, base)
    if t["status"] != "ok":
        return t
    doc = t["doc"]
    rel = _rel(doc, base)
    out = {"status": "ok", "rule": t["rule"], "kind": t["kind"], "doc": rel,
           "terms": t.get("terms", []), "ids": t.get("ids", []), "matches": [],
           "missing": list(t.get("terms") or t.get("ids") or [])}
    if t["kind"] == "terms" and t.get("scope") == "answers":
        lines, allowed = _answer_lines(doc, base)
    else:
        lines, allowed = _load(doc), None
    if lines is None:
        return {**out, "status": "missing", "lines": [],
                "reason": f"{rel} n'existe pas ou ne se lit pas"}
    out["lines"] = lines
    if t["kind"] == "terms":
        out["terms"] = t["terms"]
        out["scope"] = t["scope"]
        out["matches"] = term_matches(lines, t["terms"], allowed)
        wanted = t["terms"]
        found = {m["label"].lower() for m in out["matches"]}
        out["missing"] = [x for x in wanted if x.lower() not in found]
    else:
        pattern = re.compile(r"B\d+\b") if t["kind"] == "block" else re.compile(r"§\d+(?:\.\d+)*")
        out["ids"] = t["ids"]
        out["matches"] = heading_ranges(lines, set(t["ids"]), pattern)
        found = {m["label"] for m in out["matches"]}
        out["missing"] = [x for x in t["ids"] if x not in found]
        if t.get("outside"):
            out["outside"] = t["outside"]
    if not out["matches"]:
        out["status"] = "notfound"
        what = ", ".join(out["missing"])
        out["reason"] = (f"aucune occurrence de {what} dans {rel}" if t["kind"] == "terms"
                         else f"{what} introuvable dans {rel}")
    return out
