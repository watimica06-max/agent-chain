# Verification — `decoupeur.md`

Read: `.claude/agents/decoupeur.md` (old), `.claude-new/agents/decoupeur.md`
(new), `docs/refonte/passes/decoupeur.md`, `docs/refonte/modifications.md`
section `# \`classeur.md\` · \`decoupeur.md\`` (lines 294–338), plus the two
table rows that section delegates to: the Qualifieur table (line 54) and the
Sondeur table (line 353). Because eight of the seventeen comments target
`.claude/commands/3_decoupe.md`, both versions of that command were read too.

Line numbers below refer to the **new** agent file unless prefixed `cmd:`
(new command) or `old:`.

Structural modifications announced for this agent, from the two tables:

| Source | Modification |
|---|---|
| Qualifieur table, line 54 | Writes `Genre:` empty beside `Nature:`; leaves both empty on each half |
| Sondeur table, line 353 | Carries the `Global:` line on every half |
| Qualifieur table, line 55 (command) | `/3_decoupe` relays to `/3a_genre`, at both places |

Pass sheet: Passés (13) — C2 · C3 · C5 · C6 · C7 · C8 · C10 · C11 · C12 · C13
· C14 · C15 · C16. Écartés (3) — C4 · C9 · C17. Reporté (1) — C1.

---

## A. Conformity

### PASSÉ

| Id | Expected (from the pass file) | Found | Verdict |
|---|---|---|---|
| C2 | Command: one existence check on `desc-produit.md` before invoking, stop names the file; the two marker greps anchored to title lines | cmd:66–67 glob, stop names the file, `/2_structure` has not run. cmd:76–77 `grep '^### .*NEW'` / `'^### .*MODIFIED'`, cmd:79–80 explains the anchor | **Conforming** |
| C3 | Agent: never-do entry excepts the blocking file; **and** the blocking file's location given as a path derived from the prompt (the folder holding the product file) | Line 107 `Write anywhere but the product file and a blocking file` — done. Line 113–114 still reads `blocked_decoupeur.md, in the feature folder` — the folder is still never defined, the prompt (cmd:101–103) still names only the product file's path | **Half applied — TO FIX.** The second half of the request was not made. |
| C5 | Move 1 gives the sentences nothing sets off a bucket; move 2 makes that bucket one block | Lines 158–161 (the extra list), 163–165 (its block), 167–169 (the justification) | **Conforming.** See B-1 for one word the bucket gained beyond the request. |
| C6 | The two-trigger sentence is named, its outcome is a blocking file whose `To resume` is a rewording upstream; the file says whether two events with one identical consequence count as one trigger | Lines 128–131 name the case and the outcome; lines 133–136 settle the identical-consequence question (one trigger) | **Conforming as to the request** — but the example chosen at 128–129 is exactly the case 133 declares not blocking; see D-1 (BLOCKING). |
| C7 | The blocking list names only cases visible in the block and unresolvable by moving sentences; the two-trigger sentence first; "two features" goes | Lines 124–136: one case, the two-trigger sentence; "the file is missing", "a block … does not exist", "two features" all gone | **Conforming** |
| C8 | Command: the blocking row sends the Product Owner to the command that can act on a rewording, not `/3_decoupe` | cmd:201 `Fill its ## Decision, then /2_structure … /3_decoupe again afterwards` | **Applied on this side only.** Neither `.claude-new/commands/2_structure.md` (reads only `blocked_redacteur.md`, lines 27 and 65) nor `.claude-new/agents/redacteur.md` (no mention of `blocked_decoupeur`) knows the file the Product Owner is sent with. The pass file itself flagged this dependency ("named in the closing section"). **Question for the group pass**: who reads the filled Decision of `blocked_decoupeur.md` during `/2_structure`? |
| C10 | The definition settles cascades; one reading, written | Lines 77–89: the root-cause reading (tap → request → response → screen is one trigger), with the sensor / timer / user counter-examples | **Conforming.** Note it is the *opposite* of the reading the pass author preferred (nearest cause), which the pass file allowed. The wording of the definition has a defect of its own — D-5 (TO FIX). |
| C11 | "may keep" becomes "keeps", without option; retired only when no new block carries what the title named | Lines 193–199 `keeps that title and that number — not a choice … Only when no new block carries what the title named is the number retired` | **Conforming.** The residual point (a `NEW` original whose kept half becomes `MODIFIED`, line 198) is left as the pass file left it — still open, see D-9. |
| C12 | Example shows a block carrying one trigger, in words belonging to no product | Line 182 `### B62 — Closing the current segment    NEW` | **Conforming on the trigger** (one user action). **Question** on the words: "segment" and `Global: ## Activity screen` (line 185) read as this project's vocabulary — is that "no product"? The `## Activity screen` value is copied from the Rédacteur's example (modifications.md line 166), so it is at least consistent across files. |
| C13 | On a turn that names blocks: read the named blocks by range from one `^### B` grep; highest number from that grep; whole-file read only when every block is named | Lines 40–45, and 189–190 `taken from the ^### B grep` | **Conforming** |
| C14 | **Two halves**: (a) the command bounds what one invocation is given — a range, sequential invocations, a ceiling ("the file has to hold one"); (b) the agent's report names the blocks it looked at and the command compares lists | (b) done: agent lines 218–230, cmd:188–194. (a) **not done**: cmd:69–70 still `every block. Name none in the prompt`, no ceiling, no range, no sequential invocation anywhere | **Half applied — TO FIX.** modifications.md lists C14 as Passé without a caveat. The command now *detects* a partial sweep (cmd:189 "a short list is a partial sweep") but has no step for what to do with one — see D-12. |
| C15 | Command: template carries an optional third line naming the blocking file; `NN` has one written rule | cmd:103 third line; cmd:123–124 `the highest blocked_decoupeur-NN.md in the folder plus one — 01 when there is none` | **Conforming** for the `NN` this command owns. The `questions-<agent>-NN.md` placeholder at cmd:51 still has no rule here — those files are written by other agents, so the rule belongs to them; NOTE only. |
| C16 | Command forbids only what its own moves could be tempted into — target was both `CALIBRATION_RISK_LEVEL.md` in "What you read" and "no risk level, no `TaskCreate`" in "What you relay" | cmd:204 reduced to `no reading of what a block says` — done. cmd:26–27 still `never open CURRENT_TECHNICAL_STATE.md or CALIBRATION_RISK_LEVEL.md` | **Half applied — TO FIX (minor).** The pass file's `Cible` named both places. |

### ÉCARTÉ / REPORTÉ — verified NOT applied

| Id | Expected | Found | Verdict |
|---|---|---|---|
| C4 (écarté) | The `Clarification needed` paragraph stays in the agent | Lines 47–50, unchanged from old:40–43 | **Not applied — correct.** But the pass file's fallback ("if kept, its outcome would have to be a blocking file and a relay row, not a reply") was not taken either, and the discard reason in modifications.md does not address it. The outcome is still a reply, which the file itself says gets lost — D-4. |
| C9 (écarté) | Nothing says what becomes of the other named blocks when one blocks | Lines 111–141: nothing added on it | **Not applied — correct.** Note the new "What you report" (218–230) now half-answers it by accident: the report lists what was looked at, so the orchestrator can see the sweep stopped short — but nothing says whether the split blocks were written back before the stop. The discard reason ("one cause, the case is rare") stands. |
| C17 (écarté) | No comparison of the product file between turns | cmd:85–86 unchanged: `Do not grep the questions file — a block an answer touched carries MODIFIED` | **Not applied — correct** |
| C1 (reporté) | Command section order unchanged | cmd sections in the same order as old (What you read → Before anything else → Which blocks → The invocation → Once it has reported → Git → What you relay) | **Not applied — correct** |

---

## B. Unannounced changes

Diff old → new, everything not covered by a pass comment or a table row.

**B-1 · Line 161 — a third kind of untriggered sentence** — TO FIX

> old (rule, line 57–58, unchanged in new 64–65): *What nothing sets off is a block too — a reference table, a catalogue of values something looks up.*
> new (move 1, line 159–161): *the sentences nothing sets off — a reference table, a catalogue of values something looks up, **a constraint the Product Owner imposed**.*

C5 asked for a bucket for "reference material"; the bucket gained a category the rule at line 64 does not list. What it changes: a block holding a behaviour and a Product-Owner constraint (a directive, in the qualifieur's genres) is now split in two by this agent, where before the constraint stayed with the behaviour. Plausibly intended as a cascade of the qualifieur's `directive` genre, but neither the pass file nor the tables announce it, and "The rule" was not updated to match. Not a defect if intended — but the rule and the move must list the same things (D-3).

**B-2 · Lines 167–169 — a justification paragraph in PART 3** — NOTE

> new: *A block holding one trigger's sentences and a catalogue is two blocks — left inside, the catalogue is probed under that trigger's questions, and its own gaps close unasked.*

This is the pass file's `Justification` for C5 lifted into the agent. Not asked for; harmless; it is the only "why" paragraph in PART 3.

**B-3 · Lines 193–199 — the kept-number rule reworded and split into two paragraphs** — NOTE

> old: *One of them may keep the original's title and number when it carries what that title named. It then carries `MODIFIED`, not `NEW` — something already pointed at it.*
> new: *The one that carries what the original's title named keeps that title and that number — not a choice. Something already points at that number, and retiring it would leave the reference pointing at nothing. / It then carries `MODIFIED`, not `NEW`. Only when no new block carries what the title named is the number retired.*

C11 covers the "may → keeps" change. The added consequence ("would leave the reference pointing at nothing") and the paragraph split are extra wording. No change of meaning.

**B-4 · Frontmatter description, line 3 — unchanged** — NOTE

> *Writes in the product file, splits only, never rewrites a sentence.*

Still true, but the agent now also writes `Genre:` and `Global:` lines and a report. Not a defect; recorded because the description is what the orchestrator sees in the registry.

**B-5 · cmd:68–70 — a sentence deleted from the command** — NOTE (command, not the agent)

> old cmd:67–70: *Other questions files say nothing here: the Rédacteur strips every marker when it integrates, so a block written at its first invocation and never split carries none by the time you run.*
> new cmd:69–70: sentence gone.

No pass comment and no table row asks for this. The pass file's closing section (question 2, "Does the Rédacteur mark the blocks it changes … the command says it strips every marker") may have been settled elsewhere. Question: was the Rédacteur's marker-stripping behaviour changed, or was the explanation just dropped?

**Nothing else changed**: no renumbering, no moved section, no rewritten table. The diff is otherwise fully accounted for by C3, C5, C6, C7, C10, C11, C12, C13, C14(b) and the two table rows.

---

## C. Gestures against tools

Frontmatter tools: `Read, Grep, Glob, Edit, Write`.

| Gesture | Line | Tool | Verdict |
|---|---|---|---|
| Grep `^### B` for titles, ranges, highest number | 40–43, 189–190 | Grep | has it |
| Load the named blocks by range | 42 | Read (offset/limit) | has it |
| Read the whole file on a first turn | 45 | Read | has it |
| Read the blocking file the prompt names | 138–139 | Read | has it |
| Write the blocks back in place of the one split | 171–172 | Edit | has it — see C-1 |
| Write `blocked_decoupeur.md` | 113 | Write | has it |
| Report the blocks looked at | 218–230 | none needed (reply) | — |

**C-1 · Edit vs Write on the product file** — NOTE. Line 171 says "write the blocks back … in place of the one you split" and names no tool. On a later turn the agent holds only the named blocks (C13, line 40); a `Write` of the product file would then truncate it to what it loaded. `Edit` is the only tool that fits, and the file does not say so. A NOTE, since the tool is present; a line saying "by Edit, never by rewriting the file" would close it.

**C-2 · `Glob` — no gesture uses it** — NOTE. The prompt names the product file (line 32), the agent "never looks for" a blocking file (139–141), and the feature folder is never located (the C3 gap). Nothing in the file globs. Either the tool is surplus, or it is the means the C3 fix would need (locate the folder holding the product file — which is a path operation, not a glob, so probably surplus).

No gesture lacks a tool. No Bash is needed: the agent runs no git.

---

## D. Internal coherence — new file alone

**D-1 · Lines 128–136 — the blocking example is the case the next paragraph says is not blocking** — BLOCKING

> 128–129: *One sentence carries two triggers — « when the user does A, or when B expires, the screen closes ».*
> 133–134: *Two events with one identical consequence are one trigger — it is one sentence saying when something holds.*

"A, or B expires → the screen closes" is two events with one identical consequence. By 133 it is one trigger, so it is not a two-trigger sentence and does not block. The only blocking cause the file names is illustrated by a non-example. An agent reading 128 blocks; one reading 133 does not. Either the example needs two consequences (« when the user does A the screen closes; when B expires it dims ») or the rule at 133 is wrong.

**D-2 · Line 133 against lines 60–62 and 73 — the number of triggers depends on the sentence's grammar** — TO FIX

> 60–62: *Another trigger is another block. Two different pieces of data are two triggers, even when the question asked of each is the same.*
> 73: *Read what fires it, not its grammatical subject.*
> 133–134: *Two events with one identical consequence are one trigger — it is one sentence saying when something holds.*

"Heart rate is missing → a dash" and "pace is missing → a dash", written as two sentences, are two triggers by line 60. Written as one sentence ("when heart rate or pace is missing, a dash shows"), they are one trigger by line 133. The count now turns on punctuation, which is what 73 forbids. Question: is 133 meant to be a rule about triggers, or only a statement that such a sentence is not a blocking case (because it can sit in one block)? If the latter, it should say so and not redefine "one trigger".

**D-3 · Line 64–65 against line 159–161 — the rule and the move list different things** — TO FIX

> 64–65: *What nothing sets off is a block too — a reference table, a catalogue of values something looks up.*
> 159–161: *the sentences nothing sets off — a reference table, a catalogue of values something looks up, a constraint the Product Owner imposed.*

Same as B-1, seen from inside the file: the move splits out a kind of sentence the rule does not name. Two readers, one applying "The rule", one applying PART 3, split differently.

**D-4 · Lines 47–48 against lines 113–115 — a stop whose outcome is a reply, in a file that says replies get lost** — TO FIX

> 47–48: *A `**Clarification needed:**` line in a block you were named stops you — say which block, and split nothing.*
> 113–115: *Write a blocking file … do not merely say it. A message in a reply gets lost; a file does not.*
> 229–230: *Nothing else is yours* (the report's closed list: blocks looked at, blocks split).

The Clarification stop's only outcome is "say which block" — a reply — and "What you report" does not list it among what the agent may say. C4 was discarded on the ground that the perimeter differs from the command's grep, which is fair; but the pass file's condition for keeping it (a blocking file and a relay row) was not met, and the command has no relay row for this outcome (cmd:199–202: blocking file / otherwise). If the stop fires, the orchestrator's row is "Otherwise → `/3a_genre`" and the block goes unsplit to the qualifieur. Question: given the command greps the whole file first (cmd:44–47), can this stop fire at all inside a worktree created from the same commit?

**D-5 · Line 77 — "another block" in the trigger definition** — TO FIX

> 77–78: *A trigger is an event that can occur without **another block** having caused it.*
> 78–80: *What exists only because **the block's own trigger** produced it is not a second trigger.*

The general definition says "another block", the application says "the block's own trigger". Read literally, 77 makes almost nothing a trigger: a tap on a screen exists only because some other block's behaviour opened that screen, so by 77 the tap is not a trigger — which 87–89 then contradicts ("the user acting … none of them needs another block to have run"). The intended reading (from 78–80) is "without a trigger of its own having produced it". One word — "another block" → "this block's trigger" or "another trigger" — and the definition holds.

**D-6 · Lines 77–80 — a block whose only trigger is a sequel has no branch** — NOTE / question

If the Rédacteur wrote the response in a block of its own (B9: "When the response comes back, the screen shows…"), then by 77–80 B9's event is a sequel of B7's trigger and "its sentences stay in the block" — which block? The agent may not merge (line 103), may not touch a block not named (104), and B9 is not a catalogue (64). The definition was written for the within-block case only. Question: is a block with zero triggers of its own a case the agent should block on, leave alone, or is it excluded by construction (the Rédacteur never writes one)?

**D-7 · Line 113–114 — "in the feature folder", never defined** — TO FIX

> *Write a blocking file — `blocked_decoupeur.md`, in the feature folder*

The prompt (cmd:101–103) carries `docs/features/<name>/desc-produit.md` and, optionally, `blocked_decoupeur.md` without a path. Nothing in the agent says the feature folder is the folder holding the product file. This is the unapplied half of C3.

**D-8 · Line 32 against lines 40–45 — "read" in two senses** — NOTE

> 32: *You read the product file the prompt names, and nothing else*
> 40: *When it names blocks, you read those blocks, not the file.*
> 45: *Only a turn that names every block is read whole.*

Line 32 uses "read" for "the file you are allowed to open"; line 40 uses it for "load into context". Coherent once understood; a first reader meets a rule and its apparent contradiction eight lines apart. Also "whole" at 45 (the file) and 158 (the block) name different things.

**D-9 · Line 179–180 against line 198 — "each … carries `NEW`" then one carries `MODIFIED`** — NOTE (pre-existing)

> 179–180: *Each block you produce carries a title, an empty `Genre:`, an empty `Nature:` and `NEW`*
> 198: *It then carries `MODIFIED`, not `NEW`.*

"Each" at 179 has an exception at 198. Was already so in the old file (141–142 / 152–154). And the open point the pass file left — a `NEW` original whose kept half is stamped `MODIFIED` at 198, so that a block nothing pointed at yet is now marked as if something had — is still unsettled; the "What another agent would settle" question 1 has no trace of an answer in this file.

**D-10 · Line 124–126 — "which is one case", followed by two paragraphs** — NOTE

> 124–126: *Block only when splitting is impossible — which is one case, and you can see it in the block itself:*

Then 128–131 (the two-trigger sentence) and 133–136 (identical vs differing consequences). The second paragraph is a criterion for recognising the first, not a second case, so the count holds — but only after D-1 is fixed; as written, the second paragraph withdraws the first.

**D-11 · Line 220–225 — the report's ground names a fact about the orchestrator** — NOTE

> *The orchestrator named a list and cannot open a block to check what became of it*

True of the command (cmd:24, cmd:135). Recorded because it is the one place the agent describes its caller's constraints; if the command changes, this line goes stale silently. Not a defect.

**D-12 · (command) cmd:188–194 — a partial sweep is detected and then nothing** — TO FIX (command)

> cmd:189–191: *a short list is a partial sweep, and nothing else can see it: you may not open a block to check.*

No step follows: no re-invocation on the blocks not reached, no relay row for it (cmd:199–202 has only "blocking file" and "otherwise"). This is the branch C14(a) would have closed with a ceiling and sequential invocations. As it stands the orchestrator sees the short list, has no row for it, and relays "Otherwise → `/3a_genre`".

---

## Summary

- **BLOCKING (1)**: D-1 — the only blocking cause is illustrated by an example the next paragraph declares non-blocking.
- **TO FIX (8)**: C3 half (feature folder undefined, = D-7) · C14 half (no ceiling, no sequential invocation, = D-12) · C16 half (`CALIBRATION_RISK_LEVEL.md` still forbidden) · D-2 (trigger count depends on grammar) · D-3 / B-1 (rule and move list different untriggered kinds) · D-4 (Clarification stop's outcome is a reply with no relay row) · D-5 ("another block" in the definition).
- **Questions (4)**: C8 — who acts on a filled `blocked_decoupeur.md` in `/2_structure`? · C12 — are "segment" and "Activity screen" product words? · B-5 — was the Rédacteur's marker-stripping changed, or only its explanation dropped from the command? · D-6 — what does the agent do with a block whose only event is another block's sequel?
- **Écartés / reporté**: all four verified not applied.
- **Tools**: every gesture has its tool; `Glob` is used by no gesture.
