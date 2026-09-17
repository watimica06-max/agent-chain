# Verification — `testeur.md`

Section 1: the file is new (🆕, no `.claude/agents/testeur.md`, no pass sheet) — the index alone is the record, every origin is `refonte`.

| # | Severity | Origin | Section | Where | Finding |
|---|---|---|---|---|---|
| F01 | NOTE | refonte | 1 | modifications.md L898 ↔ testeur.md L227 | The index says an older test failing is always a block, while the file adapts it when the sheet declares the signature modified and blocks only otherwise, so the record states a rule the file does not carry. |
| F02 | NOTE | refonte | 1 | modifications.md L897 ↔ testeur.md L221 | The index says a new test that passes is always rewritten, while the file leaves green a test asserting a declaration alone, so the record omits a branch the file has. |
| F03 | TO FIX | refonte | 3 | testeur.md L206 ↔ testeur.md L92 | When the conventions name no test command the file says « use what they give », but the `Bash` bound admits only the command the conventions name, so on a project whose conventions are not yet derived move 4 has no command it may run and the red check cannot happen. |
| F04 | TO FIX | refonte | 2 | testeur.md L187 ↔ testeur.md L138 | Move 2 defines *no* as « cannot be observed from outside the running code » and sends every *no* to the manual list, while L138 makes an internal criterion (« the value is cached ») a block, so the same criterion is routed to two outcomes and move 2 has no branch that ends in a blocking file. |
| F05 | TO FIX | refonte | 2 | testeur.md L136 ↔ testeur.md L105 | « Two things block you » is followed by two cases, but L105 already made a signature the testeur cannot test against a third block, so the closed count is false and that block has no `## Where` wording (criterion or failing test) that fits it. |
| F06 | TO FIX | refonte | 2 | testeur.md L23 ↔ testeur.md L221 | « Every new test has to fail » and the `## Red` template (« every new test failed », L280) stand beside the rule that a declaration-only test is left green, so a run that follows L221 cannot write a truthful `## Red` and the old absolute rule was left standing beside the new exception. |
| F07 | TO FIX | refonte | 2 | testeur.md L207 ↔ testeur.md L270 | Three outcomes are to be « said in your report » — no test command named (L207), a green declaration-only test (L221), a criterion gone with its behaviour (L233) — and the four-heading template has no heading to receive any of them, so each lands in an unnamed place or nowhere. |
| F08 | TO FIX | refonte | 2 | testeur.md L119 ↔ testeur.md L132 | The blocking procedure commits « the tests you did write, the blocking file with them » and never says to write `tests.md`, yet L132 reads a pre-existing `tests.md` as the trace of a blocked run and resumes from its `## Tests`, so a resumed run finds no `## Tests` and rewrites every criterion. |
| F09 | NOTE | refonte | 2 | testeur.md L84 ↔ testeur.md L230 | The file forbids taking another lot's tests as input (« what they assert is not your criterion ») and then orders adapting an older test so that « it keeps its assertion », which cannot be done without reading that assertion, and the L86 exception covers adding only. |
| F10 | TO FIX | refonte | 4 | testeur.md L132 ↔ 8_code.md L113 | The command skips the testeur whenever `code/<lot>/tests.md` is there, while step 4b (L170) names a filled `blocked_testeur.md` in its prompt, so after a Product Owner decision the resume rule at L132 fires only if the orchestrator disregards L113, and the realisateur may run on a lot whose criteria are half-covered. |
| F11 | TO FIX | refonte | 4 | testeur.md L221 ↔ realisateur.md L21 | The realisateur is told « every one of them failed », and the command (8_code.md L113) that the testeur « checks each fails red », while the testeur may leave a declaration-only test green, so a downstream reader takes as given a state the producer does not guarantee. |
| F12 | NOTE | refonte | 4 | testeur.md L58 ↔ detailleur.md L265 | The testeur takes `## Files` as naming « where your tests go », but the sheet carries a dash when the lot creates everything it touches, so on such a lot the test file has no named home and lands in `## Outside the lot` on every run. |
| F13 | NOTE | refonte | 4 | testeur.md L259 ↔ realisateur.md L335 | The reason given for committing — « the realisateur runs `git restore` » — is not what the realisateur does: it restores only the files it edited, never a test file, so the stated cause is false and only the worktree-removal cause at L260 holds. |
| F14 | TO FIX | refonte | 4 | testeur.md L233 ↔ 8_code.md L113 | The testeur reports that a criterion's behaviour is gone and that « only the Product Owner removes a behaviour », but the command relays nothing from the testeur's report (it relays the concepteur's `## Placements` line, L112), so the removal reaches nobody and is never decided. |

Checked and found sound: the frontmatter's six tools each have a stated gesture and `Bash` is bounded; `## Declared`, `## Signatures`, `## Acceptance criteria`, `## Files`, `permanente` and the not-implemented throw exist as the concepteur, detailleur and architecte write them; `## Red`, `## Tests`, `## Criteria with no test`, `## Outside the lot` and `code/recette.md` each have their reader in the realisateur, relecteur or `/9_controle`; the prompt, model and blocking-file path match the command and `CLAUDE.md`.

| # | Status | Where | One line |
|---|---|---|---|
| B.1 (rationale row) | open | — | |
| C (test command, `Bash` scope) | fixed | `.claude-new/agents/testeur.md` l.92-96, l.205-207 | |
| C (commit — question) | fixed | `.claude-new/agents/testeur.md` l.121-123, l.255-260 | |
| C (Grep/Glob unused — NOTE) | fixed | `.claude-new/agents/testeur.md` l.74-79 | |
| D.1 | fixed | `.claude-new/agents/testeur.md` l.138-147 | |
| D.2 | fixed | `.claude-new/agents/testeur.md` l.142-143, l.161-162 | |
| D.3 (question) | fixed | `.claude-new/agents/testeur.md` l.223-233 | |
| D.4 | fixed | `.claude-new/agents/testeur.md` l.78-79, l.84-86 | |
| D.5 | fixed | `.claude-new/agents/testeur.md` l.121-134 | |
| D.6 (question) | fixed | `.claude-new/agents/testeur.md` l.58-59, l.282-284 · `.claude-new/agents/detailleur.md` l.244-248, l.259-263 | |
| D.7 | fixed | `.claude-new/agents/testeur.md` l.235-237 | |
| D.8 (question) | fixed | `.claude-new/agents/testeur.md` l.216-221 | |
| D.9 | fixed | `.claude-new/agents/testeur.md` l.92-96, l.205-207 | |
| D.10 | moot | `.claude-new/CLAUDE.md` l.94-96 | `effort` is now declared optional in `CLAUDE.md` ("Its absence is not an omission"); the other items were counts (still right: six moves l.176, four headings l.153) and style, no change asked |
