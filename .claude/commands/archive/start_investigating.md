---
description: Run a report-only investigation, no fix, no task numbering
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
argument-hint: "<what to investigate, in full>"
---

Act as the orchestrator, in **investigation mode**: report only, no
fix, no step number, no manager/reviewer cycle.

**The argument is mandatory** — the brief itself, as text: what to
establish, against what, and what would count as an answer. Without it,
ask for it and stop. Do not reword it into something narrower.

## What you read

Nothing but the brief. You do not read the code — the developer does
that. `CLAUDE.md`'s standing reading rules apply: never open
`CURRENT_TECHNICAL_STATE.md` or `CALIBRATION_RISK_LEVEL.md`.

## How it runs

🔴 **Never create or number a `docs/tasks/step_XX/` folder.** This is
not a step. Create
`docs/investigations/<short-descriptive-name>/` — its own namespace,
which cannot collide with step numbering.

1. Write `docs/investigations/<name>/task.md`: the brief, scoped, and
   an explicit line stating **report only, no fix, no code changes**.
2. Delegate to the **developer** agent — it has the right tools
   (Read/Grep/Glob/Bash) and is the natural code-inspecting role. No
   separate investigator role exists or is needed.
   - `model: sonnet`, `isolation: "worktree"`,
     `run_in_background: false`.
   - 🔴 **`sonnet` regardless of how risky the eventual fix looks** —
     this is outside the risk table. An investigation's whole value is
     its thoroughness, but Opus is for HIGH-risk implementation, not
     for reading and reporting. Do not scale it either way on apparent
     simplicity. *(`step_45_fix` had to be corrected after its original
     technical premise turned out wrong — under-resourcing an
     investigation lets a false premise reach a task file.)*
3. 🔴 **The subagent returns its findings as text; YOU write the
   file.** The harness blocks a delegated subagent from writing a
   report ("Subagents should return findings as text, not write report
   files"). Write its text to
   `docs/investigations/<name>/REPORT.md` yourself. If you instruct the
   subagent to write it, it is blocked and the finding survives only as
   unsaved output.
4. Commit, then **merge the worktree back into `master` yourself** —
   from the main checkout root, not the worktree path:
   ```
   git merge --no-ff <worktree-branch> -m "Merge investigation: <name>"
   ```
   Confirm `docs/investigations/<name>/` is visible on `master` before
   calling it done. ⚠️ **Never `git push`, never open a PR** — this
   repo has no remote, and that path silently strands the report on an
   unmerged branch. It went unnoticed across several investigations.

No `plan.md`, no `result.md`, no manager, no reviewer. One developer
pass producing `REPORT.md` is the whole deliverable.

📌 If the findings warrant a fix, that becomes its own numbered
`docs/tasks/step_XX_fix/` at that point. Never renumber the
investigation folder itself.
