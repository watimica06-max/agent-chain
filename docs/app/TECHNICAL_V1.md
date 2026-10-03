# Chain cockpit — technical design, version 1

A local application that lets the Product Owner run the agent chain
without editing files by hand. Version 1 covers the two things that cost
her the most time: **answering questions and blocking files**, and
**knowing which command comes next**.

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
- A live view of the running command, a permission card, two stop
  buttons.

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
   it and says so on its last line (§9). The application only reads that
   line and highlights the matching button.
3. **The application writes only where the Product Owner writes today**:
   `Answer:` fields, `## Decision` sections, `stop.md`. Everything else
   is read-only.
4. **Write back to the file you read.** A blocking file read from a live
   worktree is answered in that worktree; one read from the main
   checkout is answered there. The only exception is `stop.md`, which
   always goes in the main checkout (`PROCESS_MECANISMES.md` §stop.md).

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
- **The application lives in its own folder**, outside any project
  repository, because it serves several projects.
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

- Every permission request reaches the `can_use_tool` callback. The
  server turns it into a card in the page (tool, input, Allow, Deny) and
  waits for the click.
- The run waits with it. No permission is granted by default.

## 7. Stopping

Two buttons, two meanings:

- **"Stop at the next step"** writes `stop.md` in the main checkout. The
  command stops before its next step, as it does today.
- **"Stop now"** calls `interrupt()` on the SDK client. The current turn
  ends unfinished.

---

## 8. File contracts

The forms depend on files a machine can parse. Version 1 adds **one
thing** to the files agents write, and changes nothing about how they
read the Product Owner's answers.

### 8.1 Questions files — `questions-<agent>-NN.md`

Target shape of one entry:

```
### Q<n>
<Key>: <value>              ← kept as today (Block:, Terms:, Entries:, Kind:)
Question: <text>
Options:
- <first proposal, full text>
- <second proposal, full text>
Défaut: <the exact text of one option>       ← optional, as today
Answer:
```

- **`Options:` is the only addition.** It is optional: an open question
  has none. It holds two to six proposals, each a full sentence that
  makes sense on its own.
- **`Défaut:`, when present, repeats one option's text verbatim**, so
  the form can pre-select it.
- **What the application writes in `Answer:`**:
  - a chosen option → its **full text**, never its position, so every
    reader keeps reading plain French as it does today;
  - an option plus a remark → `<option text> — <remark>`;
  - free text → the text as typed;
  - a pre-selected default the Product Owner leaves as is → the default's
    text, written explicitly.

### 8.2 Blocking files — `blocked_<agent>.md`

- **Two families, as the file is today**:
  - one block per file, with a single `## Decision`;
  - numbered entries (`## Blocking N`), with one decision per entry.
- **Addition**: an `Options:` list in each block or entry, in the same
  shape as §8.1. Where it sits is settled by the analysis.
- **Only what waits on the Product Owner is shown.** For the files the
  Arbitre answers first, the application reuses the commands' own test
  (`/8_code` step 4b: empty, partial, filled) and shows only the entries
  left to her.
- The Vérificateur's file carries no `## Decision` and is never shown as
  a form.

### 8.3 Answers are tested the way the commands test them

Before saving, the application checks that what it wrote passes the
command's own test (for example `^Answer:\s*$` no longer matches). A
form that saves but leaves the file "unanswered" for the command is a
bug.

---

## 9. The next step — `Next:`

**Every command ends its relay with exactly one line in this grammar:**

```
Next: run /<command> <arguments>
Next: answer questions
Next: answer blocking
Next: manual <what the Product Owner does, in a few words>
Next: stop <reason>
Next: done
```

- `run` → the page highlights the button of that command, with its
  arguments filled in.
- `answer` → the page highlights the matching form.
- `manual` → the page shows the instruction; for example a test on the
  emulator, or a manual command such as `/conventions` or `/fusion`.
- `stop` and `done` → the page shows the reason.
- **No `Next:` line** → the page says the next step is unknown and shows
  the full relay. The application never guesses.

---

## 10. Open points settled by the analysis

- The exact list of agents and commands that write questions files and
  blocking files, and the change each needs.
- Where `Options:` sits in each blocking-file family.
- Whether any reader of `Answer:` needs more than one line.
- The `Next:` value for every way each command can end.
