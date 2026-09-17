# Plan — diagnostiqueur

Built against `.claude-new/agents/diagnostiqueur.md` (572 lines) and the
two commands that name it: `.claude-new/commands/diagnostique.md`
(179 lines — the only one that invokes it) and
`.claude-new/commands/audit_blocages.md` (reads its blocking files,
invokes nothing). The index `docs/refonte/modifications.md` was opened
at the lines F01 and F02 cite. No pass sheet exists
(`docs/refonte/passes/diagnostiqueur.md` absent), so the report's
section 2 rows have no request text behind them.

Twenty findings judged: the report's eighteen (F01–F18), plus
`fichiers.md` F05 and `chemins-aval.md` F12 — the only two hits in the
six thematic reports. **Twenty `confirmed`**, none stale, none wrong:
every cited line reads today as the report describes it. One line
reference is out of date (`chemins-aval.md` F12 cites
`diagnostique.md L235` in a 179-line file) — the fact it names stands
at L173-174, so the finding is confirmed, not stale.

The report's section 2 `other` rows are the same defects under another
name: D-3 is F06, D-16 is F10, D-11 is answered inside F08. Its three
`open` rows (D-12, D-19, D-22) carry no text and no line — see
`## Not judged`.

**One finding goes to `## To settle`** — F10, the state-document input
with no outcome — and F04 hangs on it.

**Decisions that hold together**: F05, F07 and F16 are one change (the
existing `desc-bug.md`); F17 and `fichiers.md` F05 are one change (the
phase-1 rename); F18 and `chemins-aval.md` F12 are the command's two
missing skips. Where a decision lands on `diagnostique.md`, its owner
is written as the command — no thematic finding puts it in
`commandes.md`, so it is applied from here.

---

## Verdicts

| Finding | Severity | Verdict | Entry |
|---|---|---|---|
| F01 | TO FIX | confirmed | below |
| F02 | NOTE | confirmed | below |
| F03 | NOTE | confirmed | below |
| F04 | NOTE | confirmed | below — hangs on F10 |
| F05 | TO FIX | confirmed | below — with F07, F16 |
| F06 | TO FIX | confirmed | below |
| F07 | TO FIX | confirmed | below — with F05, F16 |
| F08 | TO FIX | confirmed | below — absorbs D-11 |
| F09 | TO FIX | confirmed | below |
| F10 | TO FIX | confirmed | `## To settle` |
| F11 | TO FIX | confirmed | below |
| F12 | TO FIX | confirmed | below |
| F13 | NOTE | confirmed | below |
| F14 | NOTE | confirmed | below |
| F15 | NOTE | confirmed | below |
| F16 | NOTE | confirmed | below — with F05, F07 |
| F17 | TO FIX | confirmed | below — with fichiers.md F05 |
| F18 | NOTE | confirmed | below |
| fichiers.md F05 | TO FIX | confirmed | below — same as F17 |
| chemins-aval.md F12 | TO FIX | confirmed | below |
| D-3 (section 2, `other`) | — | = F06 | — |
| D-11 (section 2, `other`) | — | = F08 | — |
| D-16 (section 2, `other`) | — | = F10 | — |
| D-12 · D-19 · D-22 (section 2, `open`) | — | not judged | `## Not judged` |

---

### diagnostiqueur.md F01 — the index marks the file untouched

Verdict: confirmed
Decision: Rewrite the index's `diagnostiqueur.md` row so it names what
the file carries — the working-file items applied, by identifier, and
the ones still open — instead of saying nothing was applied.
Where: modifications.md L1601 ↔ diagnostiqueur.md L38-45, L76-79,
L120-124, L138, L164-167, L225-231, L311-313, L333-338, L411-421,
L432-444, L459-460, L472-474, L493-495, L503-505
Cited: modifications.md L1601 — "| `diagnostiqueur.md` | ⚠️ **Pas de
fiche**, et rien du fichier de travail |"
Cited: diagnostiqueur.md L76-79 — "You block when producing is
impossible — 📌 four cases: a prompt naming no gap · a report set that
does not match `bug-list.md` · a report that does not carry what an
entry needs · a closure that fails" (D-4, marked fixed by the report
itself); L311-313 — "Moving a behaviour from one place to another is
the same case — 🔴 `Bearer: none`" (D-3); L503-505 — "If the file
already exists, write the blocking file rather than overwriting it"
(D-5).
Owner: diagnostiqueur — the correction of the file updates its own
index row
Also in: —

The row is the only record for this agent, and it is false on the one
thing it says. The rewrite is a record, not a rule: no agent prose
changes for it.

---

### diagnostiqueur.md F02 — the command rewrite the index never names

Verdict: confirmed
Decision: Add a `diagnostique.md` entry to the index's command section,
naming the git section moved ahead of the invocation and the `git mv`
rename rule.
Where: modifications.md L1320-1522 ↔ diagnostique.md L44-70, L157-158,
L164-171
Cited: modifications.md L1320 — "# Les commandes", and none of its
headings down to L1522 is `diagnostique.md` (grep on the whole index:
no hit for the command's name). The command section's table at
L1603-1611 lists every command but `/diagnostique` and
`/audit_blocages`.
Cited: diagnostique.md L44 — "## Git, before invoking", L85 — "Phase
1 — one `Agent()` per remaining gap"; L168 — "git mv
blocked_diagnostiqueur.md blocked_diagnostiqueur-NN.md". No `TaskCreate`
and no risk level in the file today (grep: no hit).
Owner: diagnostique.md (command)
Also in: —

What the index can record is what the file holds today; that the two
items were *dropped* cannot be shown without reading history, which is
forbidden. The entry names the present state.

---

### diagnostiqueur.md F03 — `Glob` granted, named nowhere

Verdict: confirmed
Decision: Name `Glob` as the gesture for the two existence checks — the
blocking file with its `-NN` siblings, and `desc-bug.md` — and confine
it to those.
Where: diagnostiqueur.md L4 ↔ L154-158, L503
Cited: L4 — "tools: Read, Grep, Glob, Write"; L154-158 — "look for
your own blocking file […] Several with `-NN` appended beside it are
settled ones — read them"; L503 — "If the file already exists, write
the blocking file". No line between L1 and L572 names `Glob`.
Owner: diagnostiqueur
Also in: —

With F07/F16 the `desc-bug.md` check moves to the head of invocation 2
and becomes a stop; it still needs the tool named.

---

### diagnostiqueur.md F04 — two sections of a 2 300-line document, no gesture

Verdict: confirmed
Decision: If F10 keeps the state-document input, name the gesture that
reaches the two sections — a grep on their headings, then a read from
there — so that "load only what your invocation lists" no longer means
the whole file.
Where: diagnostiqueur.md L138 ↔ L144
Cited: L138 — "`docs/CURRENT_TECHNICAL_STATE.md` — 📌 its `## Traps —
general` and `## Dead state` sections"; L144 — "Load only what your
invocation lists."
Owner: diagnostiqueur
Also in: —

Hangs on `## To settle` F10: if the input is dropped, this entry is
moot.

---

### diagnostiqueur.md F05 — "four cases", and a fifth

Verdict: confirmed
Decision: Keep the enumeration at four by taking the existing
`desc-bug.md` out of the block cases — it becomes the stop F07
describes.
Where: diagnostiqueur.md L76-79 ↔ L503-505
Cited: L77-79 — "four cases: a prompt naming no gap · a report set
that does not match `bug-list.md` · a report that does not carry what
an entry needs · a closure that fails"; L503 — "If the file already
exists, write the blocking file rather than overwriting it".
Owner: diagnostiqueur
Also in: —

One change with F07 and F16.

---

### diagnostiqueur.md F06 — a move gap has two bearer rules

Verdict: confirmed
Decision: Drop "The bearer is where it lands" and keep `Bearer: none`
for a move, as L275-282 and L311-313 already say.
Where: diagnostiqueur.md L311-313 ↔ L316-317
Cited: L311-313 — "Moving a behaviour from one place to another is
the same case — 🔴 `Bearer: none`: 📌 where it lands is the Cadreur's,
not yours."; L316-317 — "The bearer is where it lands."
Cited: L279-282 — "That is the shape of a behaviour that has to move:
🔴 you establish it belongs elsewhere, not where it lands. 📌 Where it
lands is a split decision".
Owner: diagnostiqueur
Also in: —

The report's D-3 row is this finding. L314-316 — one gap, not two,
because between the halves the behaviour exists nowhere — stays: it
argues for one entry, not for a bearer.

---

### diagnostiqueur.md F07 — a block nothing can lift

Verdict: confirmed
Decision: Make an existing `desc-bug.md` a stop that names the file
and says what it holds is settled — not a block — and have the command
not issue phase 2 when the file exists, the mirror of its L77 skip;
a re-assembly is obtained by the Product Owner deleting the file.
Where: diagnostiqueur.md L503-505 ↔ L173-180; diagnostique.md L107
Cited: L503-505 — "If the file already exists, write the blocking
file rather than overwriting it — 📌 a run of yours got past the
closures and was interrupted after writing it, and what it holds is
settled."; L173-180 — "How you apply it, at invocation 2 — 🔴 the
decision does not replace what is missing. Re-run the count […] Every
report is there → Assemble"; L166-167 — "you have no tool that removes
a file. ⚠️ The orchestration does it".
Cited: diagnostique.md L107 — "Phase 2 — one `Agent()`, once every
report exists." — nothing tests `desc-bug.md`; L164-171 rename only
`blocked_diagnostiqueur.md`, and `git mv` does not remove.
Owner: diagnostiqueur
Follows: diagnostique.md (command) — adds the phase-2 skip and says
that an existing `desc-bug.md` is relayed as done
Also in: —

L66-67 ("Write a blocking file — do not merely say it") is about a
production that cannot happen; here the production exists, and the
agent's own words say it is settled. A block whose only exit is a
deletion the agent cannot make and the orchestration is not told to
make is a wait with no end.

---

### diagnostiqueur.md F08 — "belongs to another entry", written into this one

Verdict: confirmed
Decision: Make what can change while the bearer stays always a second
`## Bearer` block — never a line of `## Expected` — and keep
`## Expected` for what the bearer's change cannot stand without
(L328-331), which is the only kind of requirement invocation 2 folds
into the entry.
Where: diagnostiqueur.md L333-335 ↔ L461-465
Cited: L333-335 — "What can change while the bearer stays as it is
belongs to another entry. 🔴 Say so in your report — 📌 a second bearer
block if it is one, a line of `## Expected` if it is a requirement.";
L461-465 — "Every second requirement a report carries goes into the
entry — a missing observer, an unreachable value, a signature that has
to change. They are part of what has to be built".
Cited: L328-331 — "One exception, and it is narrow: 📌 what has to
change so that the bearer can change. ⚠️ Test it by asking whether the
bearer's own change stands without it — if it does, that other thing
is a separate entry."
Owner: diagnostiqueur
Also in: —

The report's D-11 row ("a signature change on something other than the
bearer") is answered by the same rule: the signature at L462 is folded
in only when the bearer's change cannot stand without it; otherwise it
is a second `## Bearer` block and its own entry. L323 ("a change of its
bearer, and of nothing else") then holds without a second reading.

---

### diagnostiqueur.md F09 — one nature per gap, one entry per bearer

Verdict: confirmed
Decision: Give the nature per `## Bearer` block — per entry — not per
gap, so that each entry lands in its own bearer's section.
Where: diagnostiqueur.md L453-454 ↔ L459-460, L555-557
Cited: L453-456 — "Give each confirmed gap a nature, among the eight.
📌 The nature of the bearer, not of what it calls"; L459 — "Write one
entry per `## Bearer` block of the report"; L555-557 — "One entry, one
bearer — 📌 a gap with several bearers gives several entries".
Owner: diagnostiqueur
Also in: —

L453's own qualifier — "the nature of the bearer" — already says per
bearer; only the unit of move 6 is wrong.

---

### diagnostiqueur.md F11 — a path rule the widening breaks

Verdict: confirmed
Decision: Let the widened search reach the manifest, the build files
and the resources with a path of their own, and narrow the path rule
to what it guards against — `docs/` and the build output.
Where: diagnostiqueur.md L198-200 ↔ L210-223
Cited: L198-200 — "Every code search targets the code folders the
conventions name — `Grep(pattern, path: "<folder>")`, never a bare
pattern. ⚠️ A search without a path sweeps `docs/` and the build
output."; L210-211 — "A behaviour does not live only in source files.
⚠️ Search everything the build carries."; L222-223 — "a value fixed in
a manifest, a build file or a resource".
Owner: diagnostiqueur
Follows: architecte — only if `docs/TECHNICAL_CONVENTIONS.md` names no
folder for the manifest, the build files and the resources; not
verified here (the conventions were not in this plan's reading list)
Also in: —

---

### diagnostiqueur.md F12 — a set-aside reason with no heading

Verdict: confirmed
Decision: Give the set-aside reason a heading — `## Today` carries it,
the file and symbol that already do it or the statement that nothing
matched — with `## Searched` carrying the paths beside the terms as
L235 already requires, and have invocation 2 copy `## Today` into
`## Gaps set aside`.
Where: diagnostiqueur.md L226-228, L244-245 ↔ L384-410, L560
Cited: L244 — "Something does it as described | `set aside` — name the
file and the symbol"; L245 — "Nothing relates to the terms at all |
`set aside` — say what you searched"; L226-228 — "`set aside`, saying
where you think it lives"; L420-421 — "On `set aside`, `## Bearer`,
`## Trigger` and `## Expected` are written empty"; L560 — "Then the gaps
set aside, with the reason their report gives"; L407-409 — the
`## Searched` example holds four terms and no path.
Owner: diagnostiqueur
Also in: —

`## Today` is the one heading L420-421 does not empty on `set aside`,
and nothing routes the reason there today: the decision makes the
implicit place the declared one.

---

### diagnostiqueur.md F13 — a second bearer has no trigger

Verdict: confirmed
Decision: Repeat `## Trigger` with `## Today` and `## Expected` under
every `## Bearer` block, and restate the heading count to match.
Where: diagnostiqueur.md L411-415 ↔ L392-393
Cited: L411-413 — "Six headings, always — 📌 and `## Bearer` repeated
once per bearer when the gap has several, each with its own `## Today`
and `## Expected` under it"; L414-415 — "`## Trigger` ends in `observed`
or `nothing observes it`, never in the trigger alone."
Owner: diagnostiqueur
Also in: —

---

### diagnostiqueur.md F14 — "by grep", and a caller's body

Verdict: confirmed
Decision: Declare the move-5 caller read in the description and in
invocation 1's inputs row.
Where: diagnostiqueur.md L3, L138 ↔ L122-124
Cited: L3 — "Reads the code by grep, at invocation 1 only."; L138 —
"the code, by grep"; L122-124 — "Read the code beyond a grep […] ⚠️ One
exception, move 5: a caller's body, to see whether it uses what it is
handed".
Owner: diagnostiqueur
Also in: —

---

### diagnostiqueur.md F15 — examples that contradict the path rule

Verdict: confirmed
Decision: State that code locations — a bearer's file, a searched
folder — are repository-root paths like `docs/`, and that only the
bug-fix folder's own files are relative to it.
Where: diagnostiqueur.md L40-41 ↔ L390, L565-566
Cited: L40-41 — "Every other path in this file is relative to that
folder — 🔴 never `C:\…` or `/…`."; L390 — "RaceRecordingRepository —
app-wear/.../race/RaceRecordingRepositoryImpl.kt"; L565 — "Step
counter: HomeScreen already renders it, lib/features/home".
Owner: diagnostiqueur
Also in: —

---

### diagnostiqueur.md F16 — the existence check after the whole assembly

Verdict: confirmed
Decision: Move the `desc-bug.md` existence test to the head of
invocation 2, before the count of reports.
Where: diagnostiqueur.md L503-505 ↔ L430-495
Cited: L430 — "Once, when every report exists."; L442-444 — "Count
both: a missing file means an investigation did not run."; L503 — "If
the file already exists, write the blocking file" — under `### What you
write`, after the nine moves and the three closures.
Owner: diagnostiqueur
Also in: —

One change with F05 and F07: the test comes first, and its outcome is
the stop.

---

### diagnostiqueur.md F17 — the phase-1 blocking file is never renamed

Verdict: confirmed
Decision: Have the command rename `investigation/blocked_<id>.md` to
`investigation/blocked_<id>-NN.md` once the investigation reports
having applied its decision — the same gesture as for
`blocked_diagnostiqueur.md`.
Where: diagnostiqueur.md L164-167 ↔ diagnostique.md L164-171, L77-79
Cited: diagnostiqueur.md L164 — "Apply it, and say in your report that
you did — 🔴 the orchestration renames the file"; L166-167 — "You never
rename it — 📌 you have no tool that removes a file. ⚠️ The orchestration
does it, once you have reported."
Cited: diagnostique.md L164-168 — "Its `## Decision` filled, run
`/diagnostique` again — 📌 name the file in the agent's prompt, and 🔴
rename it once the agent reports having applied it: git mv
blocked_diagnostiqueur.md blocked_diagnostiqueur-NN.md"; L77-79 — "Skip
a gap whose report already exists, unless its
`investigation/blocked_<id>.md` carries a filled `## Decision`."
Cited: audit_blocages.md L26-29 — "Every `blocked_*-NN.md` of the
working folder […] 🔴 Three places: `code/**/`, the folder's own root
[…], and `investigation/` *(a `/diagnostique` phase 1)*" — the renamed
file already has a reader.
Owner: diagnostique.md (command)
Follows: — (diagnostiqueur L154-158 already reads the `-NN` siblings
in `investigation/`; audit_blocages.md L26-29 already lists them —
verified, nothing to rewrite on either side)
Also in: — (`fichiers.md` F05 is the same defect, entered below)

---

### diagnostiqueur.md F18 — a blocked gap re-issued on an empty decision

Verdict: confirmed
Decision: Have the command also skip a gap whose
`investigation/blocked_<id>.md` still carries an empty `## Decision`,
relaying it as still standing instead of re-issuing its investigation.
Where: diagnostique.md L77-79 ↔ diagnostiqueur.md L163, L433-434
Cited: diagnostique.md L77-79 — "Skip a gap whose report already
exists, unless its `investigation/blocked_<id>.md` carries a filled
`## Decision`." — a gap with no report and an empty decision matches
neither clause.
Cited: diagnostiqueur.md L163 — "A `## Decision` still empty | 🔴
Stop. Nothing changed — say the blocking file still stands"; L433-434 —
"a gap whose investigation blocked has no report at all."
Owner: diagnostique.md (command)
Follows: — (L163 stays as the agent's own guard)
Also in: —

---

### fichiers.md F05 — the applied phase-1 decision that never settles

Verdict: confirmed
Decision: Same as diagnostiqueur.md F17 — the command renames the
phase-1 file once its decision is reported applied.
Where: diagnostique.md L168 ↔ diagnostiqueur.md L71
Cited: diagnostique.md L168 — "git mv blocked_diagnostiqueur.md
blocked_diagnostiqueur-NN.md" — the only rename the command performs.
Cited: diagnostiqueur.md L71 — "1 | `investigation/blocked_<id>.md` —
🔴 your own identifier, so ten calls never collide".
Cited: audit_blocages.md L34-36 — "And `code/**/blocked_*.md` without a
number — one still standing. ⚠️ Read it and list it under `### Still
open`" — an unrenamed file with a filled decision is listed as open.
Owner: diagnostique.md (command)
Follows: —
Also in: — (same decision as diagnostiqueur.md F17)

---

### chemins-aval.md F12 — one phase-1 block, two decisions

Verdict: confirmed
Decision: Have the command withhold phase 2 while a phase-1 block
stands — its L107 already says "once every report exists" — and relay
the blocked identifiers from its own phase-1 results, so that no
`blocked_diagnostiqueur.md` is written for a report no decision can
supply.
Where: diagnostique.md L173-178 (the report's "L235" — the file has
179 lines) ↔ diagnostiqueur.md L163, L173-184
Cited: diagnostique.md L107 — "Phase 2 — one `Agent()`, once every
report exists."; L173-174 — "A phase-1 block does not cancel phase 2 —
invocation 2 counts the reports against `bug-list.md` and blocks itself
if one is missing."; L176-178 — "Say which identifier the missing
report belongs to, taken from invocation 2's own block."
Cited: diagnostiqueur.md L163 — "A `## Decision` still empty | 🔴
Stop. Nothing changed — say the blocking file still stands"; L180 —
"One is still missing | 🔴 Block again, naming which — a decision cannot
write a report"; L182-184 — "A missing report is fixed by re-running
its investigation, not by a decision."
Owner: diagnostique.md (command)
Follows: diagnostiqueur — L173-184 keep their guard for a direct
invocation, and L182-184 stop telling the Product Owner to have the
gap re-run through a decision on the assembly's file; the command's
own L173-178 change to match
Also in: —

The two command rules contradict each other today (L107 against
L173-174); the decision keeps the one that costs no invocation and no
empty decision. The other route — the orchestration removing
`blocked_diagnostiqueur.md` once the report appears — needs a deletion
gesture the command does not have and the agent's L182-184 argue
against.

---

## Not judged

`diagnostiqueur.md` section 2, rows D-12, D-19, D-22 — `open`, with no
text, no line, and no pass sheet on disk to say what they asked. There
is nothing to confirm or contradict; they get no verdict and no
decision. If the Product Owner holds the working file they come from,
its three items are the input this plan lacks.

---

## To settle

### diagnostiqueur.md F10 — the state document is read, and nothing follows

Verdict: confirmed
Decision:
Where: diagnostiqueur.md L138 ↔ L238-246
Cited: L138 — "`docs/CURRENT_TECHNICAL_STATE.md` — 📌 its `## Traps —
general` and `## Dead state` sections, to see whether the gap is a trap
already recorded"; L238-246 — the verdict table has five rows, none on
a recorded trap; moves 1 to 5 (L205-377) never name the state document.
Owner: diagnostiqueur
Also in: —

The previous round's D-16 gave the input a purpose and left the outcome
unwritten; what the Product Owner wants from that reading is not in any
file this plan read. Three options, with what each costs:

| Option | What it costs |
|---|---|
| **Drop the input** — invocation 1 reads the conventions and the code only | A gap the state document already records as a trap or as dead state is investigated from nothing; the Détailleur reads the state document later in any case. F04 becomes moot. |
| **Keep it as a search aid** — a recorded trap or dead symbol is named in `## Today` (and, for dead state, feeds move 3's bearer search); the verdict is unchanged | A reach gesture (F04) and one line under `## Today`; the cheapest outcome that uses the reading. |
| **Keep it as a verdict input** — a gap recorded as a trap is `set aside` with the state document as its reason | Wrong on its face: a recorded trap is a known pitfall, not a fix; the gap stands regardless. Listed only because it is the reading L138's wording invites. |

F04's decision applies only under the second option.
