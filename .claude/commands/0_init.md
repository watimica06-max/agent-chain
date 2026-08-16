---
description: Create the upstream scaffolding for a brand-new application
allowed-tools: Read, Glob, Write, Bash
---

Create, and nothing else:

- `docs/PRODUIT_GLOBAL.md` — with `# Application` as its only line
- `docs/features/` — empty
- `docs/process/GRILLE_CADRAGE_PRODUIT.md` — only if absent; never
  overwrite it

🔴 **Stop if `docs/PRODUIT_GLOBAL.md` already exists.** This command is
for a new application, and overwriting the global would lose every
domain in it.

Then commit alone: `docs: init upstream scaffolding`.
