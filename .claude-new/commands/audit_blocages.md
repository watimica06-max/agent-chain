---
description: Read a cycle's blocking files and report what recurs across them
allowed-tools: Read, Grep, Glob, Edit, Write
argument-hint: "<feature folder name>"
---

Act as the orchestrator. **You do this yourself — no agent.**

📌 **Run by hand, whenever the Product Owner asks.** 🔴 **No command
calls it**, and it changes nothing: it reads and it reports.

**The argument is mandatory**: the feature folder name. Without it, ask
for it and stop.

🔴 **The working folder is the highest `bugfix-NN/` in it, if there is
one; the feature folder itself otherwise.** 📌 **One audit per working
folder** — a correction cycle's blocks are audited apart from the
feature's.

📌 **Every path below is relative to the working folder.**

---

## What you read

**Every `blocked_*-NN.md` of the working folder** — the settled ones,
numbered. 🔴 **Four places**: `code/**/`, `cadrage-produit/` *(the
sondeurs)*, the folder's own root *(`blocked_architecte`,
`blocked_diagnostiqueur`)*, and `investigation/` *(a `/diagnostique`
phase 1)*.

⚠️ **A glob on `code/**/` alone misses three families** — 📌 **and the
audit would report a feature as having blocked on nothing.**

📌 **And every `blocked_*.md` without a number, in the same four
places** — one still standing. ⚠️ **Read it and list it under
`### Still open`**: a block waiting for a decision is worth reporting,
and its own findings wait with it.

🔴 **Never put it in `## Files read`** — it is not finished, and a
later pass has to read it again once it carries a decision.

**`audit-blocages.md`** at the working folder's root, if it is there —
🔴 **your own earlier passes.**

🔴 **Nothing else.** Not the code, not the sheets, not the reports —
you audit what the blocks say, not whether they were right.

---

## What you skip

🔴 **Every file `audit-blocages.md` already names as read.** ⚠️ **Its
`## Files read` section lists them, one subsection per pass** — read
them all, and skip every path they carry.

📌 **That is what makes this cheap to repeat.** 🔴 **But read your own
earlier findings in full** — a pattern shows across passes, and one
pass alone would not see it.

---

## What you look for

**1. What recurs.** 🔴 **Two blocks that name one same symbol, file or
module are one finding.**

📌 **Take the names from each block's `## Where`** — that field names
them exactly. ⚠️ **Never group on what the blocks are about**: that is a
judgement, and two blocks both about *a widened contract* may share no
name at all.

📌 **Say the shared name, and list the blocks that carry it.** 🔴 **The
name is what a later pass matches on** — write it exactly as the block
does.

🔴 **A name may be shared across passes.** 📌 **Your earlier
`### Names carried by more than one block` sections hold the names
already seen**: a block read this pass carrying one of them joins that
group, and you say which pass first named it.

⚠️ **A name seen once before and once now is a finding** — a pass alone
would call each of them single.

**2. A decision naming nothing it rests on.** 🔴 **A decision names a
rule by its identifier, an entry by its number, or a symbol where the
same problem is already settled.**

⚠️ **Naming none of the three, it invented something** — name the
block, and quote what it says instead. 📌 **A mention with no
identifier does not count**: *the conventions require it* names
nothing.

📌 **Blocks settled before the Arbitre existed carry no such
citation** — 🔴 **say so once and pass over them**: the finding is about
what the Arbitre writes.

🔴 **A decision handed back cites nothing either, and is not one** —
it belongs to finding 4. ⚠️ **This finding is about a decision that
settles**.

**3. A block asking for something outside its author's reach.** 🔴
**Read its `## To resume` literally**: what does it ask for, and who
could give it?

📌 **Each agent owns one thing** — the Cadreur the split, the
Vérificateur its order, the Détailleur a sheet, the Réalisateur the
code of one lot, the Relecteur its verdict. 🔴 **A block asking for
what an agent before its author owns is one**, whatever it asks for.

⚠️ **If it asks for nothing its author could not give itself, it is not
one** — do not infer.

**4. What was handed back.** 📌 **A `## Decision` opening on *not
settled here*.** 🔴 **Quote the reason it gives**, and nothing more —
the Arbitre wrote which behaviour it turned on, or what the corpus does
not say.

⚠️ **Never supply a reason it does not give.**

**5. Two decisions asking for different shapes**, on blocks that share
a name. 🔴 **Only there** — the shared names give you the pairs, and
two blocks sharing no name are not comparable.

⚠️ **Different is what the decisions tell the agent to do**, not how
they word it.

🔴 **A shared name may span two passes.** 📌 **Your earlier
`### Names carried by more than one block` holds the names you have
already seen**: a block read this pass carrying one of them belongs to
that group. ⚠️ **Re-open the earlier blocks it names** — that is the
one case where you read a file `## Files read` lists.

---

## What you write

**`audit-blocages.md`** at the working folder's root. 🔴 **Append,
never rewrite** — earlier passes are the record.

📌 **Number your pass from the last one in the file**, or 1 if there is
none. ⚠️ **No date** — you have no clock, and the order is what
matters.

🔴 **On the first pass, write the title and the two headings below**;
on any other, append your `## Pass <n>` section and add your files
under `## Files read`.

    # Audit of blocks — <working folder>

    ## Files read

    ### Pass 1
    code/lot-10/blocked_realisateur-01.md
    code/lot-10/blocked_realisateur-02.md

    ### Pass 2
    code/blocked_detailleur-01.md

    ## Pass 2

    ### Still open
    ### Names carried by more than one block
    ### Decisions resting on nothing
    ### Blocks asking outside their author's reach
    ### Handed back
    ### Decisions asking for different shapes

📌 **`## Files read` is grouped by pass** — 🔴 **only your own pass's
subsection is written**, the earlier ones stay untouched.

📌 **A heading with nothing under it carries a dash** — 🔴 an empty
heading says *looked at, found nothing*, its absence says *not looked
at*.

**One finding per line, three parts separated by ` | `:**

    <what you found> | <the blocks> | <the field, quoted>

🔴 **The first part opens on the name, the rule or the symbol the
finding turns on**, so a later pass can match on it. ⚠️ **Under
`### Names carried by more than one block`, the first part is that name
and nothing else.**

**Under `### Still open`, one path per line** — nothing else to say
about a block that has no decision yet.

⚠️ **A finding you cannot anchor in a quoted field is not one** —
leave it out.

⚠️ **No recommendation, no correction.** 🔴 **You report what the blocks
say**; what to do about it is the Product Owner's.

---

## What you never do

- 🔴 **Change a blocking file** — not even one still open
- 🔴 **Rewrite an earlier pass**
- 🔴 **Read a file `## Files read` already names** — ⚠️ **except when
  finding 5 sends you back to one**
- 🔴 **Judge whether a decision was right** — only whether it rests on
  something
- 🔴 **Invoke an agent**
- Touch the code, the sheets or the reports
