# Chain cockpit — technical design, version 1.4

A local application that lets the Product Owner run the agent chain
without editing files by hand. Version 1 covers the two things that cost
her the most time: **answering questions and blocking files**, and
**knowing which command comes next**.

*1.4 — each question beside the passage it is about (§14); what every
run and every agent consumes, and the two usage windows (§13).*

*1.3 — where the feature stands: a scan of the files (§10), the stored
`Next:` checked against them (§2.2, §11); « Chaîne » and « Correction »
as flows (§12); the working folder is the feature alone (§4).*

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
2. **The next step** — the command prints it on its last line (§9); the
   application never decides it, with one fallback (1.3):
   1. **The files are the ground truth.** A stored `Next:` is a statement
      the chain made at one moment; a run that crashed, a bug of the
      cockpit, or an answer saved since can make it wrong.
   2. **The chain's `Next:` is trusted right after its run, and checked
      against the files at every other moment** (§11). A stored `Next:`
      the files contradict is dropped, and the page says so.
   3. **The scan's proposal is always labelled « déduite du dossier ».**
   4. **A wrong deduction costs little**, because every command tests its
      own preconditions before it acts and stops with its own `Next:`.
      `tools/cockpit/scan_rules.md` §2 checks that this is true before it
      is relied on.

   *Checked in 1.3: it is not true of `/2_structure`, `/3_decoupe`,
   `/6_convertit`, `/7_lots`, `/8_code`, `/9_controle`, `/fusion` and
   `/diagnostique` — each files, copies, commits or branches before one
   of its tests. The page asks for confirmation before launching them,
   even when the step is the one proposed.*
3. **The application writes only where the Product Owner writes today**:
   - `Answer:` fields;
   - `## Decision` sections;
   - `## Décision du Product Owner` in `code/redecoupage.md`;
   - `stop.md`;
   - *(1.3)* a new `bugfix-NN/` and its `bug-list.md`, which she used to
     create by hand (§12).

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
  - **the feature**, picked from `docs/features/`. *(1.3: its
    `bugfix-NN/` are no longer picked here — they live under
    « Correction », §12. A 1.2 value `feature/bugfix-NN` reads as the
    feature.)*
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
- shape 5: the last `## Decision`, empty — **unless** the `# Request N`
  its `## Where` names has an empty `## Verdict`, or none
  (`cmd/7_lots.md:210`, `:244-245`): the Architecte answers it, not her.
  **A filled verdict is shown (1.4.1)**: refused by the Cadreur, it is hers
  (`cmd/7_lots.md:213`, `agents/cadreur.md:1119`), and nothing on disk
  tells a refusal from a verdict the Cadreur has yet to read
  (`cmd/7_lots.md:211`) — the entry says so. Applied, the file is renamed
  and gone;
- the relecteur's file: **always shown (1.4.1)**. Its act rows
  (`cmd/8_code.md:748-750`) differ from « anything else » (`:751`) only
  by what `## What blocks` says; the application guesses it from the
  words — an input named, said missing — and when the guess fires, the
  entry carries what it saw, and stays to decide;
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
- **No `Next:` line** → right after the run, the page says so, shows the
  full relay and offers « Continuer la session »; at any later moment the
  scan's proposal takes its place, labelled (§11).

The grammar is defined once, in `.claude/CLAUDE.md`. Each command gives
its values.

---

## 10. Where the feature stands — the scan (1.3)

`tools/cockpit/scan.py` reads the feature folder and its `bugfix-NN/` —
**files only**: no Claude call, no git command (`HEAD` is read from
`.git/`), no write; about 40 ms on `premiere-app`. Every step of the main
chain and of each correction chain gets one state — **faite**,
**t'attend**, **en cours**, **bloquée**, **à faire**, or **inconnu** when
no rule places it. Each rule is a test of the command itself, with its
lines: **`tools/cockpit/scan_rules.md` is the table to check the scan
against**, and a test fails when a cited line no longer says what its
rule reads.

- **An open question or blocking entry belongs to the step named after
  it in « `answer …, then run X` »** — X is « t'attend ».
- **The proposed step** is the first one, in chain order, not « faite »;
  it is proposed when it is « t'attend » or « à faire », never past a
  « bloquée » or « inconnu » one. While the highest `bugfix-NN/` has a
  step not done, the proposal is the correction's: the commands act on
  it.
- `/8_code` also reports its lots, « n / N en PASS », from the verdicts
  the way `/8_code` reads them.

## 11. The next step, decided in this order (1.3)

1. **A run is going** → that run.
2. **A run has just ended** → its `Next:`, as it printed it — the only
   moment a `Next:` is trusted without a check.
3. **At every other moment** — « Où on en est ? », the page opening, a
   save of answers — the scan runs and checks the stored `Next:`:
   - it holds → shown, « dit par la chaîne »;
   - `answer …, then run X` with nothing left to answer → X, same label;
   - **the files contradict it** → dropped; the scan's proposal takes its
     place, « déduite du dossier », and the page says « Le dernier relais
     disait <X> ; les fichiers disent <Y>. »
4. **No stored `Next:`** → the scan's proposal, labelled.

A stored `Next: run X` is contradicted when a step before X is
« t'attend », when X is « faite » or « bloquée », or when `HEAD` moved
since the relay — `HEAD` is stored with each relay, so a move is not a
cockpit run's. A `manual`, `stop` or `done` line is contradicted by a
`HEAD` move only. **Every dropped `Next:` is written once to the log of
the run that printed it** (`"type": "NextDropped"`, with the reason and
the trigger).

## 12. The screens (1.3)

Tableau de bord · À répondre · **Chaîne** · **Correction** · Paramètres,
and « Où on en est ? » in the top bar.

- **Tableau de bord** — « Prochaine étape » follows §11 and says where it
  comes from; « Pourquoi ? » shows the step's rule, its files and lines.
- **Chaîne** — replaces « Run »: the main chain as a flow, one step per
  command, its state as a colour and a word. The next step stands out;
  one click launches it with the feature, or with the `Next:` line's own
  arguments. A step that is neither the chain's `Next:` nor the scan's
  proposal asks for confirmation, and so does every command
  `scan_rules.md` §2 flags. A step « t'attend » opens « À répondre »
  filtered on it; the running step shows the live run under it; the test
  step carries « Déployer » (`/deploie`) and what to test from
  `code/recette-ordonnee.md`.
- **Correction** — the feature's `bugfix-NN/`, newest first, each as the
  correction flow. Only the highest launches. « Nouvelle correction »
  creates the next `bugfix-NN/` and its empty `bug-list.md` — those two
  things only — and opens it for writing; `bug-list.md` is the one file
  written there, and only until `desc-bug.md` exists.
- **Paramètres** — the application folder and the feature; « Commandes »
  stays the escape hatch.

The page writes nothing beyond §2.3's places — the last of them, `bugfix-NN/bug-list.md`, new in 1.3.

## 13. Consumption (1.4)

### 13.1 What the stream gives — checked on a real stream

There were no run logs in `tools/cockpit/logs/` to check against. The
check was made on two real sessions run for it — not chain commands: a
Haiku session in a scratch folder, an agent nesting another, two parallel
tool calls, then `/usage` (Claude Code 2.1.285, `claude-agent-sdk`
0.2.163). Its second stream is `tests/fixtures/logs/2026-10-06-094500-probe.jsonl`.

- **Input and cache tokens, per agent: exact.** Assistant messages carry
  `usage` and `message_id`; parallel tool calls repeat one id; the
  subagent's messages carry its `parent_tool_use_id`, a nested agent's
  its own. Deduplicated per id, the orchestrator plus every agent equals
  the result's `model_usage` input (28 + 3 805 + 1 600 = 5 433). 🔴 **Only
  with `forward_subagent_text`**: without it a subagent message holding no
  tool call never reaches the stream — the nested agent of the first
  session was missing whole. The runner turns it on.
- **Output tokens, per agent: not in the stream** — since 1.4.3, read
  from `model_usage`, one model per consumer, below.
  - per-step `output_tokens` is a placeholder (« Per-step `output_tokens`
    is a placeholder », Agent SDK, *Track cost and usage*) — seen: 1, 3, 6
    on messages that wrote 51 to 202;
  - the Agent tool's result gives `subagent_tokens` (one total, input and
    output mixed) for a foreground agent, and `async_launched` for a
    background one; `TaskNotificationMessage.usage.total_tokens` is one
    total too — neither is an output count;
  - `message_delta` stream events carry the real count, but for the main
    session only: `StreamEvent.parent_tool_use_id` is « Always `None`.
    Stream events are emitted for the main session only » (Python SDK
    reference) — seen: none for either subagent.
- **Not from the transcripts (removed in 1.4.3).** 1.4.1 read each
  subagent's output from the transcripts Claude Code keeps, all or none
  against `model_usage`. On the first real run from the cockpit
  (`/1_lexique premiere-app-3`, `tools/cockpit/logs/2026-10-06-111521-1_lexique.jsonl`)
  the check refused the figures, as meant: the subagent's transcript kept
  the placeholder on the last line of 7 of its 11 messages, and its sum
  fell 28 689 short. A subagent's transcript is not a reliable source.
- **Output tokens, per agent, by model (1.4.3).** The final result's
  `model_usage` gives the exact output per model. A pass's output is its
  model's `outputTokens` **only if** that model's `inputTokens`,
  `cacheReadInputTokens` and `cacheCreationInputTokens` equal **exactly**
  the pass's own deduplicated sums from the stream, and no other pass ran
  on that model — the proof that nothing else (the orchestrator, another
  agent, an internal call of Claude Code) used it in the run. Otherwise
  unknown: no subtraction, no estimate. On that run: Opus in 22, cache
  read 975 519, cache creation 137 769 — the lexicographe's sums exactly
  — so its output is Opus's, 58 759. The orchestrator's own sums are
  Sonnet's (28 · 529 616 · 50 115). Two agents on one model, as the
  Cadreur and the Vérificateur, are both unknown. `model_usage` is
  cumulative over the session: that run has two results (the orchestrator
  waited for its background agent), the first with Sonnet alone
  (16 · 288 241 · 45 575, 1 566 written), the second with both and
  Sonnet's grown to the figures above. A resumed session's earlier spend
  therefore breaks the equality, and its passes stay unknown.
- **Run totals:** the latest result's `model_usage`, which counts
  subagents (« Use `modelUsage`… for whole-tree token accounting; the
  `usage` field undercounts as soon as nesting occurs »). A resumed
  session's results count its earlier spend: a continuation records what
  it added since the session's last run.

### 13.2 The usage windows

- **A `RateLimitEvent` comes at the first response of every session**,
  and again when a value changes (seen 0.04 → 0.05). Its
  `rate_limit_info.raw.unifiedWindows` holds **both** windows,
  `five_hour` and `seven_day`, each with `utilization` and `resetsAt`.
- **`/usage` sent in the run's own session answers without a model call**
  — `duration_api_ms` 0, `num_turns` 0, cost unchanged — and its text gives
  « Current session: N% used · resets … » and « Current week (all models):
  N% used · resets … ». The runner asks it once, when the run is over,
  logs it as a probe (never the run's work, never its relay) and stores
  both windows. If it fails, the last measure stays, with its age.
- Not used: a status line script receives `rate_limits` too (« only
  after the first API response in the session »), but it is a script the
  terminal interface runs; `/usage` needs no script and no setting.

### 13.3 What is stored and shown

- Every log line carries `at`, the time the message was received.
- `tools/cockpit/stats.sqlite` (`sqlite3`, ignored by git): `runs`,
  `agent_passes`, `rate_limits`. A subagent's `output_tokens` is its
  model's figure, or NULL — unknown —, never the placeholder.
- The runs already stored get their agents' output at the server's
  start, from the `model_usage` of each run's log (1.4.3).
- The logs written since 1.1 are loaded at the server's start, once each
  (by path), marked `backfilled`. They carry `at` on every line since
  1.1, so their durations are known; a log without it would leave them
  unknown.
- Dashboard: two gauges — percent used, left, the reset, and « mesuré il
  y a … ». A measure whose window has reset since is shown as such, never
  as current. Under the run: one line per agent that hands back —
  « écrits : à la fin du run », its output being known only then — and,
  at its end, the run's totals and each agent's line with its figure or
  « inconnu ». Tokens and time only.
- `/2_structure` no longer asks for confirmation when proposed (1.4.3):
  its three stops after the filing leave only the lexicographe's empty
  file filed, a state the next command reads correctly
  (`scan_rules.md` §2).

## 14. « À répondre » beside its document (1.4)

- Two panes: the questions; the document the focused question points to,
  read-only. `tools/cockpit/context_rules.md` gives, writer by writer and
  with its lines, what an entry points to — `Terms:` to words, `Block:`
  to a `### B<n>` section, `Entries:` to `§n.m` headings. A target no
  instruction gives is no context, said.
- Several occurrences: « 1 / n », previous and next. A target not in the
  file: said, nothing highlighted. A blocking entry: no document.
- Keyboard: `1`-`6` an option, `T` the text field, `Échap` out of it,
  `Entrée` or `↓` next, `↑` previous, `Ctrl+S` save. None but `Ctrl+S`
  fires in a text field.
