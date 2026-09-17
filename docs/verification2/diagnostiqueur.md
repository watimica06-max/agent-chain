# Verification — `diagnostiqueur.md`

Section 1: no pass sheet exists for this agent (`docs/refonte/passes/diagnostiqueur.md` absent); the index alone is the record.

| # | Severity | Origin | Section | Where | Finding |
|---|---|---|---|---|---|
| F01 | TO FIX | refonte | 1 | modifications.md L1601 ↔ diagnostiqueur.md L38-45, L76-79, L120-124, L138, L164-167, L225-231, L311-313, L333-338, L411-421, L432-444, L459-460, L472-474, L493-495, L503-505 | The index marks the file untouched ("rien du fichier de travail", no ✅) while the file carries some twenty changes — paths rule, four block cases, move-5 exception, state-document sections, orchestration rename, second widening, `Bearer: none` on a move, per-bearer report blocks, block on an existing `desc-bug.md` — so none of them can be checked against a request and the index does not tell the truth for this agent. |
| F02 | NOTE | refonte | 1 | modifications.md L1320-1522 ↔ diagnostique.md L44-70, L157-158, L164-171 | The command was rewritten (git section moved ahead of the invocation, `TaskCreate` and risk level dropped, a `git mv` rename rule added) and the index's command section never names `diagnostique.md`, so those changes are unrecorded too. |
| F03 | NOTE | pre-existing | 3 | diagnostiqueur.md L4 ↔ L154-158, L503 | `Glob` is granted and no gesture names it, while the two gestures that need it — finding the settled `-NN` files beside the blocking file, and testing whether `desc-bug.md` already exists — name no tool at all, so the agent may reach for `Glob` anywhere or skip those checks. |
| F04 | NOTE | refonte | 3 | diagnostiqueur.md L138 ↔ L144 | The input names two sections of a 2 300-line state document but no gesture says how to reach them, so the agent reads the whole file to obey "load only what your invocation lists". |
| F05 | TO FIX | refonte | 2 | diagnostiqueur.md L76-79 ↔ L503-505 | Blocking is announced as "four cases", and a fifth — `desc-bug.md` already existing — is ordered as a block later, so the enumeration that tells the agent when it may block is wrong. |
| F06 | TO FIX | refonte | 2 | diagnostiqueur.md L311-313 ↔ L316-317 | A behaviour that moves is given `Bearer: none` ("where it lands is the Cadreur's") and, three lines on, "The bearer is where it lands" — the old rule left standing beside the new one, so a move gap has two contradictory bearer rules and the entry's `Bearer:` line is undecidable. |
| F07 | TO FIX | refonte | 2 | diagnostiqueur.md L503-505 ↔ L173-180 | An existing `desc-bug.md` is a block, but no decision can lift it: the resume path re-runs the assembly and meets the same block, the agent has no tool that removes the file and nothing tells the orchestration to, so the cycle waits on a `## Decision` that nothing can apply. |
| F08 | TO FIX | refonte | 2 | diagnostiqueur.md L333-335 ↔ L461-465 | What "belongs to another entry" is to be written as "a line of `## Expected`", and invocation 2 folds every requirement of `## Expected` into the same entry, so what the rule says belongs elsewhere lands in the very entry it should be kept out of. |
| F09 | TO FIX | refonte | 2 | diagnostiqueur.md L453-454 ↔ L459-460, L555-557 | Move 6 gives one nature per gap and move 7 writes one entry per `## Bearer` block, so a gap with a view bearer and a repository bearer gets one nature and one of its entries is filed in the wrong section. |
| F10 | TO FIX | refonte | 2 | diagnostiqueur.md L138 ↔ L238-246 | The state document is read "to see whether the gap is a trap already recorded", and no verdict row, move or heading says what follows when it is, so the reading has no outcome. |
| F11 | TO FIX | pre-existing | 2 | diagnostiqueur.md L198-200 ↔ L210-223 | Every search must target the code folders the conventions name and never a bare pattern, yet the agent is also told to search manifests, build files and resources — "everything the build carries" — which those folders do not hold, so one of the two rules is broken on every gap. |
| F12 | TO FIX | pre-existing | 2 | diagnostiqueur.md L226-228, L244-245 ↔ L384-410, L560 | A `set aside` verdict must say where the behaviour lives, or name the file and symbol, and invocation 2 copies "the reason their report gives", but none of the six headings holds a reason — `## Bearer`, `## Trigger`, `## Expected` are written empty and `## Searched` holds terms — so the reason has no place and the set-aside list is written from nothing. |
| F13 | NOTE | refonte | 2 | diagnostiqueur.md L411-415 ↔ L392-393 | Only `## Today` and `## Expected` are repeated under each `## Bearer`, so a second bearer has no `## Trigger` and cannot end in "observed" or "nothing observes it", and "six headings, always" no longer holds for a multi-bearer report. |
| F14 | NOTE | refonte | 2 | diagnostiqueur.md L3, L138 ↔ L122-124 | The description and the inputs table still say "the code, by grep" while the move-5 exception now has the agent read a caller's body, so the declared inputs understate what invocation 1 opens. |
| F15 | NOTE | pre-existing | 2 | diagnostiqueur.md L40-41 ↔ L390, L565-566 | Every path that does not start with `docs/` is relative to the bug-fix folder, yet the example bearer `app-wear/.../race/...kt` and the set-aside example `lib/features/home` are repository-root paths, so the examples contradict the path rule they sit under. |
| F16 | NOTE | pre-existing | 2 | diagnostiqueur.md L503-505 ↔ L430-495 | The rule blocking on an existing `desc-bug.md` stands after the nine moves and the three closures, so a full assembly is done before the check that makes it pointless. |
| F17 | TO FIX | refonte | 4 | diagnostiqueur.md L164-167 ↔ diagnostique.md L164-171, L77-79 | The agent hands the rename to the orchestration, but the command renames only `blocked_diagnostiqueur.md`; a phase-1 `investigation/blocked_<id>.md` keeps its filled `## Decision` forever, and the skip rule then re-issues that gap at every launch, which re-applies the decision and rewrites its report. |
| F18 | NOTE | pre-existing | 4 | diagnostique.md L77-79 ↔ diagnostiqueur.md L163, L433-434 | A gap whose investigation blocked has no report, so the command re-issues it even when its `## Decision` is still empty, and the agent stops at once — one wasted invocation per launch until the Product Owner answers. |

Checked and sound: the blocking-file shape and both file names against `audit_blocages.md`; the three closures and the five set aside against the grid's headings (both `docs/` and `docs-new/`); the nine section names and the `Bearer:` line against the Cadreur, Détailleur and Vérificateur; the two state-document headings; both invocation prompts against what the agent expects.

| # | Status | Where | One line |
|---|---|---|---|
| B′-1 | fixed | `agents/diagnostiqueur.md` 541–544 · `agents/detailleur.md` 558 | |
| C-rename | fixed | `agents/diagnostiqueur.md` 164–167 · `commands/diagnostique.md` 165–170 | |
| D-1 | fixed | `agents/diagnostiqueur.md` 411–413, 439–440, 459, 555–556 | |
| D-2 | fixed | `agents/diagnostiqueur.md` 120–121, 546 | |
| D-3 | other | `agents/diagnostiqueur.md` 311–317 | 311–313 now writes `Bearer: none` for a move, but 316–317 still ends *"The bearer is where it lands"* — both answers sit in one paragraph |
| D-4 | fixed | `agents/diagnostiqueur.md` 76–79 | |
| D-5 | fixed | `agents/diagnostiqueur.md` 474, 493–495, 503–505 | |
| D-6 | fixed | `agents/diagnostiqueur.md` 139, 432–434 | |
| D-7 | fixed | `agents/diagnostiqueur.md` 38–42 | |
| D-8 | fixed | `agents/diagnostiqueur.md` 173–175 | |
| D-9 | fixed | `agents/diagnostiqueur.md` 122–124 | |
| D-10 | fixed | `agents/diagnostiqueur.md` 333–338 | |
| D-11 | other | `agents/diagnostiqueur.md` 347–348, 365, 375, 462 | *"second gap"* became *"second requirement"*; the question on 323 vs 462–464 (a signature change on something other than the bearer) is not answered |
| D-12 | open | — | |
| D-13 | fixed | `agents/diagnostiqueur.md` 186–187 | |
| D-14 | fixed | `agents/diagnostiqueur.md` 417–418 | |
| D-15 | fixed | `agents/diagnostiqueur.md` 230–231 | |
| D-16 | other | `agents/diagnostiqueur.md` 138 | The input line now states a purpose (*Traps — general*, *Dead state*, whether the gap is a trap already recorded); moves 1 to 5 still never use the outcome |
| D-17 | fixed | `agents/diagnostiqueur.md` 150 | |
| D-18 | fixed | `agents/diagnostiqueur.md` 267–268 | |
| D-19 | open | — | |
| D-20 | fixed | `agents/diagnostiqueur.md` 536–539 | |
| D-21 | fixed | `agents/diagnostiqueur.md` 472–473 | |
| D-22 | open | — | |
