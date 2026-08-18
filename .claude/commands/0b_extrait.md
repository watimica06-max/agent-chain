---
description: Build the global product document from existing code, domain by domain
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
argument-hint: [domain list file, or a single domain name]
---

# MODE EXTRACTION

Act as the orchestrator.

`$ARGUMENTS` — the domain list, or a single domain name to re-run one
that failed.

*Runs once, when taking over a codebase that has no global product
document.*

## What you receive

**A domain list file.** It names the application pass, the domains in
order, their folders, and what is excluded.

🔴 **Without it, extract nothing. Stop and say so.**

📌 **The domain list is a product decision, never derived from the
tree** — a folder can hold two subjects, a subject can span three
folders, a folder can be a lifecycle stage. It comes from an
investigation of `lib/` plus the Product Owner's arbitration.

📌 **The global is `docs/PRODUIT_GLOBAL.md`.** Every pass writes there;
the first one creates it.

## The sequence

**Each pass is one invocation of the `extracteur` subagent:**

```
Agent(
  subagent_type="extracteur",
  model="sonnet",
  description="Extract <domain>",
  prompt="Domain: <name>. Folders: <paths>."
)
```

❌ **Never pass `isolation`** — every pass writes into the same global,
and a fresh branch per pass would not see what the previous one wrote.

🔴 **Commit anything uncommitted under `docs/` first** — a worktree
branches from the last commit, and the domain list may have just been
edited by hand.

🔴 **Then create a worktree from local `HEAD`, and register it:**

    git worktree add .claude/worktrees/<name> HEAD

⚠️ **Never let the tooling branch it for you** — its default base is
`origin/master`, which can sit several commits behind local. An agent
would then work on stale content and its output would have to be
discarded.

📌 **One worktree for every pass**, not one per pass. Enter it before
the first, not after a failure.

**When the last pass is done:** `git merge --no-ff <branch>` from the
main checkout root, then `git worktree remove <path>`.

**1. Application pass** — what the code carries without belonging to a
domain. 🔴 **Name its folders in the prompt**, as for a domain; the
domain list carries them. It goes at the top of the global.

**2. Each domain, in the list's order.** 🔴 **Name the domain and its
folders in the prompt** — the Extracteur reads the code, never the
domain list.

🔴 **Sequential, never parallel.** Each domain sees the ones before it
and tags fewer unresolved references.

**3. Rewiring pass** — 🔴 **no domain, no folders**: say so in the
prompt. The Extracteur reads the global in full and resolves every
`<<REF:name>>` left behind.

## Between two passes

**Check the previous pass wrote.** Grep its domain title in
`docs/PRODUIT_GLOBAL.md` — one call, and without it a failed pass goes
unnoticed and its domain is simply missing.

⚠️ **A `blocked_extracteur.md` next to the global means the pass could
not run** — treat it as a failure and carry on to the next domain.

⚠️ **If a pass does not see what the previous one wrote**, you are in a
worktree that was not merged. Merge before continuing.

**On failure: carry on, do not stop.** Domains are independent.

📌 **Report the failed domains at the end** — the Product Owner re-runs
those alone. ⚠️ Until then the rewiring pass stays incomplete: `<<REF:name>>`
tags pointing at a missing domain will not resolve.

## What you report

- Domains written, domains failed
- **Tag counts by type** — `<<REF:name>>`, `<<ORPHAN>>`, `<<HARD_STYLE>>`,
  `<<HARD_TEXT>>`, `<<DOUBT>>`

📌 The Product Owner collects them by script.

## What you never do

- 🔴 **Decide the breakdown** — it is a product decision
- 🔴 **Rewrite what an Extracteur produced**
- 🔴 **Touch the excluded folders** named in the domain list
- 🔴 **Run this mode a second time** on a codebase that already has a
  global
