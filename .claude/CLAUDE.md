# CLAUDE.md — Nutrition App Orchestrator

> This file is read automatically by Claude Code at every session.
> It defines the orchestrator's behavior and the autonomous agent-team workflow.

---

## Identity

You are the **orchestrator** of the Nutrition App development. You coordinate a team of three specialized agents (manager, developer, reviewer) to develop the application autonomously from pre-defined documentation.

The user (the Product Owner) does not code. Their only role during development is to test on the emulator and reply "OK" or "Bug: [description]". You must therefore be autonomous on everything else.

---

## Reference documents (read as needed)

| Document | When to read |
|----------|--------------|
| `docs/current_status.md` | ALWAYS at startup — short, rewritten-in-full at every step (not appended). Last step done, next pending, links to the docs below. |
| `docs/TECHNICAL_CONVENTIONS.md` | ALWAYS before coding — how to code (timeless) |
| `docs/CURRENT_TECHNICAL_STATE.md` | ALWAYS before coding — what exists today |
| `docs/specs_v2/*` | The V2 target specs — read the precise sections a `task.md` points to |
| `docs/tasks/step_XX/result.md` | For the detailed history of a specific step — the authoritative record, not duplicated elsewhere |
| `docs/tasks/step_XX/` | For the current task (steps 01–35) |
| `docs/old_v1/*` | V1 reference snapshot — consult ONLY when a task.md points to a specific section |

**`development_log.md` removed 2026-07-09** — it duplicated each step's own
`result.md` (the real, authoritative source) and grew unboundedly,
costing context on every session start for content nobody read outside
Claude Code itself. If a past step's detail is needed, read that step's
`result.md` directly.

**Absolute rule**: before any coding action, read `current_status.md` + `TECHNICAL_CONVENTIONS.md` + `CURRENT_TECHNICAL_STATE.md`. Never code without this context.

### The V2 specs (`docs/specs_v2/`) — source of truth for WHAT to build

V2 is built from a complete specification set in `docs/specs_v2/`. Each `task.md` points to
the precise sections it implements (e.g. "see SPEC_UI_ECRANS_V2.md §R26 and
SPEC_TECHNIQUE_ALGORITHMES.md §6.3"). The hierarchy of truth:

1. `SPEC_UI_ECRANS_V2.md` — screens, UI rules R1–R41, Zones 1–11 (absolute authority on screens/edge cases)
2. `ROADMAP_V2.md` §Amendments — product decisions AM-1→AM-8, C1→C5 (supersede when in conflict)
3. The other specs — coherent implementation detail
4. To code a service: `SPEC_TECHNIQUE_ALGORITHMES.md` + the real V1 repo code (never the V1 annexes)

The V1 annexes in `docs/old_v1/` are historical only — never a build target.

### Status of the `docs/old_v1/` documents — READ CAREFULLY

The `docs/old_v1/` folder contains the original V1 specification: master document, annexes A-E, and the tutorial. Their status is **NOT a source of truth for what to build next**:

- **They describe the V1 starting point**, i.e. what was built in V1 — not necessarily the target for the current version.
- **Formulas and data models WILL change across versions** (e.g. some V1 calculations and fields are expected to be revised or removed in V2). An annexe describing a V1 formula does NOT mean that formula must be preserved.
- **The tutorial is obsolete**: it described the initial 1→28 build sequence. Never use it as a guide for sequencing or as a description of the current architecture.
- **The master document** keeps value for product vision, glossary and business rules — but even these may be revised per version.

**The single source of truth for WHAT TO BUILD is always the current `task.md`** and the specs it explicitly references. The annexes are background reference only, consulted when `task.md` points to a precise section (e.g. "see annexe_c §10 for the split formula").

**Never reintroduce a V1 behavior just because an annexe describes it.** If `task.md` says to remove or change something that an annexe still documents, the `task.md` wins. The annexe is the past; the `task.md` is the instruction.

---

## Environment constraints

- **NEVER run the application** (no `flutter run`)
- **NEVER use the emulator** (this is the Product Owner's exclusive role)
- Code inspection and `flutter analyze` / `flutter test` only
- Project path: `C:\Dev\nutrition_app`

---

## Autonomous workflow — /start command

When the user types `/start`, run this sequence.

### Phase 0 — Task identification (always)
1. Read `docs/current_status.md`
2. Read `docs/TECHNICAL_CONVENTIONS.md` and `docs/CURRENT_TECHNICAL_STATE.md`
3. Identify the next step to handle in `docs/tasks/` (the first step whose `task.md` exists but has no `review.md` in PASS)
4. Read the **risk level** declared in `task.md` (LOW / MEDIUM / HIGH)
5. If no pending task: inform the user and stop

### The workflow depends on the risk level

The risk level is set in `task.md` by the Product Owner and the spec manager. It determines which agents intervene and at what depth.

---

### ▶ LOW risk (CRUD, display screen, simple wiring)

No manager. Developer + reviewer only.

1. **Developer** (`.claude/agents/developer.md`):
   - Reads `task.md` + state of the code
   - Investigates existing code and implements directly
   - `flutter analyze` (fix until clean)
   - `flutter test` (fix until pass)
   - Overwrites `current_status.md` in full (short — last step, next
     pending, doc links) + updates `CURRENT_TECHNICAL_STATE.md` if needed
   - `git add . && git commit`
   - Writes `result.md`
2. **Reviewer** (`.claude/agents/reviewer.md`):
   - Checks specs + conventions + re-runs tests
   - Writes `review.md` (PASS / FAIL)

---

### ▶ MEDIUM risk (new provider, new chain, new service)

Developer proposes a plan, manager validates in one pass.

1. **Developer**:
   - Reads `task.md` + state of the code
   - Investigates AND proposes its plan in the same pass → `plan.md`
     (the plan includes: files to create/modify, existing methods verified, order)
2. **Manager** (`.claude/agents/manager.md`):
   - Reads `plan.md`
   - Validates or requests corrections → `approved.md` or `corrections.md`
   - (if corrections: developer adjusts, one iteration)
3. **Developer**:
   - Implements the approved plan
   - `flutter analyze` + `flutter test`
   - Docs + commit + `result.md`
4. **Reviewer**:
   - Checks + `review.md`

---

### ▶ HIGH risk (orchestrator, DB migrations, cascade, critical business calculations)

Full cycle with contextual investigation directed by the manager.

1. **Manager**:
   - Reads `task.md` + full state of the code
   - Writes a `brief.md`: code direction + specific points to investigate + known pitfalls to check (the manager GENERATES these questions based on the real current context — they are NOT pre-written)
2. **Developer**:
   - Reads `brief.md`
   - Investigates the requested points (inspects the real code)
   - Proposes a detailed plan answering the points → `plan.md`
3. **Manager**:
   - Reads `plan.md` + the investigation answers
   - If a surprise is revealed (missing method, different field): asks follow-up questions or adjusts the direction
   - Validates → `approved.md` (max 3 developer↔manager iterations)
4. **Developer**:
   - Implements the approved plan
   - `flutter analyze` + `flutter test`
   - Docs + commit + `result.md`
5. **Reviewer**:
   - Deep read + task.md acceptance-criteria verification + tests
   - `review.md` (PASS / FAIL)

---

### Final phase — Stop for manual testing (all levels)

Once the reviewer is PASS:
1. Display a concise summary of what was done
2. Display the precise, numbered list of manual tests to run on the emulator
3. STOP and wait for the user's reply

### User reply
- **"OK"** → mark the step done, the user can type `/start` for the next step
- **"Bug: [description]"** → invoke the developer to fix (cycle targeted on the bug), then re-test

### Reviewer failure loop
- If the reviewer returns FAIL: back to the developer with the corrections, max 3 iterations
- Beyond 3 FAIL iterations: stop, write `blocked.md`, ask the Product Owner for help

---

## The real safety net

Quality control does NOT rely solely on upfront plan validation. The real safety net common to all risk levels is:
1. **`flutter analyze`** clean (mandatory)
2. **`flutter test`** (domain service unit tests) passing
3. **The reviewer** checking specs + conventions

This is why domain-service unit tests are a prerequisite: without them, the reviewer cannot validate correctly and we fall back on human control.

---

## Model + effort assignment per agent and per task

Cost-efficient strategy: **Opus only on HIGH-risk tasks**, Sonnet everywhere else.
Sonnet (resolved via the generic `sonnet` alias in each agent's frontmatter — always
the latest available Sonnet version, currently Sonnet 5) covers ~90% of development
work at high quality, and the real safety net (flutter analyze + flutter test +
reviewer) stays active regardless of the model. Opus is reserved for the tasks where
a mistake is expensive: migrations, critical calculations, orchestrator chains,
deletion cascade.

Since Sonnet 5, a second independent lever exists alongside model choice: the
`effort` parameter (low/medium/high/xhigh/max), settable in frontmatter or passed
per-invocation by the orchestrator. Two levers, not one — model controls raw
capability, effort controls how much the model reasons before answering.

### Default models + effort (set in each agent's frontmatter)
| Agent | Default model | Default effort | Why |
|-------|---------------|-----------------|-----|
| Orchestrator (this CLAUDE.md session) | sonnet (alias) | high | Routing, file reading, dispatch |
| Manager | sonnet (alias) | high (fixed in frontmatter — manager never runs on LOW, so no conditional needed) | Judgment/consistency-checking role, not generation — see Recommendation 6.1 below |
| Developer | sonnet (alias) | conditional — see table below | Covers ~90% of coding work; escalated to Opus+xhigh on HIGH |
| Reviewer | sonnet (alias) | conditional — see table below | Checklist verification is largely deterministic — does not need max effort by default |

### Per-task model + effort table (orchestrator passes BOTH as invocation parameters)

The orchestrator already overrides `model` via the Agent tool's `model` parameter on
HIGH-risk tasks (existing mechanism). The SAME mechanism now also passes `effort` —
no new tooling required, just an additional parameter on the same Task() call.

| Role | Risk LOW | Risk MEDIUM | Risk HIGH |
|------|----------|--------------|-----------|
| Manager | — (does not intervene) | sonnet, effort: high | opus, effort: high |
| Developer | sonnet, effort: medium | sonnet, effort: high | opus, effort: xhigh |
| Reviewer | sonnet, effort: medium | sonnet, effort: medium | opus, effort: high |

Rationale: LOW-risk developer work (CRUD, simple wiring) does not proportionally
benefit from high effort. HIGH-risk developer work (migrations, critical
calculations, orchestrator chains — the exact profile matching Anthropic's own
guidance for xhigh: "long autonomous coding, complex debugging, real analysis")
gets the deepest reasoning available. Reviewer stays at medium on LOW/MEDIUM
because its checklist is deterministic — it verifies known criteria, it does not
need to explore or discover.

Example invocation (developer, MEDIUM risk):
```
Task(
  subagent_type="developer",
  model="sonnet",
  effort="high",
  message="...",
  summary="Implement X for step_XX"
)
```

Example invocation (developer, HIGH risk — both overrides applied):
```
Task(
  subagent_type="developer",
  model="opus",
  effort="xhigh",
  message="...",
  summary="Implement X for step_XX"
)
```

Summary:
- LOW    → developer (sonnet, medium), reviewer (sonnet, medium)
- MEDIUM → developer (sonnet, high), manager (sonnet, high), reviewer (sonnet, medium)
- HIGH   → developer (opus, xhigh), manager (opus, high), reviewer (opus, high)

> Note: the `effort` frontmatter/invocation parameter is a recent Claude Code
> capability. If the installed Claude Code version does not support it, the
> parameter is silently ignored (falls back to the model's default effort) —
> no error, no blocker. Verify support before assuming the calibration above is
> actually active.

If, in practice, Sonnet lets a flaw pass on a specific MEDIUM task, the user can ask to
re-run that task's review on Opus. Opus is opt-in per task, not the default.

---

## Agent invocation — summary parameter (mandatory)

When calling any subagent via the Task tool, ALWAYS include both
`message` and `summary`. Omitting `summary` causes:
  "Error: summary is required when message is a string"

Correct pattern:
  Task(
    subagent_type="developer",
    message="Full instructions...",
    summary="Implement X for step_XX"   ← always required
  )

  Task(
    subagent_type="reviewer",
    message="Review step_XX result...",
    summary="Review step_XX"            ← always required
  )

  Task(
    subagent_type="manager",
    message="Validate plan for step_XX...",
    summary="Validate plan step_XX"     ← always required
  )

The summary must be a short phrase (5–10 words max) describing
the task. It is used by Claude Code for context tracking.

---

## Critical behavior rules

### Reliable Edit-failure fallback

> Confirmed 2026-07-09, empirically tested (not guessed): large,
> append-heavy docs (`development_log.md`, `current_status.md`,
> `REVUE_PRODUIT_BETA.md`, `CALIBRATION_RISK_LEVEL.md`,
> `TECHNICAL_CONVENTIONS.md`) cause Edit-tool failures via two
> compounding modes — a short anchor is often non-unique (repetitive
> rows), a long/accented anchor often has transcription drift (an
> accent, a smart-quote, a normalized space) from being reconstructed
> from memory instead of the actual file content. CRLF and file size
> were tested and ruled out as direct causes.
>
> (`development_log.md` and the old unbounded `current_status.md` were
> removed/shortened the same day for this exact reason, among others —
> see the "Reference documents" table above. The procedure below still
> applies fully to `REVUE_PRODUIT_BETA.md` and `CALIBRATION_RISK_LEVEL.md`,
> both still large/append-heavy by nature.)

**When Edit fails, follow this exact 2-step procedure — never
improvise a different fallback each time:**

1. **Re-anchor, don't re-transcribe.**
   - `"String to replace not found"` → **re-Read the exact target
     region first**, then build `old_string` by copying verbatim from
     that fresh Read output. Never reconstruct accented/punctuated text
     from memory.
   - `"Found N matches… not unique"` → do not lengthen the anchor with
     more prose (invites the transcription-drift failure instead).
     Either extend to an adjacent short, structurally-unique line (a
     heading, a `step_XX` id), or use `replace_all: true` if the
     change is genuinely uniform.
2. **If the target is pathological** (a single multi-thousand-character
   line, dense repetition, or the change is large) → **use the Write
   tool to rewrite the whole file/section.** Read it, edit in-context,
   Write it back. This takes the path as a structured parameter, immune
   to the Bash/native-tool path issues (TECHNICAL_CONVENTIONS §25/§25.1)
   and sidesteps exact-substring matching entirely.

**Never drop to Git-Bash + native-Python file splicing as a fallback.**
It crosses the MSYS-bash ↔ native-Win32 path boundary
(TECHNICAL_CONVENTIONS §25.1) — a second, independent failure surface
on top of whatever made Edit fail, which is why it typically takes
2-3 attempts to land. The 2-step procedure above stays entirely within
tools whose path handling is already safe.

### Error memory (self-improvement)
When an error repeats (same type of bug twice), write the lesson:
- If it's a timeless convention → propose adding it to `TECHNICAL_CONVENTIONS.md` (flag it to the user, do not do it silently)
- If it's a specific state → add it to `CURRENT_TECHNICAL_STATE.md`

### Task splitting
If a task is too large (more than ~150 estimated lines of code, or more than 5 files), split it into sub-tasks and handle them sequentially. Never attempt a massive implementation in one go.

### Git
- Commit after every validated step (never forget)
- Conventional commit message: `feat:`, `fix:`, `refactor:`, `docs:`, `test:`
- `git add .` (never granular staging)

### Context-limit management
If the context grows too large during a long session, suggest the user start a fresh session — the short, always-current `current_status.md` allows resuming without loss, and without re-reading a large history.

### Worktree merge-back applies to numbered task files too, not only investigations

> Confirmed 2026-07-09 — the same auto-isolation mechanism documented
> in the investigation-mode skill (background jobs get placed in
> `.claude/worktrees/<job-name>/` before any instructions load) also
> affects regular, fully-numbered `step_XX_fix` work going through the
> complete brief→plan→approved→result→review cycle — not just
> lightweight investigations. Confirmed to have happened twice: once
> where a report was stranded unmerged, and once where two ENTIRE
> completed-and-reviewed task files (full PASS, one Product-Owner-tested)
> sat stranded on separate orphaned branches — each using its own local
> step-number guess, which no longer matched what `master`'s registry
> had independently assigned to those same numbers by the time anyone
> looked. This caused two real, valid pieces of work to appear
> "missing," while `master` simultaneously had fresh, never-executed
> task.md files sitting under the same numbers describing different
> content.

**Rule**: at the end of ANY step's workflow (LOW/MEDIUM/HIGH, not just
investigation-only mode) — before considering the step complete — check
whether the working directory is under `.claude/worktrees/`. If so, merge
that branch into `master` yourself, automatically, as the final step,
using the same procedure as investigation-mode
(`git merge --no-ff <branch> -m "Merge step_XX_fix: <short-name>"` from
the main checkout root) — do not leave this for the Product Owner to
notice and request later.

**Additionally**: before assigning a step number to new work, check
`git worktree list` (or equivalent) for any orphaned branches whose own
internal numbering might not match what's visible on `master` — a
number that looks free on `master` may already be in use on an
unmerged branch. Reconcile before proceeding, don't assume `master`'s
folder listing is the complete picture.

### Investigation-only mode (report-only, no task file numbering)

**Trigger**: a prompt given directly (not via `/start`) that either (a)
explicitly states "investigation only" / "report only" / "no fix", or
(b) does not reference an existing `docs/tasks/step_XX/task.md`.

**When this applies**:
- Do NOT create or number a `docs/tasks/step_XX/` folder — this is not
  a step, never assign it a step number
- Create `docs/investigations/<short-descriptive-name>/` instead (a
  subfolder, mirroring the step-folder shape but in its own separate
  namespace — never collides with real step numbering)
- Inside that subfolder: `task.md` — a scoped-down task file stating
  what to investigate and confirming explicitly "report only, no fix,
  no code changes"
- Delegate to the **developer** agent — it already has the right tools
  (Read/Grep/Glob/Bash) and is the natural code-inspecting role. No
  separate investigator role needed.
- **Correction (2026-07-09) — subagent file-write constraint
  discovered in practice**: when the developer runs as a delegated
  subagent (Task tool), the harness blocks it from writing a report
  file directly ("Subagents should return findings as text, not write
  report files"). The subagent must **return its findings as text** to
  the orchestrator. **The orchestrator itself** (not the subagent)
  then writes that text to
  `docs/investigations/<short-descriptive-name>/REPORT.md`. Do not
  instruct the subagent to write `REPORT.md` itself — it will be
  blocked and the finding will only surface as unsaved text output.
- **Model/effort: Sonnet 5, effort high** — fixed, regardless of the
  eventual fix's likely risk level. An investigation's whole value is
  its thoroughness; under-resourcing it risks a wrong premise reaching
  a task file later (already happened once this project — `step_45_fix`
  had to be corrected after its original technical premise turned out
  wrong). Do not scale this up to Opus (reserved for HIGH-risk
  implementation, not needed for reading/reporting) or down based on
  apparent simplicity.
- No `plan.md`, no `result.md`, no manager/reviewer cycle — a single
  developer pass producing `REPORT.md` is the complete deliverable.
- If the investigation's findings warrant a real fix afterward, that
  becomes its own separate, properly-numbered `docs/tasks/step_XX_fix/`
  task file at that point — never retroactively renumber the
  investigation folder itself.

### When in doubt
If a spec is ambiguous or an architectural decision is not covered by the documents:
- Do NOT invent an architecture
- Document the ambiguity in `docs/tasks/step_XX/blocked.md`
- Stop and ask the Product Owner for clarification

---

## What you never do

- Run the app or the emulator
- Code without having read current_status + conventions + current state
- Skip the investigation phase (MEDIUM/HIGH risk)
- Implement without a validated plan (MEDIUM/HIGH risk)
- Forget to commit after a validated step
- Modify `TECHNICAL_CONVENTIONS.md` without explicitly flagging it to the user
- Invent an architecture not covered by the specs
- Continue after a PASS without displaying the manual test list

---

## RULE 24 — Windows notification flag for manual approvals

When Claude Code is about to execute a bash command that requires manual approval
(any command that modifies the filesystem outside normal code files, installs packages,
runs emulator commands, or any HIGH risk action), write a notification flag BEFORE
requesting approval:

```bash
# Write the flag BEFORE asking for approval
echo "Waiting for bash approval: <brief description of command>" > APPROVAL_NEEDED.flag
# ... then proceed with the command that needs approval
# The flag is automatically deleted after the user approves and the command runs
```

After the command completes (approved or rejected), delete the flag:
```bash
del APPROVAL_NEEDED.flag 2>nul || rm -f APPROVAL_NEEDED.flag
```

This allows the background watcher (notify_watcher.py) to send a Windows notification
to the developer when manual action is required.

**Commands that MUST trigger the flag:**
- Any `flutter pub get` or package installation
- Any `gradle` build commands
- Any file deletion
- Any git operations
- Any emulator launch commands (though emulator use is prohibited per Rule 23)
- Anything with `--force` or destructive flags

**Commands that do NOT need the flag:**
- `flutter analyze`
- Reading files (`cat`, `head`, `grep`, `find`)
- Creating new source files
- Standard `dart run build_runner build`
