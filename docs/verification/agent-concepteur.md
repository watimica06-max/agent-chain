# agent-concepteur — verification

**Read**: `.claude/agents/concepteur.md` — **does not exist** (the agent is new: `# 🆕
\`concepteur.md\``) · `.claude-new/agents/concepteur.md` (new, 202 lines) ·
`docs/refonte/passes/concepteur.md` — **does not exist** (no pass sheet, as announced) ·
`docs/refonte/modifications.md` § `` # 🆕 `concepteur.md` `` (lines 844–888).

**What the section says**: no "Sa fiche de passe", no PASSÉ / ÉCARTÉ / REPORTÉ. Two things
instead: a table "Ce qu'il porte" (six rows: gesture, what it proves, what it reads, what it
never does, one rule *added while writing* — an empty body throws *not implemented* and never
returns a default —, its report) and "La demande" (per lot, before the Testeur and the
Codeur: name the symbols, write the interface files with empty bodies, compile, commit; plus
the rationale *why him and not the Détailleur*).

Since there is neither an old file nor a pass sheet, **section A verifies the new file against
"La demande" and the table**, and **section B lists what the new file carries that neither
announces** (there is no old text to diff, so "unannounced" means: not in the section). C and
D are given full attention. Line numbers are those of the **new** file unless marked *cmd*
(`.claude-new/commands/8_code.md`), *det* (`.claude-new/agents/detailleur.md`), *cad*
(`.claude-new/agents/cadreur.md`), *rea* (`.claude-new/agents/realisateur.md`), *conv*
(`docs/TECHNICAL_CONVENTIONS.md`).

Cross-file facts used below, all read from `.claude-new/` unless stated:

- The concepteur is invoked by `8_code` with the prompt *"Working folder: <…>. Your lot:
  <lot>."* and nothing else (cmd 206–211); `8_code` says a filled `## Decision` is not a stop —
  *"invoke the agent it names on the lot it names, and let it apply the decision"* (cmd 342–345).
- The Détailleur's sheet has **five fields**: `## Signatures`, `## Acceptance criteria`,
  `## Dependencies` (with *pre-existing* / *produced by lot-NN*), `## Conventions`,
  `## Requests` (det 229–258, 625–628). **No field names a file.**
- `Modifies` and `Touches` are fields of a **lot in the split** (`code/decoupage.md`, cad
  708–724): *"`Needs`, `Produces` and `Modifies` carry symbols, and symbols only … never a
  file"*; *"`Touches` carries the files a lot has to open that declare no symbol of its own"*.
- The Réalisateur finds files by grep (*"grep each of those names to find its file"*, rea
  502–503), scopes its `Bash` to `git add`, `commit`, `status`, `git mv`, `git restore` and the
  commands the conventions name (rea 570–575), and never leaves a dirty working tree (rea 401).
- `8_code` refuses to force-remove a worktree with uncommitted files — *"an agent handed back
  leaving work uncommitted is a fault of that agent"* (cmd 390–393) — and merges *"before
  handing back, always — including a `blocked_*.md`"* (cmd 402).
- `docs/TECHNICAL_CONVENTIONS.md` as it stands carries **no `permanente` marker** (0 hits); the
  marker is introduced by the new architecte (architecte 116–124). The only commands the
  conventions name are `./gradlew check` (R4, conv 30) and `./gradlew :<module>:check` (R72,
  conv 42); no compile-only task.
- The PO's own check recorded at modifications.md 1046–1052: the concepteur used to read a
  `## Symbols` section *"qui n'existe pas — le champ s'appelle `## Signatures`. Corrigé dans
  les deux agents neufs."* — the same class of defect as **A-5 / D-3** below, one occurrence of
  which survived.

---

## A. Conformity

No pass sheet: nothing listed PASSÉ, ÉCARTÉ or REPORTÉ. The table and "La demande" are the
only spec; each row is checked against the new file.

| # | Expected (table / La demande) | Found | Verdict |
|---|---|---|---|
| A-1 — gesture | *"Il écrit les déclarations de la fiche avec des corps vides, et il compile — puis il commite"*; demande: *"il nomme les symboles ; il écrit les fichiers d'interface avec des corps vides ; il compile ; il commite"* | Role 14–15; moves 3 (144), 4 (158), 5 (170). **"Il nomme les symboles"** is not taken literally: 146–148 *"Exactly the signature the sheet gives — name for name"* and 77–78 *"Change a signature the sheet gives … is not yours to improve"*. The Détailleur names, the concepteur copies. | **Conforming** — the table's stricter reading (*"aucune signature modifiée"*) wins over the demande's verb; consistent with modifications.md 1047–1049 (*"ils consomment les signatures … ils ne les produisent pas"*) |
| A-2 — what it proves | *"La signature tient dans le langage — aujourd'hui elle vit en prose, et une signature impossible est découverte par le Réalisateur"* | 20–27, near-verbatim. | **Conforming** — but see **D-9**: the "today" is the demande's, not the agent's |
| A-3 — what it reads | *"La fiche, les conventions `permanente` en entier, et les fichiers que la fiche déclare"* | 53–60: the sheet (`## Signatures`, `## Dependencies`), the `permanente` rules *"and those the sheet names"*, *"the files the sheet says you touch, and the ones holding the symbols it needs"*. 62–63 closes the list. | **Conforming, with two additions** the table does not announce (the sheet's own `## Conventions`, and the files holding the needed symbols) — both reasonable; see **B-2**. ⚠️ *"the files the sheet says you touch"* has no referent in the sheet — see **A-5 / D-3** |
| A-4 — what it never does | *"Aucun corps, aucun test, aucune signature modifiée — une signature qu'il ne peut pas écrire est un blocage"* | 74–78 (body, test, signature); 78 *"a signature you cannot write is a block"*; 111–113 the block cases. | **Conforming** |
| A-5 — added while writing | *"Un corps vide lève *not implemented*, il ne retourne pas une valeur par défaut — sinon le test rouge du Testeur pourrait passer dessus"* | 17–18 *"A body is empty, or throws the language's not implemented — nothing else"*; 150–153 *"Whichever the conventions prescribe — and if they prescribe neither, throw: an empty body that returns a default is a body the testeur's red test could pass on"*; 74–75 *"not a default value that stands in for one"*. | **Partially conforming.** The table says the body **throws**, full stop. The file lets the conventions choose *empty* over *throw* and only defaults to throw. The rationale given (a red test could pass on it) argues against exactly the option the file keeps open — see **D-8** |
| A-6 — report | `code/<lot>/conception.md` — *"les symboles et leur fichier, la compilation, les fichiers touchés hors fiche"* | 176–192: `## Declared` (symbol + file), `## Compile` (command + outcome), `## Placements not settled by the conventions`, `## Outside the lot`. | **Conforming, plus one field** (`## Placements not settled by the conventions`) the table does not announce — see **B-3**. ⚠️ `## Outside the lot` contradicts the rule at 82–83 — see **D-2** |
| A-7 — position | *"Par lot, avant le Testeur et le Codeur"* | Line 3 and 29: *"once per lot, before the testeur and the realisateur"*. Matches cmd 81–86 (concepteur → testeur → realisateur). | **Conforming** — "Codeur" in the demande is the realisateur; no agent named *codeur* exists in `.claude-new/agents/` |
| A-8 — "20 agents dans la chaîne" | | `.claude-new/agents/` holds 20 files; new `CLAUDE.md` lists 10 upstream + 8 downstream + arbitre + architecte = 20. | **Conforming** |

Nothing listed ÉCARTÉ or REPORTÉ.

---

## B. Unannounced changes

No old file, so no diff. What follows is what the new file carries beyond the table and "La
demande". None of it contradicts the section; all of it is un-announced.

| # | Line | In the file | Not in the section | Severity |
|---|---|---|---|---|
| B-1 | 88–119 | A full blocking protocol: `code/<lot>/blocked_concepteur.md`, four-heading shape, the four block cases (111–113), *not on a signature you find odd* (115–116), the filled-`## Decision` re-entry (118–119). | The section only says *"une signature qu'il ne peut pas écrire est un blocage"*. The shape is the chain's standard one (identical to det 264–283) and `8_code` already counts it among *"the five agents of the loop"* (cmd 316). | **NOTE** — consistent with the chain |
| B-2 | 57–60 | Reads the sheet's `## Conventions` (*"and those the sheet names"*) and *"the ones holding the symbols it needs"*. | Table: *"La fiche, les conventions `permanente` en entier, et les fichiers que la fiche déclare"*. Two extra inputs. | **NOTE** — both are needed to compile (a *pre-existing* type has to be imported from somewhere) |
| B-3 | 136–142, 186–188 | Move 2, *"Work out where each declaration goes — from the conventions, never from taste"*, with a fallback (*"put it where the sheet's `Modifies` or `Touches` points, and say so in your report"*) and a matching report field `## Placements not settled by the conventions`. | The section's gesture list has no placement step and the report has three items, not four. | **NOTE** on the addition itself — but the fallback is broken, see **D-3** |
| B-4 | 41–42, 31–39 | *"The orchestration names your lot in the prompt"*; the three path bases (relative; `docs/` = repo root; `code/<lot>/` = working folder). | Not in the section; matches the `8_code` template (cmd 206–211) and the sibling agents. | **NOTE** |
| B-5 | 65–68, 130–134 | *"The permanent rules are the most important thing you read — more than the sheet's own conventions list"*; the *pre-existing* / *produced by* reading of `## Dependencies`. | Not in the section. The first is lifted from rea 66–70; the second matches det 625–628 exactly. | **NOTE** |
| B-6 | 194–198 | *"`## Compile` says the command and its outcome — it is what the next agents take as given, and neither compiles again before writing"*; *"`## Outside the lot` is a dash or a list — never omitted"*. | Not in the section. The testeur does read *"that the module compiles"* from `conception.md` (testeur 61–62), so the contract exists on the other side. | **NOTE** |
| B-7 | 1–6 | Frontmatter: `tools: Read, Grep, Glob, Edit, Write, Bash`, `model: sonnet`, **no `effort`**. | The section says nothing on frontmatter. New `CLAUDE.md` 87–88: *"Every agent carries its own `model` and `effort` in its frontmatter"*; `realisateur.md`, `relecteur.md`, `detailleur.md` carry one, `concepteur.md` and `testeur.md` do not. | **NOTE** — question for the author: is `effort` meant to be present on every new agent? |

---

## C. Gestures against tools

**Frontmatter tools** (line 4): `Read, Grep, Glob, Edit, Write, Bash`.

### Gestures and their means

| Gesture | Where | Tool | Verdict |
|---|---|---|---|
| Read the sheet (`## Signatures`, `## Dependencies`, `## Conventions`), the conventions, the files it touches and the ones holding the needed symbols | 53–60, 127–134 | Read | has the means |
| Find *"the ones holding the symbols it needs"* — a *pre-existing* type, a symbol *produced by* an earlier lot, the file a convention places a kind of symbol in | 59–60, 130–132 | Grep (+ Glob) | has the means — ⚠️ **never named**: the file says *read* everywhere and never says *grep*; the sibling realisateur spells it out (rea 502–503). Left to the agent's initiative |
| Detect *"two symbols the sheet names identically"* and a name that already exists in the code | 113 | Grep | has the means, same remark |
| Write the declarations into existing files | 144–156 | Edit | has the means |
| Create a new file when the conventions place a symbol in a file that does not exist yet | 136–142 | Write | has the means |
| Write `code/<lot>/conception.md`, `code/<lot>/blocked_concepteur.md` | 176, 90 | Write | has the means |
| **Compile** *"by the command the conventions name"* | 158–159 | Bash | has the means — but see **D-12**: the conventions name `./gradlew check` / `:<module>:check`, not a compile task |
| Fix a non-signature compile error (import, package line) and compile again | 164–165 | Edit + Bash | has the means |
| **Commit**, *"staging explicitly what belongs to the lot"* | 170 | Bash (`git add`, `git commit`) | has the means |
| Apply a filled `## Decision` the prompt names | 118–119 | Read + the above | has the means — **if the prompt names it**; the `8_code` template does not, see **D-6** |
| Undo what it wrote when it blocks (so as not to leave a dirty worktree) | — **no such gesture exists**, see **D-4** | would be Bash (`git restore`) or Edit | the tool is there, the instruction is not |

No gesture lacks a tool.

### Tools no gesture uses

- **`Glob`** — no gesture names it and none needs it in so many words. The file names files
  directly (sheet, conventions, report, blocking file) and finds symbols by content; Glob is at
  most a helper for Grep. **NOTE**, harmless.
- **`Bash` is unbounded.** Two gestures use it (compile, commit). Unlike the realisateur (rea
  387–389, 570–575: *"`git add`, `commit`, `status`, `git mv`, `git restore`, and the analysis
  and test commands the conventions name. Nothing else at all"*), the concepteur has **no
  scope rule** on its shell: nothing forbids a shell search, a wait, a merge, a branch, a
  worktree operation, a `git push`. The same model, the same worktree, no fence. **TO FIX** —
  a one-line copy of the realisateur's rule.

---

## D. Internal coherence (new file alone)

| # | Line | Quote | Finding | Severity |
|---|---|---|---|---|
| D-1 | 125 vs 127–170 | *"**Four moves, in this order.**"* — then **1.** (127), **2.** (136), **3.** (144), **4.** (158), **5.** (170) | Announced count does not match: five moves, not four. (The demande lists four bullets — the placement step was added while writing and the count was not updated.) | **TO FIX** |
| D-2 | 82–83 vs 190–192, 198 | 82: *"🔴 **Touch a file the sheet does not declare** — 📌 **say so and block instead**"* · 190–192: *"## Outside the lot — <every file you touched that the sheet does not declare, or a dash>"* · 198: *"`## Outside the lot` is a dash or a list — never omitted"* | A rule contradicted elsewhere in the file. Under 82 the field can never legitimately hold anything but a dash — an entry in it is a confession of a rule broken. The realisateur, which has the same field, carries the exception that makes it meaningful (rea 165–166: *"A decision authorised it, or you could not compile without it"*); the concepteur has the field without the exception. Which one is meant? Either 82 gets the realisateur's exception (a missing import in a build file, a manifest entry a declaration needs — cases 164–165 already ask it to fix) or the field goes. | **TO FIX** |
| D-3 | 137–142 (also 59, 82, 192) | 137–138: *"📌 **The sheet says which files the lot touches**"* · 140–142: *"A symbol whose file the conventions do not settle — 📌 **put it where the sheet's `Modifies` or `Touches` points**"* | **A reference to a section that does not exist.** The Détailleur's sheet has five fields — `## Signatures`, `## Acceptance criteria`, `## Dependencies`, `## Conventions`, `## Requests` (det 229–258) — and **none names a file**. `Modifies` and `Touches` are fields of a lot in `code/decoupage.md` (cad 708–724), a file the concepteur is forbidden to open (62–63: *"Nothing else. Not the technical document, not the product file, not another lot's sheet"*). Worse, `Modifies` *"carr[ies] symbols, and symbols only … never a file"* (cad 715–716), so even read from the split it does not point at a file. Consequences: move 2's fallback leads nowhere; rule 82 (*"a file the sheet does not declare"*) and report field 192 have no referent — **every** file is one the sheet does not declare. Same class of error as the `## Symbols` → `## Signatures` slip the PO caught (modifications.md 1049–1052), one instance of which survived. | **BLOCKING** |
| D-4 | 158–170, 88–119 | 167–168: *"You do not go out on a red compile. Either it is green, or you wrote a blocking file."* · 170: *"**5. Commit**"* only after a green compile | **A procedure branch that leads nowhere.** Move 3 writes every declaration; move 4 compiles; a signature error is a block. At that point the declarations are on disk, uncommitted, and the file says nothing about them: not *drop them* (the realisateur's rule when a lot goes back: rea 288 *"Drop what you wrote. Commit nothing"*), not *commit what compiles* (rea 333–334), not *never leave a dirty working tree* (rea 401). Nor whether `blocked_concepteur.md` itself is committed. The orchestration then meets a worktree with uncommitted files, must not force it, and attributes the fault to the agent (cmd 390–393) — while *"Merge before handing back, always — including a `blocked_*.md`"* (cmd 402) cannot happen. The block, the one exit the file provides, strands the run. | **TO FIX** |
| D-5 | 161–168 | 164–165: *"It does not compile for another reason — a missing import, a wrong package line — fix it and compile again."* · 167–168: *"Either it is green, or you wrote a blocking file."* | A second branch that leads nowhere: the module does not compile, the cause is **not** a signature and **not** the concepteur's (the tree was red before it touched it, a dependency of a *produced by* lot is missing, the build file is broken). Block cases (111–113) are exhaustive and all signature-shaped; *"fix it and compile again"* has no bound and no exit. The agent can neither block (not allowed) nor finish (not green). | **TO FIX** — one line: a red compile whose cause is outside the lot is a block, with `## Where` naming what is red |
| D-6 | 118–119 | *"📌 **A blocking file the prompt names carries a filled `## Decision`** — 🔴 **apply it and carry on.** ⚠️ **You never look for one yourself.**"* | Coherent in itself, but the only invocation of this agent (cmd 206–211) is *"Working folder: <…>. Your lot: <lot>."* — no slot for a file. `8_code` 342–343 says *"invoke the agent it names on the lot it names, and let it apply the decision"*, without saying the prompt names the file. With *"you never look for one yourself"*, a settled `blocked_concepteur.md` is never applied. **Question**: is the omission in the `8_code` template, or should the concepteur look for a filled `## Decision` in `code/<lot>/` like `8_code` itself does (cmd 48–49)? | **TO FIX** (one side or the other) |
| D-7 | 29, 118–119 | *"One invocation per lot"* · *"apply it and carry on"* | A second invocation on the same lot (after a Decision) starts at move 1 with no notion of what the first run left — declarations already on disk, possibly a partial commit if D-4 is fixed by *commit what compiles*. The realisateur has `reprise_realisateur.md` and *"you kept what you had done"* (rea 397–398); the concepteur has nothing. Move 3 rewritten from scratch over existing declarations is a duplicate-symbol compile error the file would then read as a signature block (113: *"two symbols the sheet names identically"*). | **NOTE** — becomes TO FIX once D-4 is settled either way |
| D-8 | 17–18, 74–75, 150–153 | 17: *"A body is empty, or throws the language's not implemented — nothing else"* · 150–153: *"Whichever the conventions prescribe — and if they prescribe neither, throw: an empty body that returns a default is a body the testeur's red test could pass on"* | A term used in two senses and a rule that undercuts its own rationale. *Empty* means two things: literally empty (only compiles for a `Unit`/`void` return in Kotlin — a non-Unit function with no return does not compile) and *throws*. The rationale says an empty body a test can pass on is the danger; an empty `Unit` body is precisely that (a test asserting *does not throw* passes, a test asserting a side effect fails only by luck). The table row (modifications.md 852) says unconditionally *"lève not implemented, il ne retourne pas une valeur par défaut"*. **Question**: is *empty* meant to stay an option for the conventions to pick, or should the file say *throws, always*, as the table does? | **TO FIX** (or a one-line clarification of what *empty* may mean) |
| D-9 | 20–24 | *"⚠️ **Today a signature lives as prose in the sheet, and nothing compiles it before the coding starts.**"* | Present tense describing the state **before** this agent existed — pasted from the demande. Read by the agent at run time it is false (it is the thing that compiles it). Harmless, but it is the file's only paragraph addressed to the PO rather than to the agent. | **NOTE** |
| D-10 | 31–39 | 31: *"The files, in the working folder you were given."* · 33: *"Every path you write or read is relative — `docs/features/…`"* · 37–39: *"A path starting with `docs/` is relative to the repository root, not to the working folder"* | Three bases for a path (working folder for `code/<lot>/…`, repo root for `docs/…`, and — unstated — repo root for the Kotlin sources it edits). The code files are the bulk of what it writes and no sentence says where their paths are anchored; 31 (*"in the working folder"*) reads as if they were there. Inherited from the siblings, but this agent is the first whose main output is outside the working folder. | **NOTE** |
| D-11 | 57–58, 65–68, 134 | *"the rules marked `permanente`, whole"* | The conventions file as it stands has no `permanente` marker (0 hits in `docs/TECHNICAL_CONVENTIONS.md`); the marker is defined by the new architecte (architecte 116–124). Until the architecte rewrites the file, *"the most important thing you read"* is an empty set and the agent reads only the sheet's `## Conventions`. Chain-wide, not specific to this file. **Question** for the sequencing of the refonte, not a defect of the agent. | **NOTE** |
| D-12 | 158–159 | *"**4. Compile.** 🔴 **The module the declarations live in**, by the command the conventions name."* | The conventions name `./gradlew check` (R4) and `./gradlew :<module>:check` (R72) — `check` runs tests and lint, not a compile alone. Two consequences the file does not foresee: lint on stubs (an unused parameter of a throwing body, a `TODO()` rule) fails for a non-signature reason with no fix the concepteur may apply (it may not write a body), and D-5 bites; and the `## Compile` line the testeur takes as *"the module compiles"* (testeur 62) would actually attest `check`. **Question**: is `check` the intended command, or should the conventions name a compile task (`:<module>:compileDebugKotlin`) for this agent? | **NOTE** — question |
| D-13 | 170 | *"**5. Commit**, staging explicitly what belongs to the lot."* | No commit-message shape, no statement that `conception.md` is part of what is committed (it is, by `8_code`'s diff rule cmd 97–98, the Relecteur's list is the diff from the lot's first commit — which is now the concepteur's). Same wording as rea 568, so consistent, but the realisateur is fenced by rea 570–575 and the concepteur is not — see **C**. | **NOTE** |
| D-14 | 93, 95–109 | *"four headings, the last one left empty"* | Count matches: `## What blocks`, `## Where`, `## To resume`, `## Decision`. | verified, no finding |
| D-15 | 44–47, 142, 200 | *the report* = `code/<lot>/conception.md` | One term, one sense throughout. | verified, no finding |

### Cross-file remarks (outside the new file, recorded for the orchestrator)

- cmd 381–382: *"The `realisateur` commits inside it, lot by lot. That is his; you do not
  commit for him."* — now three agents commit per lot (concepteur move 5, presumably the
  testeur, the realisateur). The sentence is stale on the `8_code` side. **NOTE**.
- Same weakness as **D-3** in the siblings: testeur 210, rea 162–163, relecteur 373–374 all
  say *"file[s] … the sheet does not declare"* although the sheet declares no file. For them
  it is a wording problem (the split's `Touches` and the grep'd files stand in); for the
  concepteur it is load-bearing, because move 2's fallback and rule 82 depend on it.
- New `CLAUDE.md` 111: the `subagent_type` list repeats `verificateur · detailleur ·
  realisateur · relecteur · controleur · arbitre` a second time. Not this agent's; noted in
  passing.

---

## Summary

- **A**: no pass sheet; the file conforms to the section's table and demande on every row
  except one (**A-5**): the *empty-or-throw* rule is made conditional on the conventions where
  the table says *throws, never a default*.
- **B**: no old file; seven un-announced additions, all NOTE-level and consistent with the
  chain's pattern, one (the placement fallback) broken — see D-3.
- **C**: every gesture has a tool; `Bash` has no scope fence (TO FIX); `Glob` is unused
  (harmless); `Grep` is never named though needed.
- **D**: one BLOCKING (**D-3** — the sheet has no `Modifies`/`Touches` and declares no file,
  so the placement fallback, the *never touch* rule and `## Outside the lot` have no
  referent), six TO FIX (**D-1** four-vs-five moves · **D-2** rule 82 against the report
  field · **D-4** a block strands uncommitted declarations · **D-5** a non-signature red
  compile has no exit · **D-6** the Decision is never handed to it · **D-8** *empty* in two
  senses), the rest NOTE or open questions (**D-11** `permanente` not yet in the conventions,
  **D-12** `check` is not a compile).
