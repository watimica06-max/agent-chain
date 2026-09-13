# Assembleur — comments

Agent: `.claude/agents/assembleur.md`
Command: `.claude/commands/4_grille.md` (the only one that invokes it)

Role, from the file: takes the four question files the sondeurs wrote
on one turn, groups their questions by block, drops within a group
what one answer would close twice, and writes one numbered list with
every question copied word for word.

Moves, in order: (1) read the named files whole, stop on a missing
one; (2) gather questions per `Block:` id, a multi-id line in every
group it names, `Block: -` last; (3) within a group, drop a question
another one's answer would close, keeping the most precise, keeping
both in doubt; (4) write `questions.md` renumbered from `Q1`, `Answer:`
empty; (5) append the `## Merge` count; (6) write the count alone when
no file holds a question. Every move feeds the output; none is idle;
the order is right. What is wrong sits inside moves 2, 3 and 5, in the
stop conditions, and in what the command does with the file afterwards.

---

## Comments

### 1

    Fichier      : .claude/agents/assembleur.md
    Cible        : Part 3, "How you merge" — the tie rule "When two say
                   the same thing, keep the one that states it most
                   precisely", together with the test "two questions
                   are the same when answering one answers the other"
    Aujourd'hui  : the sameness test is satisfied in one direction
                   ("answering one answers the other"), and the tie is
                   settled by precision. The file's own example shows
                   the pair: "what format does the date take" and "is
                   the hour written with a leading zero" are declared
                   one question.
    Le défaut    : Plane 3, criterion 4 (two readings) and Plane 2,
                   question 1. Answering the format question answers
                   the leading-zero one; the reverse does not hold. On
                   the "most precise" reading, the leading-zero question
                   is kept and the format question is dropped — the
                   broader gap is lost, and the person's answer ("yes, a
                   zero") closes nothing about the format. On the other
                   reading, "precise" means "best worded", and two
                   readers keep different questions.
    Ce qu'il faut: when one question's answer closes the other and not
                   the reverse, the kept question is the one whose
                   answer closes the other — the covering one. Only when
                   each answer closes the other does wording decide.
    Justification: robustness — a covering gap dropped for its narrower
                   twin is a gap that reaches the code; the example in
                   the file is exactly that case.

### 2

    Fichier      : .claude/agents/assembleur.md
    Cible        : Part 3, "How you merge" — the multi-block rule
                   ("`Block: B12, B15` is gathered with `B12` and with
                   `B15`", "a question kept once is kept once") and the
                   drop rule, read together with "everything else is
                   copied as written"
    Aujourd'hui  : a question naming several blocks is compared in each
                   of its groups; nothing says what happens when it is a
                   duplicate in one group and not in another, or when it
                   is dropped against a twin whose `Block:` line names
                   fewer blocks than its own.
    Le défaut    : Plane 2, question 1 (the move does not reach as far
                   as it claims) and question 3 (a case not foreseen).
                   Two failures follow. (a) `Q: Block: B12, B15` is a
                   twin of `Qa: Block: B12` in group B12, and of nothing
                   in group B15; the agent drops it in B12 and it is
                   gone from B15 too — the gap between the two blocks
                   the global sondeur was run to find is lost. (b) It is
                   a twin of `Qa: Block: B12` and `Qa` is the more
                   precise; `Qa` is kept with its `Block: B12` line
                   copied as written, and B15 no longer appears anywhere
                   in the output — whoever places the answer by the
                   `Block:` line never touches B15.
    Ce qu'il faut: a question is dropped only against a twin whose
                   `Block:` line names every block the dropped one
                   names. A multi-block question that has a twin in one
                   of its groups and none in another stays, whatever the
                   twin's precision. The `Block:` line stays uneditable,
                   as today — the rule above makes editing it
                   unnecessary.
    Justification: robustness — both cases drop a cross-block gap, the
                   one kind of gap a single reading cannot find and the
                   global invocation is paid for.

### 3

    Fichier      : .claude/agents/assembleur.md
    Cible        : Part 1, "Role" ("dropping what two of them raise
                   twice"), "What you never do" ("Drop a question raised
                   by one sondeur only"), against Part 3 ("within a
                   group, two questions are the same when …")
    Aujourd'hui  : the role and the forbidden list count sondeurs; the
                   merge rule counts answers and never mentions which
                   file a question came from.
    Le défaut    : Plane 3, criterion 4, and the known case "two
                   passages asking for different things". Two questions
                   from one file that one answer closes — a
                   question-by-question reading raises the same gap
                   under two grid questions; the global raises one
                   crossing from both sides — are "raised by one sondeur
                   only" under the first passage and duplicates under
                   the second. One agent drops them, the next keeps
                   them.
    Ce qu'il faut: one reading, stated once: the file a question came
                   from is not part of the test; what is never dropped
                   is a gap that no other question's answer closes,
                   whoever raised it. I conclude the same-file pair is
                   dropped; the forbidden line should say "a gap raised
                   once", not "a sondeur alone".
    Justification: round trips — the person answers one gap twice on
                   every same-file pair; robustness unchanged under the
                   in-doubt rule.

### 4

    Fichier      : .claude/agents/assembleur.md
    Cible        : Part 2 ("Read those files, whole"), Part 3 ("How you
                   merge" — the `Block:` line, `Block: -`), and "When
                   you cannot produce"
    Aujourd'hui  : the input's shape is never stated. The agent learns
                   that a question has a `Block:` line from the
                   gathering rule, that `-` means no block from one
                   sentence, and the rest from its own output format
                   ("copied, word for word"). The only stop is a missing
                   file — a case the command already refuses before
                   invoking ("Check the four questions files exist …
                   a missing one stops the command").
    Le défaut    : Plane 2, question 3 (what happens when it cannot) and
                   question 4 (a reader who has seen nothing else). The
                   foreseen stop cannot occur; the stops that can are
                   not foreseen: a question with no `Block:` line, a
                   `Block:` value that is neither ids nor `-`, a file
                   that is neither empty nor a list of questions (a
                   sondeur's prose "nothing found", a heading with no
                   entry). On each, the agent chooses silently — files
                   it under `-`, skips it, counts the file as empty —
                   and the `## Merge` count hides the choice.
    Ce qu'il faut: the shape one input question takes is stated (the
                   heading, the `Block:` line and its two forms, the
                   `Question:` line, the empty `Answer:`), and what
                   counts as an empty file. A question the agent cannot
                   place in a group, or a file whose content is neither
                   empty nor that shape, is a stop in
                   `blocked_assembleur.md`, naming the file and the
                   passage — never a guess. The missing-file line can
                   stay; it costs nothing, since the files are opened
                   anyway.
    Justification: robustness — a question silently filed under `-` or
                   skipped is a gap that never reaches the person, and
                   the merge reads as complete.

### 5

    Fichier      : .claude/agents/assembleur.md
    Cible        : frontmatter, `tools: Read, Grep, Glob, Write`
    Aujourd'hui  : Grep and Glob are granted; no move greps or globs,
                   and Part 2 forbids the one use they would have
                   ("Never inferred from the folder — the orchestrator
                   looked, you do not look again").
    Le défaut    : Plane 2, question 2 (a capability nothing uses) and
                   the known case of a forbidden thing kept reachable.
                   The folder the agent works in also holds `closed/`
                   (previous turns' files under the same names) and the
                   blocking files; a listing is how a previous turn's
                   `par-bloc-NN.md` enters a merge.
    Ce qu'il faut: the agent can read and write, and nothing else; the
                   rule "never inferred from the folder" then holds by
                   construction.
    Justification: robustness — a stale file merged is a turn of
                   already-answered questions asked again; tokens —
                   nothing to pay for a listing.

### 6

    Fichier      : .claude/commands/4_grille.md
    Cible        : the order of the sections "The four invocations" →
                   "Then the merge" → … → "What you relay", where the
                   last line reads "If an agent returns a `blocked_*.md`:
                   relay it and stop"
    Aujourd'hui  : the only check between the four sondeurs and the
                   merge is that the four files and the record exist.
                   The stop on a sondeur's blocking file is the last
                   sentence of the command, after the merge, the copy to
                   the root and the relay table.
    Le défaut    : Plane 1, order (a constraint stated after what it
                   constrains); for the command, "does what it says to
                   run next match what can happen". A sondeur that
                   blocks and still leaves its file — whole or partial —
                   passes the existence check; the merge runs, the
                   turn's `questions-sondeur-NN.md` is written as if
                   four full readings were in it, and the block is
                   relayed afterwards, next to a file that looks
                   complete. If the partial file is empty and the others
                   raise nothing, the loop ends on it.
    Ce qu'il faut: the blocking-file check on the four sondeurs sits
                   between "wait for all four" and the merge: any
                   `cadrage-produit/blocked_*.md` at its unnumbered name
                   means no merge this turn, and no questions file at
                   the root.
    Justification: robustness — a merge missing one reading is the
                   case the command itself names as "a merge nobody can
                   trust", and this is the path by which it happens;
                   round trips — a merge paid, then discarded.

### 7

    Fichier      : .claude/commands/4_grille.md
    Cible        : "Once it has reported" — copy of
                   `cadrage-produit/questions.md` to
                   `questions-sondeur-NN.md`, "Renumber `Q1` upward",
                   "Drop its closing `## Merge` section", and "What you
                   relay" (the counts); with the agent's Part 3 "What
                   you write" on the other side
    Aujourd'hui  : the agent numbers from `Q1` in block order and
                   appends `## Merge`. The command, which "never open[s]
                   … a questions file's content", then renumbers a file
                   already numbered from `Q1` (a no-op, or a second
                   numbering scheme nobody describes — two readings),
                   strips a section from inside it (a content edit on a
                   file it may not read), and relays per-file and kept
                   counts from a source it does not name. The agent
                   expects an `<out>` folder; the prompt gives a file
                   path.
    Le défaut    : Plane 1 (a move whose result is undone downstream:
                   the `## Merge` section has one reader, and that
                   reader deletes it), and for the command, "does the
                   prompt carry what the agent needs" — the destination
                   the agent could write to directly is known to the
                   command (it computes `NN`) and withheld.
    Ce qu'il faut: after the agent has written, the command edits no
                   line of the questions file. Either the prompt names
                   the final destination and the agent writes the
                   turn's file where it will be read, or the count
                   leaves the questions file — the agent's report, or a
                   file of its own — and the renumber line goes. Either
                   way the counts the command relays come from a named
                   place (the report, or a grep of the count lines).
    Justification: round trips — a by-hand content edit by the
                   orchestrator on a file it must not read is the class
                   of step that fails and costs the turn; tokens — one
                   file written once instead of written, copied, and
                   archived twice (`closed/` and `questions/sondeur/`).

### 8

    Fichier      : .claude/commands/4_grille.md
    Cible        : "What you relay" — the row "Wrote a blocking file →
                   Fill its `## Decision`, then `/4_grille` again", as
                   it applies to `blocked_assembleur.md`; and "Git, in
                   this mode" (the archiving of the six files before
                   invoking)
    Aujourd'hui  : one row for every blocking file. On the assembleur's,
                   the relaunch archives the four sondeur files into
                   `closed/`, re-runs four opus sondeurs, and only then
                   names the decision in the assembleur's prompt — on
                   four fresh files that no longer contain what the
                   decision was about.
    Le défaut    : for the command, "every row names an outcome … and
                   what to run next matches what can happen". Today the
                   assembleur's block cannot occur (comment 4's
                   pre-check); once comment 4 gives it real stop cases,
                   this row answers each with a full turn, and the
                   decision the person wrote is read against inputs that
                   have been replaced.
    Ce qu'il faut: a settled `blocked_assembleur.md` re-runs the merge
                   alone, on the four files still standing, with the
                   decision in its prompt — no archiving, no sondeur.
                   The row says so, and the git section leaves the
                   four files in place in that case.
    Justification: tokens — four opus invocations, the largest reading
                   of the upstream, paid for a sonnet merge that failed
                   on its input; round trips — a decision answered
                   against nothing, and the same block possibly written
                   again.

---

## From the verdict

Section 2, "Assembleur — the role holds … reads question files only,
so it cannot lose a hole by comparing to the product file … 'in doubt
keep both' prices the error correctly."
Already found, and narrower than the agent: the in-doubt rule holds,
but the tie rule beside it ("keep the one that states it most
precisely") can drop the covering question of a pair — comment 1. The
agent can lose a hole without ever opening the product file.

Sweep row 16 — the four sondeur files → Assembleur; `/4_grille`
checks existence; "wired".
Already found. The command's existence check is what makes the agent's
own missing-file stop a net that never fires (comment 4); the wire
holds, the stop that matters is elsewhere.

Sweep row 20 — `cadrage-produit/questions.md` (with `## Merge`) →
`/4_grille` copies, renumbers, strips `## Merge`; "wired".
Already found, as the defect: the wire is a content edit by a command
that may not read the file, on a numbering that already exists —
comment 7.

Sweep row 22 — `Block:` line, "ids only, `-` for feature-level";
readers: Assembleur (groups), Rédacteur (where it lands).
Not found as such; the agent confirms both forms and adds the
multi-id list (`Block: B12, B15`), which the row does not name. The
row's second reader is what gives comment 2 its weight: a kept twin
whose `Block:` line names fewer blocks is a block the answer never
lands in.

Loop U5 — four Sondeurs → Assembleur → `/4_grille` → person …; stop
by the command's grep.
Already found; nothing in the agent moves the stop. Comment 6 names
the path by which a blocked reading enters the loop as a complete one.

D7 (command-level, not the agent) — "`cadrage-produit/closed/` is
created and nothing is said to fill or read it."
Contradicted by the command. `4_grille.md`, "Git, in this mode": "And
the previous turn's six `cadrage-produit/` files: `git mv
docs/features/<name>/cadrage-produit/par-bloc.md
docs/features/<name>/cadrage-produit/closed/par-bloc-NN.md` — The same
for `par-question.md`, `par-nature.md`, `global.md`, `releve.md` and
`questions.md`." The producer is the command; a reader is still
nobody, which is the half of D7 that stands.

---

## What another agent would settle

Does the sondeur write each question as `### Qn` / `Block:` /
`Question:` / `Answer:`, `-` for a feature-level question, a
comma-separated id list for a crossing, and a truly empty file when
it found nothing?
`sondeur.md`.
Yes: comment 4's input shape is one line to copy, and the gathering
rule reaches everything. No — another heading, another separator, a
file with a header and no entry — the merge groups on a line that is
not there, and today files the residue silently.

Does a sondeur that blocks still write its questions file, whole or
partial?
`sondeur.md`.
Yes: comment 6 is a live path — a partial reading is merged as a full
one every time a sondeur blocks. No: the existence check catches it,
and comment 6 is an ordering defect with no run behind it yet.

Does the Rédacteur place an answer by the `Block:` line, in every
block the line names?
`redacteur.md`.
Yes: comment 2(b) loses an integration on every drop that narrows the
line, and the rule "drop only against a twin naming every block" is
load-bearing. No (it places by content): 2(b) is harmless and 2(a)
alone stands.

Does anything downstream of `questions-sondeur-NN.md` — Lexicographe
invocations 3/4, Rédacteur invocation 2 — depend on the numbering
(unique across turns, or restarting at `Q1`) or on the `### Qn`
headings?
`redacteur.md`, `lexicographe.md`.
Depends on cross-turn uniqueness: the command's "Renumber `Q1` upward"
is a real second scheme, misdescribed, and comment 7 should state it
rather than remove it. Depends on nothing: the line is a no-op and
goes.

Does the global sondeur raise one crossing once, or from each side
(`Block: B12, B15` once, or `Block: B12` and `Block: B15`
separately)?
`sondeur.md`.
Once: the multi-id rule is the only place a crossing is compared, and
comment 2 is the whole of it. From each side: the same crossing sits
in two groups as two single-block questions, is never compared across
groups by rule, and reaches the person twice — a same-file pair, which
comment 3 decides.
