# Verification 4 — does the chain hold together

**Five investigations, one wave.** 🔴 **No per-agent round.**

📌 **Why not**: ⚠️ **two full reading rounds found the same volume** —
🔴 **the gain is no longer in reading an agent against itself.**

🔴 **What this round looks at is the surface the correction campaign
touched**: 📌 **476 sides applied across 343 work entries**, ⚠️ **and
only 24 replayed.** 🔴 **Almost all of it was coupling** — a field added
on one side and read on four others, a route rewritten, a prompt given
a parameter.

📌 **These five are the only angle that reads the chain as a system.**

⚠️ **What it still will not show**: 🔴 **an agent that runs badly.** 📌 **A
route can close on paper and a prompt miss its parameter at run time** —
**only a real cycle shows that.**

🔴 **Every list of « what changed » below is a starting point, never a
boundary.** ⚠️ **An investigation that only looks where a change was
made cannot see what that change broke elsewhere** — 📌 **the last
serious defect of this chain was not in the file that was edited, it
was in the four files that read it.**

---

## Setup

🔴 **The chain under verification is `.claude-new/` and `docs-new/`.**
📌 **`.claude/` and `docs/` hold the state before the refonte** — ⚠️
**open them only to fill the `Origin` column.**

🔴 **Everything is written to `docs/verification4/`.**

📌 **Two records say what changed** — 🔴 **read both, the recent one
first:**

- `docs/verification3/plan.md` — 🔴 **this round's 63 entries**, their
  decision, owner and followers. ⚠️ **No third party has read what they
  produced.**
- `docs/verification2/plans/conflits.md` — 📌 **the previous campaign's
  work table**, already verified once.

---

# The five investigations, in parallel

| | |
|---|---|
| **V1 · Renames** | 🔴 **The names the campaign created**, and the ones it retired |
| **V2 · Writers and readers** | 🔴 **A field written on one side and read on four** |
| **V3 · Paths and loops, upstream** | 🔴 **Does every route close?** |
| **V4 · Paths and loops, downstream** | 🔴 **The same, on the coding loop** |
| **V5 · Handovers** | 🔴 **What one agent writes against what the next reads** |

📌 **Upstream and downstream handovers are one investigation here**, not
two — ⚠️ **the campaign changed both sides of the same fields**, and
splitting them is what let `## Files` pass through twice.

## V1 — Renames

```
READ-ONLY. Write docs/verification4/renommages.md

🔴 **First, read the entries of `docs/verification3/plan.md` that touch
your scope** — 📌 **what changed this round, and what nobody has
checked since.** ⚠️ **Then do everything below, in full**: 🔴 **those
entries are where to start, not where to stop.**

🔴 **Read what you need, never a folder whole** — 📌 **the chain is
830 KB.**

⚠️ **Do not report formatting** — 📌 **a script already guards it and
the chain is clean of it**: 🔴 **unclosed bold, dead references, numeric
counts, colliding move numbers, orphan fragments, empty separators,
repeated lines, known typos.** 📌 **Your work is what a script cannot
see.**


🔴 **A full sweep, not a list.** ⚠️ **The correction campaign applied
476 sides through 41 invocations**, and 📌 **a correction that reworded
a rule could rename a field on the way**: 🔴 **the work table says what
was meant to change, never what did.**

⚠️ **Ten late fixes touched nine files no table line named.** 📌 **So a
list of expected names would miss exactly what nobody announced.**

---

## 1 — Build the inventory

🔴 **Every name an agent or a command writes or reads**, across all of
`.claude-new/` and `docs-new/`:

- **Section headings inside a produced file** — `## Symbols`,
  `## Acceptance criteria`, `## Outside the lot`, `## Decision`…
- **Field keys on a line** — `Bearer:`, `Anchor:`, `Genre:`,
  `Nature:`, `Kind:`, `Mode:`, `Consumes:`, `Answer:`, `Défaut:`…
- **Fixed values a reader matches** — `PASS`, `comportement`,
  `permanente`, `coverage`, `reasoning`, `carried`…
- **File and folder names** — `fiche-executable.md`, `par-genre/`,
  `code/<lot>/`, `architecte/`…
- **Marks** — `<<ASSUMED`, `[B?:`, `NEW`, `MODIFIED`, `§9 Text`…
- **Prompt parameters** — 🔴 **the lines a command passes an agent**:
  `Invocation 1 — Confront.`, `Your block:`, `Affected lots:`,
  `Mode:`, `Group:`… ⚠️ **a parameter the agent does not read is a
  silent no-op**
- **Skill names** — 📌 **`technical-state-format` and any other an agent
  loads**: ⚠️ **a wrong name loads nothing, and nothing says so**

📌 **`Select-String` is your tool** — ⚠️ **the shell is PowerShell, not
bash.** 🔴 **Never read a file whole to build this.**

⚠️ **The inventory is your reading, never your report.**

---

## 2 — For each name, three questions

**1. Who writes it?** **2. Who reads it?** **3. Does an older spelling
survive anywhere?**

🔴 **Report a name that appears on one side only** — 📌 **written and
never read, or read and never written.**

⚠️ **Two legitimate cases, and they are not findings**: 📌 **a file the
Product Owner writes by hand** — `idees.md`, `bug-list.md`, an answered
questions file — 🔴 **has no writer in the chain**; 📌 **and a file
written for her to read** — a report, a manual test list — **has no
reader in it.** ⚠️ **Say so in one line rather than listing them.**

🔴 **Report two spellings of one thing** — 📌 **`## Traps` against
`## Traps — general`, `Modifies` against `## Files`**: ⚠️ **one
character is enough**, and a reader that greps finds nothing.

🔴 **Report a value a writer can produce and no reader matches** — 📌
**`PASS with reservation` against a reader keyed on `PASS`.**

---

## 3 — Names to check first

📌 **Start here, then sweep the rest.** ⚠️ **These are the ones the
campaign created or moved**, so they have the least history behind
them:

- `## Files` and `## Declared` — 🔴 **the campaign split them**: the
  sheet carries existing files, the conception report the created ones
- `Anchor: … (B12)` — the block identifier travelling to the lot list
- `Kind: forme` — a fifth value of the architecte's questions file
- `Mode: divergence` · `Group:` · `## Blocking N`
- `## What governed the code, besides the sheet`
- `## Placements not settled by the conventions`
- `## Redécoupage: archivable`
- The Vérificateur's round-number line in `code/sequence.md`
- `## Invocation` in the rédacteur's blocking file
- `## Git, before invoking` / `## Git, once it has reported` — ⚠️
  **`/5_reclasse` keeps the old `## Git, in this mode`**, deliberately:
  it invokes no agent

**Removed — report any surviving occurrence:**
`/cycle` and `cycle.md` · `stop1.md` attributed to `/cycle` ·
`CALIBRATION_RISK_LEVEL.md` · `TaskCreate` · a risk level ·
`<<TECHNICAL` · `blocked_<agent>` used inside an agent file

**Your report — one table, and nothing else.** 🔴 **No evidence section,
no development, no restatement of what you read.**

    | # | Severity | Origin | Where | Finding |

- **`#`** — 🔴 **`F01`, `F02`…**, one numbering for the whole report,
  whatever the severity. ⚠️ **Never a prefix that encodes severity.**
- **`Severity`** — `BLOCKING` · `TO FIX` · `NOTE` · `QUESTION`.
- **`Origin`** — 🔴 **one word**: `refonte` when the same file under
  `.claude/` or `docs/` did not have it, `pre-existing` when it did,
  `unknown` when you cannot tell. ⚠️ **Never a guess.**
- **`Where`** — 🔴 **file and line, both sides, separated by `↔`** —
  `concepteur.md L141 ↔ detailleur.md L229`. ⚠️ **Never a file without a
  line**: 📌 **there is no evidence section to fall back on.**
- **`Finding`** — 🔴 **one sentence, carrying what it costs.** 📌 *« The
  Concepteur is sent to a field that does not exist, so three of its
  rules never fire »* — ⚠️ **not** *« problem with `Modifies` »*.

📌 **Sort by `#`.** 🔴 **A census is a reading, never a report** — ⚠️
**only the anomalies are written.**

📌 **One exception, at the end, three lines at most**: 🔴 **what you
checked and found sound** — ⚠️ **named, never developed.**
```

## V2 — File writers and readers

```
READ-ONLY. Write docs/verification4/fichiers.md

🔴 **First, read the entries of `docs/verification3/plan.md` that touch
your scope** — 📌 **what changed this round, and what nobody has
checked since.** ⚠️ **Then do everything below, in full**: 🔴 **those
entries are where to start, not where to stop.**

🔴 **Read what you need, never a folder whole** — 📌 **the chain is
830 KB.**

⚠️ **Do not report formatting** — 📌 **a script already guards it and
the chain is clean of it**: 🔴 **unclosed bold, dead references, numeric
counts, colliding move numbers, orphan fragments, empty separators,
repeated lines, known typos.** 📌 **Your work is what a script cannot
see.**


Census every file the chain produces and consumes, across
`.claude-new/` and `docs-new/`.

🔴 **Do not read the chain whole** — 📌 **work by grep.** ⚠️ **The shell
is PowerShell**: `Select-String`, not `grep`.

**1. Build the list of names.** 🔴 **Two passes, then the union** — 📌
**neither alone is complete:**

    Select-String -Path .claude-new\**\*.md, docs-new\**\*.md `
      -Pattern '`[^`]*\.md`' -AllMatches |
      ForEach-Object { $_.Matches.Value } | Sort-Object -Unique

📌 **catches the names written in prose.**

    Select-String -Path .claude-new\**\*.md, docs-new\**\*.md `
      -Pattern '[A-Za-z0-9_<>/.-]+\.md' -AllMatches |
      ForEach-Object { $_.Matches.Value } | Sort-Object -Unique

📌 **catches those inside code blocks**, where backticks are absent. ⚠️
**Discard the fragments the second pass produces** — 🔴 **a name must
have a stem before `.md`.**

**2. For each name**, `Select-String` it across both folders and 🔴
**read only the hit lines and their surroundings.**

**3. Open a file in full** only when the hits do not settle who writes
it.

**4. One line per file**: 🔴 **who writes it, who reads it, at what
point of the cycle.**

⚠️ **The census is your reading, never your report.** 📌 **Build it
whole all the same** — 🔴 **an anomaly is only visible against the
complete set.**

---

## The anomalies to report

- 🔴 **A file written that nobody reads** — ⚠️ **except one written for
  the Product Owner**: 📌 **a report, a manual test list**
- 🔴 **A file read that nobody writes** — ⚠️ **except one she writes by
  hand**: 📌 **`idees.md`, `bug-list.md`, an answered questions file**
- 🔴 **A file written by two agents with no stated order**
- 🔴 **A file one agent deletes and another still reads** — 📌 **the
  campaign deleted `cycle.md`, and `/8_code` now deletes a lot's
  `fiche-executable.md`, `conception.md`, `tests.md` and `verdict.md`
  on a `Cause: sheet`**: ⚠️ **check every reader of those four.**
- 🔴 **A file an agent writes that its own file does not name** — ⚠️
  **two wave-3 invocations left scratch files behind**
  (`_fix3b_tmp.py`, `w3.diff.tmp`): 📌 **if an agent is allowed to write
  what it likes, say so.**

---

## What to check first

📌 **The campaign changed hands or content on these** — 🔴 **start
there:**

- `conception.md` — 📌 **it now carries the files a lot created**, not
  only its symbols: ⚠️ **check every reader of `## Declared`**
- `code/blocked_verificateur.md` — 📌 **`/7_lots` removes it at the head
  of every run**: ⚠️ **check nothing else expects to find it**
- `code/redecoupage.md` — 📌 **the Arbitre writes it, `/7_lots` renames
  it, and the relay of its two sections moved there**
- `code/sequence.md` — 📌 **it gained the Vérificateur's round number**
- `desc-bug.md` — 📌 **it carries the block identifier now**
- `docs/refonte/modifications.md` — ⚠️ **no longer maintained**: 🔴
  **report any agent or command that still writes to it**

**Your report — one table, and nothing else.** 🔴 **No evidence section,
no development, no restatement of what you read.**

    | # | Severity | Origin | Where | Finding |

- **`#`** — 🔴 **`F01`, `F02`…**, one numbering for the whole report,
  whatever the severity. ⚠️ **Never a prefix that encodes severity.**
- **`Severity`** — `BLOCKING` · `TO FIX` · `NOTE` · `QUESTION`.
- **`Origin`** — 🔴 **one word**: `refonte` when the same file under
  `.claude/` or `docs/` did not have it, `pre-existing` when it did,
  `unknown` when you cannot tell. ⚠️ **Never a guess.**
- **`Where`** — 🔴 **file and line, both sides, separated by `↔`** —
  `concepteur.md L141 ↔ detailleur.md L229`. ⚠️ **Never a file without a
  line**: 📌 **there is no evidence section to fall back on.**
- **`Finding`** — 🔴 **one sentence, carrying what it costs.** 📌 *« The
  Concepteur is sent to a field that does not exist, so three of its
  rules never fire »* — ⚠️ **not** *« problem with `Modifies` »*.

📌 **Sort by `#`.** 🔴 **A census is a reading, never a report** — ⚠️
**only the anomalies are written.**

📌 **One exception, at the end, three lines at most**: 🔴 **what you
checked and found sound** — ⚠️ **named, never developed.**
```

## V3 — Paths and loops, upstream

```
READ-ONLY. Write docs/verification4/chemins-amont.md

🔴 **First, read the entries of `docs/verification3/plan.md` that touch
your scope** — 📌 **what changed this round, and what nobody has
checked since.** ⚠️ **Then do everything below, in full**: 🔴 **those
entries are where to start, not where to stop.**

🔴 **Read what you need, never a folder whole** — 📌 **the chain is
830 KB.**

⚠️ **Do not report formatting** — 📌 **a script already guards it and
the chain is clean of it**: 🔴 **unclosed bold, dead references, numeric
counts, colliding move numbers, orphan fragments, empty separators,
repeated lines, known typos.** 📌 **Your work is what a script cannot
see.**


Scope: `/1_lexique`, `/2_structure`, `/3_decoupe`, `/3a_genre`,
`/3b_nature`, `/4_grille`, `/5_reclasse`, `/6_convertit`,
`/conventions`, `/fusion`, `/fusion_compare`, `/fusion_applique`.

⚠️ **`/cycle` is deleted** — 🔴 **report any command that still names
it.**

🔴 **For each command, enumerate every possible state of the folder when
it is launched, and verify each has a written outcome.** 📌 **A state
with no routing line is a hole.**

🔴 **For each loop: what terminates it?** 📌 **Report any exit condition
that is unreachable, and any loop that can restart on itself.**

---

## What the correction campaign changed here

📌 **Start with these** — 🔴 **they are routes that were rewritten, and
a rewritten route is where a hole opens:**

**The `Défaut:` gate.** 🔴 **An entry with an empty `Answer:` and a
`Défaut:` line is answered — silence accepts the proposal.** 📌 **Three
gates now test both** (`/1_lexique`, `/2_structure` twice). ⚠️ **Check
every other gate that tests an empty `Answer:`**: 🔴 **one that should
carry the exception and does not stops on an answered file; one that
carries it where no `Défaut:` can exist is dead weight.**

**The Qualifieur's new block.** 🔴 **A block whose sentences call for two
genres is now a blocking file**, routed through `/2_structure` to the
Rédacteur, then `/3_decoupe`. ⚠️ **Trace it to the end**: 📌 **does the
rewritten block come back to `/3a_genre`, and can the loop run twice on
the same block?**

**The Qualifieur's new question.** 📌 **A `transverse`-or-`comportement`
doubt is now asked**, where the agent was silent. 🔴 **Check the
questions file it writes has a gate that reads it**, and that the
answered file is filed where `/3a_genre` expects.

**`questions-architecte-*.md` stays at the root.** 📌 **Four commands
file root questions files away** — `/3a_genre`, `/3b_nature`,
`/4_grille`, `/6_convertit`. 🔴 **All four must carry the exception**:
⚠️ **a command that files it breaks `/conventions`, the only reader.**

**`/3b_nature`'s relay order.** 📌 **Answers first, decision second.** 🔴
**Check the two are not both required at once.**

**`/6_convertit`'s new dispatch row.** 📌 **A nature carrying
`<<ASSUMED` whose product question is answered runs, part unchanged.**
🔴 **Check it cannot collide with the row above it**, and that the
re-run lifts the mark.

**`/conventions` and invocation 4.** 📌 **Invocations 1, 2 and 4 run on
a feature folder; 3 runs on either.** 🔴 **How does the command know
which to run?**

**The split Git section.** 📌 **Every command that invokes an agent now
carries `## Git, before invoking` and `## Git, once it has reported`.**
⚠️ **`/5_reclasse` keeps the old single heading, deliberately — it
invokes none.** 🔴 **Check every command creates its worktree before it
invokes**, ⚠️ **and that none lost half its section in the split.**

---

## Still to check, as before

- An empty questions file · an unanswered one · two at the root
- A blocking file with an empty decision · a filled one · an already
  numbered one · 🔴 **one whose `## Decision` is partly filled**
- The second closing pass: it fires when the first returns an empty
  file, and must run once only
- The Convertisseur's short loop against its long loop
- The Fusionneur dropping `directive` and `hors périmètre`: 🔴 **what
  happens to a feature whose blocks are all of those two genres?**

🔴 **Trace three end-to-end scenarios and say where each stops**: 📌 **a
first feature on an empty project · a feature on a project that already
has some · a correction cycle.**

**Your report — one table, and nothing else.** 🔴 **No evidence section,
no development, no restatement of what you read.**

    | # | Severity | Origin | Where | Finding |

- **`#`** — 🔴 **`F01`, `F02`…**, one numbering for the whole report,
  whatever the severity. ⚠️ **Never a prefix that encodes severity.**
- **`Severity`** — `BLOCKING` · `TO FIX` · `NOTE` · `QUESTION`.
- **`Origin`** — 🔴 **one word**: `refonte` when the same file under
  `.claude/` or `docs/` did not have it, `pre-existing` when it did,
  `unknown` when you cannot tell. ⚠️ **Never a guess.**
- **`Where`** — 🔴 **file and line, both sides, separated by `↔`** —
  `concepteur.md L141 ↔ detailleur.md L229`. ⚠️ **Never a file without a
  line**: 📌 **there is no evidence section to fall back on.**
- **`Finding`** — 🔴 **one sentence, carrying what it costs.** 📌 *« The
  Concepteur is sent to a field that does not exist, so three of its
  rules never fire »* — ⚠️ **not** *« problem with `Modifies` »*.

📌 **Sort by `#`.** 🔴 **A census is a reading, never a report** — ⚠️
**only the anomalies are written.**

📌 **One exception, at the end, three lines at most**: 🔴 **what you
checked and found sound** — ⚠️ **named, never developed.**
```

## V4 — Paths and loops, downstream

```
READ-ONLY. Write docs/verification4/chemins-aval.md

🔴 **First, read the entries of `docs/verification3/plan.md` that touch
your scope** — 📌 **what changed this round, and what nobody has
checked since.** ⚠️ **Then do everything below, in full**: 🔴 **those
entries are where to start, not where to stop.**

🔴 **Read what you need, never a folder whole** — 📌 **the chain is
830 KB.**

⚠️ **Do not report formatting** — 📌 **a script already guards it and
the chain is clean of it**: 🔴 **unclosed bold, dead references, numeric
counts, colliding move numbers, orphan fragments, empty separators,
repeated lines, known typos.** 📌 **Your work is what a script cannot
see.**


Scope: `/7_lots`, `/8_code`, `/9_controle`, `/deploie`,
`/diagnostique`, `/audit_blocages`, `/audit_conventions`.

🔴 **Same work: every state, every outcome, every loop and what
terminates it.**

---

## What the correction campaign changed here

📌 **Start with these** — 🔴 **the downstream loop took most of the
campaign's changes:**

**`/8_code` now deletes.** 🔴 **On a `Cause: sheet`, it reverts the
lot's commits and deletes `fiche-executable.md`, `conception.md`,
`tests.md` and `verdict.md`**, then runs the Détailleur in its ordinary
mode — 📌 **which no longer skips the lot, its sheet being gone.** ⚠️
**Trace it whole**: 🔴 **what if the revert conflicts? what if the lot
is not the last coded? what re-runs after the sheet is rewritten?**

**And it passes `## Findings` in the Détailleur's prompt** — 📌 **a
parameter, not a mode.** 🔴 **Check the agent is told what to do with
it.**

**`Mode: divergence`.** 🔴 **The two modes treat the same lot in
opposite ways** — ordinary skips a lot that has a sheet, divergence
rewrites it. 📌 **Check every invocation of the Détailleur says which**,
⚠️ **and that no path reaches it with neither.**

**The numbered decision.** 🔴 **A blocking file can carry several
`## Blocking N`, each answered on its own number**, and 📌 **a number
with no answer means that entry still waits.** ⚠️ **`/8_code` must count
the answers against the headings** — 🔴 **trace what happens on a
half-answered file: is it applied, renamed, or stopped?**

**`/7_lots` removes `code/blocked_verificateur.md`** at the head of
every run. 📌 **Check it cannot remove one that was just written**, and
that the round it belongs to is over.

**The round count.** 📌 **The Vérificateur now writes the round number
in `code/sequence.md`, and the Cadreur reads that line.** 🔴 **Check the
three-round cap is reachable from a cold re-entry** — ⚠️ **the old count
on archived files was always zero.**

**`/9_controle` on two folders.** 📌 **Phases 1-3 run on the feature
folder, 4-6 on the working folder.** 🔴 **Trace both cycles**: ⚠️ **a
feature cycle where the two are the same, and a correction cycle where
they are not.**

**Its map is built on `Genre: comportement` alone**, 📌 **and blocks a
correction cycle built are marked `carried`.** 🔴 **Check no block falls
through**: ⚠️ **the four other genres must each be named as taken up
elsewhere.**

**The block identifier travels.** 📌 **`bug-list.md` → `desc-bug.md`
title → `Anchor: … (B12)` → `/9_controle` marks `carried`.** 🔴 **Follow
it end to end**, ⚠️ **and report where the chain does not say how it is
written.**

---

## Still to check, as before

- 🔴 **The per-lot loop chains five agents** — `detailleur`,
  `concepteur`, `testeur`, `realisateur`, `relecteur`. 📌 **What happens
  if each blocks, one by one?**
- The attempt counter: where it lives, who writes it, who increments
  it, 🔴 **what happens if it is missing**, ⚠️ **and what happens on a
  first attempt that committed nothing**
- The escalation to `opus` after two `Cause: reasoning`
- The return to the split: who writes it, who reads it, when it is
  archived, and the stop at the third
- The Cadreur's three rounds with the Vérificateur
- 📌 **`/9_controle`'s six phases**: 🔴 **three do not run on a
  correction cycle — do the other three actually run?**

🔴 **Trace four scenarios**: 📌 **a lot that passes first time · a lot
that fails three times · a redécoupage mid-block · a lot whose review
returns `Cause: sheet`.**

**Your report — one table, and nothing else.** 🔴 **No evidence section,
no development, no restatement of what you read.**

    | # | Severity | Origin | Where | Finding |

- **`#`** — 🔴 **`F01`, `F02`…**, one numbering for the whole report,
  whatever the severity. ⚠️ **Never a prefix that encodes severity.**
- **`Severity`** — `BLOCKING` · `TO FIX` · `NOTE` · `QUESTION`.
- **`Origin`** — 🔴 **one word**: `refonte` when the same file under
  `.claude/` or `docs/` did not have it, `pre-existing` when it did,
  `unknown` when you cannot tell. ⚠️ **Never a guess.**
- **`Where`** — 🔴 **file and line, both sides, separated by `↔`** —
  `concepteur.md L141 ↔ detailleur.md L229`. ⚠️ **Never a file without a
  line**: 📌 **there is no evidence section to fall back on.**
- **`Finding`** — 🔴 **one sentence, carrying what it costs.** 📌 *« The
  Concepteur is sent to a field that does not exist, so three of its
  rules never fire »* — ⚠️ **not** *« problem with `Modifies` »*.

📌 **Sort by `#`.** 🔴 **A census is a reading, never a report** — ⚠️
**only the anomalies are written.**

📌 **One exception, at the end, three lines at most**: 🔴 **what you
checked and found sound** — ⚠️ **named, never developed.**
```

## V5 — Handovers, upstream and downstream

```
READ-ONLY. Write docs/verification4/passages.md

🔴 **First, read the entries of `docs/verification3/plan.md` that touch
your scope** — 📌 **what changed this round, and what nobody has
checked since.** ⚠️ **Then do everything below, in full**: 🔴 **those
entries are where to start, not where to stop.**

🔴 **Read what you need, never a folder whole** — 📌 **the chain is
830 KB.**

⚠️ **Do not report formatting** — 📌 **a script already guards it and
the chain is clean of it**: 🔴 **unclosed bold, dead references, numeric
counts, colliding move numbers, orphan fragments, empty separators,
repeated lines, known typos.** 📌 **Your work is what a script cannot
see.**


For each consecutive pair, verify that what the first writes matches
exactly what the second expects: same section names, same field names,
same shape, same possible values. Cite the writer's line and the
reader's line. A one-character gap in a section name is BLOCKING.

🔴 Read only the sections that say what the agent reads and writes.
⚠️ The heading is not the same in every agent — three forms coexist:
- `## What you read` and `## What you write` — 📌 **most agents**
- `## Where you work` — a table of paths, used by cadreur,
  convertisseur, lexicographe
- The invocation table under `## INVOCATION n`, or a `| # | Invocation |
  Inputs | Output |` table — used by redacteur, fusionneur,
  diagnostiqueur, and every multi-invocation agent

📌 `Select-String -Path <agent> -Pattern '^## '` first, pick the
headings that apply, then read those ranges. ⚠️ **The shell is
PowerShell, not bash.** 🔴 An agent where none of the three forms
appears is itself a finding — report it rather than skipping it.

Pairs, upstream:
lexicographe→redacteur · redacteur→decoupeur · decoupeur→qualifieur ·
qualifieur→classeur · classeur→sondeur · sondeur→assembleur ·
assembleur→redacteur · redacteur→convertisseur ·
convertisseur→architecte · convertisseur→cadreur ·
9_controle→redacteur · redacteur→fusionneur

Pairs, downstream:
cadreur→verificateur · verificateur→detailleur · detailleur→concepteur
· concepteur→testeur · testeur→realisateur · realisateur→relecteur ·
relecteur→detailleur · relecteur→controleur · detailleur→arbitre ·
realisateur→arbitre · arbitre→architecte

Never exercised, check hardest: 9_controle→redacteur ·
detailleur→concepteur · concepteur→testeur · testeur→realisateur

⚠️ **A pair is not always consecutive.** 🔴 **A field written by one
agent can be read by three that come later** — 📌 **`## Declared` of
`conception.md` is read by the Testeur, the Réalisateur and the
Relecteur.** 🔴 **Check every reader a field has, not only the next
agent.**

---

## Commands hand over too

🔴 **A prompt is a handover.** 📌 **What a command passes an agent has
to match what the agent reads** — ⚠️ **a parameter the agent never
reads is a silent no-op, and the command believes it did its job.**

🔴 **For each agent, take the `Agent()` templates that invoke it** and
check every line of the prompt against the agent's own reading rules:

- `Mode: divergence` — 📌 **`/8_code` → détailleur**
- `Group:` — 📌 **`/9_controle` → contrôleur**
- `## Findings` of a verdict — 📌 **`/8_code` → détailleur, on a
  `Cause: sheet`**
- `Affected lots:` · `Your block:` · `Blocking file:` ·
  `Invocation n —` · the answered questions file · the technical file
  of a nature

⚠️ **And the reverse**: 🔴 **a rule that keys on something the prompt
never carries.** 📌 **The Contrôleur's `Group:` was that case before the
campaign** — **the rule existed, the prompt did not name it, and every
group hit it.**

---

## The fields the campaign moved

🔴 **A field is a handover.** 📌 **These changed hands, shape or reader
during the correction campaign** — ⚠️ **check each against every one of
its readers, not only the next agent:**

**`## Files` and `## Declared`.** 🔴 **The sheet's `## Files` carries
the files the lot opens that already exist**, from `Touches`; 📌 **the
files a lot creates are named by the Concepteur in `conception.md`'s
`## Declared`.** ⚠️ **Four agents test `## Outside the lot` against
both** — 🔴 **check each reads both, and that neither is expected to
carry what the other does.**

**`## What governed the code, besides the sheet`.** 📌 **The Réalisateur
writes it, the Relecteur reads it to tell a decided divergence from a
drift.** 🔴 **Check the two describe the same field.**

**`## Blocking N` and the numbered `## Decision`.** 📌 **One shape,
stated by the Arbitre, written by the Détailleur and the Réalisateur.**
⚠️ **The Concepteur, the Testeur and the Relecteur write four `##`
headings and no numbering** — 🔴 **check the Arbitre's rule says which
files it governs.**

**The round number in `code/sequence.md`.** 📌 **Written by the
Vérificateur, read by the Cadreur.** 🔴 **Same line, same shape?**

**`Anchor: … (B12)`.** 📌 **Written by the Cadreur from `desc-bug.md`'s
entry title, read by `/9_controle`.** 🔴 **Three hands** — ⚠️ **check the
form survives all three.**

**`Kind: forme`.** 📌 **A fifth value of the Architecte's questions
file.** 🔴 **Check `/conventions` relays it like the four others.**

**`## Invocation` in the rédacteur's blocking file.** 📌 **Written by
the Rédacteur, read by `/2_structure` and `/fusion` to route.** 🔴
**Check both read it, and that its values match the agent's
invocations.**

**`R<n>` against `§<n>`.** 📌 **The Architecte numbers rules `R<n>`; the
sheet's `## Conventions` cites them; the Relecteur reports them.** ⚠️
**A section number where a rule number was meant opens a whole
section** — 🔴 **check the three agree.**

**`PASS with reservation`.** 📌 **Every reader matches the `PASS`
prefix.** 🔴 **Check each of the five readers** — `relecteur`,
`detailleur`, `verificateur`, `8_code`, `9_controle` — ⚠️ **matches a
prefix and not a whole line.**

**Your report — one table, and nothing else.** 🔴 **No evidence section,
no development, no restatement of what you read.**

    | # | Severity | Origin | Where | Finding |

- **`#`** — 🔴 **`F01`, `F02`…**, one numbering for the whole report,
  whatever the severity. ⚠️ **Never a prefix that encodes severity.**
- **`Severity`** — `BLOCKING` · `TO FIX` · `NOTE` · `QUESTION`.
- **`Origin`** — 🔴 **one word**: `refonte` when the same file under
  `.claude/` or `docs/` did not have it, `pre-existing` when it did,
  `unknown` when you cannot tell. ⚠️ **Never a guess.**
- **`Where`** — 🔴 **file and line, both sides, separated by `↔`** —
  `concepteur.md L141 ↔ detailleur.md L229`. ⚠️ **Never a file without a
  line**: 📌 **there is no evidence section to fall back on.**
- **`Finding`** — 🔴 **one sentence, carrying what it costs.** 📌 *« The
  Concepteur is sent to a field that does not exist, so three of its
  rules never fire »* — ⚠️ **not** *« problem with `Modifies` »*.

📌 **Sort by `#`.** 🔴 **A census is a reading, never a report** — ⚠️
**only the anomalies are written.**

📌 **One exception, at the end, three lines at most**: 🔴 **what you
checked and found sound** — ⚠️ **named, never developed.**
```

# Git, in this mode

🔴 **One worktree for the whole campaign**, created before the first
invocation and merged once at the end. ⚠️ **Not one per
investigation**: each writes a distinct file, and five merges
buy nothing.

**Before invoking anything:**

```
git worktree add ../verif-<date> -b verification/<date>
cd ../verif-<date>
mkdir docs\verification4
```

🔴 **Enter the worktree before invoking, not after a write fails** — 📌
**the harness blocks a subagent's writes until the session is
isolated.** ⚠️ **Measured on this project: the agent does the full job,
cannot write, and the whole invocation is redone.**

🔴 **`docs/verification4/` is created by the `mkdir` above**, before the
first agent runs — 📌 **an agent that
has to create its own folder sometimes writes beside it instead.**

❌ **Never pass `isolation`** — 📌 **the agents read the same files and
write different ones.**

**Once every report is written:**

```
git add docs/verification4/
git commit -m "Verification campaign <date>"
cd <main checkout root>
git merge --no-ff verification/<date>
git push
git worktree remove ../verif-<date>
```

🔴 **The commit is yours** — 📌 **the agents have no Bash.**

🔴 **The push is part of the merge, not an afterthought.** ⚠️ **A
campaign that sits only on the local machine is lost with it.**

⚠️ **A worktree holding uncommitted files refuses a plain remove** — 🔴
**never force it**: say what is left there and stop.

📌 **Merge even when reports are missing** — 🔴 **what was written is
worth keeping**, and say which are missing.

---

# After the reports

🔴 **Read them together, triage, fix in one pass.** ⚠️ **No fixing as
the reports land** — two concurrent edits on one file lose each other.

📌 **Order**: the BLOCKING findings first.

**What the last campaign taught about the fixing itself:**

🔴 **Re-read the whole agent after correcting it.** ⚠️ **A fix that
moves a section breaks cross-references a grep cannot see**, and about
one correction in five left something behind — a rule stated twice, an
entry lost while repairing a list, a fix applied at one site of three.

🔴 **Run `coherence.py` after every agent**, not at the end. 📌 **It
catches a broken bold or a lost line while the edit is still in mind**;
ten minutes later it costs ten times more to place.

🔴 **When a batch of edits reports a failure, retry it before moving
on.** ⚠️ **A correction reported as passed and never applied is the
worst outcome**: it is believed.

🔴 **A fix that is right for one agent is not automatically right for
its siblings.** 📌 **Check the sibling has the same gesture before
propagating** — ⚠️ **propagating without checking created defects twice
in the last campaign.**

---

# What this round does not prove

⚠️ **Five clean reports is not « the chain works ».**

✅ **What it establishes**: 🔴 **every name has a writer and a reader**
· **every route has an outcome** · **every handover matches on both
sides.**

🔴 **What it does not**: ⚠️ **that any of it runs.** 📌 **A route can
close on paper and a prompt miss its parameter at run time; an agent
can read a field that exists and do the wrong thing with it.**

🔴 **This is the third reading round.** 📌 **The first two found the same
volume** — ⚠️ **do not open a fourth.**

**The measure that follows** — 🔴 **one real cycle on a small feature,
end to end.** 📌 **That is what says whether the chain is usable**, and
nothing else will.
