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
| `features/premiere-app-3/idees.md`, `lexique.md`, `questions-lexicographe-01.md` | the feature's root, after the lexicographe's sweep (agents/lexicographe.md:310-316) |
| `real/premiere-app-3/questions-lexicographe-01.md` | the same sweep, as first written, every entry open |
| `context/premiere-app-3/idees.md`, `questions-lexicographe-02.md` | the settling pass (agents/lexicographe.md:538-544) and the idea file it points to |
| `logs/2026-10-06-111521-1_lexique.jsonl` | the cockpit's own log of `/1_lexique premiere-app-3` |
| `logs/2026-10-06-094500-probe.jsonl` | a probe run of the SDK in a scratch folder, an agent calling a nested one (`outer`, `inner`) |
| `hyrox/deploie.md` | hyrox_tracker's `.claude/commands/deploie.md` at its commit 1305da0 — the command 1.8's profile replaces, its lines cited by docs/app/DEPLOY_PROFILE.md §5 |

## Hand-written, after a template

| Fixture | Template |
|---|---|
| `hand/questions-classeur-01.md` | agents/classeur.md:147-153 |
| `hand/questions-redacteur-01.md` | agents/redacteur.md:288-294 — Q1 answered over several lines, as the writer writes it |
| `hand/questions-sondeur-02.md` | agents/sondeur.md:394-421 — `Options:`, `Défaut:` |
| `hand/questions-architecte-02.md` | agents/architecte.md:546-553 — a title on `Block:`, `Kind:` |
| `hand/questions-lexicographe-02.md` | agents/lexicographe.md:538-544, and :336-350 for Q2's two meanings; the file's title as premiere-app-3's |
| `hand/convertisseur/technique-model.md`, `technique-transversal.md` | agents/convertisseur.md:389-395 |
| `hand/blocked_lexicographe.md` | agents/lexicographe.md:76-83 |
| `hand/blocked_architecte.md` | agents/architecte.md:250-256 — `## Invocation` first |
| `hand/blocked_redacteur.md` | agents/redacteur.md:373-392 and :404-410 — invocation 3, one `## Blocking N` and one `## Decision` per entry |
| `hand/blocked_qualifieur.md` | agents/qualifieur.md:267-286 |
| `hand/blocked_cadreur.md`, `hand/cadreur-request/blocked_cadreur.md` | agents/cadreur.md:192-211 — the first appended twice, its last `## Decision` live |
| `hand/cadreur-request/architecte-cadreur.md` | agents/cadreur.md:242-248 — two `# Request N`, the first with its verdict |
| `hand/blocked_verificateur.md` | agents/verificateur.md:200-211 — three headings, no `## Decision` |
| `hand/blocked_concepteur-01.md` | agents/concepteur.md:149-166 — `## Decision` filled |
| `hand/blocked_relecteur-acte.md`, `blocked_relecteur-autre.md` | agents/relecteur.md:279-297 |
| `hand/blocked_detailleur.md` | agents/detailleur.md:334-354 — `## Blocking N — lot-NN`, one `## Decision` at the end |
| `hand/blocked_realisateur.md` | agents/realisateur.md:310-321 |
| `hand/redecoupage/redecoupage.md`, `redecoupage-01.md`, `redecoupage-02.md` | agents/cadreur.md:1054-1061 — the Cadreur's two sections |
| `hand/questions-hors-gabarit.md` | **none, on purpose**: a `## Q1` heading no template writes — the file the parser reports as an error |

## Built in the tests

The folders a test writes itself say their template in the test:
`test_codelots.hand_folder` and its redécoupage sections
(agents/arbitre.md:379-399), `test_scan.build_chain` (a feature through the
whole chain, two corrections), and the git history of
`test_codelots.test_a_lots_commits_are_found_by_their_subject_after_the_split_in_force`
(8_code.md:198-229).
