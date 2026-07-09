---
name: investigation-mode
description: Report-only investigation workflow for the Nutrition App orchestrator — creates docs/investigations/<name>/ instead of a numbered task step, produces REPORT.md, no fix applied. Use when asked to investigate or report only, or given a prompt that doesn't reference an existing docs/tasks/step_XX/task.md.
---

# Investigation-only mode (report-only, no task file numbering)

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