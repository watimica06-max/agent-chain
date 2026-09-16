# agent-diagnostiqueur — verification

**Read**: `.claude/agents/diagnostiqueur.md` (old, 539 lines) · `.claude-new/agents/diagnostiqueur.md`
(new, 539 lines) · `docs/refonte/passes/diagnostiqueur.md` — **does not exist** ·
`docs/refonte/modifications.md` — **no section of its own**: `grep -n '^# '` gives 24 headings
and none is `` # `diagnostiqueur.md` ``. The file names the agent once, in § *Reprise par
fichier* (line 1601), as the only agent row **without a check mark**:

> `| \`diagnostiqueur.md\` | ⚠️ **Pas de fiche**, et rien du fichier de travail |`

**What that means for this report**: no pass sheet, no "Ce qui a changé", no "La demande",
no PASSÉ / ÉCARTÉ / REPORTÉ. The two agent files are **byte-identical** (`diff` empty, same
md5 `5e054c81…`), and so are the two `commands/diagnostique.md`. Section A is therefore
empty by construction and section B has no diff to report; the weight of this report is in
**C and D**, on a file nobody has read critically — and in the one thing B can still do:
say what the refonte changed *around* an unchanged file.

Line numbers below are those of the new file (identical in the old). Cross-file facts come
from `.claude-new/` unless marked *old*: `commands/diagnostique.md`, `agents/cadreur.md`,
`agents/verificateur.md`, `agents/detailleur.md`, `agents/convertisseur.md`,
`agents/classeur.md`; and the heading list only (`grep '^#'`) of
`docs/process/GRILLE_FERMETURE_TECHNIQUE.md`.

---

## A. Conformity

Nothing to verify: no pass sheet, no structural modification, no "La demande".

| # | Expected | Found | Verdict |
|---|---|---|---|
| — | modifications.md lists no PASSÉ, ÉCARTÉ or REPORTÉ defect for this agent | Old and new files byte-identical | **Nothing applied, nothing to check** |

**One question rather than a verdict.** The *Reprise par fichier* row says *"rien du fichier
de travail"* — nothing from a working file was carried over. That working file is not in my
reading list and I did not look for it. If it holds comments on the Diagnostiqueur, they are
unprocessed and this report does not cover them.

---

## B. Unannounced changes

**None.** `diff .claude/agents/diagnostiqueur.md .claude-new/agents/diagnostiqueur.md` is
empty. No renumbering, no moved section, no reworded rule, no rewritten table. The frontmatter
(lines 1–7) is identical, `tools`, `model: sonnet`, `effort: medium` included.

### B′. What the refonte changed around it — the file did not follow

The file is unchanged, but three things it depends on moved. None is announced for this
agent anywhere in `modifications.md`.

| # | What moved | Where the Diagnostiqueur still says the old thing | What it changes | Severity |
|---|---|---|---|---|
| B′-1 | **The technical document's preamble** is now `# Preamble` with four `##` parts — `## Intent and vocabulary` · `## Out of scope` · `## Cross-cutting rules` · `## Dependencies` (`convertisseur.md` 121–126; *old* convertisseur wrote a flat `## Preamble`) | 471–472 *"in the technical document's shape"*; 476–480 write `## Preamble` with three inline lines `Intent:` / `Out of scope:` / `Dependencies:`; 509–510 *"Three lines are enough"* | `desc-bug.md` is no longer in the technical document's shape. The Cadreur's lookup *"the preamble's `Out of scope`"* (`cadreur.md` 378) still finds a line; the Détailleur's *"the preamble's `Vocabulary` fixes the terms"* (`detailleur.md` 559) finds nothing — the file says at 509–510 that this is deliberate (*"a bug-fix cycle has no vocabulary of its own"*), but the Détailleur is not told so. | **TO FIX** — either align the shape, or tell the consumers a `desc-bug.md` preamble has no `Vocabulary` and no `Cross-cutting rules` |
| B′-2 | The chain no longer has an **Extracteur** (`CLAUDE.md` new, § *Identity*; `modifications.md` 1569) | Nowhere — the file never named it | Nothing. Listed so the reader knows it was checked. | — |
| B′-3 | **`Bearer: none`** is now handled by the Cadreur (`cadreur.md` 315–322: it decides where it lands, a production rather than a modification) and the Détailleur (`detailleur.md` 51) | 271–278, 288, 500–503 already write it | The output is consumed as written — this is the one place the unchanged file and the changed chain agree. But the file's own prohibition at 115–116 says the opposite — see **D-2**. | — |

The eight natures (517–519) match `classeur.md` 67–79 name for name and in order; the nine
sections with §9 Text match `convertisseur.md` 72–90; the three closures named at 456–460
and the two excluded by name at 462–463 all exist as `##` headings of
`GRILLE_FERMETURE_TECHNIQUE.md` (Traceability · Nothing dropped · Completeness · What a
nature owes · Declared links · Singularity · Agreement between entries · Resources), and
*"the rest bear on a translation you did not make"* (463–464) covers the remaining three.
Verified, no finding.

---

## C. Gestures against tools

**Frontmatter tools** (line 4): `Read, Grep, Glob, Write`. No `Edit`, no `Bash`.

### Gestures and their means

| Gesture | Where | Tool | Verdict |
|---|---|---|---|
| Read the gap from the prompt; read `bug-list.md` whole at invocation 2 | 55–56, 417–418 | Read | has the means |
| Read `docs/TECHNICAL_CONVENTIONS.md` before searching, for the code folders | 132, 222–223 | Read | has the means |
| Read `docs/CURRENT_TECHNICAL_STATE.md` | 132 | Read | has the means — **but no move uses it**, see D-16 |
| Grep the code, always with a `path:` on a conventions folder; widen three times; grep every thing the fix names | 203–205, 212, 230, 332–334 | Grep | has the means |
| Search *"everything the build carries"*, including *"a value fixed outside the code"* | 215–216, 228 | Grep + Glob inside the worktree | has the means inside the repository. **Question**: a value fixed *outside the code* that is also outside the repository (an environment, a store listing, a device setting) is out of reach of every tool the agent has — is 228 meant to stay inside the repository? |
| Find the settled `blocked_<id>-NN.md` / `blocked_diagnostiqueur-NN.md` beside the blocking file | 152–154 | Glob | has the means |
| Find every `investigation/*.md` and count them against `bug-list.md` | 133, 417, 420 | Glob + Read | has the means — the count itself is wrong, see **D-6** |
| Check whether `desc-bug.md` already exists before writing | 473 | Glob | has the means |
| Load `docs/process/GRILLE_FERMETURE_TECHNIQUE.md` at invocation 2 | 452–453 | Read | has the means |
| Write `investigation/<id>.md`, `desc-bug.md`, `investigation/blocked_<id>.md`, `blocked_diagnostiqueur.md` | 373, 471, 67–68 | Write | has the means |
| Apply a filled `## Decision` to your own gap (invocation 1) — a reasoning step, no file touched | 174–176 | — | nothing needed |
| **Move 5 — "Read each caller against the new mechanism"**: what it holds today, whether it uses what the new mechanism hands it | 350–365 | Read exists — but 117–118 forbids using it on code (*"Read the code beyond a grep — never"*) | the tool is there, the rule takes it away — see **D-9** |
| **Rename** `blocked_*.md` → `blocked_*-NN.md`: *"`git mv`, or the equivalent: one file, under a new name … never write the numbered one and leave something at the old name — not a copy, not a note, not an empty file"* | 160, 162–165 | **none** — no `Bash`, no move or delete tool. `Write` creates the numbered file and cannot remove the unnumbered one; overwriting it with nothing is what 163–165 forbids. Line 167–168 then says the leftover *"reads as a block still standing, and the next run treats it as one"*: the agent's only reachable outcome is a block that never lifts. | **BLOCKING** |

The rename finding is chain-wide: the same sentence sits in six new agents (`architecte`,
`detailleur`, `diagnostiqueur`, `fusionneur`, `realisateur`, `relecteur`) and only the
Réalisateur carries `Bash`. The reports on the Architecte, Détailleur and Fusionneur already
flag it. Listed here because this file carries it too, and because on this agent it bites at
both invocations (67–68: two blocking files, two renames).

### Tools no gesture uses

None. `Read`, `Grep`, `Glob`, `Write` are each required by at least one gesture above.
The absence of `Edit` is coherent with the file: it never edits — one report written once
(373–374), `desc-bug.md` written once and never overwritten (473–474). ⚠️ That coherence
breaks on one branch — see **D-5**.

---

## D. Internal coherence (new file alone)

### BLOCKING

**D-1 · 295–297 vs 373–374, 403, 420, 437, 521 — a gap with several independent bearers has
no shape that can carry it.**

> 295–297: *"**Several that do not** — 🔴 **one entry each, however many there are.** ⚠️
> **Twenty sites of one same omission are twenty entries**"*

> 373–374: *"**`investigation/<id>.md`** … 🔴 **One file, yours alone**"* · 403: *"**Six
> headings, always**"* — one `## Bearer` heading (380) · 420: *"🔴 **One gap in
> `bug-list.md`, one report.**"* · 437: *"**7. Write its entry**, from `## Today` and
> `## Expected`"* — singular · 521: *"🔴 **One entry, one gap**"*

Invocation 1 gets one gap and writes one report with one `## Bearer`. Invocation 2 turns one
report into one entry, *"one entry, one gap"*. Nowhere does either invocation say how one
report carries twenty bearers, or how the assembly splits one report into twenty entries.
The rule at 295–305 (three paragraphs, all 🔴/⚠️) is the most insistent in move 3 and
nothing downstream can honour it. Either the report shape needs a way to hold several
`## Bearer` blocks and move 7 needs *"one entry per bearer block"*, or 295–305 is wrong.

### TO FIX

**D-2 · 115–116 and 512–513 vs 271–273, 288, 500–503 — an entry without a symbol is
forbidden, then required.**

> 115–116: *"🔴 **Write an entry without a symbol** — it could not be cut into a lot"* (under
> *What you never do*) · 512–513: *"🔴 **Every entry names its bearer** … **the symbol that
> will carry the fix.**"*

> 271–273: *"🔴 **write the entry with its bearer left unnamed**"* · 288: *"`Bearer: none`"*
> · 500–503: *"An entry whose bearer you could not name carries `Bearer: none — nothing in
> the project holds this behaviour today`. 🔴 **Never omit the line**"*

The new Cadreur (`cadreur.md` 315–322) consumes `Bearer: none` and cuts a lot from it, so
the *"could not be cut into a lot"* at 116 is the stale half. 115–116 should say *"without a
`Bearer:` line"*, and 512–513 *"names its bearer, or `none`"*.

**D-3 · 275–278 vs 307–311 — a behaviour that has to move: bearer `none`, or the
destination?**

> 275–278: *"⚠️ **That is the shape of a behaviour that has to move**: 🔴 **you establish it
> belongs elsewhere, not where it lands.** 📌 **Where it lands is a split decision**"* —
> in the paragraph that writes `Bearer: none`

> 307–311: *"⚠️ **One exception: moving a behaviour from one place to another.** … **The
> bearer is where it lands.**"*

Two 🔴 rules, thirty lines apart, give opposite answers to the same case. The Cadreur
(`cadreur.md` 315–318) decides where a `none` lands, which sides with 275–278 — but then
310–311 must go, or say when the agent may name the destination itself.

**D-4 · 72–74 vs 119–120, 424–425, 466–467 — "you block only when …" enumerates two cases and
the file has four.**

> 72–74: *"🔴 **You block only when producing is impossible** — a prompt naming no gap, or a
> report set that does not match `bug-list.md`."*

> 119–120: *"one that does not [carry everything] is a blocker"* · 424–425: *"A report that
> leaves you unable to write an entry is a blocker"* · 466–467: *"🔴 **A closure that fails
> is a blocker**, not a question"*

A failed *Completeness* closure on a report that is complete enough to write an entry is
neither of the two cases at 72–74. Either 72–74 lists the cases as examples (drop *"only"*),
or the two extra cases are not blocks.

**D-5 · 473–474 vs 62–63, and the move-9 branch that leads back to it.**

> 473–474: *"🔴 **If the file already exists, stop and say so** rather than overwriting it."*

> 62–63: *"🔴 **Write a blocking file** — do not merely say it. A message in a reply gets
> lost; a file does not."*

*"Say so"* is exactly what 62–63 forbids, and the command (`commands/diagnostique.md`,
*What you relay*) relays a phase-2 stop only through `blocked_diagnostiqueur.md`. Worse, the
branch is reachable from the file's own procedure: move 9 runs *"once every entry is
written"* (452); if the entries are already in `desc-bug.md` when a closure fails and the
agent blocks (466–467), the re-run after the Product Owner's decision finds `desc-bug.md`
present and must stop at 473. **Question**: are the entries held until the three closures
pass, and written in one go? If so, say it at 449–452; if not, the block at move 9 is a
dead end without a manual delete.

**D-6 · 133, 417, 420 vs 67, 151–154 — `investigation/*.md` is not the set of reports.**

> 133: *"Every `investigation/*.md`"* · 417: *"🔴 **Read them all**"* · 420–421: *"🔴 **One
> gap in `bug-list.md`, one report.** Count both"*

> 67: *"`investigation/blocked_<id>.md`"* · 151–154: *"`investigation/blocked_<id>.md` …
> **Never another's.** … **Several with `-NN` appended beside it are settled ones**"*

The folder holds reports, standing blocks and settled blocks, all `*.md`. Counted as
written, a gap whose investigation blocked has a file in `investigation/` and the count
matches — the very case 420–422 exists to catch. Read as written, invocation 2 opens
another invocation's blocking file, which 152 forbids. The report set must be defined as
`investigation/<id>.md` for each identifier of `bug-list.md`, excluding `blocked_*`.

**D-7 · 38–39 vs 132–133, 452–453 — "every path is relative to the bug-fix folder", except
the four that are not.**

> 38–39: *"🔴 **Every path in this file is relative to that folder**, and every path you write
> or read is relative"*

> 132: *"`docs/TECHNICAL_CONVENTIONS.md` · … · `docs/CURRENT_TECHNICAL_STATE.md`"* · 133,
> 452–453: *"`docs/process/GRILLE_FERMETURE_TECHNIQUE.md`"*

From `docs/features/<name>/bugfix-NN/`, `docs/TECHNICAL_CONVENTIONS.md` does not resolve.
The Cadreur states the same split explicitly (`cadreur.md` 40–41: *"not to the working
folder — the conventions are shared by the whole project"*); this file needs the same
sentence.

**D-8 · 179–180 — "re-run your first move" names a move that is not one.**

> 179–180: *"Re-run your first move: count the gaps, count the reports."*

Invocation 2's moves are numbered 6 to 9 (427–429) and the first, move 6, is *"Give each
confirmed gap a nature"* (431). The count lives at 420–422, before the moves and unnumbered.
Either number it (a move 6, the rest shifting — which breaks *"four moves"* at 427) or write
*"re-run the count at the head of the assembly"*.

**D-9 · 350–365 vs 117–118, 245–246 — move 5 asks for a reading the file forbids.**

> 350: *"**5. Read each caller against the new mechanism.**"* · 356–361: *"**What it holds
> today — does the new mechanism accept it?** … **What the new mechanism hands it — does it
> use it?** … a caller that compiles without reading it is a dead field"*

> 117–118: *"🔴 **Read the code beyond a grep** — you confirm a behaviour, you do not review
> an implementation"* · 245–246: *"⚠️ **Confirming is not reviewing.**"*

Whether a caller *uses* a field it is handed is not a grep result; it is read from the
caller's body. **Question**: is move 5 the intended exception to 117–118 — in which case
117–118 should name it — or is it meant to stop at grepping the call sites and their
arguments?

**D-10 · 327–328 vs 200–201, 373–374 — "write it, or point at the one that already covers
it" is not possible at invocation 1.**

> 327–328: *"📌 **What can change while the bearer stays as it is belongs to another entry.**
> 🔴 **Write it, or point at the one that already covers it**"*

> 200–201: *"🔴 **You never see the others**, and nothing you write depends on them."* ·
> 373–374: *"🔴 **One file, yours alone**"*

An invocation-1 run cannot point at another entry (it sees none) and cannot write a second
one (one file, six headings). The only place the instruction can be honoured is invocation 2,
which is told to write one entry per gap (521). Same root as **D-1**.

### NOTE

**D-11 · 339–340, 357, 367–369, 439–442 — "gap" in two senses.** A *gap* is an item of
`bug-list.md`: one report, one entry (420, 521). A *second gap* is a requirement found while
investigating one — it gets no report and no entry, it *"goes in `## Expected`, or in
`## Trigger`"* (367–369) and *"into the entry"* (439). Same word, opposite fate. A separate
question hangs on it: 317 says *"An entry requires a change of its bearer, and of nothing
else"*, and 439–441 folds *"a signature that has to change"* into the entry. Does a signature
change on something other than the bearer always fall under the narrow exception at
322–325? If not, 317 and 439–441 contradict.

**D-12 · 271–330 — "entry" used in invocation 1 for what only invocation 2 writes.** Sixteen
occurrences of *entry* between 271 and 330, all in the investigation, whose output is *"a
report"* (35, 373). *Entry* is defined at 437 and 521 as a numbered item of `desc-bug.md`.
A reader of move 3 alone concludes invocation 1 writes entries.

**D-13 · 170–172 vs 191–192 — the same sentence twice, once "feature", once "cycle".**

> 170–172: *"📌 **The numbered ones are the record of what this feature has already been
> blocked on**, and the next run reads them."*

> 191–192: *"📌 **The numbered ones are the record of what this cycle has already been
> blocked on** — 🔴 **the next run reads them.**"*

The blocking files live in `bugfix-NN/` (65–68), so *cycle* is the right word; 170–172 is
the wrong duplicate.

**D-14 · 403–405, 407–408 — `## Trigger` when there is no trigger.** Move 3 locates *"the
trigger when there is one"* (248, 259). 404–405 says `## Trigger` *"ends in `observed` or
`nothing observes it`, never in the trigger alone"*; 407–408 says it is empty on `set aside`.
A confirmed gap with no trigger at all is left without a rule — empty, `none`, or
`nothing observes it`?

**D-15 · 212 vs 230 — "the third widening" against a ladder of two.** 212: *"the exact term,
then its parts, then what would hold it"* — three searches, two widenings. 230: *"🔴 **Stop
after the third widening.**"* Is the exact-term search counted as a widening, or is a fourth
search expected?

**D-16 · 132 — `docs/CURRENT_TECHNICAL_STATE.md` is an input nothing uses.** Listed for
invocation 1 at 132, absent from moves 1 to 5 (207–369) and from the rest of the file; the
conventions are read at 222–223, the technical state nowhere. Under *"Load only what your
invocation lists"* (138) the agent will load it and have no instruction for it.

**D-17 · 144–146 — two consecutive `---`.** An empty section between *Which invocation is
this?* and *When you resume after a blocking file*. Cosmetic; likely a paragraph that was
removed.

**D-18 · 264 — "Two names for one thing would be grouped as two."** In context (261–264: an
interface and its implementation, *"the bearer is the one others depend on"*) the rule wants
one entry, not two — but the sentence states what would happen, not what to avoid, and reads
as the opposite instruction. Question on the intended reading.

**D-19 · 471–472, 515, 527 — "in the technical document's shape", with a section the
technical document does not have.** `desc-bug.md` carries *"nine sections, always"* (515)
plus *"## Gaps set aside"* (527), which the technical document has no equivalent of and the
Cadreur never mentions (`cadreur.md` 300–333). Does the Cadreur skip a section it does not
know, or is a `## Gaps set aside` holding two bullet lines read as entries? Question.

**D-20 · 500–501 vs 505–506 — "never qualify the word", right under a line that does.**
500–501 mandate `Bearer: none — nothing in the project holds this behaviour today`; 505–506:
*"🔴 **Never qualify the word**"*. The Cadreur matches `Bearer: none` as a prefix
(`cadreur.md` 315) so nothing breaks, but the two sentences pull against each other; 505–506
should say *"never qualify it with a count"* or similar.

**D-21 · 431, 434–435, 449 — §9 Text has no nature, and move 8 files "inside the section its
nature names".** Coherent with `convertisseur.md` 90 (*"§9 Text carries no nature"*), and
434–435 already routes a missing key to §9; 449 just needs *"or §9 Text"*.

**D-22 · 29–30 vs `commands/diagnostique.md` — who finds the highest `bugfix-NN/`.** 29–30:
*"the bug-fix folder you were given — the highest `bugfix-NN/` of the feature"*. The command
resolves it and passes the full path in the prompt (*"Bug-fix folder:
docs/features/<name>/bugfix-NN/"*). Coherent as written — *given* is the operative word —
but *"the highest"* invites the agent to look for itself; a Glob on `bugfix-*` from the wrong
root would find another one. Not a defect, a reading risk.

---

## Summary

| Severity | Count | Ids |
|---|---|---|
| BLOCKING | 2 | C-rename (no tool for `git mv`, both invocations) · D-1 (several independent bearers: no shape can carry them) |
| TO FIX | 10 | B′-1 · D-2 · D-3 · D-4 · D-5 · D-6 · D-7 · D-8 · D-9 · D-10 |
| NOTE | 12 | D-11 to D-22 |

**Verified, no finding**: old and new byte-identical; eight natures and their order; nine
sections and §9 Text; the three closures run and the two excluded by name; `Bearer:` line and
`Bearer: none` as consumed by the new Cadreur and Détailleur; the four-heading blocking-file
shape and the `-NN` settling convention; the command's prompts (bug-fix folder, invocation
number, gap text and identifier) against what the file expects at 135–136 and 200.
