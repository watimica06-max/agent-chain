---
description: Run the autonomous agent workflow for the next pending task in docs/tasks/
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
---

Act as the orchestrator of the Nutrition App development and execute the workflow below for the next pending task in `docs/tasks/`.

## Phase 0 — Task identification (always)
1. Read `docs/current_status.md`
2. Read `docs/TECHNICAL_CONVENTIONS.md` and `docs/CURRENT_TECHNICAL_STATE.md`
3. Identify the next step to handle in `docs/tasks/` (the first step whose `task.md` exists but has no `review.md` in PASS)
4. Read the **risk level** declared in `task.md` (LOW / MEDIUM / HIGH)
5. If no pending task: inform the user and stop

## The workflow depends on the risk level

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
| Orchestrator (this session) | sonnet (alias) | high | Routing, file reading, dispatch |
| Manager | sonnet (alias) | high (fixed in frontmatter — manager never runs on LOW, so no conditional needed) | Judgment/consistency-checking role, not generation |
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

If no pending task exists, say so and stop.