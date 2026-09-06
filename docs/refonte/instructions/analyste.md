# Instructions — analyste

Verdict: **changed** (D1: a `Default:` line under every question, silence
never consent; D2: every downstream agent's answers come back through
the Analyste). Base: `.claude/agents/analyste.md`. No earlier pass
named this agent under *Consequences elsewhere* — the folder was empty.

Every `Cible` quotes the text it aims at, so the entries can be applied
top to bottom; where one relies on another, the justification says so.

---

### 1

    Fichier      : .claude/agents/analyste.md
    Opération    : add text
    Cible        : section "Which invocation is this?", right after the
                   three-row table, before "Invocations 1 and 2 loop"
    Aujourd'hui  : nothing — the table lists the invocations; nothing
                   says how the agent learns which one it is running
    Après        : 🔴 **The orchestrator's prompt names your invocation.**
                   The feature folder does not tell 1 from 2 — after a
                   round, both see the same files. ⚠️ **No invocation
                   named in the prompt → stop and write
                   `blocked_analyste.md`** (see *When you cannot
                   produce*).
    Justification: Robustness — a missing stop. Invocations 1 and 2 see
                   the same folder state; an agent told nothing infers
                   one and runs it, and a grid run in a context that has
                   read the answers is exactly what the second
                   invocation exists to prevent.

### 2

    Fichier      : .claude/agents/analyste.md
    Opération    : replace text
    Cible        : section "Which invocation is this?", the paragraph
                   "📌 **Invocation 1 also serves the questions raised by
                   the Convertisseur and the Fusionneur** — same work,
                   same branching."
    Aujourd'hui  : that paragraph — two agents named
    Après        : 📌 **Invocation 1 serves every questions file,
                   whichever agent wrote it** — the person's answers to a
                   downstream agent's questions come back through you,
                   by the same moves as an answer to your own.
    Justification: Robustness, D2 — a list where a class is meant. The
                   verdict routes the Architecte's answers through the
                   Analyste and this sentence does not name it; the next
                   agent to ask would be missed the same way. Naming the
                   class closes it for good.

### 3

    Fichier      : .claude/agents/analyste.md
    Opération    : drop text
    Cible        : section "Which invocation is this?", the paragraph
                   "📌 **Between two sessions, re-read the product file**
                   — it is your state."
    Aujourd'hui  : that paragraph
    Après        : dropped
    Justification: Tokens — a read no move uses: the agent runs one
                   invocation per call and has no "session" to resume;
                   read literally it is a whole-file read of a file that
                   "runs to hundreds of lines". And it contradicts "You
                   never read it whole" and the *What you never do*
                   entry — two passages asking different things.

### 4

    Fichier      : .claude/agents/analyste.md
    Opération    : replace text
    Cible        : section "When you resume after a blocking file", the
                   two paragraphs "**How you apply it** — **as an
                   answer.** It enriches the block its `## Where` names,
                   by the same five passes as a questions file." and
                   "🔴 **A decision bringing its own trigger becomes its
                   own block**, exactly as an answer would."
    Aujourd'hui  : every decision is applied as an answer to a block
    Après        : **How you apply it depends on what was blocked:**

                   | The decision | What you do |
                   |---|---|
                   | Settles a product matter — a behaviour, a scope, which of two readings holds | Apply it as an answer to the block `## Where` names, by the five passes of *When you read a questions file*. 🔴 A decision bringing its own trigger becomes its own block, exactly as an answer would |
                   | Supplies or corrects an input — a path, a file that was missing, a premise that was false | Take it as that input; nothing enters the product file from it |

                   Then delete the file and carry out the invocation you
                   were called for.
    Justification: Robustness — a rule that holds in one of the cases the
                   agent handles. The agent's own blocking causes are "a
                   missing input, a file you were told to read that is
                   not there, a false premise": a decision on any of
                   those names no block to enrich, and an agent told to
                   enrich one invents which. The last line states what
                   follows the unblocking, which nothing said.

### 5

    Fichier      : .claude/agents/analyste.md
    Opération    : replace text
    Cible        : INVOCATION 1, the "Inputs" table "The root holds /
                   What you read" (two rows: "No questions file at all"
                   and "One or more, any prefix")
    Aujourd'hui  : | No questions file at all | `idees.md` … |
                   | One or more, any prefix | 🔴 **The highest-numbered
                   one, and it alone.** Never `idees.md`, never an
                   earlier questions file |
    Après        : | The root holds | What you read |
                   |---|---|
                   | No questions file, and `questions/` holds none either | `idees.md` — free-form, in French, that is the point |
                   | No questions file, and `questions/` holds filed ones | 🔴 **Nothing to integrate — say so and stop.** The idea was structured on an earlier turn; reading it again files the whole feature a second time |
                   | Exactly one questions file whose entries carry no mark (pass e) | 🔴 **That file, and it alone.** Never `idees.md`, never a filed one |
                   | One or more, every entry marked | Nothing to integrate — say so and stop |
                   | Several with unmarked entries | 🔴 **Stop and write `blocked_analyste.md`** — you cannot tell which is the latest |
    Justification: Robustness — "the highest-numbered one" reads two ways
                   once two agents' files share the root: numbers are per
                   agent ("Your number: the highest
                   questions-analyste-NN"), so `analyste-02` and
                   `convertisseur-01` do not compare. Two missing stops
                   besides: a root emptied by filing sends the agent back
                   to `idees.md` and it restructures the feature over the
                   blocks it already has; a file already consumed is
                   integrated twice. The marks pass e writes (entry 10)
                   are the one fact that tells a consumed file from a
                   pending one.

### 6

    Fichier      : .claude/agents/analyste.md
    Opération    : replace text
    Cible        : INVOCATION 1, "How you load the product file", the
                   numbered steps 1 to 4
    Aujourd'hui  : 1. **Grep `NEW`** — strip the marker from every title
                   line it returns. 🔴 **One targeted edit per line** …
                   2. **Grep `^###`** … 3. **Load only the blocks the
                   answers name** … 4. **Edit those blocks in place**
    Après        : 1. **Grep `^###`** — the list of block titles, nothing
                      more
                   2. **Load only the blocks the answers name** by
                      identifier — 🔴 **a ranged read per block**, never
                      the file
                   3. **Edit those blocks in place**, 🔴 **and put `NEW`
                      on the title line of every block you write into** —
                      enriched, split, created, or flagged. Invocation 2
                      closes what carries `NEW`, and strips it.
    Justification: Robustness and tokens. Robustness: `NEW` becomes the
                   one signal of "moved since the last closure", for
                   changed and created blocks alike, so invocation 2 no
                   longer reconstructs the moved set from the questions
                   file (entry 11) — the read the card tolerates only
                   because "a question it has read it cannot unsee"
                   disappears. And the strip moves to the invocation that
                   closes (entry 12), so a closed block never carries
                   `NEW` — "NEW while unclosed", as the verdict's file
                   table defines the marker; today the last turn's blocks
                   keep it after the loop ends and every downstream
                   reader sees closed blocks marked unclosed. Tokens: one
                   grep and one edit per marker fewer at invocation 1.

### 7

    Fichier      : .claude/agents/analyste.md
    Opération    : add text
    Cible        : INVOCATION 1, pass a, right after its four-row table,
                   before "⚠️ **The question's identifier says where the
                   answer applies, not where it lives.**"
    Aujourd'hui  : nothing — nothing says what an entry whose `Answer:`
                   line is empty gets
    Après        : 🔴 **An empty `Answer:` is not an answer, and the
                   `Default:` line above it is not one either** — the
                   chain takes nothing the person did not write.
                   Integrate nothing from it: write the question,
                   verbatim, as a `**Clarification needed:**` line at the
                   end of the block its `Block:` names — which marks that
                   block `NEW` — and mark the entry `[unanswered]`.
                   Invocation 2 asks it again.
    Justification: Robustness, D1 — the verdict adds the Default line and
                   refuses silence as consent; an agent facing an empty
                   answer under a ready-made default, with no rule,
                   files the default — the very decision the verdict
                   forbids. Round trips: the question comes back on the
                   next file instead of vanishing; today it comes back
                   only through the `^Block:` grep that entry 11
                   removes, and for a downstream agent's file (no
                   invocation 2 follows) it never comes back at all.

### 8

    Fichier      : .claude/agents/analyste.md
    Opération    : reorder (move a paragraph, widen its scope)
    Cible        : INVOCATION 1, pass b, the paragraph "⚠️ **If the block
                   carries a `**Clarification needed:**` line on that
                   subject, remove it** — the question is settled."
    Aujourd'hui  : stated under pass b (split) only
    Après        : dropped from pass b; at the end of pass a, after the
                   text entry 7 adds:
                   ⚠️ **Whatever the row, if the block carries a
                   `**Clarification needed:**` line on the answer's
                   subject, remove it** — the question is settled.
    Justification: Round trips — stated under the split pass, the rule
                   reaches less than it should: a flag on a block
                   enriched without a split stays, invocation 2 "collects
                   every `**Clarification needed:**` still in the product
                   file", and the person answers the same question a
                   second time.

### 9

    Fichier      : .claude/agents/analyste.md
    Opération    : add text
    Cible        : INVOCATION 1, pass a, right after "**a. Each answer
                   goes to a block — which one is the question.**",
                   before "🔴 **Before writing it, ask two things of the
                   answer:**"
    Aujourd'hui  : nothing — every answer goes to a block
    Après        : **Of an answer to a downstream agent's question, ask
                   first what invocation 3 asks of a bug line: does it
                   say anything about what the application does?** An
                   answer that does not — it names a library, a storage,
                   a class — is not written into the product file: mark
                   the entry `[not product]` and leave it to the agent
                   that asked.
    Justification: Robustness, D2 — now that the Convertisseur's and the
                   Architecte's answers all come through invocation 1,
                   "each answer goes to a block" forces a purely
                   technical answer into a file that "names things as
                   the user sees them, never by code identifiers", and
                   the Fusionneur carries it into the global. One test
                   per entry, already defined for invocation 3. Unsure
                   how often such answers occur; see *Consequences
                   elsewhere* for what the asker has to do with the mark.

### 10

    Fichier      : .claude/agents/analyste.md
    Opération    : replace text
    Cible        : INVOCATION 1, pass e
    Aujourd'hui  : **e. Mark every entry you integrated** — append
                   `[integrated: B7]` to it in the questions file, naming
                   every block you wrote into. 🔴 **Last, once passes a to
                   d are done** — a block created at pass d has to appear
                   in that mark too.
    Après        : **e. Mark every entry, exactly one mark each** —
                   `[integrated: B7, B12]` naming every block you wrote
                   into, `[unanswered]`, or `[not product]`. 🔴 **Last,
                   once passes a to d are done** — a block created at
                   pass d has to appear in the mark too. 🔴 **No entry
                   stays unmarked**: a file with an unmarked entry is the
                   one the next invocation 1 reads as pending.
    Justification: Robustness — entry 5 tells a consumed file from a
                   pending one by its marks; a file where only the
                   integrated entries carry one is neither. The three
                   marks are the three outcomes entries 7 and 9 create.

### 11

    Fichier      : .claude/agents/analyste.md
    Opération    : replace text
    Cible        : INVOCATION 2, the "Inputs" paragraph and the whole
                   "### Which blocks you close" subsection, from its
                   table down to "📌 **A block no answer touched was
                   closed on an earlier turn.**" — keeping the two
                   paragraphs "⚠️ **A closed block cited by one of yours
                   is read, never closed.** …" and "📌 **You close the
                   product file as it stands, not what was asked about
                   it.**"
    Aujourd'hui  : inputs: the product file · the grid · the global; a
                   branch on "The root holds" (no questions file → every
                   block; one or more → the blocks that moved), the moved
                   set built from a grep of `^Block:` in the
                   highest-numbered questions file plus a grep of `NEW`
    Après        : **Inputs**: the product file · the grid,
                   `docs/process/GRILLE_CADRAGE_PRODUIT.md` · the global
                   — 🔴 **grep its `^#` index, never read it whole**, it
                   runs past 250 KB. ⚠️ **Not the raw idea. Not a
                   questions file — not even by grep.**

                   ### Which blocks you close

                   🔴 **Every block marked `NEW`, and no other.** Grep
                   `NEW` in the product file, load those blocks by a
                   ranged read each, and no others. A block without the
                   marker was closed on an earlier turn. On the first
                   turn every block carries it.

                   (then the two kept paragraphs)
    Justification: Tokens — one grep of the product file replaces a grep
                   of the questions file, a grep of the product file and
                   a branch on the folder's state. Robustness — the
                   questions file leaves this invocation's inputs
                   altogether; the card tolerates its grep only because
                   "a question it has read it cannot unsee", and a grep
                   of `^Block:` lines still lands the block titles of
                   every question in the context that must not have seen
                   them. The moved set no longer depends on which file
                   the orchestration left at the root. Rests on entry 6:
                   every block written into carries `NEW`.

### 12

    Fichier      : .claude/agents/analyste.md
    Opération    : replace text
    Cible        : INVOCATION 2, the paragraph "⚠️ **You do not touch the
                   product file** — answers arrive through invocation 1."
    Aujourd'hui  : that paragraph
    Après        : ⚠️ **You write nothing into the product file** —
                   answers arrive through invocation 1 — 🔴 **except one
                   edit per block you closed: strip `NEW` from its title
                   line once its entries are in the questions file.** A
                   block still marked after your run is one you did not
                   close.
    Justification: Robustness — the marker means unclosed (verdict's file
                   table: "`NEW` while unclosed"); stripping it where the
                   closure happens makes that true at every moment, and a
                   run that dies mid-way leaves exactly the unclosed
                   blocks marked for the next one. Tokens: the block is
                   already loaded here; at invocation 1 it cost a grep
                   and an edit of its own.

### 13

    Fichier      : .claude/agents/analyste.md
    Opération    : replace text
    Cible        : INVOCATION 2, "### The shape of every entry": the line
                   "🔴 **One entry per question, four lines, no
                   exception.** Numbering restarts at Q1 in each file:"
                   and the example under it
    Aujourd'hui  : four lines — `### Q1`, `Block:`, `Question:`,
                   `Answer:`
    Après        : 🔴 **One entry per question, five lines, no
                   exception.** Numbering restarts at Q1 in each file:

                       ### Q1
                       Block: B7 — Rejecting invalid durations
                       Question: what happens to an entry whose duration is zero?
                       Default: an entry whose duration is zero is ignored, like a negative one.
                       Answer:

                   **`Default:` is the statement the chain would take if
                   the question went unanswered** — in the product file's
                   prose, present indicative, one sentence, ready to be
                   filed as it stands, so that agreeing costs the person
                   one word. When the chain would do nothing, the Default
                   says so. 🔴 **It is never taken as the answer**: an
                   empty `Answer:` comes back as a question.

                   **One line opens the file, above Q1**, for the person:
                   *An empty Answer is asked again next turn — to take the
                   Default, write it under Answer.*
    Justification: Round trips, D1 — a question with a proposed answer is
                   read in seconds and answered in a word; the opening
                   line spares the round where she leaves it empty
                   believing silence consents. Robustness: a Default in
                   the product file's prose is filed verbatim by
                   invocation 1, with no rewording between what she
                   agreed to and what the chain builds.

### 14

    Fichier      : .claude/agents/analyste.md
    Opération    : replace text
    Cible        : INVOCATION 2, the paragraph "**Then apply the grid's
                   parts 1, 2 and 5 to every block of the product file**,
                   one block at a time. Then part 4, once, on the
                   feature."
    Aujourd'hui  : that paragraph
    Après        : **Then run the grid on every block you close, one block
                   at a time** — 🔴 **the grid says which of its parts run
                   on a block and which run once on the feature**; you do
                   not restate its dispatch. Part 4 runs whole on the
                   first turn — your file's number is 01 — and on later
                   turns only its two per-instance questions, on the
                   things the blocks you close name.
    Justification: Robustness — two passages asking different things
                   ("every block of the product file" against "only the
                   blocks that moved"); a count that no longer matches
                   (parts 1, 2 and 5, where the grid also routes a
                   trigger-less block to part 3, which the agent never
                   names); and "once, on the feature" reads two ways on a
                   later turn — never again, and a permission a turn-3
                   block introduces is never asked, or every turn, and
                   retroactivity is asked each round. Tokens: the grid's
                   dispatch is stated once, in the grid.

### 15

    Fichier      : .claude/agents/analyste.md
    Opération    : replace text
    Cible        : INVOCATION 2, the "## Questions set aside" example and
                   the line after it "📌 **By category when the whole
                   category is out**, question by question otherwise."
    Aujourd'hui  : - Synchronisation: no block of that nature
                   - Paid access: the feature touches no plan limit
                   … By category when the whole category is out
    Après        :     ## Questions set aside

                       - Personal data: the feature collects none
                       - System permissions: the feature uses none
                       - Retroactivity: no setting changes

                   📌 **One line per part-4 question set aside** — the two
                   per-instance ones, one line per thing they name.
    Justification: Robustness — two readers, two verdicts. The rule three
                   lines above says only part 4's questions can be set
                   aside; the example sets aside a part-2 nature, which
                   the grid never asks of a feature holding no block of
                   that nature ("what it does not generate from the
                   blocks present, it does not ask"), and a "paid access"
                   item that exists in no part. An agent given the
                   example copies the example, and pads the section with
                   categories the grid never raised.

### 16

    Fichier      : .claude/agents/analyste.md
    Opération    : replace text
    Cible        : INVOCATION 3, moves 1 and 2, the lines "**1. Read every
                   `bugfix-*/bug-list.md` of the feature**, oldest folder
                   first." and "**2. On each line, ask: does this say
                   anything about what the application does?**"
    Aujourd'hui  : those two lines
    Après        : **1. Read every `bugfix-*/bug-list.md` in the feature
                   folder**, oldest folder first.
                   **2. On each statement it holds — a line, an entry, a
                   paragraph, whatever the file's layout — ask: does this
                   say anything about what the application does?**
    Justification: Robustness — a file named without a path (the folder
                   is named in the table at the top of the file, never
                   in the move), and a shape assumed: nothing here
                   describes the Diagnostiqueur's file, and a product
                   statement spread over two lines of one entry, read
                   line by line, is two technical fragments and is
                   dropped.

### 17

    Fichier      : .claude/agents/analyste.md
    Opération    : replace text
    Cible        : INVOCATION 3, move 3 whole: from "**3. Integrate what
                   you kept**, by passes a to c …" down to "… rather than
                   answered against a title list."
    Aujourd'hui  : integrate by passes a to c, "the block is found the
                   same way"; a behaviour the product file describes
                   nowhere is a new block marked `NEW`; passes d and e do
                   not apply
    Après        : **3. Integrate what you kept**, by passes a to d of
                   *When you read a questions file*. A bug line names no
                   block: find it on the `^###` title list by the
                   trigger-and-output test, loading a candidate block
                   only to confirm.

                   🔴 **A behaviour no block covers goes through the four
                   moves of *When you read the idea file* — the global's
                   index included**: a corrected behaviour the global
                   already describes takes the global's title, it is not
                   a new one.

                   ⚠️ **Pass e does not apply** — there is no entry to
                   mark. Every block you write into carries `NEW`, as at
                   invocation 1.
    Justification: Robustness — "the block is found the same way" points
                   at a step that loads "the blocks the answers name by
                   identifier", and a bug line carries none: the agent
                   has to guess how. And the current text sends every
                   uncovered behaviour to a new block without asking the
                   global, where the correction of an existing behaviour
                   lands under a second title the Fusionneur cannot
                   merge — a move that searches one folder where two
                   carry the thing. Pass d is what decides "no block
                   covers it"; saying it does not apply contradicts the
                   next sentence.

### 18

    Fichier      : .claude/agents/analyste.md
    Opération    : replace text
    Cible        : INVOCATION 3, the "Output" paragraph: "**Output**: the
                   product file, and `questions-analyste-NN.md` — 🔴
                   **written even when empty**, since its presence is
                   what says this pass has run."
    Aujourd'hui  : that paragraph
    Après        : **Output**: the product file, with `NEW` on every block
                   you wrote into. Invocation 2 follows, as after any
                   invocation 1, and its questions file — written even
                   when empty — is what says this pass has run.
    Justification: Robustness — today a block this invocation creates is
                   marked `NEW` and nothing closes it: the questions file
                   it writes holds no closure (it runs no grid, and could
                   not in a context that has read the bug lists), so a
                   behaviour a correction settled enters the product file
                   without ever meeting the grid, and the marker stays.
                   Tokens: a file that carried nothing is no longer
                   written. Needs the command to chain invocation 2 — see
                   *Consequences elsewhere*.

### 19

    Fichier      : .claude/agents/analyste.md
    Opération    : replace text
    Cible        : section "How you write", the paragraph "🔴 **Every
                   block you create carries `NEW` on its title line** —
                   from the idea file, from a split, from a subject no
                   block covered:" and, after the example, "📌
                   **Invocation 2 greps it** to know which blocks to
                   close. **You strip every `NEW` before writing**, so
                   only this turn's are marked."
    Aujourd'hui  : `NEW` marks created blocks; invocation 1 strips it
    Après        : 🔴 **Every block you write into carries `NEW` on its
                   title line** — created from the idea file, from a
                   split, from a subject no block covered, or an existing
                   block enriched, split or flagged:
                   (example unchanged)
                   📌 **Invocation 2 greps it** to know which blocks to
                   close, **and strips it once the block is closed. You
                   never strip it.**
    Justification: Robustness — the rule of entries 6 and 12, stated
                   where the file's conventions live; left as is, two
                   passages of one agent ask different things about who
                   strips the marker and what it marks.

### 20

    Fichier      : .claude/agents/analyste.md
    Opération    : replace text
    Cible        : section "Which invocation is this?", the table, rows 2
                   and 3
    Aujourd'hui  : | 2 | Grid | The product file · the grid · the global ·
                   **the latest questions file, grepped only** | The next
                   questions file |
                   | 3 | Bug-fix decisions | Every `bugfix-*/bug-list.md`
                   · the product file · the global | The product file,
                   plus a questions file |
    Après        : | 2 | Grid | The product file · the grid · the global |
                   The next questions file |
                   | 3 | Bug-fix decisions | Every `bugfix-*/bug-list.md`
                   · the product file · the global | The product file |
    Justification: Robustness — a summary that no longer matches the body
                   after entries 11 and 18; the table is the first thing
                   the agent reads and the one it loads its inputs from.

### 21

    Fichier      : .claude/agents/analyste.md
    Opération    : replace text
    Cible        : section "What you never do", three entries, plus one
                   added
    Aujourd'hui  : - 🔴 **`Read` a questions file** — grep it, at
                   invocation 2
                   - 🔴 **Close a block no answer touched and no `NEW`
                   marks** — it was closed on an earlier turn
                   - 🔴 **Create a block without `NEW`** — invocation 2
                   would never close it
    Après        : - 🔴 **Open a questions file at invocation 2**, by
                   `Read` or by grep — invocation 1 alone reads them
                   - 🔴 **Close a block not marked `NEW`** — it was closed
                   on an earlier turn
                   - 🔴 **Write into a block without marking it `NEW`** —
                   invocation 2 would never close it
                   - 🔴 **Take an empty `Answer:`, or the `Default:` line,
                   as an answer**
    Justification: Robustness — a forbidden thing matching no rule, three
                   times over once entries 6, 7 and 11 are applied; two
                   readers take two actions when the list and the body
                   disagree. The fourth entry mirrors the D1 rule of
                   entry 7.

---

## Consequences elsewhere

Convertisseur, Architecte, and any agent that writes a
`questions-<agent>-NN.md` : after the Analyste's invocation 1 every
entry of their file carries one mark. `[integrated: Bn]` — the answer is
in the product file, block Bn, and is read from there (D2). `[not
product]` — the answer was not written into the product file; the asker
reads it from the entry itself (entry 9; unsure whether such answers
occur — if they never do, entry 9 is one test paid for nothing).
`[unanswered]` — no invocation 2 follows a downstream file, so nobody
re-asks it: the asker's next file has to, or the question is lost. The
Analyste reads only `Block:` and `Answer:` from their entries; whether
their entries carry a `Default:` line (D1) is their own pass's matter.

The command that runs the cycle (and whatever runs invocation 3) : (a)
after invocation 3, run invocation 2 and the loop with the person
exactly as after an invocation 1 — invocation 3 no longer writes a
questions file, and the blocks it marks `NEW` are closed by nothing
else (entry 18). (b) Leave at most one unconsumed questions file at the
feature root; the Analyste blocks on two (entry 5). (c) The loop with
the person has no ceiling and cannot have one inside the agent —
invocation 2 may not look at past questions, so it cannot count how
often one was asked; if a bound is wanted, the command holds it. (d) A
first-turn closure loads every block of the feature in one invocation,
with no bound on their number and nothing signalling an overflow; if a
feature ever exceeds one context, the command splits the closure by
domain — the agent cannot know it is too large.

Diagnostiqueur : nothing required — the Analyste reads `bug-list.md`
statement by statement whatever its layout (entry 16). If the file ever
marks which entries settle a product behaviour, the Analyste's test at
invocation 3 becomes a grep.

Fusionneur : the product file it merges carries `NEW` on no block once
the loop has ended (entries 6, 12) — today the last turn's blocks keep
it. Nothing to change unless it reads the marker.

The product grid (`docs/process/GRILLE_CADRAGE_PRODUIT.md`) : no fault
found. The agent now refers to the grid's own dispatch (which parts run
per block, which once) instead of restating it (entry 14); a later
change to that dispatch needs no change in the agent.

The verdict card 4.1 : its sentence "it may only grep the questions
file" no longer describes invocation 2, which opens none (entry 11).
