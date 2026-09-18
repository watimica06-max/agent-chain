# Correction campaign — plan

**The second verification round produced 26 reports.** 🔴 **13 BLOCKING ·
186 TO FIX · 270 NOTE · 14 QUESTION**, plus 49 findings of the first
round still open.

⚠️ **The fourteen questions are already settled** — 📌
`docs/verification2/decisions.md`.

**Four waves.** 🔴 **Nothing is modified before wave 3**, and 📌 **wave 4
reads the result.**

---

## Why the guards below exist

📌 **The previous correction round produced roughly one new defect for
every five fixes.** 🔴 **Its worst case is worth naming**, because every
guard here comes from it:

⚠️ **A field `## Files` was added to the spec sheet, said to carry « the
lot's `Modifies` and `Touches` ».** 🔴 **`Modifies` carries symbols and
never a file** — the Cadreur says so in its own file — **and both are a
dash on a production lot.**

📌 **The two sides agreed with each other.** ⚠️ **Nobody re-read the
line they both relied on.**

---

# Wave 1 — one plan per agent, 21 in parallel

🔴 **Twenty agents, plus one for the commands.**

📌 **A plan is raw material, not a work list** — ⚠️ **wave 2 merges the
twenty-one into one.** 🔴 **Two plans finding the same defect under two
identifiers is expected**: 📌 **do not try to avoid it, and never look
at another agent's report to do so.**

`lexicographe` · `redacteur` · `decoupeur` · `qualifieur` · `classeur` ·
`sondeur` · `assembleur` · `convertisseur` · `architecte` ·
`fusionneur` · `cadreur` · `verificateur` · `detailleur` ·
`concepteur` · `testeur` · `realisateur` · `relecteur` · `arbitre` ·
`controleur` · `diagnostiqueur`

```
READ-ONLY. Modify nothing. Write one file:
docs/verification2/plans/<agent>.md

Read:
1. `.claude-new/agents/<agent>.md` — the file to be corrected
2. The commands that invoke it:
   Select-String -Path .claude-new\commands\*.md -Pattern '<agent>'
   🔴 **Read only those.**
3. `docs/verification2/<agent>.md` — its report, both parts
4. `docs/verification2/decisions.md` — the fourteen settled questions
5. The six thematic reports, filtered to your agent:
   Select-String -Path docs\verification2\renommages.md,
     docs\verification2\fichiers.md,
     docs\verification2\chemins-amont.md,
     docs\verification2\chemins-aval.md,
     docs\verification2\passages-amont.md,
     docs\verification2\passages-aval.md -Pattern '<agent>'

⚠️ **Never `.claude/`** — 📌 **that is the chain before the refonte**:
🔴 **it has no `qualifieur`, no `concepteur`, no `testeur`**, and a plan
built against it would propose going backwards.

---

## First, judge the finding

🔴 **Every finding gets a verdict before it gets a decision.**

| Verdict | |
|---|---|
| `confirmed` | ✅ **It holds** — you read it in the files |
| `stale` | ⚠️ **It describes an earlier state** — 🔴 **cite the line that shows it is already fixed** |
| `wrong` | 🔴 **The fact is false** — 🔴 **cite the line that contradicts it** |
| `overstated` | 📌 **Real, but not at that severity** — say which |

🔴 **`stale` and `wrong` require a citation. Without one, the verdict is
`confirmed`.**

🔴 **One case is settled in advance: a finding whose only complaint is
that `modifications.md` does not record a change.** 📌 **Verdict
`moot`** — ⚠️ **that index belongs to the refonte, which is closed, and
it is no longer kept up to date.**

📌 **Say in one line what the unrecorded change is, all the same** — 🔴
**another section may find that change wrong**, and wave 2 merges the
two entries.

⚠️ **This is not a formality.** 📌 **The previous round declared nine
corrections applied that were not** — 🔴 **a verdict with nothing behind
it is how a real defect disappears.**

📌 **Only a `confirmed` gets a decision.** 🔴 **The other three say why
and stop.**

---

## Then, for a `confirmed`, write the entry

    ### <report> <id> — <short title>

    Verdict: confirmed
    Decision: <one imperative sentence>
    Where: <file L… ↔ file L…>
    Owner: <which agent applies it>
    Also in: <the other plans that carry this decision, or —>

🔴 **`Decision` is what to do, never how to word it.** ⚠️ **The agent
that applies it writes the prose.**

**When the `Where` names two files** — 🔴 **open both before deciding**,
and 📌 **quote the line from the other side inside your entry:**

    Cited: cadreur.md L753 — "`Needs`, `Produces` and `Modifies` carry
    symbols, and symbols only"

⚠️ **If you cannot quote it, you do not decide.** 🔴 **Write the entry
with `Verdict: confirmed` and `Decision: —`**, and say what you could
not verify.

📌 **This is the guard that the `## Files` failure calls for**: ⚠️ **the
decision was built on a line nobody opened.**

**`Owner` and `Follows`** — 🔴 **for a finding that spans two agents:**

📌 **`Owner` is the one that decides the form** — the agent that writes
the field, the file or the rule.

📌 **`Follows` are the ones that change their own text to match** — ⚠️
**they modify too**: 🔴 **a reader whose test keys on that field has a
line to rewrite.**

⚠️ **Never *« the other one only reads »*** — 📌 **that is true of a
handful of findings and false of most**: 🔴 **a field added on one side
is a test rewritten on four others.**

**`## To settle`** — 🔴 **a decision that turns on intent, scope or
user-facing behaviour is not yours.** 📌 **Write it in a
`## To settle` section at the end of the plan**, with what each option
costs, ⚠️ **and leave its `Decision` empty.**

---

## The twenty-first plan — the commands

🔴 **Read the six thematic reports whole**, not filtered.

📌 **Keep only the findings no agent's name appears in** — ⚠️ **a
finding that names two commands and no agent lands in no other plan.**

📌 **Same verdicts, same entry shape.** 🔴 **Write
`docs/verification2/plans/commandes.md`.**
```

---

# Wave 2 — consolidation, one invocation

🔴 **Runs once wave 1 is fully back.** ⚠️ **This is not a check on the
plans** — 📌 **it is where the twenty-one plans become one list of work.**

📌 **Three things it does**: 🔴 **merge the duplicates**, **give every
finding one owner**, **and re-read the lines the decisions rest on.**

```
READ-ONLY. Modify nothing. Write one file:
docs/verification2/plans/conflits.md

Read the twenty-one plans in `docs/verification2/plans/`.

🔴 **Plus `docs/verification2/plans/a-trancher.md`** — 📌 **the questions
the Product Owner has settled since wave 1**: ⚠️ **a `Decision:` there
supersedes what a plan said about that finding.**

🔴 **Plus, for step 3, the files their `Cited:` lines name.**

---

## 1 — Merge on `Where`, never on the identifier

🔴 **Two entries are the same defect when their `Where` share one file
and one line** — 📌 **whatever identifiers they carry, and whatever else
each names besides.**

⚠️ **They rarely cite the same set.** 📌 **Measured: `detailleur.md` F20
names four files, `passages-aval.md` F01 names six, and they overlap on
two** — 🔴 **one shared line is enough.**

⚠️ **In doubt, merge.** 📌 **A merge that was wrong shows up as one
decision that does not fit** — 🔴 **a duplicate applied twice does
not.**

⚠️ **This happens by construction**: 🔴 **the six thematic reports were
written to cross what the agent reports found**, so a defect seen from
an agent and the same defect seen from a handover carry two different
identifiers.

📌 **Measured on three reports: `detailleur.md` F20 and
`passages-aval.md` F01 are one defect.**

**Merge them into one entry:**

    ### <the identifier you keep> — <short title>

    Same as: <the other identifiers, with their reports>
    Decision: <one, and one only>
    Where: <file L… ↔ file L…>
    Owner: <one agent>
    Cited: <the quotation, from whichever entry carried it>

🔴 **Keep the entry that carries a `Cited:` line.** ⚠️ **If none does,
keep any and mark it**: 📌 **step 3 will judge it.**

🔴 **Two merged entries whose `Decision` lines differ is a conflict** —
📌 **report both, settle neither.**

---

## 2 — One owner, and every side present

🔴 **Every finding has exactly one `Owner`.**

| | |
|---|---|
| **Two plans claim `Owner`** | 🔴 **A conflict** |
| **No plan claims it** | 🔴 **Assign it**: 📌 **the agent that writes the field, the file or the rule** |

🔴 **And name every `Follows`** — 📌 **each agent whose own text has to
change to match.** ⚠️ **A `Follows` missing is a side that will not be
corrected.**

🔴 **A `Where` naming two agents must appear in both plans.** ⚠️ **When
one side is missing, write the entry it lacks:**

    ### <identifier> — <short title>   (added by consolidation)

    Decision: <what this side changes, or: read what <owner> writes>
    Where: <the line in this agent's file>
    Owner: <the other agent>
    Follows: <this agent, when it has text to change>

📌 **Why the entry exists at all**: 🔴 **so the agent knows nothing is
expected of it**, ⚠️ **rather than discovering later that a field it
reads has changed.**

---

## 3 — Re-read what each decision rests on

🔴 **For every merged entry whose `Where` names two files**: 📌 **open
the file the `Cited:` line points at, at that line, and read it.**

| | |
|---|---|
| **It says what the decision assumes** | ✅ **Nothing to report** |
| **It says something else** | 🔴 **A conflict** — quote both |
| **There is no `Cited:` line** | 🔴 **A conflict** — the decision was taken without opening the other side |

⚠️ **This is the check the previous round did not have.** 📌 **Its
failure was not two plans disagreeing** — 🔴 **it was two plans agreeing
on a line neither had read.**

---

**Your output — two tables.**

**First, the work**: 🔴 **one line per defect, after merging.**

    | # | Severity | Decision | Where | Owner | Follows | Same as |

📌 **This table is what wave 3 applies.** 🔴 **It supersedes the plans**
— ⚠️ **an agent applies this list, not its own file.**

**Then, the conflicts** — 🔴 **one section each, not a table**: 📌 **the
Product Owner writes into this file.**

    ### <identifier> — <short title>

    Kind: divergent | cited | owner
    Plans: <the plans involved>
    What is wrong: <one sentence>
    Quotations: <for a `cited` conflict, both — otherwise —>

    Arbitration:

🔴 **Leave `Arbitration:` empty.** ⚠️ **Do not resolve a conflict, and
do not suggest a resolution** — 📌 **the Product Owner writes there**,
and a conflicted entry stays out of the first table until she has.
```

---

# Wave 3 — applying

🔴 **Runs once the conflicts are arbitrated.**

**Order matters.** 📌 **The twenty agents in parallel, then the commands
one at a time.** ⚠️ **Two invocations writing `8_code.md` at once lose
each other.**

🔴 **The command order is fixed, and the prompt carries it**, so that
the last one to write does not overwrite the others.

```
Write into `.claude-new/`. One agent per invocation.

Read:
1. `docs/verification2/plans/conflits.md` — 🔴 **its first table is your
   work list**: 📌 **the lines whose `Owner` is you.**
2. `.claude-new/agents/<agent>.md` — the file you correct
3. Every file a `Where` or a `Cited:` line names
4. `docs/verification2/plans/<agent>.md` — 📌 **your plan, for context
   only**: ⚠️ **never as the list of what to apply.**

🔴 **The consolidated table supersedes the plans.** ⚠️ **Your plan may
carry an entry that was merged into another, or reassigned** — 📌
**applying it as well would do the same gesture twice.**

🔴 **Apply the lines where you are the `Owner` or a `Follows`.** 📌
**Nothing else.**

📌 **As `Owner`, you decide the form** — the field, the wording, the
rule. 📌 **As a `Follows`, you take that form as given** — ⚠️ **you
change your own text to match it, you do not redesign it.**

🔴 **A line naming you nowhere is read, never applied** — 📌 **its
presence tells you a file you read is about to change.**

---

## You may refuse

🔴 **If, opening the files, you see the plan rests on a false fact — do
not apply it.** 📌 **Say so, quote the line, and carry on with the
rest.**

⚠️ **A plan is a reading, not an authority.** 📌 **The previous round
failed exactly here**: 🔴 **a correction built on a false premise was
applied by an agent that never opened the file it named.**

---

## While you work

🔴 **Re-read the whole agent after correcting it** — ⚠️ **moving a
section breaks cross-references a grep cannot see**, and 📌 **about one
correction in five leaves something behind**: a rule stated twice, an
entry lost while repairing a list, a fix applied at one site of three.

🔴 **A replacement that fails is retried before you move on.** ⚠️ **A
correction reported as applied and never applied is the worst
outcome**: 📌 **it is believed.**

🔴 **Never propagate to a sibling agent without opening it** — 📌 **check
it has the same gesture first.** ⚠️ **Propagating without checking
created defects twice in the previous round.**

🔴 **Run `python3 .claude-new/scripts/coherence.py <your file>` after
every edit**, not at the end — 📌 **it catches a broken bold or a lost
line while the edit is still in mind.**

---

**Your report** — one table.

    | # | Applied | Where | One line |

- **`Applied`** — `yes` · `refused` · `blocked`
- **`One line`** — 🔴 **only for `refused` and `blocked`**: what you saw
```

---

# Wave 4 — the closing check, one invocation

🔴 **Runs once every agent of wave 3 has reported.** ⚠️ **Nothing in the
plan so far looks at the chain after it has been corrected** — 📌 **and
the previous round's defects were created exactly there.**

⚠️ **This is not a third verification round.** 🔴 **Two questions, and
nothing else.**

```
READ-ONLY. Modify nothing. Write one file:
docs/verification2/plans/cloture.md

---

## 1 — The script, on everything

    python3 .claude-new\scripts\coherence.py

🔴 **Report every line it returns.** 📌 **The chain returned zero before
wave 3** — ⚠️ **anything here was introduced by a correction.**

---

## 2 — Replay what spans two files

🔴 **Take every `BLOCKING` of the consolidated table, and every `TO FIX`
whose `Where` names two files.** 📌 **Read each against the corrected
files.**

⚠️ **Why those and not all of them**: 🔴 **a finding inside one file
breaks that agent; one that spans two breaks the chain** — 📌 **and a
correction applied on one side only is the failure this campaign exists
to prevent.**

| | |
|---|---|
| `gone` | ✅ **The defect is not there** |
| `standing` | 🔴 **It is** — 📌 **quote the line** |
| `moved` | ⚠️ **The correction landed and broke something adjacent** — 🔴 **quote both** |

📌 **`moved` is the one that matters.** ⚠️ **It is what the previous
round produced about fifty-five times**: 🔴 **a rule stated twice, a
cross-reference left pointing at where a rule was, an entry lost while
repairing a list, a correction applied at one site of three.**

🔴 **Look for those four shapes** around every line wave 3 touched.

---

**Your report** — one table.

    | # | Status | Where | One line |

🔴 **No new findings.** ⚠️ **A defect you meet that no BLOCKING names is
not yours** — 📌 **note it in one line at the end, and go no further.**
```

---

# What this campaign does not prove

⚠️ **Wave 4 closing clean is not « the chain works ».**

**What it establishes:**

✅ **The known BLOCKING findings are gone** · ✅ **every cross-file
`TO FIX` landed on both sides** · ✅ **the form is clean** · ✅ **the
corrections broke nothing on the lines they touched.**

**What it does not:**

🔴 **That the single-file `TO FIX` were applied well** — 📌 **nothing
replays them**, and they are most of the volume.

🔴 **That no new defect was born elsewhere** — 📌 **wave 4 looks around
the lines wave 3 touched**, not at the whole chain.

🔴 **That the chain runs.** ⚠️ **Nothing executes it**: 📌 **this whole
campaign is document reading.**

**The measure that follows** — 🔴 **one real cycle on a small feature,
end to end.** 📌 **A gate that stops, a prompt missing a parameter, a
loop that never closes: none of those is visible to a reader**, and two
verification rounds have not found one.

⚠️ **Do not open a third reading round on the strength of this one.** 📌
**Two rounds found the same volume** — 🔴 **the next gain is in running
the chain, not in reading it again.**

---

# What comes back to the Product Owner, and when

📌 **After wave 1** — 🔴 **the `## To settle` sections**: the product
decisions.

📌 **After wave 2** — 🔴 **the conflicts**, to arbitrate. ⚠️ **A
conflicted entry stays out of the work list until you settle it**, so
nothing is applied on a defect you have not seen.

🔴 **Nothing during wave 3** — 📌 **except a `refused`**, which is read
at the end with the rest.

📌 **After wave 4** — 🔴 **the `standing` and the `moved`.** ⚠️ **A
`moved` is a defect the campaign created**: 📌 **it is corrected
straight away, by the agent that made it, with wave 4's quotation in
hand.**

---

# Git, in this mode

🔴 **One worktree for the whole campaign**, created before the first
invocation and merged once at the end.

```
git worktree add ../correction-<date> -b correction/<date>
cd ../correction-<date>
mkdir docs\verification2\plans
```

🔴 **Enter the worktree before invoking**, not after a write fails — 📌
**the harness blocks a subagent's writes until the session is
isolated.**

❌ **Never pass `isolation`** — 📌 **the agents read the same files; in
wave 3 they write different ones.**

**Once every agent has reported:**

```
git add .claude-new/ docs/verification2/
git commit -m "Correction campaign <date>"
cd <main checkout root>
git merge --no-ff correction/<date>
git push
git worktree remove ../correction-<date>
```

🔴 **The commit is yours** — 📌 **the agents have no `Bash`.**
