---
description: Create the scaffolding a brand-new application needs before the chain can run
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

Create, and nothing else:

**Upstream** — what the product chain reads and writes:

- `docs/PRODUIT_GLOBAL.md` — with `# Application` as its only line
- `docs/features/` — empty
- `docs/process/GRILLE_CADRAGE_PRODUIT.md` — only if absent; never
  overwrite it
- `docs/process/GRILLE_FERMETURE_TECHNIQUE.md` — same rule; the
  Convertisseur loads it by name

**In `.gitignore`, at the project root** — 🔴 **append if the lines are
absent**, never rewrite the file:

    docs/features/*/stop.md
    docs/features/*/stop1.md

📌 **`/cycle` creates `stop1.md` in each feature folder.** Renaming it
to `stop.md` halts the chain before the next phase; neither is ever
committed.

**Downstream** — what the code chain reads and writes:

- `docs/CURRENT_TECHNICAL_STATE.md` — with `# Technical state` as its
  only line. 🔴 **The Cadreur blocks without it**, and the Réalisateur
  writes into it from the first lot
- `docs/TECHNICAL_CONVENTIONS.md` — 🔴 **not created empty.** It holds
  the project's own coding conventions, and the Détailleur, the
  Réalisateur and the Relecteur all read it. **Say it has to be written
  by hand before `/7_decoupe` runs**, and create nothing

🔴 **Stop if `docs/PRODUIT_GLOBAL.md` already exists.** This command is
for a new application, and overwriting the global would lose every
domain in it.

**Then report what the Product Owner still has to provide before the
chain runs end to end:**

- `docs/TECHNICAL_CONVENTIONS.md`, written by hand
- the `technical-state-format` skill, which the Réalisateur loads
  before writing to `CURRENT_TECHNICAL_STATE.md`

📌 **Neither blocks the upstream chain** — only `/7_decoupe` onward.

Then commit alone: `chore: scaffolding for the chain`, and push.

📌 **No agent, no worktree** — this command writes in place and
commits.
