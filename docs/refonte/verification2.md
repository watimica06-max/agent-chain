# Refonte verification — investigation plan

**46 investigations, two waves** — 📌 **20 agents × 2, then 6 thematic.**
🔴 **Wave 2 starts once wave 1 is done.**

🔴 **Every investigation is READ-ONLY.** Each writes one report under
`docs/verification2/` and changes nothing else. ⚠️ **`docs/verification/`
is the previous round's** — 📌 **only wave 1's part 2 opens it.**

🔴 **Each prompt below is self-contained** — 📌 **paste it as it is.**

🔴 **Once both parts of an agent are back, join them:**

    cat docs/verification2/part2/<agent>.md \
        >> docs/verification2/<agent>.md
    rm docs/verification2/part2/<agent>.md

⚠️ **No fixing as the reports land** — 🔴 **read them together, triage,
fix in one pass.**

---

# Wave 1 — one investigation per agent, 20 in parallel

`lexicographe` · `redacteur` · `decoupeur` · `qualifieur` · `classeur` ·
`sondeur` · `assembleur` · `convertisseur` · `architecte` ·
`fusionneur` · `cadreur` · `verificateur` · `detailleur` ·
`concepteur` · `testeur` · `realisateur` · `relecteur` · `arbitre` ·
`controleur` · `diagnostiqueur`


🔴 **Two invocations per agent, and they do not share a reading.** 📌
**Part 2 is a separate agent** — ⚠️ **one that has read the previous
round's report cannot look at the chain with a fresh eye.**

📌 **They write two files, and the orchestration joins them afterwards**
— 🔴 **one file per agent in the end:**

    cat docs/verification2/part2/<agent>.md \
        >> docs/verification2/<agent>.md
    rm docs/verification2/part2/<agent>.md

⚠️ **Never let part 2 append to part 1's file itself** — 📌 **appending
means opening it**, and 🔴 **a part 2 that has seen part 1's table reads
a finding missing from it as settled**, when it may only be a finding
part 1 did not see.

---

## Part 1 — the chain as it stands

```
READ-ONLY. Modify nothing. Write one file:
docs/verification2/<agent>.md

🔴 **Read what you need, never a folder whole** — 📌 **the chain is
830 KB.**

⚠️ **Do not report formatting** — 📌 **a script already guards it and
the chain is clean of it**: 🔴 **unclosed bold, dead references, numeric
counts, colliding move numbers, orphan fragments, empty separators,
repeated lines, known typos.** 📌 **Your work is what a script cannot
see.**


🔴 **Never open `docs/verification/`** — 📌 **an earlier report exists**;
⚠️ **reading it would make you look for what it found instead of what
is there.**

Read:
1. `.claude-new/agents/<agent>.md`       — the file under verification
2. `.claude/agents/<agent>.md`           — 🔴 **the previous round's
   file**, to fill the `Origin` column and for nothing else
3. `docs-new/refonte/modifications.md` — 🔴 **your section only**:
   `grep -n '^# '` returns its headings; read from yours to the next.
   📌 Two agents share one section: `# \`classeur.md\` · \`decoupeur.md\`.
4. `docs-new/refonte/passes/<agent>.md` — the defect analysis. ⚠️ **Six
   agents have none**: `concepteur`, `testeur`, `arbitre`, `fusionneur`,
   `diagnostiqueur`, `qualifieur`. 🔴 **For those, section 1 is the index
   alone** — say so in one line and carry on.
5. Its commands: `grep -ln '<agent>' .claude-new/commands/` — 🔴 **only
   the ones that invoke it.**

Four sections, four comparisons — 🔴 **worked in the order below.**

---

### The four comparisons

🔴 **Each section is one comparison** — 📌 **what the file is held
against is what makes the finding true:**

| | The file compared to | |
|---|---|---|
| **1** | 🔴 **The record** — the index, the pass sheet | A correction listed as done and absent |
| **3** | 🔴 **Its own declaration** — the frontmatter | A gesture with no tool, a tool with no gesture |
| **2** | 🔴 **Itself** | Two rules that contradict, a count that does not match |
| **4** | 🔴 **The rest of the chain** | A fact asserted about another file |

🔴 **Work them in that order: 1, then 3, then 2, then 4.** ⚠️ **A finding
belongs to the first section that could see it**, and to that one only.

📌 **Why that order** — 🔴 **each comparison is wider than the one
before**: ⚠️ **a gesture with no tool is always also a branch leading
nowhere**, and the reverse is not true. 📌 **1 comes first because it
depends on nothing**; **4 last because it is the only one that leaves
the file.**

⚠️ **The same fact under two headings is the defect this order exists to
prevent** — 📌 **27 findings of the first round said twice what another
section had already said.**

---

### 1 — AGAINST THE RECORD

🔴 **The index and the pass file, against the agent file.** 📌 **One
question: does the index tell the truth?**

- A comment listed **PASSÉ** whose change is not in the file
- A comment listed **ÉCARTÉ** or **REPORTÉ** whose change is there
- A comment listed **PASSÉ** applied differently than asked — 📌 **say
  how**
- A change in the file the index does not mention at all
- A numbering mismatch between the index's `C<n>` and the pass file's
  `### <n>`

🔴 **You state the gap, never what it costs.** ⚠️ **What a difference
breaks is a finding of section 2 or 4**, with its own number — 📌 **and
if no later section finds anything, the difference cost nothing.**

### 3 — AGAINST ITS OWN DECLARATION

🔴 **The frontmatter, against the gestures.**

- **A gesture with no tool** — 📌 **the file orders something the tools
  cannot do**
- **A tool no gesture uses** — 🔴 **a tool with no stated use is a tool
  the agent may use to do what the file forbids**
- **A gesture whose tool is never named** — ⚠️ **an agent that reads a
  file whole to find a heading obeyed the tool and broke the rule**
- **An unbounded `Bash`**

⚠️ **A tool removed whose gesture survived** — 📌 **check that pairing
first.**

### 2 — AGAINST ITSELF

🔴 **One file: the agent.** 📌 **Everything here is visible without
opening anything else** — ⚠️ **and was not already caught by section
3.**

- **A rule contradicted elsewhere in the file** — 🔴 **including an old
  rule left standing beside a new one**
- **An announced count that does not match** — ⚠️ **in words as often as
  in numerals**: *« four moves »*, *« two invocations »*, *« six
  fields »*
- **A term used in two senses**
- **A procedure branch that leads nowhere** — 📌 **a case with no
  outcome, an outcome with no file to write it in, a wait nothing ends**
- **A reference to a section that does not exist**, or that says
  something else
- **An example that contradicts the rule it illustrates**
- **A rule placed after what it governs**

### 4 — AGAINST THE REST OF THE CHAIN

🔴 **Bounded.** 📌 **Two sets, and nothing beyond them:**

- **The commands that invoke it** — 🔴 **read those**
- **Every file the agent writes or reads** — 📌 **`grep -rln` its name
  across `.claude-new/`**, then ⚠️ **read only the hit lines and their
  surroundings**: 🔴 **never another agent whole.**

What to look for:

- **A fact asserted about another file** — 🔴 **verify it**: a section
  name, a field name, a heading, a file path
- **A producer and its reader disagreeing** — 📌 **one writes a field
  nobody reads, or reads one nobody writes**
- **A prompt that does not carry what the agent's rule requires**
- **A fact from another project written as a rule** — 📌 **a size in KB,
  a build command, a framework word, a language keyword**
- **A term the two files spell differently** — ⚠️ **one greps what the
  other writes**

---

**Your report — one table, and nothing else.** 🔴 **No evidence section,
no development, no restatement of what you read.**

    | # | Severity | Origin | Section | Where | Finding |

- **`#`** — 🔴 **`F01`, `F02`…**, one numbering for the whole report,
  whatever the severity. ⚠️ **Never a prefix that encodes severity.**
- **`Severity`** — `BLOCKING` · `TO FIX` · `NOTE` · `QUESTION`.
- **`Origin`** — 🔴 **one word**: `refonte` when `.claude/agents/<agent>.md`
  did not have it, `pre-existing` when it did, `unknown` when you cannot
  tell. ⚠️ **Never a guess.**
- **`Section`** — 🔴 **1, 2, 3 or 4**, one only.
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

---

## Part 2 — the previous round's findings, one by one

```
READ-ONLY. Modify nothing. Write one file:
docs/verification2/part2/<agent>.md

🔴 **Read what you need, never a folder whole** — 📌 **the chain is
830 KB.**

⚠️ **Do not report formatting** — 📌 **a script already guards it and
the chain is clean of it**: 🔴 **unclosed bold, dead references, numeric
counts, colliding move numbers, orphan fragments, empty separators,
repeated lines, known typos.** 📌 **Your work is what a script cannot
see.**


Read:
1. `docs/verification/agent-<agent>.md` — the previous round's report
2. `.claude-new/agents/<agent>.md` and whatever files that report names

🔴 **Never open `docs/verification2/<agent>.md`** — 📌 **the new round's
own report**: ⚠️ **your job is the file, not its list.**

🔴 **Take every `BLOCKING`, `TO FIX` and `NOTE` of that report, in its
own order, and give each a status.**

| Status | |
|---|---|
| `fixed` | ✅ **The change asked for is in the file** |
| `open` | 🔴 **It is not** |
| `other` | ⚠️ **Something changed, but not what was asked** — 📌 **one line saying what** |
| `moot` | 📌 **The finding no longer applies** — 🔴 **say why**: a rule it depended on has gone |

🔴 **Grep to find the passage, read it to judge.** ⚠️ **A string being
present does not mean the rule reads right** — 📌 **a table row can
still order what the rule three lines below forbids.**

⚠️ **A `QUESTION` is answered or it is not** — 🔴 **never answer it
yourself.**

**Output**: one table, nothing else.

    | # | Status | Where | One line |

- **`#`** — 🔴 **the identifier the previous report gave it**, unchanged
- **`Where`** — 📌 **file and line in `.claude-new/`**, ⚠️ **or `—` when
  the change is absent**
- **`One line`** — 🔴 **only for `other` and `moot`**; 📌 **empty for
  `fixed` and `open`.**

⚠️ **No development, no re-argument, no new finding.** 📌 **A defect you
meet that the report does not name is not yours** — 🔴 **the other
invocation is looking for it.**
```


# Wave 2 — thematic, 6 in parallel

⚠️ **Two of the first round's eight are not among them.**

📌 **The reading budget ran once and gave what it had to give** — 🔴
**the next useful measure needs a real cycle on `premiere-app-3`**, not
a re-read of the same files.

📌 **The transfer from `sujets.md` to the index is history** — 🔴 **the
refonte is closed**: ⚠️ **a decision that never reached the index only
matters if the chain does not carry it**, and that is what wave 1 reads,
in the files themselves.

## V2.1 — Renames

```
READ-ONLY. Write docs/verification2/renommages.md

🔴 **Read what you need, never a folder whole** — 📌 **the chain is
830 KB.**

⚠️ **Do not report formatting** — 📌 **a script already guards it and
the chain is clean of it**: 🔴 **unclosed bold, dead references, numeric
counts, colliding move numbers, orphan fragments, empty separators,
repeated lines, known typos.** 📌 **Your work is what a script cannot
see.**


For each name below, grep all of .claude-new/ and docs-new/ and answer:
1. Who writes it?
2. Who reads it?
3. Does the old name survive anywhere?

🔴 **The names of the first round were swept and are settled** — 📌
**these are the ones the correcting round created**, plus one it
removed.

New names:
- `## Files` of a spec sheet — the lot's files, carried into the sheet
- `## Redécoupage: archivable` in `code/sequence.md`
- `Mode: divergence` in the détailleur's prompt
- `Group:` in the contrôleur's prompt
- `## What governed the code, besides the sheet` of a lot's report
- `## Placements not settled by the conventions` of a conception report
- `## Blocking N` / one numbered answer per blocking, in a blocking file

Changed:
- `## Git, before invoking` and `## Git, once it has reported` — 🔴 **the
  old `## Git, in this mode` split in two**; ⚠️ **`/5_reclasse` keeps
  the old heading**, deliberately: it invokes no agent

Removed — report any surviving occurrence:
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

## V2.2 — File writers and readers

```
READ-ONLY. Write docs/verification2/fichiers.md

🔴 **Read what you need, never a folder whole** — 📌 **the chain is
830 KB.**

⚠️ **Do not report formatting** — 📌 **a script already guards it and
the chain is clean of it**: 🔴 **unclosed bold, dead references, numeric
counts, colliding move numbers, orphan fragments, empty separators,
repeated lines, known typos.** 📌 **Your work is what a script cannot
see.**


Census every file the chain produces and consumes.

🔴 Do not read the chain whole — it is 828 KB. Work by grep:
1. Two passes, then take the union — neither alone is complete:
   `grep -rhoE '\`[^\`]*\.md\`' .claude-new/ docs-new/ | tr -d '\`' | sort -u`
   catches the names written in prose (about 168),
   `grep -rhoE '[a-zA-Z0-9_<>/.-]+\.md' .claude-new/ docs-new/ | sort -u`
   catches those inside code blocks, where backticks are absent.
   ⚠️ Discard the fragments the second pass produces — a name must have
   a stem before `.md`.
2. For each name, `grep -rn` it across .claude-new/ and docs-new/, and
   read only the hit lines and their surroundings.
3. Open a file in full only when the hits do not settle who writes it.

One line per file: who writes it, who reads it, at what point of the
cycle.

Then report three anomalies:
- A file written that nobody reads
- A file read that nobody writes
- A file written by two agents with no stated order

Check specifically that nothing still expects: the Contrôleur's
blocking file, the Vérificateur's blocking file, the second table of
`couverture.md`.

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

## V2.3 — Paths and loops, upstream

```
READ-ONLY. Write docs/verification2/chemins-amont.md

🔴 **Read what you need, never a folder whole** — 📌 **the chain is
830 KB.**

⚠️ **Do not report formatting** — 📌 **a script already guards it and
the chain is clean of it**: 🔴 **unclosed bold, dead references, numeric
counts, colliding move numbers, orphan fragments, empty separators,
repeated lines, known typos.** 📌 **Your work is what a script cannot
see.**


Scope: /1_lexique, /2_structure, /3_decoupe, /3a_genre, /3b_nature,
/4_grille, /5_reclasse, /6_convertit, /conventions, /fusion,
/fusion_compare, /fusion_applique.

For each command, enumerate every possible state of the folder when it
is launched, and verify each has a written outcome. A state with no
routing line is a hole.

For each loop: what terminates it? Report any exit condition that is
unreachable, and any loop that can restart on itself.

Check specifically:
- An empty questions file · an unanswered one · two at the root
- A blocking file with an empty decision · a filled one · an already
  numbered one
- The second closing pass: it fires when the first returns an empty
  file, and must run once only
- The Convertisseur's short loop (technical questions) against its long
  loop (product questions)
- The Architecte's invocation 4: how does the command know to run it
  rather than invocation 1?

Trace three end-to-end scenarios and say where each stops: a first
feature on an empty project · a feature on a project that already has
some · a correction cycle.

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

## V2.4 — Paths and loops, downstream

```
READ-ONLY. Write docs/verification2/chemins-aval.md

🔴 **Read what you need, never a folder whole** — 📌 **the chain is
830 KB.**

⚠️ **Do not report formatting** — 📌 **a script already guards it and
the chain is clean of it**: 🔴 **unclosed bold, dead references, numeric
counts, colliding move numbers, orphan fragments, empty separators,
repeated lines, known typos.** 📌 **Your work is what a script cannot
see.**


Scope: /7_lots, /8_code, /9_controle, /deploie, /diagnostique,
/audit_blocages, /audit_conventions.

Same work: every state, every outcome, every loop and what terminates
it.

Check specifically:
- The per-lot loop of /8_code chains five agents (detailleur,
  concepteur, testeur, realisateur, relecteur). What happens if each
  blocks, one by one?
- The attempt counter: where does it live, who writes it, who
  increments it, what happens if it is missing?
- The escalation to opus after two `Cause: reasoning`
- The return to the split: who writes it, who reads it, when is it
  archived, and the stop at the third
- The Cadreur's three rounds with the Vérificateur
- /9_controle: six phases, three of which do not run on a correction
  cycle. Do the other three actually run?

Trace three scenarios: a lot that passes first time · a lot that fails
three times · a redécoupage mid-block.

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

## V2.5a — Handovers, upstream

```
READ-ONLY. Write docs/verification2/passages-amont.md

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
- `## What you read` and `## What you write` — 9 agents of 20
- `## Where you work` — a table of paths, used by cadreur,
  convertisseur, lexicographe
- The invocation table under `## INVOCATION n`, or a `| # | Invocation |
  Inputs | Output |` table — used by redacteur, fusionneur,
  diagnostiqueur, and every multi-invocation agent

📌 `grep -n '^## '` the agent first, pick the headings that apply, then
read those ranges. 🔴 An agent where none of the three forms appears is
itself a finding — report it rather than skipping it.

Pairs:
lexicographe→redacteur · redacteur→decoupeur · decoupeur→qualifieur ·
qualifieur→classeur · classeur→sondeur · sondeur→assembleur ·
assembleur→redacteur · redacteur→convertisseur ·
convertisseur→architecte · convertisseur→cadreur ·
9_controle→redacteur · redacteur→fusionneur

Never exercised, check hardest: 9_controle→redacteur

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

## V2.5b — Handovers, downstream

```
READ-ONLY. Write docs/verification2/passages-aval.md

🔴 **Read what you need, never a folder whole** — 📌 **the chain is
830 KB.**

⚠️ **Do not report formatting** — 📌 **a script already guards it and
the chain is clean of it**: 🔴 **unclosed bold, dead references, numeric
counts, colliding move numbers, orphan fragments, empty separators,
repeated lines, known typos.** 📌 **Your work is what a script cannot
see.**


Same work and same reading rule as V2.5a.

Pairs:
cadreur→verificateur · verificateur→detailleur · detailleur→concepteur
· concepteur→testeur · testeur→realisateur · realisateur→relecteur ·
relecteur→detailleur · relecteur→controleur · detailleur→arbitre ·
realisateur→arbitre · arbitre→architecte

Never exercised, check hardest: detailleur→concepteur ·
concepteur→testeur · testeur→realisateur

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
investigation**: each writes a distinct file, and forty-six merges
buy nothing.

**Before invoking anything:**

```
git worktree add ../verif-<date> -b verification/<date>
cd ../verif-<date>
mkdir -p docs/verification2/part2
```

🔴 **Enter the worktree before invoking, not after a write fails** — 📌
**the harness blocks a subagent's writes until the session is
isolated.** ⚠️ **Measured on this project: the agent does the full job,
cannot write, and the whole invocation is redone.**

🔴 **`docs/verification2/` and `docs/verification2/part2/` are created
by the `mkdir` above**, before the first agent runs — 📌 **an agent that
has to create its own folder sometimes writes beside it instead.**

❌ **Never pass `isolation`** — 📌 **the agents read the same files and
write different ones.**

**Once every report is written:**

```
git add docs/verification2/
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

📌 **Order**: wave 1 BLOCKING findings first.

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
