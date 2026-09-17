---
description: Split the product file by genre, then sort the behaviours by nature
allowed-tools: Read, Grep, Glob, Write, Bash
argument-hint: "<feature folder name>"
---

Act as the orchestrator, in **upstream mode**.

**This command invokes no agent.** 🔴 **Two mechanical moves, in this
order:**

**1. The split by genre** — 📌 **the product file's blocks, sorted into
one file per genre.** ⚠️ **Only the behaviours go on through the
chain**; the other five go each to the reader that needs them.

**2. The sort by nature** — 📌 **the behaviour blocks, under the nature
the classeur gave each one.** 🔴 **The Convertisseur translates one
nature at a time**, and this is where each nature's blocks are
gathered.

🔴 **Both files are written afresh on every run** — ⚠️ **a block that
changed may have changed genre or nature too**, and a file kept from an
earlier run would file it under the old one.

📌 **The product file stays the master.** 🔴 **What this command writes
are views** — ⚠️ **a block filed under the wrong genre is never lost**,
and the next run puts it right.

**The argument is mandatory**: the feature folder name. Without it, ask
for it and stop — never guess which feature is meant.

Feature folder: `docs/features/$ARGUMENTS/`

---

## What you read

🔴 **`desc-produit.md`, to copy its blocks — never to judge them**, and
`par-genre/comportements.md`, which you have just written.

📌 **Greps and copies** — ⚠️ **you read no block to decide anything.**

⚠️ **`CLAUDE.md`'s standing reading rules apply**: never open
`CURRENT_TECHNICAL_STATE.md`.

---

## Before anything else

🔴 **First, the grid has to have closed.** 📌 **A
`questions-sondeur-NN.md` holding no `### Q`, at the root or filed**,
and — when the feature attaches to the global — 📌 **a
`questions-existant-NN.md` too.** ⚠️ **Neither there, or one holding
questions** → 🔴 **stop**: say to run `/4_grille`.

⚠️ **This command is what closes the upstream** — 📌 **it writes the
views every later step reads**, and a product file still open would be
split on a state about to change.

🔴 **Grep `-c '^Genre:$'` in `desc-produit.md`** — it must return zero.
⚠️ **Anything else means a block was left unqualified**: 📌 say which,
say `/3a_genre` has to run, and stop.

🔴 **Then every block carrying `Genre: comportement` has a filled
`Nature:`** — 📌 `grep -B1 '^Nature:$'`, keeping the ones whose `Genre:`
says `comportement`. ⚠️ **One hit and you stop**: say which, and that
`/3b_nature` has to run.

📌 **A block of any other genre carries an empty `Nature:`, and that is
right** — 🔴 **only a behaviour has one.**

🔴 **Grep `^### Q` in each before touching it** — 📌 **a file holding
questions is not yours to file**: ⚠️ **it waits on an answer, or its
answers were never integrated.** 🔴 **Stop and say which.**

📌 **Filed, it is read by no command again** — ⚠️ **and its answers are
lost for good.**

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

## What you write — 1. The split by genre

**Six files, under `par-genre/` in the feature folder, replaced
whole:**

| File | Who reads it |
|---|---|
| `par-genre/comportements.md` | 🔴 **This command's second move**, then the Convertisseur |
| `par-genre/transverses.md` | 📌 **Every nature invocation of the Convertisseur** |
| `par-genre/directives.md` | The Architecte |
| `par-genre/references.md` | The Convertisseur — its Text section |

🔴 **The file name is the genre, plural, without accent, a hyphen for a
space** — 📌 `référence` → `references.md`, `hors périmètre` →
`hors-perimetre.md`. ⚠️ **You grep the genre as the block writes it,
accents included** — 🔴 **`^Genre: référence$`**, never the file name.

| `par-genre/hors-perimetre.md` | The Convertisseur — its preamble |
| `par-genre/recette.md` | 🔴 **The Product Owner**, handed back by `/9_controle` |

🔴 **One grep per genre** — `grep -B1 '^Genre: <genre>$'` — 📌 **and each
block copied from its `### B` line to the next heading of any level.**

🔴 **Copied as it stands, by script — never retyped.**

🔴 **Delete the previous run's six files first** — 📌 **a genre that no
longer has any block would otherwise keep the file it had.** ⚠️ **A
genre with no block gets an empty file**, never no file: its absence
would read as *the split did not run*.

⚠️ **A `Genre:` value that is not one of the six** — 📌 say which block,
and stop without writing.

**Then count** `^### B` across the six files and in `desc-produit.md`.
🔴 **The two counts match** — ⚠️ **a difference means a block carries no
genre, or was copied twice**; say so, and stop without committing.

---

## What you write — 2. The sort by nature

**`desc-par-nature.md`, at the feature folder's root, replaced whole**
— 🔴 **from `par-genre/comportements.md`, never from the product
file**: 📌 **only a behaviour has a nature.**

    # Product file by nature

    ## model

    ### B3 — Race segment structure
    Genre: comportement
    Nature: model

    <its text>

    ## persistence

    *(none)*

🔴 **The eight natures, in this order, one heading each** — `model`,
`persistence`, `calculation`, `transition`, `external exchange`,
`synchronisation`, `presentation`, `access`. 📌 **A nature no block
carries still gets its
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

**Then count** `^### B` in `desc-par-nature.md` and in
`par-genre/comportements.md`. 🔴 **The two counts match** — ⚠️ **a
difference means a block was lost or doubled**; say so, and stop
without committing.

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

📌 **How many blocks under each genre**, one line — 🔴 **then how many
under each nature.**

**What to run next** — 📌 **indications for the Product Owner.**
⚠️ **You relay them; you run nothing after this command.**

📌 `/6_convertit`.

🔴 **Nothing else is yours**: no phase chain.
