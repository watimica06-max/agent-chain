---
description: Sort the product file's blocks by nature, for the Convertisseur
allowed-tools: Read, Grep, Glob, Write, Bash
argument-hint: "<feature folder name>"
---

Act as the orchestrator, in **upstream mode**.

**This command invokes no agent.** 🔴 **It writes `desc-par-nature.md`
— the product file's blocks, sorted under the nature the classeur gave
each one.** 📌 **The Convertisseur translates one nature at a time, and
this is where each nature's blocks are gathered.**

🔴 **It writes the file afresh on every run** — ⚠️ **a block that
changed may have changed nature too**, and a file kept from an earlier
run would file it under the old one.

**The argument is mandatory**: the feature folder name. Without it, ask
for it and stop — never guess which feature is meant.

Feature folder: `docs/features/$ARGUMENTS/`

---

## What you read

🔴 **`desc-produit.md`, to copy its blocks — never to judge them.**

⚠️ **`CLAUDE.md`'s standing reading rules apply**: never open
`CURRENT_TECHNICAL_STATE.md` or `CALIBRATION_RISK_LEVEL.md`.

---

## Before anything else

🔴 **Grep `-c '^Nature:$'` in `desc-produit.md`** — it must return zero.

⚠️ **Anything else means a block was left unclassed.** 📌 **Grep
`-B1 '^Nature:$'` to say which**, say `/3b_nature` has to run, and
stop.

🔴 **File every root `questions-*.md`**, by `git mv`:

    git mv docs/features/<name>/questions-<agent>-NN.md \
           docs/features/<name>/questions/<agent>/

📌 **This command reads none of them.** 🔴 **A questions file stays at
the root only while it waits to be answered or integrated** — ⚠️ **the
next one written has to be the only one there**, or the next command
cannot tell which one waits.

📌 **Create `questions/<agent>/` if it does not exist**; nothing to file
is a normal outcome.

---

## What you write

**`desc-par-nature.md`, at the feature folder's root, replaced whole:**

    # Product file by nature

    ## model

    ### B3 — Race segment structure
    Nature: model

    <its text>

    ## persistence

    *(none)*

🔴 **The eight natures, in this order, one heading each** — `model`,
`persistence`, `calculation`, `transition`, `external exchange`,
`synchronisation`, `presentation`, `access`. 📌 **A nature no block carries still gets its
heading**, with `*(none)*` under it.

🔴 **Under each, every block whose `Nature:` line carries it**, in the
product file's order. 📌 **A block runs from its `### B` line to the
next heading of any level.**

🔴 **Copied as it stands, by script — never retyped.** ⚠️ **A block
retyped is a block that may have changed**, and nothing downstream
would see it.

🔴 **Except its marker**: strip a trailing `NEW` or `MODIFIED` from
the `### B` line. ⚠️ **It says what moved on the Rédacteur's last
turn**, and `/6_convertit` compares these blocks against the last ones
it translated — 📌 **a marker coming or going would read as a change.**

⚠️ **A `Nature:` value that is not one of the eight** — say which
block, and stop without writing.

**Then count** `^### B` in both files. 🔴 **The two counts match** —
⚠️ **a difference means a block was lost or doubled**; say so, and
stop without committing.

---

## Git, in this mode

📌 **No agent, no worktree** — this command writes in place.

🔴 **Commit the feature folder**, `chore: product file by nature`, and
push.

⚠️ **A push that fails — diverged remote, no network — is reported, not
retried and not worked around.** The commit holds locally; say so and
carry on.

---

## What you relay

📌 **How many blocks under each nature**, one line.

**What to run next** — 📌 **indications for the Product Owner.**
⚠️ **You relay them; you run nothing after this command.**

📌 `/6_convertit`.

🔴 **Nothing else is yours**: no phase chain, no risk level, no
`TaskCreate`.
