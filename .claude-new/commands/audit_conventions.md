---
description: Read what the conventions gained during a cycle and report what it costs
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
folder.**

📌 **Paths starting with `docs/` are relative to the repository root**;
every other path is relative to the working folder.

---

## What you read

**Every `architecte/*.md`** — the conventions requests, with their
`## Verdict`.

📌 **One whose verdict is empty is untreated** — ⚠️ **read it and list
it under `### Requests still untreated`**: a request nobody answered is
worth reporting.

🔴 **Never put it in `## Requests read`** — a later pass has to read it
again once it carries a verdict.

**`docs/TECHNICAL_CONVENTIONS.md`** — 🔴 **in full.**

**`couverture.md`** — which entry each rule came from.

🔴 **On a correction cycle it is not in the working folder**: the
Architecte writes it when it derives the conventions, and that runs on
the feature folder. ⚠️ **Look for it one level up**, at the feature
folder's root, and use it from there.

📌 **The rules it traces still hold** — the conventions file is shared
by the whole project, feature cycles and correction cycles alike.

⚠️ **Absent from both** — 🔴 **findings 1, 4 and 7 cannot be made.**
**Say so under each of their headings** — *no coverage file* — and make
the others. 📌 **Finding 6 keeps running**: it reads your earlier passes
and `TECHNICAL_CONVENTIONS.md`, nothing else.

**The technical document** — 🔴 **only the entries `couverture.md`
names**, one at a time, for finding 4. 📌 **The one those entries live
in**: `couverture.md` traces to the document it was written against,
which may be the feature's `spec-technique.md` rather than this cycle's
`desc-bug.md`.

**`code/decoupage.md`** — 📌 **for finding 7 alone**, its lots'
`Anchor` lines.

**`audit-conventions.md`** at the working folder's root, if it is
there — 🔴 **your own earlier passes.**

🔴 **Nothing else.** Not the code, not the sheets — you audit what the
rules say, not whether the code follows them.

---

## What you skip

🔴 **Every request `audit-conventions.md` already names as read.** ⚠️
**Its `## Requests read` section lists them, one subsection per
pass** — read them all, and skip every path they carry.

📌 **`TECHNICAL_CONVENTIONS.md` is read every pass** — it changes, and
that is the point of the audit.

🔴 **Read your own earlier findings in full.**

---

## What you look for

**1. What the cycle added.** 🔴 **A rule the conventions carry and
`couverture.md` traces to no entry of the technical document** came
from a request, not from the corpus.

📌 **Name it, and name the request that produced it.** ⚠️ **That is a
rule nobody read before it started binding every lot.**

🔴 **Name the lot too** — the request file carries it in its name,
`architecte/detailleur-lot-04.md`. ⚠️ **On a correction cycle the line's
first column carries the request's path from the feature folder,
`bugfix-NN/architecte/detailleur-lot-04.md`** — 📌 **the lot is still
read from the file name, and the `bugfix-NN/` prefix tells which cycle
the rule came from.** 📌 **That lot was coded under the
rule as it stood, and the rule written for it governs only what
follows** — ⚠️ **say so, and leave the Product Owner to decide whether
it stays that way.**

**2. A rule no lot can follow inside its own scope.** 🔴 **One asking
for something a lot cannot supply on its own** — whatever that
something is.

📌 **The test is the scope, not the thing**: a lot produces symbols and
touches the files its `Modifies` names. ⚠️ **A rule asking for anything
beyond that — a symbol nobody produces, a declaration outside the code,
a tool nobody installed — cannot be obeyed**, and the block comes much
later, at detailing.

**3. Two rules of one section asking for different shapes.** 🔴 **Pair
them by the section of `TECHNICAL_CONVENTIONS.md` they sit in** — that
is what makes them comparable, and it is mechanical.

⚠️ **Contradicting is one telling a lot to do what the other forbids**,
not two rules a lot finds awkward together. 📌 **Say which entry each
traces to.**

**4. A rule binding something its entry does not mention.** 📌
**`couverture.md` gives the entry each rule traces to** — 🔴 **open it
and look for the thing the rule binds.**

⚠️ **A rule may say in code terms what the entry says in behaviour
terms** — that is its work, and it is not a finding. 🔴 **A finding is a
rule binding a second thing the entry never names**: another field,
another moment, another symbol.

**5. What was refused, and where it belongs.** 📌 **A verdict that
turns a request down names where the thing goes** — the code, the
tooling, the machine.

🔴 **Quote that**, and nothing more. ⚠️ **Whether it landed there is not
yours to say**: you do not read the code.

**6. A rule already reported, still unchanged.** 🔴 **Your earlier
passes name rules by their identifier** — 📌 **`TECHNICAL_CONVENTIONS.md`
is read every pass, so you see whether each still says what it said.**

⚠️ **A rule reported twice and unchanged is worth saying once more**,
under the same heading as before, marked as standing since pass `<n>`.

**7. A rule the split never meets.** 🔴 **No lot's `Anchor` cites the
entry `couverture.md` traces it to.**

📌 **That is the whole test** — the rule is well-founded, its entry
exists, and the split cut no lot from it. ⚠️ **It costs a read at every
lot and catches nothing.**

📌 **Distinct from finding 2**: there a lot meets the rule and cannot
obey it; here no lot meets it at all.

---

## What you write

**`audit-conventions.md`** at the working folder's root. 🔴 **Append,
never rewrite.**

📌 **Number your pass from the last one in the file**, or 1 if there is
none. ⚠️ **No date** — you have no clock.

🔴 **On the first pass, write the title and the two headings below**;
on any other, append your `## Pass <n>` section and add your requests
under `## Requests read`.

    # Audit of conventions — <working folder>

    ## Requests read

    ### Pass 1
    architecte/realisateur-lot-04.md

    ### Pass 2
    architecte/cadreur.md

    ## Pass 2

    ### Requests still untreated
    ### Rules the cycle added
    ### Rules no lot can follow in its own scope
    ### Contradictions
    ### Rules binding what their entry does not mention
    ### Refused, and where they belong
    ### Standing since an earlier pass
    ### Rules the split never meets

📌 **`## Requests read` is grouped by pass** — 🔴 **only your own pass's
subsection is written.**

📌 **A heading with nothing under it carries a dash.**

**One finding per line, three parts separated by ` | `:**

    <the rule's identifier> | <what you found> | <what it rests on>

🔴 **The identifier comes first**, so a later pass can match on it. ⚠️
**The third part names an entry, a request, or a second rule** —
whatever the finding was read from.

**Under `### Requests still untreated`, one path per line.**

⚠️ **No recommendation, no correction.** 🔴 **You never edit
`TECHNICAL_CONVENTIONS.md`** — that is the Architecte's, and only
through a request.

---

## What you never do

- 🔴 **Change a conventions file, or a request**
- 🔴 **Rewrite an earlier pass**
- 🔴 **Read a request `## Requests read` already names**
- 🔴 **Judge whether a rule is good** — only whether it can be followed,
  whether it rests on something, and whether it fires
- 🔴 **Invoke an agent**
- Touch the code or the sheets
