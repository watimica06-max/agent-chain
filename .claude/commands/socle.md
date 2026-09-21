---
description: Create the scaffolding a brand-new application needs before the chain can run
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

Create, and nothing else:

**Upstream** — what the product chain reads and writes:

- `docs/PRODUIT_GLOBAL.md` — with `# Application` as its only line
- `docs/features/` — empty

**In `.gitignore`, at the project root** — 🔴 **append if the lines are
absent**, never rewrite the file:

    docs/features/*/stop.md
    docs/features/*/stop1.md

📌 **A `stop.md` in a feature folder halts the command that reads it,
before its next step.** 🔴 **`stop1.md` is the same file disarmed** — 📌
**the Product Owner renames one into the other to halt and to resume.**
⚠️ **Neither is ever committed**, which is why both are ignored.

**Downstream** — what the code chain reads and writes:

- `docs/CURRENT_TECHNICAL_STATE.md` — with `# Technical state` as its
  only line. 📌 **Two agents write into it — the Réalisateur from the
  first lot, the Arbitre for the platform trap it settles a block
  with** — and the Détailleur, the Diagnostiqueur and the Arbitre read
  it. ⚠️ **Not the Cadreur**: it establishes what the code carries by
  grep
- `docs/TECHNICAL_CONVENTIONS.md` — 🔴 **create nothing.** 📌 **The
  Architecte writes it, at `/conventions`** — ⚠️ **which runs by hand
  after `/6_convertit` and before `/7_lots`.** 🔴 **Say so**

🔴 **Stop if `docs/PRODUIT_GLOBAL.md` already exists.** This command is
for a new application, and overwriting the global would lose every
domain in it.

**Then report what the Product Owner still has to provide before the
chain runs end to end:**

- `docs/TECHNICAL_CONVENTIONS.md` — 📌 **by running `/conventions`**,
  not by hand
- the `technical-state-format` skill, which the Réalisateur and the
  Arbitre load before writing to `CURRENT_TECHNICAL_STATE.md`

📌 **Neither blocks the upstream chain** — only `/7_lots` onward.

Then commit alone: `chore: scaffolding for the chain`, and push.

📌 **No agent, no worktree** — this command writes in place and
commits.
