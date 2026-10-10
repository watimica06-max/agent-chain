---
description: Confront the product file against every spec sheet
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
argument-hint: "<feature folder name>"
---

Act as the orchestrator, in **downstream mode**.

**This command invokes `controleur` once per group of blocks, then
once more to assemble.**

**The argument is mandatory**: the feature folder name. Without it, ask
for it and stop — never guess which feature is meant —
`Next: stop argument missing`. ⚠️ **A name,
never a path** — 📌 **you derive the folders from it**, as `/7_lots`,
`/8_code` and `/audit_conventions` do.

**Feature folder**: `docs/features/<name>/`.

🔴 **The working folder is the highest `bugfix-NN/` in it, if there is
one; the feature folder itself otherwise.** 📌 **A `bugfix-NN/` working
folder means a correction cycle** — the lots just coded are its own.

🔴 **The six phases do not all read the same folder:**

| Phases | Folder |
|---|---|
| **1 to 3** | 🔴 **The feature folder, always** — 📌 **the product file, its map, the sheets the feature cut and the report live there**, and a correction cycle has no product file to confront |
| **4 to 6** | 🔴 **The working folder** — 📌 **the lots just coded, their `code/recette.md`, their blocking files** |

📌 **Every `code/` path below is under the folder its phase names.**
⚠️ **Two files sit at the feature folder's root whatever the working
folder** — `par-genre/recette.md` and `registre-questions.md`; each
phase that reads or writes them says so.

---

## What you read

📌 **At phase 1**: `tracabilite.md`, the `Genre: comportement` lines of
`desc-produit.md`, the `Anchor:` lines and the `## Entries with no lot`
section of `code/decoupage.md` and, for each `bugfix-NN/` of the
feature folder, the `Anchor:` lines of its own `code/decoupage.md`
**by grep** — 🔴 **never any of those files whole.**

**Then only whether `desc-produit.md` is there**, and whether every lot
of `code/sequence.md` — the sequences *When it runs* names — carries a
`verdict.md` whose `## Status` opens on `PASS` — 📌 **the prefix**: ⚠️ **a `PASS with reservation` is a coded
lot.** 🔴 **Its reserved points sit under `## Findings`, one line
each** — copy them, with the lot's name, for *What you relay*. ⚠️
**Never a verdict on them, never a block, and no agent is handed
them.**

⚠️ **Nothing else.** `CLAUDE.md`'s standing reading rules apply.

---

## When it runs

🔴 **This command hands the Product Owner three things, and nothing
else:**

| | |
|---|---|
| **The manual list**, assembled and ordered | 📌 **Every check the Product Owner can make on the device, ordered so that each starts from the state the one before it left** |
| **The register of escaped product questions** | 📌 **Gathered, never concluded** |
| **The product decisions taken while coding** | 📌 **One file per cycle**, for the Rédacteur |

🔴 **It runs after the main cycle and after every correction cycle.**
⚠️ **The Contrôleur confronts the feature's product file with the
feature's sheets, every time** — 📌 **a correction cycle has no product
file, and its sheets are never confronted**: 🔴 **the blocks it built
reach the Contrôleur marked `carried`, through the map of phase 1.**

🔴 **`desc-produit.md` absent from the feature folder** — 📌 **say so
and stop**: there is nothing to confront the sheets with —
`Next: stop desc-produit.md missing`.

🔴 **`tracabilite.md` absent from the feature folder** — 📌 **phase 1
reads it**: say so and stop, the conversion did not finish —
`Next: stop tracabilite.md missing`.

🔴 **Stop if a lot of a sequence has no `verdict.md` whose `## Status`
opens on `PASS`** — name it: `Next: stop <lot> not PASS`. 📌 **Two sequences when the working folder
is a `bugfix-NN/`**: ⚠️ **the feature folder's, whose sheets phases 1
to 3 confront, and the working folder's, whose lots phases 4 to 6
read.**

⚠️ **He would otherwise read an incomplete set of sheets** — 📌 **and
report an intention as missing when it is merely unwritten.**

📌 **An existing `rapport-controle.md` is not a reason to stop.** He
writes the next free number beside it; that is how two states are
compared — ⚠️ **the report before a correction cycle, and the one
after it, where the blocks that cycle built read `carried` instead of
missing.**

---

## Git, before invoking

🔴 **Commit the feature folder first**, before creating the worktree:

    git add docs/features/<name>/ && git commit -m "chore: pre-control"

📌 **Nothing to commit is a normal outcome** — carry on.

🔴 **Then create a worktree from local `HEAD`, and register it:**

    git worktree add .claude/worktrees/<name> HEAD

⚠️ **Never let the tooling branch it for you** — its default base is
`origin/master`, which can sit several commits behind local. An agent
would then work on stale content and its output would have to be
discarded.

📌 **Enter the worktree before invoking the agent**, not after it
fails — the harness blocks a subagent's writes until the session is
isolated.

---

## How it runs

**Six phases.**

📌 **`code/recette.md` absent from the working folder** — ⚠️ **normal,
not a stop**: no lot had a check the Product Owner can make on the
device. 🔴 **Phase 4 then builds from `par-genre/recette.md` alone**,
and says the other source was empty.

### Phase 1 — build the block-to-lot map

🔴 **Greps and a crossing**, no agent.

🔴 **Keep the blocks carrying `Genre: comportement`, plus every other
block whose `tracabilite.md` line carries at least one entry.** 📌 **The
genre comes from `desc-produit.md`, by grep** —
`grep -B1 '^Genre: comportement$'`, the block heading one line above
each hit, as `/3a_genre` reads the empty ones. ⚠️ **The other five
genres produce no lot by construction**, and each is taken up
elsewhere — 🔴 **save the block that gave an entry**, which its
`tracabilite.md` line keeps whatever its genre:

| Genre | Where it is taken up |
|---|---|
| `recette` | 📌 **Phase 4** — `par-genre/recette.md` feeds `code/recette-ordonnee.md` |
| `directive` | 📌 **The Architecte** turned it into a conventions rule |
| `transverse` | 📌 **Its constraint half, the preamble's `## Cross-cutting rules`** — ⚠️ **its code half is an entry**, and a transverse block that gave one is kept through that entry's lot, like a behaviour |
| `référence` | 📌 **The Convertisseur**, §9 Text of the technical document |
| `hors périmètre` | ⚠️ **Set aside by the Product Owner, explicitly** |

⚠️ **Say how many blocks you kept — the behaviours, and the blocks of
another genre an entry kept — how many each genre set aside, and how
many are marked `carried`** — 🔴 **so none of them reads as dropped.**

**a.** `tracabilite.md` gives block → entries.

**b.** The `Anchor:` fields of `code/decoupage.md` give entry → lots.

🔴 **Plus its `## Entries with no lot` section** — 📌 **one line per
entry, and the reason opens the line after the dash, in one of three
forms the Cadreur fixes**; ⚠️ **each is read differently:**

    §4.7 — already carried by the code
    §8.1 — carried by §4.1 and §5.2
    §2.9 — nothing to build

| The reason opens on | What the entry gets |
|---|---|
| `already carried by the code` | 🔴 **The mark `carried`** — 📌 **built before this feature ran**; without it the Contrôleur reports its intentions missing |
| `carried by §…` | 🔴 **The lots of the entries it names** — ⚠️ **follow each `§` through the `Anchor:` lines**, no mark |
| `nothing to build` | 🔴 **No lot and no mark** — 📌 **an attribution or a boundary**: its block answers through its other entries, or gets the dash |

⚠️ **Only the first form marks** — 🔴 **an entry with no lot is not an
entry already built**, and marking the other two would hide a gap.
📌 **Anything after the form, past a comma, is the Cadreur's prose** —
you read the opening words alone.

**b'.** 🔴 **The blocks a correction cycle built** — 📌 **grep `(B<n>)`
in the `Anchor:` lines of every `bugfix-NN/code/decoupage.md` under the
feature folder**: the Cadreur writes there, on a bug-fix cycle, the
block identifier the gap came from —

    Anchor: §2.3 — <the entry's title> (B12)

⚠️ **Every block found there is marked `carried`**: 🔴 **its missing
intentions were built, elsewhere**, and none of the feature's sheets
shows it. 📌 **A gap the Product Owner raised from use carries no
`B<n>`** and marks nothing — that is accepted.

**c.** Cross them into `tracabilite-full.md`, at the feature folder's
root.

🔴 **One line per kept block, in block order** — its identifier, then
the lots that build its entries, deduplicated; 📌 **then the word
`carried` when b marked one of its entries or b' marked the block**,
after the lots or after the dash:

    B1   lot-01
    B43  lot-21, lot-30, lot-33
    B59  —
    B60  lot-12  carried
    B61  —  carried

🔴 **A line carrying both lots and the mark is a block built in two
places** — 📌 **the Contrôleur reads the lots' sheets like any other
block's, and an intention no sheet carries is found with the mark as
its reason.** ⚠️ **A line with the mark and no lot is one found line**,
and no sheet is read for it. 📌 **The mark is set on the block, never
on an intention** — the Contrôleur tells the two apart, not you.

📌 **Two spaces at least after the identifier**; nothing else on the
line, no title, no prose, no header. **That is the format the script
parses** — ⚠️ **it reads the identifier and the `lot-NN` references,
and ignores the mark**: the lots stay on the line so the grouping and
the check in **d** still see them.

**d.** 🔴 **Check the crossing before going on** — 📌 **count the blocks
the filter above kept and the lines of `tracabilite-full.md`**: ⚠️
**they match, or a block was lost in the join.** 🔴 **Never every block
of `tracabilite.md`** — it lists the set-aside ones too, with a dash,
and that count can never match.

🔴 **And grep every lot of `code/decoupage.md` in it** — 📌 **a lot
appearing in no line built no entry any block names**, which is either
a split defect or a crossing defect. ⚠️ **Say which lots, and stop** —
`Next: stop <lots> in no line of the map`.

🔴 **Every kept block appears.** A block whose entries no lot cites
gets a dash — it still needs an answer, and the group carrying it reads
no sheet for it.

### Phase 2 — group the blocks

    python .claude/scripts/grouper.py docs/features/<name>/tracabilite-full.md --auto

📌 **The script sweeps every budget and picks one**, weighing the
context of a pass against the number of passes. **It prints the groups
under `=== budget …`, one `G<n>` line each.**

🔴 **Take the grouping it prints, unchanged.** ⚠️ **Never regroup by
hand, never override the budget** — the split has to be reproducible
from the same input.

📌 **A `|` inside a `G<n>` line separates atoms**, not groups.
**Everything on one such line is one group.**

⚠️ **The script prints identifiers alone** — 🔴 **the `carried` mark
does not survive it.** 📌 **Read it back from `tracabilite-full.md`
when you write each group's prompt**, in phase 3.

### Phase 3 — one Contrôleur per group, then one to assemble

**What you do**: invoke the agent via `Agent()` with the feature folder
and the group it takes — and nothing else.

🔴 **Never paraphrase the agent's process in your invocation** — not
its inputs, its checks, its output format. It reads its own
instructions.

### Invocation parameters

```
Agent(
  subagent_type="controleur",
  model="sonnet",
  description="control G1 <feature>",
  prompt="Feature folder: docs/features/<name>/.
          Invocation 1 — Confront.
          Group: G1.
          Blocks: B15, B53 (carried), B54, B56.
          Sheets: code/lot-29, code/lot-43, code/lot-44."
)
```

🔴 **The folder is the feature folder, on both cycles** — 📌 **the
product file and the sheets it confronts are there.**

🔴 **A block marked `carried` in `tracabilite-full.md` carries
`(carried)` after its identifier in `Blocks:`** — 📌 **that is how the
mark reaches the agent**, which confronts the block against the sheets
like any other and finds, with the mark as the reason, the intentions
no sheet carries. ⚠️ **Its lots go in `Sheets:` like any other
block's** — 🔴 **a marked line with lots is a block built in two
places**, and dropping its sheets would read every intention as
carried. 📌 **A marked line with the dash brings no sheet**, and the
agent writes one found line for it.

🔴 **Empty `code/controle/` before issuing the groups** — 📌 **the
partials of an earlier run would otherwise still be there.**

⚠️ **Issue every group together**, then wait for all of them.

**Then, once every group has reported:**

```
Agent(
  subagent_type="controleur",
  model="sonnet",
  description="assemble <feature>",
  prompt="Feature folder: docs/features/<name>/.
          Invocation 2 — Assembly.
          Groups issued this run: G1, G2, G3.
          Blocks per group, one line each:
            G1: B1, B2, B3
            G2: B4, B5
            ..."
)
```

🔴 **Name the groups this run issued, and the full block list** — 📌
**identifiers alone, no `(carried)` here**: assembly reads the list
against each partial's opening line, and the mark is not a block. ⚠️
**Without the groups, a partial left by an earlier run is merged with
this run's** — 📌 **and its lines speak of sheets that have changed
since.** ⚠️ **Without the block list, a group that wrote nothing is
invisible**: the numbering alone shows a hole between `B6` and `B8`,
never the last blocks of the feature.

❌ No `effort` parameter. ⚠️ **`run_in_background` may not exist
either** — in this environment the Agent tool always runs async and
notifies on completion. Do not pass it; wait for the notification.

❌ **Never pass `isolation`.**

---

### Phase 4 — the manual list

🔴 **Two sources**: 📌 **`code/recette.md`**, the lines the testeur wrote
lot by lot, in the working folder, **and `par-genre/recette.md`**, what
the Product Owner said she wanted to check herself.

🔴 **`par-genre/recette.md` sits at the feature folder's root, and
nowhere else** — `/5_reclasse` writes it there, on the main cycle. ⚠️
**On a correction cycle it is not in the working folder**: 📌 **look for
it one level up, at the feature folder's root**, and use it from there.

🔴 **You add nothing and you reword nothing** — 📌 **you order.** ⚠️
**Every line is copied as it stands**; 🔴 **the one thing you write is
an announcement, on a line of its own opening on `## `** — 📌 **in
French, in the forms this phase names, and no other.**

⚠️ **Every reset costs the Product Owner dearly** — 🔴 **as few as
possible, and each one announced on its own line.**

🔴 **Order by state, never by intention.** 📌 **Two kinds of line, and
they are not ordered the same way:**

| The line | How it is ordered |
|---|---|
| **Its five fields** — `Lot:` · `From:` · `Do:` · `Expect:` · `Leaves:`, the shape of `agents/testeur.md`, move 5 | 🔴 **By the states lines leave** — the walk below |
| **Without them** — an older feature's line, a block of `par-genre/recette.md` | 📌 **As before** — after the walk, see below |

**The walk** — 🔴 **one current state, starting at `application
vide`, and the lines placed one at a time:**

1. 🔴 **The next line starts from the current state** — 📌 **its
   `From:` is, word for word, the `Leaves:` of the line placed before
   it, or `application vide` at the start.** 📌 **Placed, its `Leaves:`
   becomes the current state**
2. 🔴 **Several start from it** — 📌 **first a line that changes
   nothing, its `Leaves:` repeating its `From:`; then a line whose
   `Leaves:` another line still to place starts from; then the rest** —
   ⚠️ **in each group, the order of `code/recette.md`**
3. 🔴 **A line that destroys or resets comes after every line that
   needs what it destroys** — 📌 **its `Leaves:` carries
   `définitivement`, or no longer holds what its `From:` held**: ⚠️
   **while a line still to place starts from a state holding what it
   takes, that line waits**, even when nothing else starts from the
   current state
4. 🔴 **None starts from it, and a line still to place starts from
   `application vide`** — 📌 **announce `## Réinitialiser
   l'application`**, and the current state is `application vide` again
5. 🔴 **None starts from it, and none starts from `application vide`**
   — 📌 **take the first line of `code/recette.md` still to place,
   preferring one no line still to place leaves**, and announce
   `## Amener l'application à : <its From:, copied>`, and that `From:`
   is the current state — ⚠️ **the one announcement that says how to
   reach a state no other line leaves**: 📌 **her own words, the line's
   starting state, and nothing added**

🔴 **The list opens on `## Depuis l'application vide`** — 📌 **when
its first line starts there**; ⚠️ **otherwise on the announcement of
step 5.**

**The lines without the five fields** — 🔴 **after the walk, as
before**, under `## Sans état décrit`, 📌 **each state change announced
on a `## ` line in her words**:

| | |
|---|---|
| **Everything checkable on an empty application** | first |
| **Then with one record** | 📌 **announce the state change** |
| **Then with several** | — |

⚠️ **A line there that does not say its state cannot be placed**:
leave it at the end, under `## État non précisé`.

⚠️ **Why it matters**: 📌 **a manual test file has existed and was
abandoned** — 🔴 **not because it was useless, but because it was
unusable**: thousands of unordered tests, with deletions and data
resets in the middle.

**Write `code/recette-ordonnee.md`**, in the working folder.

### Phase 5 — the register of escaped product questions

🔴 **Two sources**: 📌 **the `## Doubts` and `## Intentions missing`
sections of `code/rapport-controle*.md`** — the latest one, in the
feature folder: the one phase 3 just wrote — **and the product
questions the Arbitre handed back**, in the numbered blocking files of
the working folder.

🔴 **They sit at two depths** — 📌 **`code/blocked_*-NN.md`** for the
Cadreur and the Détailleur, **`code/<lot>/blocked_*-NN.md`** for the
four agents of the loop. ⚠️ **Glob both** — 🔴 **the unnumbered ones are
still open**, and not yours to read.

🔴 **One case per line, and you conclude nothing.** ⚠️ **No class
proposed, no grid change suggested** — 📌 **an isolated case says
nothing; ten together let a shape show.**

📌 **Its reader is the Product Owner, across cycles** — 🔴 **she decides
whether a recurring kind of escaped question becomes an entry of
`.claude/grids/GRILLE_CADRAGE_PRODUIT_V2.md`.** ⚠️ **Append, never overwrite**: the
file is the record of every cycle, not of this one.

**Write `registre-questions.md`, at the feature folder's root** — 🔴
**one register per feature, outside any `bugfix-NN/`**: ⚠️ **a
`code/` under a correction cycle is a fresh folder each cycle**, and a
register written there would record one cycle alone. 📌 **Every cycle
appends to the same file.**

### Phase 6 — the product decisions taken while coding

🔴 **A product question settled during the coding went into a sheet** —
📌 **never into the product file, never into the global.**

🔴 **Gather them from the same two depths as phase 5**, in the working
folder: 📌 **every `## Decision` that settles what the application
does**, as opposed to how it is built.

⚠️ **The test is the one the Arbitre uses** — 📌 **a decision on a
behaviour, a wording, what the user sees.** 🔴 **A technical decision
is not one.**

**Write `code/decisions-produit.md`**, in the working folder — 📌 **one
decision per line, in this shape:**

    B12  <the decision, as the ## Decision wrote it>
    —  <a decision the file ties to no block>

🔴 **The identifier first, then two spaces, then the decision** — 📌 **a
dash where no block is derived.** 🔴 **Nothing before the identifier**:
the Rédacteur greps it, and reads it as written.

⚠️ **A `## Decision` written on several lines — the Arbitre's three
parts, one under the other — is written as one line**: 🔴 **its parts
joined in order on the identifier's line, nothing dropped and nothing
on a continuation line.** 📌 **The Rédacteur reads one line per
decision, and a continuation line would open on no identifier.**

⚠️ **No blocking file names a block** — 🔴 **it names a lot, and you
derive the block from the lot through the map of phase 1:**

| The blocking file | Where its lot is |
|---|---|
| The Détailleur's, `code/blocked_detailleur-NN.md` | 📌 **The `## Blocking N — lot-NN` heading** the decision answers — one lot per blocking, so one line per numbered answer |
| The four agents of the loop, `code/<lot>/blocked_*-NN.md` | 📌 **The `code/<lot>/` folder it sits in** |

🔴 **Then the lot in `tracabilite-full.md`** — 📌 **one line carries
it → that block's identifier; several lines, or none → the dash.**
⚠️ **On a correction cycle the lot is a `bugfix-NN/` lot**, absent from
that file: 🔴 **its block is the `(B<n>)` its `Anchor:` lines carry**,
the one b' grepped — one identifier → that block; several, or none →
the dash. 📌 **The Cadreur's, `code/blocked_cadreur-NN.md`, precedes
every lot** — its decisions take the dash.

🔴 **The decision is copied, in the language the `## Decision` was
written in — French.** 📌 **The Rédacteur translates it at `/fusion`,
invocation 3, as it translates an answer at invocation 2** — ⚠️ **you
translate nothing, and reword nothing.**

🔴 **The Rédacteur reads it at `/fusion`**, invocation 3. ⚠️ **Write it
even empty** — 📌 **its absence would read as *the phase did not run*.**

---

## Git, once it has reported

🔴 **Every end of the run merges first, once the worktree exists — a
stop included, the map's crossing among them, as much as phase 6
written.** 📌 **Five steps, in this order:**

1. 🔴 **`git add` and `git commit` inside the worktree** — ⚠️ **the
   agent has no Bash and commits nothing**, and the files phases 1, 4,
   5 and 6 wrote by hand — those the run reached — are uncommitted
   too; 📌 **`git merge` takes the worktree's commit, not
   its files**, and
   `git worktree remove` refuses a dirty tree
2. 🔴 **Read the worktree's commit id, then leave it** —
   `git -C <path> rev-parse HEAD`; ⚠️ **a session isolated in a
   worktree cannot issue a git command against the main checkout**:
   the merge below, issued from inside it, is refused
3. `git merge --no-ff -m "<message>" <commit id>` from the main checkout root
4. `git push`
5. `git worktree remove <path>`

⚠️ **A worktree still dirty after step 1 refuses a plain remove** — 🔴
**never force it**: 📌 **say what is left there, and stop** —
`Next: stop worktree dirty: <files>`. 📌 **What
is left is something step 1 did not stage** — a fault of this run,
never of the agent: it was not to commit it. Forcing the removal
destroys it.

🔴 **The push is part of the merge, not an afterthought.** A report
that sits only on the local machine is lost with it.

⚠️ **A push that fails — diverged remote, no network — is reported, not
retried and not worked around.** The merge holds locally; say so and
carry on.

🔴 **Merge before handing back, always** — an unmerged commit is
invisible to whoever reads next.

---

## What you relay

**The agent's own report, and the four files this run wrote**, by name:

| | |
|---|---|
| `code/rapport-controle-NN.md` | 📌 **In the feature folder** — 🔴 **the intentions of a block marked `carried` that no sheet carries read as found there, with the mark as the reason** |
| `code/recette-ordonnee.md` | 🔴 **What the Product Owner checks by hand** — in the working folder |
| `registre-questions.md` | 🔴 **At the feature folder's root, read by the Product Owner across cycles** — 📌 **a kind of product question that keeps escaping upstream is a question the framing grid is missing** |
| `code/decisions-produit.md` | 📌 **Read by the Rédacteur at `/fusion`** — in the working folder |

**Plus the reservations the verdicts hold**, one line each — 📌
**the lot, and the `## Findings` line the Relecteur wrote for a `PASS
with reservation`.** 🔴 **A reservation says *it passes, but it is worth
looking at*** — ⚠️ **relayed here, it reaches the Product Owner at the
one moment she reviews the whole feature.** 📌 **None to relay is said
in one word.**

🔴 **Nothing else is yours**: no reading of those files, no summary of
what they hold, no decision on what to do next.

🔴 **The relay ends on its `Next:` line**, in `CLAUDE.md`'s grammar —
📌 **every ending of this command names its own**, stops included. 📌
**This one, on a run that wrote its four files**: `Next: manual lire le
rapport de contrôle et la recette, décider d'une bug-list`.

📌 **The Product Owner reads them and decides** whether the control
report becomes a `bug-list.md` for a correction cycle. 🔴 **A gap she
takes from the report keeps its `B<n>` in `bug-list.md`** — 📌 **in
parentheses, at the end of the gap's first line, after the `G<n>` each
gap she writes opens on**, as the Diagnostiqueur writes it into
`desc-bug.md`:

    G03 <what is wrong> (B12)

🔴 **That is the form the Diagnostiqueur greps** — ⚠️ **written anywhere
else on the gap, the identifier is lost**, and the block reads missing
at the next control. 📌 **The Diagnostiqueur carries it into
`desc-bug.md`, the Cadreur into the lot list, and phase 1 of the next
control marks the block `carried` from there.** ⚠️ **Say so when you
relay the report** — one sentence, so the form reaches her with the
file.

⚠️ **The manual list is the one to run before deciding** — 📌 **a gap
the Contrôleur cannot see shows there.**
