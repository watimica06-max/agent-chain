# Code rules — /8_code, lot by lot

Cockpit 1.5. The « Code » tab (`codelots.py`) reads a working folder's
`code/` the way `/8_code` and its agents read and write it — files, the
stats store's agent passes, and `git log` read-only. No Claude call, no
write. Every rule below is a line of a command or an agent: `test_scan.py`
checks that each cited line still says what the rule reads in it, the way
it checks `scan_rules.md`. Paths are relative to `.claude/commands/` unless
they start with `agents/`.

A state or a field no rule gives is **« inconnu »**: listed in §8, never
guessed.

---

## 1. The lots and their order

| Rule | What | Lines |
|---|---|---|
| `L-ORDRE` | The lots, in order: the `lot-NN` of `code/sequence.md`'s `## Order`; the blocks: its `## Blocks`, `block-N: lot-…, lot-…`. A lot is named `lot-` and its number. The `Round: N` line above them is the Vérificateur's and is not read. | 8_code.md:38-39 · agents/verificateur.md:107-115 |
| `L-TITRE` | What the Product Owner can read of a lot: its section `## lot-NN` in `code/decoupage.md`, five fields — `Anchor` (the entries it builds from, `§n.m — heading`: shown as its **title**), `Needs`, `Produces`, `Modifies`, `Touches` (its **scope**). No lot carries a title of its own. | agents/cadreur.md:848-854 |

The reader of « n / N en PASS » (`scan.lot_order`, `scan.lot_verdict`) is the
one the « Code » tab uses: the bar and the badge cannot disagree.

## 2. The states of a lot

Read in this order — the first that applies:

| Rule | State | Test | Lines |
|---|---|---|---|
| `E-ENCOURS` | **en cours** | a `/8_code` run of the cockpit goes on this working folder, and its running agent's input names the lot (§6); when no running agent names one (the Détailleur on a block, the orchestrator between two agents), the next lot by the command's own rule: the first of the sequence with no `verdict.md` whose `## Status` starts with `PASS` — said so | 8_code.md:605-606 · 8_code.md:80-82 |
| `E-BLOQUE` | **bloqué** | a blocking entry waiting on her belongs to the lot — read by « À répondre », never again here: an unnumbered `code/<lot>/blocked_*.md`, or an entry `## Blocking N — <lot>` of `code/blocked_detailleur.md` | 8_code.md:348-355 · 8_code.md:748-758 |
| `E-PASSE` | **passé** | `## Status` starts with `PASS`; « avec réserve » for `PASS with reservation` | 8_code.md:80-82 · agents/relecteur.md:116 |
| `E-REDEC` | **redécoupé** | a lot of the split that came back: `code/redecoupage.md` names it under `## Ce qui ne l'est pas` — « the lot in hand, whose code is dropped, and the lots left », or « the block's lots » — in an Arbitre's section (`## Ce qui bloque` …) after the Cadreur's last `## Ce qui revient` / `## Ce que j'en fais`. Once the Cadreur has written those two, the split in `code/` is the new one even when the file stays unnumbered — a re-split that did not hold (`## Defects` carrying lines, a block standing) leaves it there — and its lots are read by the other rules | agents/arbitre.md:392-396 · agents/cadreur.md:1054-1061 · 7_lots.md:165-167 · 7_lots.md:224 · 7_lots.md:227 |
| `E-INCONNU` | **inconnu** | a `verdict.md` with no readable `## Status` | aucune règle : un verdict sans « ## Status » lisible |
| `E-TROIS` | **échoué 3 fois** | not PASS, `## Attempts` at 3 or more: the lot is the Product Owner's | 8_code.md:318-320 |
| `E-ANNULE` | **annulé** | not PASS, `## Cause` reads `sheet`, and no `fiche-executable.md`: a run reverted the lot's commits and deleted its sheet, which the Détailleur writes again | 8_code.md:163-165 · agents/relecteur.md:183-186 |
| `E-ECHOUE` | **échoué** | any other verdict not PASS: a fresh Réalisateur, then the Relecteur again | 8_code.md:262-264 |
| `E-ENTAME` | **entamé** | no verdict, some of its files there: the sheet, then `conception.md`, `tests.md`, `compte-rendu.md` — each agent skipped when its report is there; « reprend au … » names the first missing, « codé, pas encore relu » when the three are there | 8_code.md:158-159 · 8_code.md:174-176 |
| `E-AFAIRE` | **pas commencé** | no verdict, no sheet, no report | 8_code.md:158-159 |

**Attempts** (`T-ESSAIS`) — the verdict's `## Attempts`, out of 3; a verdict
without the line reads 1, and the row says so; no verdict, 0 — an empty first
attempt is counted in the run's memory alone, never on disk. —
8_code.md:318-320 · 8_code.md:322-323 · 8_code.md:331-336 · agents/relecteur.md:173-175

## 3. The passes of a lot

| Rule | What | Lines |
|---|---|---|
| `P-ORDRE` | Per lot, in order: the Détailleur when the lot has no sheet (it works on the lot's **block**), then the Concepteur, the Testeur, the Réalisateur — each skipped when its report is there — then the Relecteur once the Réalisateur has reported. A FAIL is a fresh Réalisateur and the Relecteur again; three codings at most (`E-TROIS`). | 8_code.md:158-159 · 8_code.md:174-176 · 8_code.md:190 |
| `P-ECRIT` | Where each writes: the Détailleur `code/<lot>/fiche-executable.md`, the Relecteur `code/<lot>/verdict.md`, the Concepteur `code/<lot>/conception.md`, the Testeur `code/<lot>/tests.md`, the Réalisateur `code/<lot>/compte-rendu.md`. | agents/detailleur.md:55-56 · agents/relecteur.md:140 · agents/concepteur.md:301-304 · agents/realisateur.md:715 |
| `P-ARBITRE` | **The Arbitre steps in** when the Détailleur or the Réalisateur blocks: they call it themselves; the orchestrator never does. Marked on a lot when an Arbitre pass names it, or when a blocking file of the Réalisateur (`code/<lot>/blocked_realisateur*.md`) or an entry of the Détailleur naming the lot (`code/blocked_detailleur*.md`, `## Blocking N — lot-NN`) exists, settled or not. A lot's folder holds the blocking files of the Concepteur, the Testeur, the Réalisateur and the Relecteur alone. | 8_code.md:760-763 · agents/realisateur.md:342-349 · agents/detailleur.md:381-388 · 8_code.md:751-754 |
| `P-ARCHITECTE` | **The Architecte steps in** at the end of a lot (move 7, on every request with an empty `## Verdict`), and when the Arbitre calls it. | 8_code.md:488-492 · agents/arbitre.md:476-486 |
| `P-DEMANDES` | The requests it answers that are a lot's: `architecte/concepteur-<lot>.md`, `realisateur-<lot>.md`, `detailleur-<lot>.md` (a request of the walk under the block's first lot), `arbitre-<lot>-blocking-N.md`; `-NN` suffixes for a second one. Marked with whether `## Verdict` is written. `arbitre-<block>-blocking-N.md` names a block, not a lot: not on a lot's row. | agents/concepteur.md:227-230 · agents/realisateur.md:466 · agents/detailleur.md:421 · agents/detailleur.md:439-440 · agents/arbitre.md:451-460 |

## 4. A lot's blocking files and questions

| Rule | What | Lines |
|---|---|---|
| `B-OU` | Three places: `code/<lot>/blocked_<agent>.md` (Concepteur, Testeur, Réalisateur, Relecteur), `code/blocked_detailleur.md` at the split's root — its entries name their lot, `## Blocking N — lot-NN` — and `blocked_architecte.md` at the working folder's root, which blocks the run, not a lot. What waits is « À répondre »'s list: the tab links to it, filtered on the lot, and parses nothing again. No questions file sits in `code/`. | 8_code.md:748-758 · agents/detailleur.md:328-331 |

## 5. A lot's commits

| Rule | What | Lines |
|---|---|---|
| `C-GREP` | The three committing agents write `<working folder>/<lot>: <what the commit carries>`, `<working folder>` the path under `docs/features/` — `premiere-app-3`, `premiere-app-3/bugfix-01`; a revert writes `Revert "<working folder>/<lot>: …"`. The tab runs the command's three lines, read-only: `<split>` (see `C-DOSSIER`), then every commit after it whose **subject** opens on one of the two, newest first, with the files each changed (`git log --name-only`). The command's list is what follows the lot's last revert; a commit before it is marked « annulé ensuite ». | 8_code.md:198-201 · 8_code.md:206-208 · 8_code.md:217-223 |
| `C-DOSSIER` | Every split, every feature and every bug-fix cycle reuses `lot-01`, `lot-02`…: the folder in the subject tells them apart, and the search starts after `<split>`, the commit that added the current `code/decoupage.md` — only a first split creates it, so a lot kept on a PASS through a redécoupage stays after it, and a deleted split's lots before it. The subject alone: never the body (`--grep` reads it), never the files a commit stages — a Réalisateur retry that touches only code is the lot's. | 8_code.md:202-203 · 8_code.md:210-215 · 8_code.md:225-229 · agents/concepteur.md:309-312 · agents/testeur.md:317-320 · agents/realisateur.md:720-726 |

## 6. During a run

| Rule | What | Lines |
|---|---|---|
| `W-LIVE` | One worktree for the whole run, `.claude/worktrees/<name>`, where the agents write and commit: while it is live, the tab reads the files there, and `git log` runs in it — the way `blocking.py` finds live worktrees. | 8_code.md:126-128 · 8_code.md:135-136 · 8_code.md:470-475 |

What the page holds while a run goes is read again when an agent hands back
(`agent_ended`), never polled.

## 7. Which lot an agent pass belongs to

Each pass is stored (1.4) with the Agent tool's input, which the stream
carries whole: `subagent_type`, `description`, `prompt` (checked on
`tests/fixtures/logs/2026-10-06-111521-1_lexique.jsonl`). The lot is read
from it — never from timing — and stored on the pass (`agent_passes.lot`,
with `block` and `folder`); the passes stored before 1.5 are read again from
their logs, once.

| Rule | Read | Lines |
|---|---|---|
| `A-LOT` | the prompt's `Your lot: <lot>` — the orchestrator names the lot of every agent of a lot, and the Détailleur's after a `sheet` FAIL | 8_code.md:605-606 · 8_code.md:564 · 8_code.md:573 · 8_code.md:582 · 8_code.md:597 · 8_code.md:442 |
| `A-DESC` | else the description: `Declare <lot>`, `Test <lot>`, `Code <lot>`, `Review <lot>`, and the Arbitre's `Settle <lot>`, whose prompt names `code/<lot>/blocked_realisateur.md` | 8_code.md:563 · 8_code.md:572 · 8_code.md:581 · 8_code.md:596 · agents/realisateur.md:346-348 |
| `A-BLOC` | the Détailleur names a **block** (`Your block:`, `Detail <block>`, `Propagate <block>`), and so does the Arbitre it calls (`Settle <block>`): the pass's lot is « inconnu », its block known | 8_code.md:418-419 · 8_code.md:440-441 · agents/detailleur.md:385-387 |
| `A-DOSSIER` | the prompt's `Working folder:` gives the folder — the feature, or its `bugfix-NN` — so that `lot-01` of one split is not taken for another's | 8_code.md:608-609 |
| `A-AUCUN` | the Architecte of move 7 is named neither a lot nor a block: its lot is « inconnu » | 8_code.md:509-510 |
| `A-IMBRIQUE` | a nested agent works for its caller: the Arbitre a Réalisateur calls, the Architecte the Arbitre calls take their caller's lot when their own input names none — read from the stream's `parent_tool_use_id`, not from timing | agents/realisateur.md:342-349 · agents/arbitre.md:476-486 |

## 8. What is left « inconnu »

- **A pass's lot**: the Détailleur's and the Arbitre's on a block
  (`A-BLOC`) — shown on the block; the Architecte of move 7 (`A-AUCUN`);
  every pass run outside `/8_code`, and every pass whose log is gone.
- **A lot's state**: a `verdict.md` with no readable `## Status`
  (`E-INCONNU`).
- **A lot's time**: the sum of its top-level passes; unknown when one of
  them has no duration, or the lot has no stored pass — every lot coded
  before the cockpit ran `/8_code`. The Détailleur's time is the block's,
  in no lot's.
- **Written tokens**: the rule of 1.4.3 — a figure only when the pass's model
  served it alone in the run.
- **An empty attempt** of the run going (no verdict yet): held in the
  orchestrator's memory only (8_code.md:331-336).

## 9. The estimate

`D-ESTIME` — « ≈ 40 min »: the median time of this working folder's passed
lots (§8, their time known) times the lots left, shown once two passed lots
have a known time, always with « ≈ ». Not a rule of the chain — demande 1.5,
§4. The Détailleur's time, a block's, is in no lot's: the estimate leaves it
out, and says so.
