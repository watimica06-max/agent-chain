---
description: Split product blocks carrying more than one trigger
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
argument-hint: "<feature folder name>"
---

Act as the orchestrator, in **upstream mode**.

**This command invokes `decoupeur`, once** — 📌 **a second time only
when its list of blocks comes back short**, see *Once it has reported*.

📌 **It runs between `/2_structure` and `/4_grille`, every turn.** 🔴 **A
block the Rédacteur just wrote or changed may carry two triggers**, and
the sondeurs would probe it as one.

**The argument is mandatory**: the feature folder name. Without it, ask
for it and stop — never guess which feature is meant.

Feature folder: `docs/features/$ARGUMENTS/`

---

## What you read

🔴 **Greps, and nothing else.** 📌 **You never open a block.**

⚠️ **`CLAUDE.md`'s standing reading rules apply**: never open
`CURRENT_TECHNICAL_STATE.md`.

---

## Before anything else

🔴 **Does `blocked_decoupeur.md` sit in the feature folder?**

| | What you do |
|---|---|
| Absent | 📌 Carry on |
| Its `## Decision` is empty | 🔴 **Stop** — say the blocking file still stands, and that its `## Decision` is to fill |
| Its `## Decision` is filled | 🔴 **Stop** — say `/2_structure` has to run first |

⚠️ **Read that one heading, nothing else.** 🔴 **A filled decision is
`/2_structure`'s alone** — 📌 **the Rédacteur reads the file and applies
it, and `/2_structure` renames it.** ⚠️ **The decoupeur never sees the
file** — 🔴 **the prompt never names it.**

🔴 **Grep `Clarification needed` in `desc-produit.md`.**

⚠️ **One hit and the command stops.** 📌 **Say which blocks carry
one**, and that `/2_structure` has to run first.

🔴 **Grep `^### Q` in each root `questions-*.md` whose prefix is not
`architecte` before touching it** — 📌 **a file holding questions is
not yours to file**: ⚠️ **it waits on an answer, or its answers were
never integrated.** 🔴 **Stop and say which.** 📌 **The architecte's is
the one exception** — ⚠️ **it is `/conventions`'s, not this chain's**,
and a `### Q` in it says nothing about the run; 🔴 **read the root as if
it were not there** — and leave it there, see below.

🔴 **File every root `questions-*.md`**, by `git mv`:

    git mv docs/features/<name>/questions-<agent>-NN.md \
           docs/features/<name>/questions/<agent>/

⚠️ **Never `questions-architecte-*.md`** — 🔴 **leave it at the root**:
📌 **it waits for `/conventions`, which is the only command that reads
it.**

📌 **This command reads none of them.** 🔴 **A questions file stays at
the root only while it waits to be answered or integrated** — ⚠️ **the
next one written has to be the only one there**, or the next command
cannot tell which one waits.

📌 **Create `questions/<agent>/` if it does not exist**; nothing to file
is a normal outcome.

---

## Which blocks it looks at

🔴 **First, `desc-produit.md` has to be there.** 📌 **One glob** — ⚠️
**absent, you stop and name the file**: `/2_structure` has not run.

**Until the grid has run once — no `questions-sondeur-*.md` anywhere:**
🔴 **every block.** 📌 **The prompt says *every block*, in those
words** — ⚠️ **the agent keys on them**, and a prompt naming no block
names nothing.

⚠️ **The markers are still there, whatever earlier turns did** — 📌 **the
Rédacteur strips them only once a grid turn has consumed them.** 🔴 **So
they say nothing about what you have already looked at**, and every
block is yours until the grid has run.

**Later turns — two greps in `desc-produit.md`:**

| Grep | What it names |
|---|---|
| `grep '^### .*NEW'` | The blocks created since the last turn |
| `grep '^### .*MODIFIED'` | The blocks changed since |

🔴 **Anchored on the title line.** ⚠️ **A bare `NEW` matches prose
inside a block**, and would name one carrying no marker at all.

📌 **A block neither grep names was already looked at**, and has not
moved since.

⚠️ **Do not grep the questions file** — 🔴 **a block an answer touched
carries `MODIFIED`**, and the second grep finds it.

📌 **Neither grep returns anything** — 🔴 **invoke nothing.** 📌
**Commit what the filing moved, if anything, and push** — no worktree.
Say there is nothing to split, and go to *What you relay*.

---

## Git, before invoking

🔴 **Commit the feature folder before creating the worktree:**

    git add docs/features/<name>/ && git commit -m "chore: answers"

⚠️ **The Product Owner fills `Answer:` fields by hand, outside this
session.** A worktree branches from the last commit — uncommitted
answers are invisible inside it.

📌 **Nothing to commit is a normal outcome** — carry on.

🔴 **Then create a worktree from local `HEAD`, and register it:**

    git worktree add .claude/worktrees/<name> HEAD

⚠️ **Never let the tooling branch it for you** — its default base is
`origin/master`, which can sit several commits behind local. The agent
would then work on stale content and its output would have to be
discarded. *(Seen once: a whole invocation lost that way.)*

📌 **Enter the worktree before invoking**, not after a write fails —
the harness blocks a subagent's writes until the session is isolated.
*(Measured on three phases: the agent does the full job, cannot write,
and the whole invocation is redone.)*

---

## The invocation

```
Agent(
  subagent_type="decoupeur",
  model="opus",
  description="Split <name>",
  prompt="The product file: docs/features/<name>/desc-produit.md.
          Look at these blocks: <B7, B28 — or: every block>."
)
```

🔴 **Never paraphrase its process** — not its rule, its checks, its
output. It reads its own instructions.

❌ No `effort` parameter. ⚠️ **`run_in_background` may not exist
either** — in this environment the Agent tool always runs async and
notifies on completion. Do not pass it; wait for the notification.

---

## Once it has reported

🔴 **A `blocked_decoupeur.md` it wrote stays at the unnumbered name.**
📌 **You rename nothing** — ⚠️ **it waits for `/2_structure`, which
applies its decision and renames it**; 🔴 **left there, it stops this
command until then.**

🔴 **Compare the list of blocks it says it looked at against the list
you named.** ⚠️ **They have to match** — 📌 **a short list is a partial
sweep**, and nothing else can see it: you may not open a block to
check. ⚠️ **On a turn whose prompt said *every block***, its list is
what tells you it reached the end.

🔴 **A short list and no blocking file: invoke the decoupeur again on
the blocks it did not reach**, and nothing else — 📌 **here, still
inside the worktree.** ⚠️ **Once *Git, once it has reported* has run,
the worktree is merged and removed**: a second invocation after it
would write outside any worktree, where the harness blocks the agent's
writes — 📌 the whole invocation lost, as *Git, before invoking* says.
📌 **Twice at most** — ⚠️ **still short at the second, invoke nothing
more**: 🔴 **say so in *What you relay***.

🔴 **A short list and a `blocked_decoupeur.md`: no re-invocation.** 📌
**The short list is expected** — it stopped on the block the file
names, and the blocks it never reached still carry their markers for
the next turn.

🔴 **Then grep `^### B` in `desc-produit.md`** and count. 📌 **Say how
many blocks the file held before, and how many it holds now** — ⚠️
**the count after the last invocation**, not the first.

⚠️ **Same count means it split nothing** — 📌 **that is a normal
outcome**, and the cycle carries on to `/3a_genre`.

🔴 **Never read a block to check its work.** 📌 **The sondeurs probe
what it produced; that is what catches a bad split.**

---

## Git, once it has reported

**Then, once it has reported — the second invocation of *Once it has
reported* included, when there was one — 📌 five steps, in this order:**

1. 🔴 **`git add` and `git commit` inside the worktree** — ⚠️ **the
   agent has no Bash and commits nothing**; 📌 **`git merge` takes the
   branch's commits, not the worktree's files**, and
   `git worktree remove` refuses a dirty tree
2. 🔴 **Leave the worktree** — ⚠️ **a session isolated in a worktree
   cannot issue a git command against the main checkout**: the merge
   below, issued from inside it, is refused
3. `git merge --no-ff <branch>` from the main checkout root
4. `git push`
5. `git worktree remove <path>`

🔴 **The push is part of the merge, not an afterthought.** A phase that
sits only on the local machine is lost with it.

⚠️ **A push that fails — diverged remote, no network — is reported, not
retried and not worked around.** The merge holds locally; say so and
carry on.

🔴 **Merge before handing back, always.** ⚠️ **A `blocked_*.md` merges
too**: the Product Owner has to see it.

---

## What you relay

📌 **How many blocks before, how many after.**

🔴 **A list still short after the second invocation: say which blocks
were never looked at** — ⚠️ **the split is incomplete and `/3a_genre`
would run on it.** 📌 **No further invocation** — *Once it has reported*
has already run the two it allows.

🔴 **A short list beside a `blocked_decoupeur.md`: relay the file and
stop**, see below — 📌 **the blocks it never reached wait for the next
turn**, their markers still on them.

**What to run next** — 📌 **indications for the Product Owner.**
⚠️ **You relay them; you run nothing after this command.**

| What just happened | Next |
|---|---|
| It wrote a blocking file | 🔴 **Fill its `## Decision`, then `/2_structure`** — ⚠️ **it blocks on a sentence carrying two triggers, and rewording is the Rédacteur's.** 📌 **`/3_decoupe` again afterwards** |
| It reports a block whose only trigger is a sequel | 📌 **Relay its identifier; the next step does not change** — 🔴 **nobody merges**: ⚠️ the two blocks carry one behaviour the grid probes twice, and 📌 **the Product Owner merges by hand when it bothers her** |
| Otherwise | 📌 `/3a_genre`, whether it split anything or not |

🔴 **Nothing else is yours**: no reading of what a block says.

**If it returns `blocked_decoupeur.md`**: relay it and stop.
