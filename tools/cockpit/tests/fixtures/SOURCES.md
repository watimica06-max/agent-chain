# Fixtures — where each one comes from

Cockpit 1.5.1. Every fixture is either a real file of the current chain
(`premiere-app-3`, copied as it stood) or a hand-written file following a
current template, named below by its line. The earlier chain's folders
(`premiere-app`, `premiere-app-2` and their `bugfix-NN/`) are never used:
no current command produces their shapes. Paths of the templates are
relative to `.claude/`.

## Real files of the current chain

| Fixture | The file |
|---|---|
| `features/premiere-app-3/idees.md`, `lexique.md`, `questions-lexicographe-01.md` | the feature's root, after the lexicographe's sweep — 📌 **in the shape before `.claude/formats/questions.md`**: questions in English, occurrences inside the question; still read |
| `real/premiere-app-3/questions-lexicographe-01.md` | the same sweep, as first written, every entry open |
| `context/premiere-app-3/idees.md`, `questions-lexicographe-02.md` | the settling pass, in the same earlier shape, and the idea file it points to |
| `logs/2026-10-06-111521-1_lexique.jsonl` | the cockpit's own log of `/1_lexique premiere-app-3` |
| `logs/2026-10-06-094500-probe.jsonl` | a probe run of the SDK in a scratch folder, an agent calling a nested one (`outer`, `inner`) |
| `hyrox/deploie.md` | hyrox_tracker's `.claude/commands/deploie.md` at its commit 1305da0 — the command 1.8's profile replaces, its lines cited by docs/app/TECHNICAL_V1.md §23.1 |

## Hand-written, after a template

| Fixture | Template |
|---|---|
| `hand/questions-classeur-01.md` | agents/classeur.md:149-155 |
| `hand/questions-redacteur-01.md` | agents/redacteur.md:318-324 — Q1 answered over several lines, as the writer writes it |
| `hand/questions-sondeur-02.md` | agents/sondeur.md:403-431 — `Options:`, `Défaut:` |
| `hand/questions-architecte-02.md` | agents/architecte.md:589-598 — a title on `Block:`, `Kind:` |
| `hand/questions-lexicographe-02.md` | the lexicographe's shape before `.claude/formats/questions.md` — Q2's two meanings inside the question; the file's title as premiere-app-3's |
| `hand/questions-lexicographe-03.md` | agents/lexicographe.md:370-380 and :413-423 — the questions format: French, the stake first, `Occurrences:` after `Options:`; generic words |
| `hand/convertisseur/technique-model.md`, `technique-transversal.md` | agents/convertisseur.md:428-434 |
| `hand/blocked_lexicographe.md` | agents/lexicographe.md:110-120 |
| `hand/blocked_architecte.md` | agents/architecte.md:285-291 — `## Invocation` first |
| `hand/blocked_redacteur.md` | agents/redacteur.md:402-421 and :430-436 — invocation 3, one `## Blocking N` and one `## Decision` per entry |
| `hand/blocked_qualifieur.md` | agents/qualifieur.md:274-293 |
| `hand/blocked_cadreur.md`, `hand/cadreur-request/blocked_cadreur.md` | agents/cadreur.md:195-214 — the first appended twice, its last `## Decision` live |
| `hand/cadreur-request/architecte-cadreur.md` | agents/cadreur.md:248-254 — two `# Request N`, the first with its verdict |
| `hand/blocked_verificateur.md` | agents/verificateur.md:202-213 — three headings, no `## Decision` |
| `hand/blocked_concepteur-01.md` | agents/concepteur.md:153-170 — `## Decision` filled |
| `hand/blocked_relecteur-acte.md`, `blocked_relecteur-autre.md` | agents/relecteur.md:283-301 |
| `hand/blocked_detailleur.md` | agents/detailleur.md:367-387 — `## Blocking N — lot-NN`, one `## Decision` at the end |
| `hand/blocked_realisateur.md` | agents/realisateur.md:336-347 |
| `hand/redecoupage/redecoupage.md`, `redecoupage-01.md`, `redecoupage-02.md` | agents/cadreur.md:1121-1128 — the Cadreur's two sections |
| `hand/questions-hors-gabarit.md` | **none, on purpose**: a `## Q1` heading no template writes — the file the parser reports as an error |

## Built in the tests

The folders a test writes itself say their template in the test:
`test_codelots.hand_folder` and its redécoupage sections
(agents/arbitre.md:379-399), `test_scan.build_chain` (a feature through the
whole chain, two corrections), and the git history of
`test_codelots.test_a_lots_commits_are_found_by_their_subject_after_the_split_in_force`
(8_code.md:206-237).
