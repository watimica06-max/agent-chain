# Chain cockpit — technical design, version 1.2

A local application that lets the Product Owner run the agent chain
without editing files by hand. Version 1 covers the two things that cost
her the most time: **answering questions and blocking files**, and
**knowing which command comes next**.

*1.2 — the permission mode (§6); the page rebuilt around four screens
and an environment diagnostic.*

*1.1 — corrected after `docs/app/analyse-v1.md`: the default is accepted
by leaving `Answer:` empty (§8.1); five blocking-file shapes, not two
(§8.2); a fourth place the Product Owner writes (§2, §8.3); `stop.md`
is read by `/8_code` only (§7); `Next:` carries a second step (§9).*

---

## 1. Scope

**In version 1**

- Pick the application folder and the working folder at launch; both
  remembered.
- One form holding every open question of the working folder:
  proposals as choices, a free-text field, one save.
- One form holding every blocking entry waiting on the Product Owner,
  same shape.
- A "next step" panel: the command the chain asks for, highlighted, one
  click to run it.
- A live view of the running command, a permission card, stop buttons.

**Not in version 1**

- No autopilot. The application never runs a command the Product Owner
  did not click.
- No multi-feature dashboard, no test checklist, no deployment page, no
  bug list.

---

## 2. Principles

1. **The application is a client of the files; the chain does not
   depend on it.** Agents and commands keep reading and writing files.
   If the application breaks, every command still runs from Claude Code
   and nothing is lost.
2. **The application never decides the next step.** The command decides
   it and prints it on its last line (§9). The application reads that
   line and highlights the matching button.
3. **The application writes only where the Product Owner writes today**:
   - `Answer:` fields;
   - `## Decision` sections;
   - `## Décision du Product Owner` in `code/redecoupage.md`;
   - `stop.md`.

   Everything else is read-only.
4. **Write back to the file you read.** A blocking file read from a live
   worktree is answered in that worktree; one read from the main
   checkout is answered there. The exception is `stop.md`, which always
   goes in the main checkout.

---

## 3. Architecture

```
Browser page  ⇄  local Python server  ⇄  Claude Agent SDK (Python)  ⇄  Claude Code
                        ⇅
                 the application repository
```

- **Local server, Python 3.12.** It serves the page, reads and writes the
  repository, runs commands and streams their events to the page.
- **It listens on `127.0.0.1` only.** It can run Claude with write
  access; it must never be reachable from the network.
- **Runs belong to the server, not the page.** Closing the tab does not
  stop a run; reopening it shows the current state.
- **One run at a time per repository.** Commands create worktrees and
  commit; two concurrent runs would collide. The server holds a lock.
- **The application lives in `tools/cockpit/` of the chain's own
  repository**, versioned with the chain it drives and with no setup;
  pointed at another project's folder, it serves that project too.
- **Windows host.** The server is started with `python`, never
  `python3`: `python3` resolves to the Microsoft Store alias on this
  machine.

---

## 4. Setup and memory

- At first launch, two buttons open the native Windows folder picker,
  run by the server:
  - **the application folder**, for example `C:\Dev\hyrox_tracker`;
  - **the working folder**: a feature folder under `docs/features/`, or
    one of its `bugfix-NN/` folders, picked from a list the server
    builds.
- Both are saved in `config.json` in the application's own folder, with
  a short list of recent pairs.
- On relaunch, the last pair opens directly. A "change" button returns
  to the picker.

---

## 5. Running a command

- **Claude Agent SDK, Python, `ClaudeSDKClient`.** Not `claude -p` as a
  subprocess: the SDK gives a permission callback and a clean
  interrupt, which the page needs.
- **The command is sent as the prompt string**, exactly as typed in a
  session: `/1_lexique premiere-app-3`. Custom commands are expanded
  before the run.
- **Project settings are loaded.** Leave `setting_sources` at its
  default, so that `.claude/commands/`, `.claude/agents/` and
  `CLAUDE.md` load. 🔴 **Never bare mode**: it skips all three, and the
  whole chain with them.
- **`cwd`** is the application folder.
- **Events stream to the page.** Subagent messages carry their parent
  tool-use id, so the page can show which agent is running.
- **At the end of the run**, the server keeps the final relay text and
  reads its `Next:` line (§9).

## 6. Permissions

- **Two modes, « Auto » and « Manuel », default Auto.** The mode is set
  in Settings, shown in the top bar and remembered in `config.json`. It
  is passed explicitly on every run, as `ClaudeAgentOptions.permission_mode`
  (`auto`, or `default` for Manuel) — never left to the CLI's default —
  and a change applies from the next run. In Auto, Claude Code's
  classifier approves or blocks the tool calls itself; a request it sends
  back to a prompt still reaches the `can_use_tool` callback, so **auto
  mode falls back to a card**, as Manuel does for every request the
  settings rules do not allow.
- Every permission request that reaches the `can_use_tool` callback is
  turned by the server into a card (tool, input, Allow, Deny), shown as a
  banner at the top of every screen, and the run waits on the click.
- No permission is granted by default.

## 7. Stopping

- **"Stop now"**, on every run, calls `interrupt()` on the SDK client.
  The current turn ends unfinished.
- **"Stop at the next lot"**, on `/8_code` only, writes `stop.md` in the
  main checkout. 📌 `/8_code` is the only command that reads it
  (`cmd/8_code.md:435-456`); on any other run the button is not shown.

---

## 8. File contracts

The forms depend on files a machine can parse. Version 1 adds **one
thing** to the files agents write — an `Options:` list — and changes
nothing about how the chain reads the Product Owner's answers.

### 8.1 Questions files

**Where they are.**
- `questions-<agent>-NN.md` at the working folder's root.
- 📌 `convertisseur/technique-<nature>.md` and
  `convertisseur/technique-transversal.md`: technical questions,
  answered **in place**, never moved to the root.

**Shape of one entry.**

```
### Q<n>
<Key>: <value>              ← as today (Block:, Terms:, Entries:, Kind:)
Question: <text, in English, may run over several lines>
Options:
- <first proposal, a full sentence, in French>
- <second proposal, a full sentence, in French>
Défaut: <the exact text of one option> — <its source>      ← optional, as today
Answer:
```

- **`Options:` is the only addition.** It is optional: an open question
  has none. It holds two to six proposals.
- **Options are written in French**, because an option chosen becomes
  the answer word for word, and answers are in French by the chain's
  rule. The question stays in English.
- **No option opens on a number and a dot** (`1.`, `2.`): see §8.2,
  shape 4.
- **`Défaut:` keeps its present form.** Its text before ` — ` repeats
  one option verbatim; what follows ` — ` is its source, unchanged.

**What the application writes in `Answer:`.**

| The Product Owner… | `Answer:` |
|---|---|
| keeps the pre-selected default, with no remark | 🔴 **left empty** — the chain already reads an empty `Answer:` under a `Défaut:` as the default accepted, and the default keeps its source |
| chooses an option | the option's full text |
| chooses an option and adds a remark | `<option text> — <remark>` |
| writes free text | the text as typed |

- 🔴 **The text always starts on the `Answer:` line**, after one space.
  Further lines may follow: 141 real answers run over several lines. A
  text that starts on the next line reads as empty to `^Answer:\s*$`.

**What the parser accepts.** Real files carry prose before the first
`### Q`, a `Question:` running over several lines, `Answer:` with no
space after the colon, and older shapes with a title on the `Block:`
line. The parser accepts all of them, and treats a file it cannot read
as an error shown to the Product Owner, never as a file with no
questions.

### 8.2 Blocking files

**Five shapes**, from `docs/app/analyse-v1.md` §B:

| Shape | Writers | Her decision goes |
|---|---|---|
| 1. One block | 11 agents | under the single `## Decision`, on the line after one blank line |
| 2. One block plus `## Invocation` | redacteur, architecte, fusionneur | same as shape 1; `## Invocation` is routing, never shown |
| 3. Numbered, one `## Decision` per `## Blocking N` | qualifieur, classeur, redacteur inv. 3 | under **each** entry's `## Decision`, after one blank line |
| 4. Numbered, one `## Decision` for all, answered `N. <text>` | detailleur, realisateur | under the single `## Decision`, one line `N. <text>` per entry left to her |
| 5. One block appended several times | cadreur | under the **last** `## Decision` of the file |

- **`Options:` sits at the end of the body of `To resume`**
  (`## To resume`, or `### To resume` in shape 4), never under a new
  heading.
- **Shape 4 counts numbered lines.** The application writes exactly one
  `N. <text>` line per answered entry, and never lets a remark start
  with a number and a dot.

**What is shown as waiting on her.** The application reuses the
commands' own tests, unchanged:
- shapes 1-3: `grep -A2 '^## Decision$'` — nothing under the heading;
- shape 4: an entry whose number is absent under `## Decision`
  (`cmd/8_code.md:319-340`). The Arbitre answers these first; only what
  it leaves is hers;
- shape 5: the last `## Decision`, empty — **unless** the block waits on
  an Architecte verdict (`cmd/7_lots.md:189-190`), which is not hers;
- the relecteur's file: only its « anything else » case
  (`cmd/8_code.md:739`);
- the vérificateur's file: never shown — it has no `## Decision`.

**During a live run.** Only shape 4 is answered in a worktree, while the
Arbitre polls it, 20 minutes at most. Every other blocking file is back
in the main checkout before the command hands back.

### 8.3 `code/redecoupage.md`

After a third redécoupage, the Product Owner writes under
`## Décision du Product Owner` (`cmd/8_code.md:606-611`,
`cmd/7_lots.md:348-352`). Free text only.

### 8.4 Answers are tested the way the commands test them

Before saving, the application checks that what it wrote passes the
command's own test — for example `^Answer:\s*$` no longer matches, or
the decision sits on the line `-A2` reads. A form that saves but leaves
the file "unanswered" for the command is a bug.

---

## 9. The next step — `Next:`

**Every command ends every relay — including every stop — with exactly
one line in this grammar, as its last line:**

```
Next: run /<command> <arguments>
Next: answer <questions | blocking | questions and blocking>[, then run /<command> <arguments>]
Next: manual <what the Product Owner does>[, then run /<command> <arguments>]
Next: stop <reason>
Next: done
```

- `run` → the page highlights that command's button, arguments filled.
- `answer` → the page opens the matching form, and shows the command
  that follows once she has answered.
- `manual` → the page shows the instruction, and the command that
  follows if there is one.
- `stop` → the page shows the reason and offers no button. 📌 A stop
  is what the chain prints when it does not know the next step; the
  application never fills that gap.
- `done` → the page says the cycle step is complete.
- **No `Next:` line** → the page says the next step is unknown and shows
  the full relay.

The grammar is defined once, in `.claude/CLAUDE.md`. Each command gives
its values.
