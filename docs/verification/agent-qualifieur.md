# Verification — `qualifieur.md`

**Inputs read**

| Input | State |
|---|---|
| `.claude/agents/qualifieur.md` (old) | **Does not exist** — the agent is new (🆕 in `modifications.md`) |
| `.claude-new/agents/qualifieur.md` (new) | Read whole — 276 lines; every line number below refers to it |
| `docs/refonte/passes/qualifieur.md` | **Does not exist** — no pass file, no defect analysis |
| `docs/refonte/modifications.md` § `# 🆕 qualifieur.md` | Lines 42–142: change table, two rules added while writing, and *La demande* |

Also opened, to settle points the agent file alone cannot: `.claude-new/commands/3a_genre.md` (its command), `.claude-new/agents/classeur.md` (the form it was written on), and the `Genre:` greps in `3b_nature.md`, `4_grille.md`, `5_reclasse.md`, `redacteur.md`, `decoupeur.md`.

**Section A is skipped** — nothing was PASSÉ, ÉCARTÉ or REPORTÉ: there is no pass sheet. In its place, section A′ holds the new file against *La demande*, the only spec that exists for it.

**Severity summary** — 2 BLOCKING · 8 TO FIX · 9 NOTE.

---

## A′. CONFORMITY TO *LA DEMANDE*

One row per point of the spec. "Found" cites the new file.

| # | La demande | Found in the new file | Verdict |
|---|---|---|---|
| A1 | `/3a_genre`, between `/3_decoupe` and `/3b_nature` | l.3 "after the decoupeur and before the classeur"; command file exists | Conforms |
| A2 | Poses a `Genre:` line on every block, nothing else | l.10–11, l.28, l.261 "In the product file, the `Genre:` line, and nothing else" | Conforms |
| A3 | Why before the Classeur: only a `comportement` has a nature | l.58–59 | Conforms |
| A4 | Why after the Découpeur: a block then carries one subject, hence **one genre** | **Absent.** Nothing in the file says one genre per block, and no branch handles a block whose sentences call for two genres (see D5) | **Not carried** |
| A5 | The six genres, table | l.49–56 — same six, same definitions | Conforms |
| A6 | The `transverse` test and its three examples | l.62–72 — same test, same three examples | Conforms |
| A7 | A transverse-looking section holds more than transverse rules | l.74–76 | Conforms |
| A8 | Doubt 1 « Est-ce transverse ? » → `comportement`, **no question** | l.106 broadens it to "**Which genre?** In doubt, `comportement`" **and** l.114 adds "You still raise it as a question" | **Departs** — see B2 |
| A9 | Doubt 2 (reach unsaid) → a mandatory question | l.117–119 | Conforms |
| A10 | The asymmetry written into the agent | l.108–112 | Conforms |
| A11 | Doubt 2 not settled by the asymmetry; the answer rewords, does not change the product | l.117–123 | Conforms |
| A12 | Questions file written every pass, even empty | l.147–148 | Conforms |
| A13 | Added rule: the reason for a directive is not a second directive | l.82–84 | Conforms |
| A14 | Added rule: a refused behaviour is not `hors périmètre` | l.91–93 | Conforms |

---

## B. UNANNOUNCED CHANGES

No old version exists, so "diff" here means: what the new file contains that neither *La demande* nor the two announced rules ask for. Material inherited verbatim from the Classeur's form (paths, questions-file mechanics, answered-questions table, blocking-file shape, PART 2) is covered by "sur la forme du Classeur" and is not listed — except where the form was **not** carried over and the omission matters.

### B1 — l.78–99 — the operative definitions of the five non-behaviour genres — NOTE

> `directive` — it imposes a means … It has no trigger and produces nothing.
> `référence` … It has no trigger either — it is read, not run.
> `recette` … It asks nothing of the code.
> `comportement` — the common case. A trigger and something produced.

Not in *La demande*, which defines the genres by their table row only. These sentences are what PART 3 actually runs on (trigger/output). They are the substance of the agent, and they are what produces the contradiction in D1 — so they are recorded here as the place the change entered.

### B2 — l.103–115 — doubt 1 both defaults **and** asks — TO FIX

*La demande*: « "Est-ce transverse ?" → Dans le doute, `comportement` » ; only doubt 2 gets « Une question obligatoire ». The asymmetry argument — « une règle mal classée en `comportement` coûte une question de trop » — means the grid's question is the whole cost of the default, i.e. the qualifieur itself asks nothing.

New file, l.103: "At the least doubt, a question — never a choice made in silence." · l.106: "**1. Which genre?** In doubt, `comportement`." · l.114: "You still raise it as a question, and the line says `comportement` meanwhile."

What it changes: every doubt-1 block now yields a question, and the command routes any question to `/1_lexique` ("Its questions file holds questions → Answer them, then `/1_lexique`"). The spec's default was designed to avoid exactly that loop. Two readings of the spec are possible (the asymmetry as *reason not to ask* vs. *reason for the placeholder*); the file chose the second without the section saying so. **Question for the Product Owner: is doubt 1 meant to produce a question, or only the default?**

### B3 — l.106 — doubt 1 widened from "transverse?" to "which genre?" — NOTE

Spec: the first doubt is « Est-ce transverse ? ». File: "Which genre?" — any pair of genres. The asymmetry holds for any genre other than `comportement` (any of them leaves the grid's file), so the widening is consistent with the reasoning. Recording it because *La demande* did not.

### B4 — l.181–182 — "Judge whether a directive is right" — NOTE

> 🔴 **Judge whether a directive is right** — 📌 **the Product Owner settled it; you say it is one**

Not in the spec. Sensible; no consequence.

### B5 — l.256–257 — "a block that did was probed as something it is not" — NOTE

> 🔴 **a block that did was probed as something it is not**, and its marker sends it back.

Copied from the Classeur, where every block *was* probed. Here it is true only for a block that was `comportement` before; a `directive` that becomes `comportement` was never probed at all — its marker still sends it on, so the instruction holds, but the reason given is wrong for half the cases.

### B6 — form of the Classeur **not** carried: "How a block is delimited" — TO FIX

The Classeur (its l.36–44) tells the agent how to find and bound a block: heading to next heading, marker on the heading line, `Genre:`/`Nature:` directly under, and "Grep `^### B7 ` — the space ends the number" because "a grep on `B7` also hits `B70`". The qualifieur says "load those, and no others" (l.42) and nothing about **how**. With the same tools and the same file, the `B7`/`B70` trap is unguarded here.

### B7 — form of the Classeur **not** carried: "The form of the line you write" — TO FIX

The Classeur (its l.46–54) fixes the line: `Nature: ` + the name "spelled exactly as the table spells it, lower case, nothing else on the line", and says why: the next commands grep it. The qualifieur never says how `Genre:` must be spelled. Downstream: `/3b_nature` keeps only `Genre: comportement`; `/4_grille` greps `^Genre: comportement$`; `/5_reclasse` greps `^Genre: <genre>$` and "A `Genre:` value that is not one of the six — say which block, and stop". Two of the six values carry accents and one a space (`référence`, `hors périmètre`). A `Genre: Comportement`, `Genre: behaviour` or `Genre: hors-perimetre` passes `/3a_genre`'s only check (`^Genre:$` count is zero), is silently dropped by `/3b_nature` and `/4_grille`, and stops `/5_reclasse` two commands later. That is the file's own "silent hole" (l.110–112), produced by a spelling it never forbids.

### B8 — form of the Classeur **not** carried: the three shapes of a `## Decision` — TO FIX

The Classeur (its l.190–200) says what to do with a filled decision: a nature among the eight → write it; a rewrite → leave the line empty and say so; a value outside the eight → leave it empty, "you never invent the ninth value". The qualifieur, l.215–216: "it says what was settled, and you resume with it" — and nothing else. Yet its command relays three distinct outcomes ("A `## Decision` names a rewrite", "names a genre outside the list", "naming a genre it could not settle"), so the orchestrator expects the agent to have distinguished them. See D6.

### B9 — form of the Classeur **not** carried: "A block that blocks does not stop the run" — TO FIX

The Classeur (its l.180–188): one block blocking does not stop the others; several blocked blocks share one file with one `## Where` each; name the blocked blocks in the report "otherwise an empty line reads as one you forgot". The qualifieur has none of it. Its command, after the run, counts `^Genre:$` and treats a non-zero count "no blocking file explains" as a defect — which presumes the agent finished the other blocks and left only the blocked one empty. The agent is never told to.

### B10 — l.269–275 — no per-block genre list in the report — NOTE

The Classeur reports "per block, the nature you gave it — one line each" because "nothing downstream catches a wrong nature". The qualifieur reports counts and asked identifiers only. Consistent with its command ("A wrong genre is caught by what follows"), so a design choice, not a defect — but the claim that a wrong genre is caught downstream is only true in one direction: a behaviour wrongly filed as `directive` is exactly what l.110–112 says nobody catches. Recorded as a question: should the report list the genre per block, for the same reason the Classeur does?

---

## C. GESTURES AGAINST TOOLS

Frontmatter, l.4: `tools: Read, Grep, Glob, Edit, Write`. No `Bash`, no `Agent` — right: git is the command's, and the agent calls nobody.

| Gesture | Where | Tool | Verdict |
|---|---|---|---|
| Read the named blocks of the product file | l.36–42, l.237 | Read (+ Grep to locate — see C1) | Has the means |
| Write the `Genre:` line in place | l.261 | Edit | Has the means |
| Write `questions-qualifieur-NN.md` | l.128, l.147 | Write | Has the means |
| Number it: "the highest … found in the root and in `questions/qualifieur/` together" | l.129–131 | Glob | Has the means — the only gesture that needs Glob |
| Read the answered questions file the prompt names | l.153–157 | Read | Has the means |
| Read a blocking file whose decision is filled | l.215–216 | Read | Has the means |
| Write `blocked_qualifieur.md` | l.188 | Write | Has the means |
| Report | l.269–275 | none needed | — |

### C1 — Grep: a tool no stated gesture uses — NOTE

No line of the file tells the agent to grep anything; l.228 even says "the orchestrator grepped, you do not grep again". The only implicit use is locating a block by heading in a file it must not read whole (l.41–42) — and that gesture is unstated (B6). Either state it (as the Classeur does, with the `^### B7 ` form) or Grep is a tool with no gesture. Same remark for Glob: it is needed (numbering) but the file never says "glob".

No gesture without a tool was found.

---

## D. INTERNAL COHERENCE (new file alone)

### D1 — l.239 against l.62–72 — the procedure cannot yield `transverse` for the file's own examples — BLOCKING

l.239–240: "**2.** 🔴 **A trigger and something produced → `comportement`.** 📌 **The common case, and you are done.**"

l.70: "*An absent value shows as a dash* | Subject: **an absent value** — a category. `transverse`"

"An absent value shows as a dash" has a trigger (a value is absent) and an output (a dash). Step 2 fires, the genre is `comportement`, "you are done" — step 3, the only place `transverse` is reachable ("a rule over a category"), is never entered. The same holds for l.53's definition ("A rule whose subject is a category") — most such rules describe a trigger and an output. The trigger/output criterion of PART 3 and the subject criterion of *The test for transverse* are two different tests, and PART 3 orders them so that the second never runs on the cases it was written for.

`recette` has the same problem: a walk-through (l.96 "a walk-through, a thing to look at") is typically "tap X, see Y" — trigger and output — and step 2 calls it `comportement`.

### D2 — l.239–244 — two branches missing: trigger without output, output without trigger — TO FIX

Step 2 covers "a trigger **and** something produced"; step 3 covers "**Neither** trigger nor output". A block with one and not the other — "The timer is shown in large digits" (output, no trigger); "When the app is backgrounded…" with the outcome elsewhere (trigger, no output) — matches neither branch. Step 4 ("Any doubt — two genres…") is not routed from there. A procedure branch that leads nowhere.

### D3 — l.103 against l.108–115 — the asymmetry argues for a silent default, then the default is not silent — NOTE

l.103: "never a choice made in silence". l.108–112 explain why `comportement` is the safe *choice* ("costs one question too many" — the grid's). l.114 then says the agent asks anyway. The three lines are not contradictory once read together, but l.108–112 no longer justify anything the agent does: if a question is raised in every case, the cost comparison between the two errors decides only what the placeholder says. Tied to B2.

### D4 — l.109 and l.114 — "question" in two senses, three lines apart — NOTE

l.109: "costs one question too many — the grid probes it and finds nothing to ask" (a **sondeur's** question). l.114: "You still raise it as a question" (the **qualifieur's**). A reader can take l.109 as "one qualifieur question too many" and conclude the opposite of what is meant.

### D5 — no branch for a block holding two genres — TO FIX

*La demande* rests on "un bloc porte alors un seul sujet, donc un seul genre" — but the decoupeur splits on **triggers**, not on genre, and a block carrying one trigger plus a sentence of another genre ("The timer shows elapsed seconds. Digits are Roboto Mono.") reaches the qualifieur whole. The file's doubt 1 (l.106) is about *which* genre for one passage, not about a block that is two passages; l.176 forbids splitting; l.274–275 forbids "judgement on the split". Nowhere does the block go. The Classeur has the matching case ("Two of its sentences produce two different things → a question: whether the Rédacteur splits it"); the qualifieur has none. Note that l.82–84 handles one sub-case (the reason for a directive) and shows the case is real.

### D6 — l.215–216 — a decision the agent cannot act on leads nowhere — TO FIX

> 📌 **A blocking file the prompt names carries a filled `## Decision`** — 🔴 **it says what was settled, and you resume with it.**

"Resume with it" when the decision is a **rewrite**: the agent may not touch text (l.174) and has no instruction to leave the line empty and say so. When the decision names a **seventh genre**: "resume with it" reads as *write it*, and the file has no rule against a value outside the six — l.212–213 even invites the blocking file to propose one ("it is how the list learns"), so a seventh value coming back as a decision is the expected path. Written, it passes `^Genre:$` and stops `/5_reclasse`. The Classeur guards both cases explicitly; here both branches end in the same sentence. (See B8.)

### D7 — l.188 against the `^Genre:$` check — a blocked block's line: empty, or what? — TO FIX

l.211–213: "You block when no genre fits at all — say what the block holds, in the blocking file." Nothing says what the `Genre:` line of that block carries meanwhile, nor whether the other named blocks are still processed. Read with l.147 ("Write the file even when empty"), l.265 ("your questions file, always") and the report of l.269, the natural reading is that the run stops — and then the questions file, "always" written, is written or not. The command, on its side, expects the count of empty lines to be explained by the blocking file, i.e. the others done. (See B9.)

### D8 — l.250–254 — a genre change leaves the `Nature:` line behind — NOTE (question)

"A different one, and you write it." A `comportement` carrying `Nature: presentation` that becomes `directive` keeps its `Nature: presentation`: the qualifieur writes one line and nothing else (l.261), and nobody downstream is told to clear it. Is a non-`comportement` block carrying a filled `Nature:` harmless (`/5_reclasse` only requires that behaviours have one), or should this file say the line is to be emptied — and by whom? Cannot be settled from this file.

### D9 — l.3 against l.147 — the description understates the questions file — NOTE

l.3: "and a questions file when a genre is in doubt". l.147: "Write the file even when empty". The frontmatter description says the file is conditional; the body says it is unconditional and that "a missing one says you did not run". The description is what the orchestrator sees when it routes.

### D10 — l.56 — "himself" — NOTE

> `recette` | What the Product Owner wants to check on the device himself

`CLAUDE.md` refers to the Product Owner as "She" throughout. Carried from *La demande*'s « lui-même ».

### D11 — counts checked — no mismatch

"The six genres" (l.44) → six rows (l.51–56). "The other five" (l.78) → five paragraphs (l.80–99). Step 3's five descriptors (l.243–244) → five non-behaviour genres. "Two doubts" (l.104) → two (l.106, l.117). "four lines" (l.134) → four (l.137–140). "four headings" (l.191) → four (l.193–207). Section references "see *Your questions*" (l.212, l.265) → section exists (l.101). "take the genre from the table" (l.242) → the table of l.49; unambiguous since the transverse table (l.68) carries no genre column.

---

## What to settle first

1. **D1** — decide which test decides: *subject* (category vs. object) or *trigger/output*, and order PART 3 so `transverse` and `recette` are reachable. Until then the agent qualifies every transverse rule the spec lists as `comportement`, and the "silent hole" runs the other way: the grid probes rules that have no block to belong to.
2. **B7** — state the spelling of the line. Cheapest fix, largest downstream reach.
3. **B8 / D6 / D7 / B9** — carry the Classeur's blocking rules over: blocked block does not stop the run, one `## Where` per block, three shapes of a decision, never a seventh value.
4. **B2** — one question for the Product Owner: does doubt 1 ask, or only default?
5. **D5** — a branch for a block holding two genres, or a statement that it cannot happen and why.
