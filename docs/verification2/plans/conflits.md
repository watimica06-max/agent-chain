# Conflits — the twenty-one plans merged on `Where`

Built from `docs/verification2/plans/*.md` (twenty-one plans) and
`docs/verification2/plans/a-trancher.md`, whose `Decision:` lines
supersede what a plan said. For every merged entry whose `Where` names
two files, the file the `Cited:` line points at was opened in
`.claude-new/` at that line; where it reads as the decision assumes,
nothing is said below.

🔴 **The first table is what wave 3 applies — it supersedes the plans.**
A defect in conflict (second part) is absent from it until the Product
Owner has written under `Arbitration:`.

Conventions in the table: `index` = `docs/refonte/modifications.md`
(a record, no agent line moves); a command name as Owner = the
commands' corrector (`commandes`); *a-trancher* = the Product Owner's
decision in `a-trancher.md`, applied as written. Severity is the one the
plan states; `—` when it states none.

---

## 1 — The work

| # | Severity | Decision | Where | Owner | Follows | Same as |
|---|---|---|---|---|---|---|
| **Arbitre, blocking files, the wait** | | | | | | |
| 1 | — | Index records the three writes outside the blocking file (trap, `code/redecoupage.md`, `architecte/` request) | modifications.md L1284 ↔ arbitre.md L219-222 | index | — | arbitre.md F01 |
| 2 | — | Index summary: two destinations skip the Architecte | modifications.md L1283 ↔ arbitre.md L371-379 | index | — | arbitre.md F02 |
| 3 | — | Index trap-heading line aligned on what the `technical-state-format` skill defines; arbitre.md L391-393 is the side kept if the skill confirms it | modifications.md L1283 ↔ arbitre.md L391-393 | index | — | arbitre.md F03 |
| 4 | — | Index records that the Contrôleur is no longer named among blocks not the Arbitre's | arbitre.md L148 ↔ modifications.md L1276-1285 | index | — | arbitre.md F04 |
| 5 | — | Index records the two added Verdict outcomes (L429, L431) | arbitre.md L429-431 ↔ modifications.md L1276-1285 | index | — | arbitre.md F05 |
| 6 | — | Index records `Bash` (bound to `sleep`) and `Skill` entering the tools — the wait is kept (a-trancher arbitre 1) | arbitre.md L4 ↔ modifications.md L1276-1285 | index | — | arbitre.md F06 |
| 7 | — | Name Grep as the tool reading a verdict's `## Status`, matched on the `PASS` prefix | arbitre.md L100 ↔ arbitre.md L4 | arbitre | — | arbitre.md F07 (prefix: decisions.md passages-aval F15) |
| 8 | — | Say Glob finds the settled `-NN` files beside the blocking file and every lot's `verdict.md` | arbitre.md L4 ↔ arbitre.md L32 | arbitre | — | arbitre.md F08 |
| 9 | — | Write the settled numbers into `## Decision` before any wait begins; the wait bears on the handed-back numbers only | arbitre.md L173-176 ↔ arbitre.md L441-456 | arbitre | — | arbitre.md F10 |
| 10 | — | *a-trancher arbitre 1*: keep the twenty-minute wait exactly as it is; write the missing found-answer branch (the Arbitre applies the answer and carries on); for the *rule in force now wrong* row (L379), once the answer is in the field the Arbitre writes the `architecte/` request with it and calls the Architecte | arbitre.md L441-462, L379 ↔ 8_code.md L204-206; CLAUDE.md L146 | arbitre | detailleur (L347 wording stands), realisateur (L318 stands), 8_code (nothing) | arbitre.md F11 · chemins-aval.md F11 (arbitre plan) — the poll in the worktree is accepted as is |
| 11 | — | Reword L82 so "no other" excludes only other open blocking files; the settled numbered ones are read | arbitre.md L82 ↔ arbitre.md L88 | arbitre | — | arbitre.md F12 |
| 12 | — | One `architecte/` request per invocation, gathering every entry that needs a rule, named by the blocking file's scope (block for `code/blocked_detailleur.md`, lot for `code/<lot>/blocked_realisateur.md`) | arbitre.md L402 ↔ arbitre.md L218; architecte.md L665-666 | arbitre | architecte (L666 keys the request name) | arbitre.md F13 |
| 13 | — | L193 says the English rule bears on prose; a file's headings follow the contract that names them | arbitre.md L193 ↔ arbitre.md L337-355 | arbitre | — | arbitre.md F14 |
| 14 | — | Key what a block bears on to the entry heading (`## Blocking N — lot-NN`) and the file's author, never the folder; open the lot's sheet and report whenever the entry names a lot; the `— lot-NN` suffix becomes mandatory | arbitre.md L84-86, L97-99 ↔ detailleur.md L284-285, L292-295 | arbitre | detailleur (L292-293 states the suffix as a rule) | arbitre.md F15 · passages-aval.md F05 (arbitre, detailleur plans) |
| 15 | — | Attribute the multi-entry file to both callers | arbitre.md L159-160 ↔ realisateur.md L251-253 | arbitre | — | arbitre.md F20 |
| 16 | — | `socle.md` names the Arbitre as a writer of `CURRENT_TECHNICAL_STATE.md` (traps) and a loader of the skill, beside the Réalisateur | arbitre.md L388 ↔ socle.md L43 | socle | — | arbitre.md F21 |
| 17 | — | The Arbitre's sentence says what an Architecte block is — a missing input or a directive that cannot be placed — never "a rule nobody has written" | arbitre.md L264-265 ↔ architecte.md L253-259 | arbitre | — | architecte.md F20 (architecte plan) — *added for arbitre* |
| 18 | — | The invocation-3 prompt carries who called — the Arbitre or the orchestration | architecte.md L268-273, L344 ↔ arbitre.md L418; 8_code.md L239; 7_lots.md L167 | architecte | arbitre (L418), 8_code (L239), 7_lots (L167), conventions (the form gained under #33) | architecte.md F19 — *added for arbitre* |
| 19 | — | Extend the move-3 grep to every symbol of `## Dependencies` as well as those marked modified; the Arbitre's file says the Réalisateur reads the two general sections whole and greps its lot's symbols, not the document whole | realisateur.md L79-80, L551-557 ↔ arbitre.md L396-398 | realisateur | arbitre (L396-398) | realisateur F19 — *added for arbitre* |
| 20 | — | Add the missing-convention trigger to the block list (a rule the code needs and the conventions do not carry is a mid-lot block the Arbitre settles through the Architecte); boundary with the end-of-lot request stated by effect on the code | realisateur.md L229-232, L398-402 ↔ passes/realisateur.md C8; arbitre.md L400-404 | realisateur | — (arbitre route exists) | realisateur F03 · F15 |
| **Architecte** | | | | | | |
| 21 | — | Record C6 as applied in part, by design (`off-grid` stays on the rule; the entry citations moved to the coverage line) | passes/architecte.md L190-192 ↔ architecte.md L128, L195-198 | index | — | architecte.md F01 |
| 22 | — | Drop "a manifest" from the never-open bullet | architecte.md L305-308 ↔ L79-82 | architecte | — | architecte.md F02 |
| 23 | — | Every command's invocation-3 trigger reads an absent `## Verdict` heading as an empty one | architecte.md L696-698 ↔ 7_lots.md L143, L155-156; 8_code.md L220-221; conventions.md L71 | commandes (7_lots · 8_code · conventions) | — | architecte.md F03 |
| 24 | NOTE | Drop the four C19 justifications and the B-4 one, keeping each rule | passes/architecte.md L443-458 ↔ architecte.md L131-133, L453-455, L511-514, L685-687 | architecte | — | architecte.md F04 (+ B-4) |
| 25 | — | Show the invocation example in its four forms | passes/architecte.md L518-534 ↔ conventions.md L169-177 | conventions | — | architecte.md F05 |
| 26 | — | Add three rows to the architecte index (`## Invocation` field, rename moved to the orchestration, five-line report) | modifications.md L636-643 ↔ architecte.md L247, L359, L377-378, L215 | index | — | architecte.md F06 |
| 27 | — | Align the never-do bullet and move 6 with *The coverage file*: the rule carries `off-grid` and no entry citation; the citations go on the `couverture.md` line | architecte.md L291-292, L442 ↔ L195-198 | architecte | — | architecte.md F07 |
| 28 | — | Define what an Arbitre-called invocation 3 does with a root `blocked_architecte.md`: neither rewrites nor applies it, refuses in the verdict any request its cause still stops, naming the file | architecte.md L382-384 ↔ L272-273, L350-364 | architecte | — | architecte.md F08 |
| 29 | — | On a `bugfix-NN/`, invocation 3 writes its `couverture.md` line one level up, in the feature folder's file; the table row names that file | architecte.md L39-45, L330, L724-729 ↔ audit_conventions.md L40-43; conventions.md L76, L84-87 | architecte | audit_conventions (L91-92 reads the lot from the request's file name) | architecte.md F09 |
| 30 | — | State the trigger mark's position once — the third field of the example at L121-122 — and drop "at the end of the line" at L140 | architecte.md L119-128 ↔ L140 | architecte | — | architecte.md F10 (realisateur F08 rests on L140: see conflict C10) |
| 31 | — | Name invocation 4 in the never-open bullet's exception | architecte.md L296-297 ↔ L98-99, L797 | architecte | — | architecte.md F11 |
| 32 | — | At invocation 4 the directives are integrated at move 6b after moves 5 and 6 derive, as at 1 | architecte.md L600-601 ↔ L797-799, L444-446 | architecte | — | architecte.md F12 |
| 33 | — | State the one exception: a directive is never a question, except the `replacement` question of invocation 4 | architecte.md L585-587 ↔ L580, L552-555 | architecte | — | architecte.md F13 |
| 34 | — | Bound "at every invocation" to 1, 3 and 4 | architecte.md L477-478 ↔ L72-73 | architecte | — | architecte.md F14 |
| 35 | — | One example, five lines, and say five | architecte.md L523-530 ↔ L536-544 | architecte | — | architecte.md F15 |
| 36 | — | Report cap = a fixed part plus one line per `coverage` question | architecte.md L215 ↔ L222-223 | architecte | — | architecte.md F16 |
| 37 | — | Justify the invocation-3 coverage line by its real reader — `audit_conventions.md` finding 1 — or drop the justification | architecte.md L728-729 ↔ L460-461; audit_conventions.md L84-88 | architecte | — | architecte.md F17 |
| 38 | — | At invocation 2 the prompt names the answered `questions-architecte-NN.md`; the agent reads that file and no other | conventions.md L169-177, L73 ↔ architecte.md L611-612, L101-102 | conventions | architecte (L611-612) | architecte.md F18 |
| 39 | — | *a-trancher architecte F21*: a missing form is raised in the Architecte's questions file under a fifth `Kind:` — `forme`; the list at L546-547 becomes five; `/conventions` relays the file as it already does | GRILLE_CONVENTIONS.md L50-52 ↔ architecte.md L294, L546-547, L594-595; conventions.md L224 | architecte | conventions (relay unchanged; readers of `Kind:`) | architecte.md F21 |
| 40 | — | List the web among the inputs of rows 1 and 4 of the invocation table | architecte.md L328, L331 ↔ L72-73, L58-62 | architecte | — | architecte.md C5 · C-5 · D-2 |
| 41 | — | Keep the wrong-recollection justification in one place | architecte.md L73-74 ↔ L478-480 | architecte | — | architecte.md B-2 |
| 42 | — | One pronoun for the Product Owner — she | architecte.md L569-570 ↔ L565-568 | architecte | — | architecte.md B-6 |
| 43 | — | Say the second row is not a filter | architecte.md L708-709 ↔ L713-717 | architecte | — | architecte.md D-5 |
| 44 | — | `/2_structure` deletes `couverture.md` with the three files it already removes on a `NEW` block | 2_structure.md L164-175 ↔ conventions.md L76-77, L89-91 | 2_structure | — | fichiers.md F03 (architecte plan) |
| 45 | — | `/7_lots` exempts `questions-architecte-*.md` from its filing, as `/3a_genre`, `/4_grille`, `/6_convertit` do | 7_lots.md L47-51 ↔ conventions.md L57-58, L72; 6_convertit.md L67-69 | 7_lots | — | fichiers.md F04 (architecte plan) |
| 46 | — | Guard: `/1_lexique` and `/2_structure` never take a `questions-architecte-*.md` as the answered file. *a-trancher architecte chemins-amont F19*: conventions.md L225 keeps "corrected by hand" alone — the behaviour enters the product file and is built in the next cycle; no upstream turn re-runs | conventions.md L225 ↔ 1_lexique.md L59-65; 2_structure.md L149, L200-201; architecte.md L646-649 | commandes (1_lexique · 2_structure · conventions) | architecte (nothing — L646-649 stands) | chemins-amont.md F19 (architecte plan) |
| 47 | — | `audit_blocages` globs the still-open blocking files in the same three places as the numbered ones | audit_blocages.md L34-36 ↔ L26-29 | audit_blocages | — | chemins-aval.md F18 (architecte plan) |
| 48 | — | `/8_code` gives a root `blocked_architecte.md` the treatment of the other blocking files — checked before invoking, renamed once the Architecte reports having applied it, as conventions.md L147-154 does | 8_code.md L406-408 ↔ 8_code.md L164-175, L235-241; conventions.md L147-154; architecte.md L352-353, L359, L377-378 | 8_code | — | chemins-aval.md F24 (architecte plan) |
| 49 | settled | The Concepteur writes an `architecte/` request for a placement the conventions do not settle, places the symbol meanwhile in the module of the one it depends on most, names both in its report; the `/8_code` relay line goes (decisions.md) | concepteur.md L189-196, L255-257 ↔ 8_code.md L112; architecte.md L663-673; detailleur.md L366-380 | concepteur | 8_code (L112 relay line), architecte (nothing), detailleur (nothing) | renommages.md F16 (architecte, concepteur, detailleur, realisateur plans) · concepteur.md F10 |
| 50 | — | *a-trancher concepteur renommages F16*: a symbol that depends on nothing goes in the module the lot's other symbols land in, said in the report; when the lot has none, the module the `architecte/` request names; never a blocking file | concepteur.md L189-191 | concepteur | — | concepteur To settle 1 |
| **Assembleur** | | | | | | |
| 51 | NOTE | State the never-dropped rule once, in the merge test; Role line and forbidden line point at the gap | assembleur.md L20-22, L44-46, L230-233 ↔ passes/assembleur.md L110-115 | assembleur | — | assembleur.md F01 |
| 52 | — | Index gains "a blocked run writes no questions file, not even an empty one" | modifications.md L517-525 ↔ assembleur.md L57-59, L270-271 | index | — | assembleur.md F02 |
| 53 | TO FIX | Define *empty* by the one test (no `### Q`, no prose), drop the "a heading, a blank line" gloss so the zero-byte file the sondeur writes is the empty file; restrict the stop's example to a `### Q` heading lacking its lines | assembleur.md L146-147 ↔ L158-159; sondeur.md L376-379, L447-448 | assembleur | — | assembleur.md F03 · F10 |
| 54 | NOTE | A missing input file is a stop that writes no `blocked_assembleur.md` and no questions file; `/4_grille` gains the relay row on the model of L408 | assembleur.md L32-33 ↔ L54, L83-85 ↔ 4_grille.md L400-408 | assembleur | 4_grille (relay row) | assembleur.md F04 |
| 55 | settled | On resume, take the `Block:` value from the blocking file's `## Decision`, merge as if the question carried it; carve-out reaches L190 and L259-260; `## To resume` asks for the value | assembleur.md L87-90 ↔ L155-156, L190, L259-260 | assembleur | — | assembleur.md F05 |
| 56 | TO FIX | Name the blocking file by its full path in the assembleur prompt | 4_grille.md L423 ↔ L52, L322 ↔ assembleur.md L4, L54, L99-100 | 4_grille | — | assembleur.md F06 |
| 57 | TO FIX | State the merge-alone exception in the tense of the turn about to run, covering every previous-turn `cadrage-produit/` file, not "four" | 4_grille.md L197-198 ↔ L63-71, L200-206, L494 | 4_grille | — | assembleur.md F07 |
| 58 | — | Announced count matches the table (six) | 4_grille.md L41 ↔ L47-52 | 4_grille | — | assembleur.md F08 |
| 59 | — | Four empty files end the first time's loop, never the product file | assembleur.md L36-37 ↔ 4_grille.md L496, L498 | assembleur | — | assembleur.md F09 |
| **Cadreur · Vérificateur · 7_lots** | | | | | | |
| 60 | — | State each rule once, in the section that owns it; the never-do list points at it | cadreur.md L266 ↔ modifications.md L947 | cadreur | — | cadreur.md F01 |
| 61 | — | Move 6 sends a symbol's caller files into `Touches`, by path; `Modifies` keeps symbols; `Touches` redefined as the files a lot opens without declaring a symbol (callers, tests, manifests) | cadreur.md L524 ↔ L753; modifications.md L962 | cadreur | detailleur (`## Files` source — see conflict C1), verificateur (meaning of `Touches` widens) | cadreur.md F02 · F08 — *added for verificateur* |
| 62 | — | No agent change; the index records the `[B?:` stop (the Convertisseur writes that reference) | cadreur.md L397 ↔ modifications.md L946 | index | — | cadreur.md F03 |
| 63 | — | Dispatch row 1 fires only when the request the blocking file's `## Where` names carries a filled `## Verdict`; a mixed file is read block by block (closes D-23) | cadreur.md L295 ↔ L954 | cadreur | 7_lots (L143-144 key on the same request) | cadreur.md F05 |
| 64 | — | After D the second dispatch runs the rows below the two blocking-file rows only; none matching with `code/decoupage.md` present → the amended split goes to the Vérificateur, never through A (closes D-21) | cadreur.md L297 ↔ L949 | cadreur | — | cadreur.md F06 |
| 65 | — | A block raised in the run that applied a decision is appended as a fresh heading block; dispatch and the command read the last `## Decision`; the command renames only when that last one is filled and reported applied | cadreur.md L128 ↔ L951 | cadreur | 7_lots (L94-95, L146 read the last one) | cadreur.md F07 |
| 66 | — | `round` = one Vérificateur call and its correction; a cadreur invocation is a `run` | cadreur.md L24 ↔ L798 | cadreur | 7_lots (nothing unless the wording moves) | cadreur.md F09 |
| 67 | — | Give the bug-fix material at L333 a heading and point L331 at it | cadreur.md L331 ↔ L333 | cadreur | — | cadreur.md F10 |
| 68 | — | The never-do entry bounds code searches only; the technical document is grepped by its own path at move 1 | cadreur.md L264 ↔ L397 | cadreur | — | cadreur.md F11 |
| 69 | — | The ceiling counts lots per block — one unit everywhere; L453-454 and L465-467 rewritten to lots, L485 and L494-495 stand; cadreur.md L106-107 and L113 say lots | cadreur.md L106, L113 ↔ verificateur.md L453-454, L465-467, L485, L494; passes/verificateur.md L477-478 | verificateur | cadreur (L106-107, L113) | cadreur.md F12 · verificateur.md F01 · F06 · F17 |
| 70 | — | Point the sentence at the feature-cycle rule in *What makes a lot* | cadreur.md L355 ↔ L333 | cadreur | — | cadreur.md F13 |
| 71 | — | The routing rule globs `architecte/` as well as `code/` | cadreur.md L44 ↔ L295 | cadreur | — | cadreur.md F14 |
| 72 | — | Name the section L145 points at | cadreur.md L145 ↔ L822 | cadreur | — | cadreur.md F15 |
| 73 | — | One outcome for a defect judged wrong — the blocking file; the second passage says the same or goes | cadreur.md L828 ↔ L852 | cadreur | — | cadreur.md F16 |
| 74 | — | The return row keys on the presence of `code/blocked_verificateur.md` alone; the file's shape (no `## Decision`) stands | cadreur.md L818 ↔ verificateur.md L206-208; 7_lots.md L79 | cadreur | — | cadreur.md F17 · verificateur.md F15 · fichiers.md F08 · passages-aval.md F03 (cadreur, verificateur plans) |
| 75 | — | The Cadreur's report states the outcome on the blocking file (decision applied, verdict applied, verdict refused, block standing); `/7_lots` stops and relays on a refused verdict instead of re-invoking | cadreur.md L961, L970 ↔ 7_lots.md L144, L146 | 7_lots (the rows) | cadreur (the report line) | cadreur.md F20 · F22 |
| 76 | — | `/7_lots` renames `code/blocked_cadreur.md` on a block lifted by a verdict exactly as on an applied decision, keyed on the report line of #75 | cadreur.md L960 ↔ 7_lots.md L146 | 7_lots | cadreur | cadreur.md F21 |
| 77 | settled | Delete `.claude-new/commands/cycle.md`; remove every mention of `/cycle` and `cycle.md` (decisions.md) | cycle.md L1, L9-10, L82, L88, L93 ↔ CLAUDE.md L49-57 | commandes | — | renommages.md F14 · cadreur.md F23 · fichiers.md F09 · verificateur.md F22 · convertisseur.md F21 |
| 78 | — | Add the "no lot of any layer can carry it" case to the blocking list, pointing at move 7's second table | cadreur.md L628 ↔ L135 | cadreur | — | cadreur.md D-13 |
| 79 | — | `/7_lots` keys the rename of `code/redecoupage.md` on the `## Redécoupage: archivable` line in `code/sequence.md`, read from disk; the Cadreur's relay stays a courtesy | 7_lots.md L100-103 ↔ verificateur.md L472-475; cadreur.md L926-927 | 7_lots | cadreur (L926-927 no longer the trigger) | renommages.md F13 (cadreur, verificateur plans) |
| 80 | — | Move 1 and the blocking list stop on any `[B` reference left in the document, not only `[B?:` (*a-trancher convertisseur 2* confirms) | convertisseur.md L754-757, L766 ↔ cadreur.md L138, L392-397 | cadreur | convertisseur (L754-757: the leftover stops the split instead of "reads as settled") | passages-amont.md F05 · convertisseur.md F22 (cadreur, convertisseur plans) |
| 81 | — | Move 5 names each entry's `Consumes:` line as the source of the direction of `Needs` between lots, beside the inventory | convertisseur.md L275-278, L295 ↔ cadreur.md L753 | cadreur | convertisseur (L275-278, L34 name the reader the Cadreur declares) | passages-amont.md F06 (cadreur, convertisseur plans) |
| 82 | — | The reader table at L28-34 says what each reader does with `Consumes:` (the Architecte finds conjunction pairs, the Cadreur orders lots) | convertisseur.md L34 ↔ architecte.md L513-514 | convertisseur | — | convertisseur.md F20 |
| 83 | — | On a bug-fix cycle the lot list states each lot's layer (the bearer's, from the code); the Vérificateur reads it there at moves 4 and 5 | verificateur.md L432-434, L503-504 ↔ L89-94; cadreur.md L77-78 | cadreur | verificateur (L432-434, L503-504 name the source) | verificateur.md F09 — *added for cadreur* |
| 84 | — | The ceiling remark is carried: the Cadreur relays it as it relays the archivable line, `/7_lots` relays it with lots, blocks and defects | verificateur.md L462-463 ↔ cadreur.md L926-927; 7_lots.md L242-243 | verificateur | cadreur, 7_lots | verificateur.md F23 — *added for cadreur* |
| 85 | — | Delete the cascade-caller exemption from `overlap` | verificateur.md L300-302 ↔ cadreur.md L573 | verificateur | — | verificateur.md F14 |
| 86 | — | Move 2's second kind is read from the need the Cadreur declares on the lot removing the call; `merge` raised only when the anchors show it | verificateur.md L336, L354-361 ↔ cadreur.md L572 | verificateur | — | verificateur.md F24 |
| 87 | — | State the `surface` test: covered when a lot names the symbol in `Produces`/`Modifies` and cites an entry the inventory lists against the operation | verificateur.md L272-273 ↔ cadreur.md L753-754 | verificateur | — | verificateur.md F13 |
| 88 | — | Inventory added to the Role path table; coded-lot rules moved into the moves they govern (L69-73 goes, #95); move 3's "badly cut" check named as the `anchor` kind at L385-387 | passes/verificateur.md L115-117, L137-138, L170 ↔ verificateur.md L39-43, L66-87, L385-387 | verificateur | — | verificateur.md F02 · C6 |
| 89 | — | Fresh-context rule stated once in *Who invokes you*, one never-do line; L24-25 sentence and L287-288 clause dropped | passes/verificateur.md L558-561 ↔ verificateur.md L24-25, L230-231, L243-249, L287-288 | verificateur | — | verificateur.md F03 |
| 90 | — | Name the gesture and bound for each remaining partial read (preamble, `## Ce qui est déjà codé`, previous sequence's sections) | verificateur.md L4 ↔ L57, L66-67, L444-445 | verificateur | — | verificateur.md F04 |
| 91 | settled | Sections matched to a layer on what the section is about (decisions.md F19); the conventions read goes (L92-94, L497-498) and its path rule with it; L36's example aligned with L27-28 | verificateur.md L27-28, L36, L92-94, L497-498 ↔ L93, L428-429; architecte.md L110-112 | verificateur | — | verificateur.md F05 · F08 · F19 |
| 92 | — | The preamble is read on both documents; on `desc-bug.md` it carries `Dependencies` and no `Vocabulary`; L58 no longer promises one on both | verificateur.md L57-59, L58, L394-395 ↔ diagnostiqueur.md L508-512 | verificateur | — | verificateur.md F07 · F18 |
| 93 | — | The previous `code/sequence.md` is read for its `## Order` as well as its `## Blocks`; coded lots keep their relative order | verificateur.md L82 ↔ L444-445; arbitre.md L346-348 | verificateur | — | verificateur.md F10 |
| 94 | — | Drop the `## Status` read and the `surface` line (L69-73): the coded set is the Arbitre's list as written | verificateur.md L72 ↔ L141; arbitre.md L348; cadreur.md L877-878 | verificateur | — | verificateur.md F11 (passages-aval F15 then moot for the Vérificateur) |
| 95 | — | Announce `## Redécoupage: archivable` in *What you write* as the conditional fourth heading | verificateur.md L104-105 ↔ L469-470 | verificateur | — | verificateur.md F12 · renommages.md F12 |
| 96 | — | `/7_lots` counts the `block-N:` lines under `## Blocks` | verificateur.md L111-114 ↔ 7_lots.md L31-32 | 7_lots | — | verificateur.md F20 |
| 97 | — | The general relay rule of `/7_lots` excepts `blocked_verificateur.md`, as L251-253 excepts the Architecte case | verificateur.md L206 ↔ 7_lots.md L147, L247-249 | 7_lots | — | verificateur.md F21 |
| **Classeur · Qualifieur · Découpeur · the upstream blocking files** | | | | | | |
| 98 | — | Index (and pass sheet) gain the emptying case, once #101 is applied | modifications.md L57 ↔ classeur.md L267, L295-300 | index | — | classeur.md F01 |
| 99 | settled | Rewrite the `presentation · anything else` frontier so a block takes the nature of what the action produces, is `presentation` only when it describes the perceived part alone; bound doubt 1 | classeur.md L93, L103-106, L115 ↔ passes/classeur.md L74-79 | classeur | — | classeur.md F02 |
| 100 | — | Record that C5 was met by moving the numbering into `/3b_nature` and removing `Glob` | passes/classeur.md L139-141 ↔ 3b_nature.md L44-47; classeur.md L125 | index | — | classeur.md F03 |
| 101 | — | The targeted edit spans from the block's heading through its `Nature:` line, for filling, rewriting and emptying alike | classeur.md L179 ↔ L47-55, L59-60, L298 | classeur | — | classeur.md F04 |
| 102 | — | L34-37: the prompt's list is the behaviours plus the blocks that left `comportement` while still carrying a nature | classeur.md L34-37 ↔ L267, L295-300; 3b_nature.md L97 | classeur | — | classeur.md F05 |
| 103 | — | Add the third block cause — one block, two answers leaving the same doubt open — with its `## To resume` | classeur.md L169-172 ↔ L223-227 | classeur | — | classeur.md F06 |
| 104 | — | The follow-up question quotes the answer it follows; L171 bounded to what the one named file holds | classeur.md L146, L166-167 ↔ L171-172 | classeur | — | classeur.md F07 |
| 105 | — | The commands test every `## Decision` heading of a multi-entry blocking file — any empty, stop; all filled, name the file (`/3a_genre` with the `## Blocking N` shape of #128, `/3b_nature`, `/2_structure`) | classeur.md L233-235 ↔ 3b_nature.md L37-39; 2_structure.md L120-121; 3a_genre.md L34-40 | commandes (3a_genre · 3b_nature · 2_structure) | classeur (L253-254 stated for every entry), qualifieur (nothing beyond #128) | classeur.md F08 · F13 · renommages.md F11 |
| 106 | — | Fold the three report lines (blocked blocks, waits on the Rédacteur, value outside the eight) into *Then report* | classeur.md L237, L246-247 ↔ L319-331 | classeur | — | classeur.md F09 |
| 107 | — | The description names the qualifieur as the agent that runs before | classeur.md L3 ↔ L35 | classeur | — | classeur.md F10 |
| 108 | — | `/3b_nature` names the answered file always as the highest under `questions/classeur/`; root-first clause and post-run filing dropped; `questions/qualifieur/` and `questions/classeur/` exempted from "read by no command again"; the stop on a root file holding `### Q` kept | classeur.md L146 ↔ 3b_nature.md L49-53, L58-60, L67-69, L71-72; 2_structure.md L89-92, L200-201 | 3b_nature | classeur (L146 stands) | classeur.md F12 |
| 109 | — | Keep the emptying rule; drop the claim that `/5_reclasse` stops on a filled line under another genre, at L298-300 and 3b_nature.md L97; ground the rule on the genre views copying the block as it stands | classeur.md L298-300 ↔ 5_reclasse.md L64-70, L172-173; 3b_nature.md L97 | classeur | 3b_nature (L97) | classeur.md F14 |
| 110 | — | `/3b_nature`'s relay list gains the blocked blocks' names and the two decision-shape lines | classeur.md L237, L246-247 ↔ 3b_nature.md L223-227, L234-237 | 3b_nature | classeur (#106) | classeur.md F15 |
| 111 | — | Blocking-file lifecycle: `/3a_genre` and `/3b_nature` rename their file only when the agent reports the genre/nature written; a block waiting on the Rédacteur stays at the unnumbered name for `/2_structure`, which names it to the Rédacteur and renames whichever of the three files it applied — never the Découpeur's alone | 2_structure.md L120, L191-194 ↔ 3a_genre.md L164-167; 3b_nature.md L161-164; qualifieur.md L270; classeur.md L246; redacteur.md L531-539 | commandes (3a_genre · 3b_nature · 2_structure) | qualifieur (L270 report line in fixed terms), classeur (L246 stands), redacteur (nothing) | classeur.md F16 · renommages.md F10 (classeur, qualifieur plans) · qualifieur.md F11 · chemins-amont.md F03 (classeur, qualifieur, decoupeur, redacteur plans) · chemins-amont.md F04 · redacteur F17 |
| 112 | — | *a-trancher classeur renommages F10*: the `/3b_nature` relay row asks for the answers first, the decision second — amend 3b_nature.md L235 | 3b_nature.md L235 ↔ 2_structure.md L117-125 | 3b_nature | — | classeur To settle |
| 113 | — | Add the optional `Global:` line, after `Nature:`, to the block form the classeur is given | classeur.md L49-51 ↔ redacteur.md L59-62 | classeur | — | classeur.md F17 |
| 114 | — | The Rédacteur reads every `## Decision` of the file, one per `## Blocking N`, rewrites what each rewrite decision names, leaves a block whose decision names a nature or a genre | classeur.md L196-235 ↔ redacteur.md L527-529, L531-539 ↔ 2_structure.md L120-121 | redacteur | classeur (shape stands), qualifieur (#128 adopts the shape) | passages-amont.md F01 (classeur, redacteur plans) · redacteur F20 |
| 115 | — | A filled `blocked_decoupeur.md` is `/2_structure`'s alone: `/3_decoupe` stops on any such file at the unnumbered name (empty: fill it; filled: `/2_structure` first), drops the prompt's third line and the post-run rename; the agent's resume branch and the "plus a blocking file" reading exception go | decoupeur.md L153-156, L32-33 ↔ L139-143; 3_decoupe.md L39, L136, L151-157, L215; 2_structure.md L120, L191-194; redacteur.md L533 | 3_decoupe | decoupeur (L153-156, L32-33; keeps L114) | decoupeur.md F10 · F15 · chemins-amont.md F05 |
| 116 | — | *a-trancher decoupeur F01*: record the removal of the `Clarification needed` stop; do not restore it; note the index line (modifications.md L318) in `todo.md` | modifications.md L318 ↔ decoupeur.md; 3_decoupe.md L44-47 | index (todo.md note) | — | decoupeur.md F01 |
| 117 | — | Nothing to apply in `.claude-new/`; the index lines on C9, C1 and C14 are stale — relay to the Product Owner | modifications.md L319, L321; passes/decoupeur.md L335-360 ↔ decoupeur.md L124-126; 3_decoupe.md L69-70, L99-125, L202-205 | index (relay) | — | decoupeur.md F02 · F03 · F04 |
| 118 | — | Two events with one identical consequence are one trigger with two values; the criterion is the consequence; drop the paragraph counting them as two; qualify the two-pieces-of-data rule with "when what follows each differs" | decoupeur.md L145-151 ↔ L51, L53-59, L220-221 | decoupeur | — | decoupeur.md F08 |
| 119 | — | The sequel judgement is made on the named block alone; no other block is opened | decoupeur.md L92-96 ↔ L40-45, L248-249 | decoupeur | — | decoupeur.md F09 |
| 120 | — | One phrasing for the first turn — the prompt says "every block", as the template does; the agent's three lines key on it | decoupeur.md L37-38, L45, L162-164 ↔ 3_decoupe.md L69-70, L135 | 3_decoupe | decoupeur | decoupeur.md F11 |
| 121 | — | Name `Global:` in the enumeration of what each half carries, conditional on the original carrying one; the example says so | decoupeur.md L197-199 ↔ L204, L230-233 | decoupeur | — | decoupeur.md F12 |
| 122 | — | `/3_decoupe` gains a relay row for the sequel-block identifiers, no change to the next step. *a-trancher decoupeur F17*: nobody merges; the Product Owner merges by hand when it bothers her | decoupeur.md L248-249 ↔ 3_decoupe.md L193-218 | 3_decoupe | — | decoupeur.md F13 · decoupeur To settle F17 (the route) |
| 123 | — | On a blocking file, no re-invocation: the short list is expected, the file relayed, the command stops | 3_decoupe.md L202-203 ↔ L220; decoupeur.md L125-126 | 3_decoupe | — | decoupeur.md F14 |
| 124 | — | The kept half keeps the original's marker — `NEW` stays `NEW` | decoupeur.md L217 ↔ redacteur.md L104-105 | decoupeur | — | decoupeur.md F16 |
| 125 | — | Stop saying the blocking file drives the rerun; the markers do | decoupeur.md L126 ↔ 3_decoupe.md L72-75, L77-91 | decoupeur | — | decoupeur.md F18 |
| 126 | — | The `Genre:` edit is anchored on the heading line and the `Genre:` line below it | qualifieur.md L4 ↔ L211-213 | qualifieur | — | qualifieur.md F03 |
| 127 | — | Name the mechanism that loads one block (heading line numbers by grep, a bounded read) | qualifieur.md L4 ↔ L41-47 | qualifieur | — | qualifieur.md F04 |
| 128 | — | Adopt the classeur's blocking-file shape — `## Blocking N` per blocked block, four headings under each, one `## Decision` each | qualifieur.md L258-259 ↔ L231-247, L267-271; classeur.md L196-197, L233-234 | qualifieur | 3a_genre (#105), redacteur (#114) | qualifieur.md F08 |
| 129 | — | Replace "undo at no cost" with what downstream does (the classeur blocks, the sondeurs find nothing); 3a_genre.md L192-194 says the same | qualifieur.md L22-24 ↔ L150-151; classeur.md L223-225; 3a_genre.md L192-194 | qualifieur | 3a_genre (L192-194) | qualifieur.md F05 |
| 130 | — | On a `MODIFIED` block carrying a genre, run the same procedure as on an empty one and compare | qualifieur.md L329 ↔ L297-303 | qualifieur | — | qualifieur.md F07 |
| 131 | — | Name `transverse` and `recette` as the two of five that read as having a trigger and an output | qualifieur.md L131-133 ↔ L113, L119 | qualifieur | — | qualifieur.md F09 |
| 132 | — | Say the orchestrator's grep is the one on empty lines and markers; finding a block by heading is the agent's own grep | qualifieur.md L288-289 ↔ L51 | qualifieur | — | qualifieur.md F10 |
| 133 | — | *a-trancher qualifieur 1*: ask on the `transverse` doubt only, the four other doubts stay silent (L140-141 narrowed); correct the price statement at L143-145 | qualifieur.md L140-145 ↔ 4_grille.md L138-146 | qualifieur | — | qualifieur.md F12 · qualifieur To settle 1 (F01 index: then matches) |
| 134 | — | `/3a_genre` relays the agent's per-block genre list beside the counts | qualifieur.md L351-354 ↔ 3a_genre.md L216-222 | 3a_genre | — | qualifieur.md F13 |
| 135 | — | *a-trancher qualifieur 2*: a two-genre block blocks (`blocked_qualifieur.md`); the majority-genre rule L88-91 is removed and F06 with it; the route is `/2_structure` → Rédacteur rewrites with `MODIFIED` → `/3_decoupe` | qualifieur.md L88-91, L356-358 ↔ 3a_genre.md L227-235; 3_decoupe.md L81-82; decoupeur.md L65-67; 2_structure.md L120 | qualifieur | 3a_genre (relay row L231 covers it), index (F02: the rule is gone) | qualifieur.md F14 · F06 (void) · F02 · qualifieur To settle 2 |
| 136 | — | `/3a_genre` looks for the answered file under `questions/qualifieur/` only; the stop on a root file holding `### Q` stays | qualifieur.md L188-189 ↔ 3a_genre.md L50-54, L68-70 | 3a_genre | — | qualifieur.md F15 · chemins-amont.md F06 |
| 137 | — | Give the distance to `/5_reclasse` correctly, or name it without counting | qualifieur.md L273-274 ↔ CLAUDE.md L52 | qualifieur | — | qualifieur.md F16 |
| 138 | — | The lexicographe owns the vocabulary in the Rédacteur's never-do list | redacteur.md L318-323 ↔ lexicographe.md L3, L176-181 | redacteur | — | lexicographe.md F13 · passages-amont.md F03 (lexicographe, qualifieur, redacteur plans) |
| **Commands, upstream** | | | | | | |
| 139 | — | Relay to the Product Owner that PROCESS_AMONT.md L1210 and PROCESS_AVAL.md L1010 describe `/cycle`, which #77 removes | PROCESS_AMONT.md L1210 ↔ PROCESS_AVAL.md L1010 | Product Owner | — | renommages.md F15 |
| 140 | NOTE | Cap the *run again* on an empty line at one more run; stop naming the blocks at the second | 3a_genre.md L233 ↔ 3b_nature.md L238 | commandes (3a_genre · 3b_nature) | — | chemins-amont.md F07 |
| 141 | — | Anchor `/4_grille`'s closure tests on the highest-numbered `questions-sondeur-NN.md` (and `questions-existant-NN.md`) wherever it sits, root or filed; L173 then tells a closed grid (second time already run) from a run that wrote nothing, naming the next step in each | 4_grille.md L162-175 ↔ L181, L253-254, L289-291; 5_reclasse.md L203; 3_decoupe.md L49 | 4_grille | — | chemins-amont.md F11 (commandes plan) · F09 · F10 (sondeur plan) |
| 142 | BLOCKING | File an answered `technique-<nature>.md` into `closed/` only after the nature has run on it, in *Once it has run*; the invocation-1 prompt names a path that exists; the answered file is archived so the *Runs* row does not fire twice | 6_convertit.md L78-83 ↔ L131, L171; convertisseur.md L385-386 | 6_convertit | convertisseur (L59, L385-386 accept the path named) | chemins-amont.md F13 · convertisseur.md F15 · fichiers.md F01 |
| 143 | — | Route the *blocking file and questions together* row by kind: product questions take the long loop of L362, decision filled before it; `/6_convertit` directly only when every question is technical | 6_convertit.md L360 ↔ L362, L62 | 6_convertit | — | chemins-amont.md F15 |
| 144 | — | *a-trancher commandes F16*: `/6_convertit` gains a dispatch row — a nature carrying `<<ASSUMED` whose product question is answered **runs**, its part unchanged (the rerun lifts the mark); the turn's relay row says so | 6_convertit.md L130-132 ↔ L363; convertisseur.md L464-470 | 6_convertit | convertisseur (nothing — L468-470 already says the rerun lifts it) | chemins-amont.md F16 · commandes To settle |
| 145 | — | Cap the re-run of a nature that did not apply its technical answer at once; a second miss is a fault of the run | 6_convertit.md L271-273 ↔ L279-280 | 6_convertit | — | chemins-amont.md F17 |
| 146 | — | Give the walk an outcome for a `bugfix-NN` argument holding no request with an empty `## Verdict`: nothing to invoke, `/8_code` carries on | conventions.md L76 ↔ L26-27 | conventions | — | chemins-amont.md F18 |
| 147 | — | Grant the reading list the two headings the walk keys on — `## Decision` filled, `## Invocation` — of `blocked_architecte.md` | conventions.md L70 ↔ L33-38; architecte.md L247 | conventions | — | chemins-amont.md F20 |
| 148 | BLOCKING | An answered or empty `questions-fusionneur-NN.md` with no `plan-fusion.md` routes to invocation 1 (row 9); row 10 is the sole route to invocation 2; rewrite L67-69 | fusion.md L47-51, L58-61, L67-69 ↔ fusionneur.md L117, L262-263 | fusion | fusionneur (nothing) | chemins-amont.md F22 (commandes plan) · fusionneur.md F20 |
| 149 | — | `/fusion_compare` gains a *what to run next* table | fusion_compare.md L131-132 ↔ 1_lexique.md L93-95 | fusion_compare | — | chemins-amont.md F26 |
| 150 | — | Put the `### Q` guard of `/3a_genre` in front of the filing step of `/3_decoupe`, `/4_grille`, `/6_convertit`, `/conventions`, `/fusion_compare` | 3_decoupe.md L49 · 4_grille.md L181 · 6_convertit.md L62 · conventions.md L110 · fusion_compare.md L36 ↔ 3a_genre.md L68-70 | commandes (the five) | — | chemins-amont.md F27 · fichiers.md F12 (sondeur plan) |
| 151 | — | `/2_structure` files the lexicographe's questions file only when it holds no `### Q`; a file holding entries stops the command with `/1_lexique` next | 2_structure.md L79-87 ↔ 1_lexique.md L58, L189-194 | 2_structure | — | chemins-amont.md F02 · fichiers.md F17 (lexicographe plan) |
| 152 | — | `/2_structure` refuses invocation 1 until the latest `questions-lexicographe-NN.md`, root or filed, holds no `### Q` | 1_lexique.md L243 ↔ 2_structure.md L119 | 2_structure | — | chemins-amont.md F28 |
| 153 | — | Anchor `/2_structure`'s `NEW` grep on the title line | 2_structure.md L164-165 ↔ 3_decoupe.md L81, L84 | 2_structure | — | chemins-amont.md F29 |
| 154 | — | Add to `/1_lexique`'s table the row "another agent's file and a `questions-lexicographe` with no `### Q`" → invoke nothing, say `/2_structure` | 1_lexique.md L61 ↔ lexicographe.md L105, L515-517 | 1_lexique | — | lexicographe.md F11 · chemins-amont.md F01 |
| 155 | — | Before filing the named blocking file, `/1_lexique` tells a block written anew from the one it named — a `## Decision` empty again is relayed, nothing filed (⚠️ the report says the same pattern holds in every command: wave 3 checks its siblings) | 1_lexique.md L178-186 ↔ lexicographe.md L72-73, L80, L85 | 1_lexique | — | chemins-amont.md F30 |
| 156 | — | `/4_grille`'s blocking-file table holds any number of unnumbered files: every empty one stops and is named, every filled one is named in its own reading's prompt | 4_grille.md L42 ↔ L54-58 | 4_grille | — | chemins-amont.md F08 (sondeur plan) |
| 157 | — | Anchor `/5_reclasse` on the highest-numbered `questions-sondeur-NN.md` and `questions-existant-NN.md`, each present and holding no `### Q`, root or filed; drop the attach condition | 5_reclasse.md L50-54 ↔ 4_grille.md L261-263, L444-447 | 5_reclasse | — | chemins-amont.md F12 (sondeur plan) |
| 158 | BLOCKING | `/4_grille` exempts an entry carrying a `Défaut:` line from the `^Answer:$` stop | sondeur.md L402-403 ↔ 4_grille.md L97-100 | 4_grille | — | sondeur.md F08 |
| 159 | — | Fix the `Global:` lookup in `/4_grille` to reach the heading three lines above | redacteur.md L59-62 ↔ 4_grille.md L257-258 | 4_grille | — | redacteur F13 |
| 160 | — | Align the justification at 6_convertit.md L141-142 with the prefix rule | redacteur.md L119-126 ↔ 6_convertit.md L141-143 | 6_convertit | — | redacteur F21 |
| 161 | — | Give the `Read:` line of the `/2_structure` template a third value, the blocking file row L120 names | redacteur.md L527-529 ↔ 2_structure.md L149, L120 | 2_structure | — | redacteur F18 |
| **Commands, downstream** | | | | | | |
| 162 | BLOCKING | Close the loop's own worktree before running `/7_lots` — commit, merge, push, remove — then open a fresh one from the merged `HEAD` and carry on (the realisateur side of L352-355 is conflict C12) | 8_code.md L365-366, L86 ↔ 7_lots.md L64, L224 | 8_code | 7_lots (nothing) | chemins-aval.md F01 |
| 163 | — | `/9_controle` reads `par-genre/recette.md` at the feature folder's root, one level up from a `bugfix-NN/` | 9_controle.md L239-240, L18 ↔ 5_reclasse.md L96, L112 | 9_controle | — | chemins-aval.md F13 |
| 164 | — | `/9_controle` derives the working folder from the feature name as `/7_lots`, `/8_code`, `/audit_conventions` do; the path argument goes | 9_controle.md L15-16 ↔ 8_code.md L25-26, L257-258 | 9_controle | 8_code (L257 relay names `/9_controle <feature>`) | chemins-aval.md F14 |
| 165 | — | `/deploie` declares the PowerShell tool its commands are written for | deploie.md L3 ↔ L35-44 | deploie | — | chemins-aval.md F15 |
| 166 | — | One `registre-questions.md` per feature, at the feature folder's root | 9_controle.md L284-287 ↔ L15-18 | 9_controle | — | chemins-aval.md F16 |
| 167 | — | The no-coverage skip names findings 1, 4 and 7; finding 6 keeps running | audit_conventions.md L48-50 ↔ L131-133, L138-139 | audit_conventions | — | chemins-aval.md F17 |
| 168 | — | `/8_code` skips the concepteur / the testeur only when `conception.md` / `tests.md` is there **and** no unnumbered `blocked_concepteur.md` / `blocked_testeur.md` sits beside it; a standing block goes through 4b (empty: stop; filled: the agent runs and resumes from its report) | 8_code.md L112-113, L164-170, L436-439 ↔ concepteur.md L162-165; testeur.md L132-134 | 8_code | concepteur (L162-165 reachable once #185 applied), testeur (L132-134 say a filled decision brings it back) | concepteur.md F11 · testeur.md F10 · chemins-aval.md F06 · passages-aval.md F06 (concepteur, testeur plans) |
| 169 | — | When the split comes back, delete `conception.md` and `tests.md` with `fiche-executable.md` for every lot with no PASS | 8_code.md L379-382 ↔ L112-113 | 8_code | concepteur, testeur (resume rules read a file now gone — intended) | chemins-aval.md F09 (concepteur, realisateur, testeur plans) |
| 170 | — | *a-trancher (concepteur chemins-aval F09 · detailleur F21 · realisateur chemins-aval F08)*: the orchestration reverts the dropped / re-cut / false-sheet lot's commits before `/7_lots` (or before re-detailing); a git conflict stops the command, which says so and resolves nothing | realisateur.md L335-338 ↔ testeur.md L228-232; 8_code.md L357-366; concepteur.md L237 | 8_code | realisateur (nothing — its restore covers its edits), concepteur (nothing), testeur (nothing) | chemins-aval.md F08 (realisateur, testeur plans) · concepteur To settle 2 · detailleur To settle |
| 171 | — | *a-trancher relecteur F19 · detailleur F21*: on `Cause: sheet`, `/8_code` reverts the lot's commits, deletes `fiche-executable.md`, `conception.md`, `tests.md`, runs the Détailleur on the block in its ordinary mode (the missing sheet is written again), and passes the verdict's `## Findings` in the prompt — a parameter, not a mode; counted as an attempt | relecteur.md L167-169, L405-407 ↔ 8_code.md L138-144; detailleur.md L467-468, L672-673; realisateur.md L519-522 | 8_code | detailleur (accepts the `## Findings` parameter; no `Mode: sheet`), relecteur (L167-169, L407 say what 8_code does), realisateur (L519-522 gains the row: a `Cause: sheet` FAIL never reaches it — stop) | detailleur.md F21 · passages-aval.md F02 · chemins-aval.md F03 · relecteur.md F19 (detailleur, realisateur, relecteur plans) |
| 172 | — | `/8_code` retires `blocked_relecteur.md` itself when it acts on the report row or the sheet row — the act is the answer, no decision is filled | 8_code.md L418-422, L169-170 ↔ relecteur.md L229-234 | 8_code | relecteur (L232-234 say when the orchestration retires it) | chemins-aval.md F10 (detailleur, realisateur, relecteur plans) |
| 173 | — | Drop the Contrôleur from 8_code.md L415 — it writes no blocking file | 8_code.md L415 ↔ controleur.md L73-78 | 8_code | — | fichiers.md F10 (controleur, relecteur plans) |
| 174 | — | The retry prompt names the verdict (`Verdict: code/<lot>/verdict.md`); Part 2 keys its FAIL case on that line | realisateur.md L50, L513-517, L495 ↔ 8_code.md L138, L295-300 | 8_code | realisateur (Part 2 case; L50) | realisateur F21 |
| 175 | — | Move 4b renames `code/<lot>/reprise_realisateur.md` to `-NN` once the run it was named to has reported; the Réalisateur says it consumed it | realisateur.md L364 ↔ 8_code.md L170-171, L134-136 | 8_code | realisateur (report line) | realisateur F23 |
| 176 | — | 8_code.md L96-97 names the three agents that commit per lot | 8_code.md L96-97 ↔ concepteur.md L237; testeur.md L255 | 8_code | — | concepteur plan, part 2 cross-file row |
| 177 | — | *a-trancher concepteur "first commit"*: commit messages read `<lot>: <what the commit carries>` in the three committing agents; `/8_code` finds the lot's first commit by `git log` on it | 8_code.md L124-125, L153-157 ↔ relecteur.md L390; concepteur.md L94 | 8_code | concepteur, testeur, realisateur (one line each) | concepteur To settle 3 — *added for concepteur, testeur, realisateur* |
| 178 | — | `/8_code` gives a root `blocked_architecte.md` the treatment of #48 (same entry) | — | — | — | see #48 |
| **Concepteur · Testeur** | | | | | | |
| 179 | — | Index `Son rapport` row, "nomme les symboles" reading, and the blocking protocol recorded — after #185, #186 and #168 | modifications.md L855, L863, L844-887 ↔ concepteur.md L245-261, L109-111, L200-201, L120-165 | index | — | concepteur.md F01 · F02 · F03 |
| 180 | — | `git status` gets its gesture at move 5 — the check of what the worktree holds before staging | concepteur.md L94 ↔ L237-239 | concepteur | — | concepteur.md F04 |
| 181 | — | One meaning: the deliverable is a body that throws *not implemented*; a body with nothing in it is the forbidden thing; stop calling the deliverable "empty" | concepteur.md L3, L15, L198 ↔ L204-207; 8_code.md L112; testeur.md L19-24 | concepteur | 8_code (L112), testeur (L19-20, L23-24) | concepteur.md F08 — *added for testeur* |
| 182 | — | The lot's first commit is the blocked run's when there was one; the resumed run's commit is not the first | concepteur.md L125-126 ↔ L237-239 | concepteur | — | concepteur.md F09 |
| 183 | — | State the no-return rule without a language's type | concepteur.md L207 ↔ CLAUDE.md L78-79 | concepteur | — | concepteur.md F12 |
| 184 | — | `conception.md` gains a field naming the decision applied (or a dash): where "say in your report" lands, what the rename keys on, and what legitimises a divergence beside the Réalisateur's field; the Relecteur reads both fields for `## Symbol divergences` | concepteur.md L158 ↔ L245-270; relecteur.md L180-190; realisateur.md L176-183 | concepteur | relecteur (L54-57, L184-190 key on two fields), 8_code (4b rename keys on it) | concepteur.md F07 · renommages.md F08 (concepteur, realisateur, relecteur plans) |
| 185 | — | On a block, the Concepteur writes `conception.md` before the blocking file (`## Declared` = what landed, `## Compile` = command and outcome), commits it with the declarations; the resumed run rewrites it whole once green | concepteur.md L120-128 ↔ L162-165, L251-253 | concepteur | 8_code (#168) | concepteur.md F06 · passages-aval.md F06 (the report half) |
| 186 | — | The blocking procedure writes `tests.md` (`## Tests` covered, `## Red` run) before the commit | testeur.md L119-123 ↔ L132-134 | testeur | — | testeur.md F08 |
| 187 | — | Index rows on an older failing test and a passing new test brought in line with the file | modifications.md L897-898 ↔ testeur.md L216-228 | index | — | testeur.md F01 · F02 |
| 188 | — | Name the one fallback move 4 runs when the conventions name no test command; admit it in the `Bash` bound; the concepteur and the realisateur take the same one | testeur.md L205-207 ↔ L92-96; concepteur.md L212-221; realisateur.md L423-427, L586 | testeur | concepteur (L212-221), realisateur (L423-427, L586) | testeur.md F03 — *added for concepteur, realisateur* |
| 189 | — | Move 2 gets a third branch — a criterion nobody can observe is a block; *no* sends to the manual list only what the Product Owner can see | testeur.md L182-189 ↔ L136-147 | testeur | — | testeur.md F04 |
| 190 | — | Count every block the file names (the untestable signature of L105, the removed behaviour of conflict C14) and give `## Where` a wording for each | testeur.md L136-143 ↔ L104-105, L159-162 | testeur | — | testeur.md F05 |
| 191 | — | `## Red` names the tests that failed and the ones left green because the declaration alone meets the criterion; the declaration-only exception is stated where the absolute is; the command run when the conventions name none goes under `## Red` too; every reader of `## Red` states the exception | testeur.md L23-26, L205-207, L216-221, L270-284 ↔ realisateur.md L20-22, L77-78; relecteur.md L333-334; 8_code.md L113 | testeur | realisateur (L20-22, L77-78), relecteur (L333-334, point 2 matching), 8_code (L113) | testeur.md F06 · F07 · F11 · passages-aval.md F12 (green-by-declaration half; the criterion-gone half is conflict C14) |
| 192 | — | The L86 exception extends to move 4 — an older test the sheet made false is read to be adapted | testeur.md L84-86 ↔ L227, L230-233 | testeur | — | testeur.md F09 |
| 193 | — | Replace the commit reason: uncommitted, the tests are never merged and the worktree is removed; drop the `git restore` cause | testeur.md L258-260 ↔ realisateur.md L335-338 | testeur | — | testeur.md F13 |
| **Contrôleur · 9_controle** | | | | | | |
| 194 | — | Realign the index's controleur section with the pass sheet's numbering; C12 moved to applied; the L36-43 grep block recorded as round-1 correction C | modifications.md L1241-1275 ↔ passes/controleur.md L471-540; 9_controle.md L53-55; controleur.md L36-43 | index | — | controleur.md F01 · F03 · F04 |
| 195 | — | *a-trancher controleur F02*: finish pass 14 — remove the two "never this file" lines and their justifications at L66-71 | passes/controleur.md L502-538 ↔ controleur.md L66-71 | controleur | — | controleur.md F02 · controleur To settle 2 |
| 196 | — | State how far the read after the grep goes (heading to the line before the next block heading) and the bounded call | controleur.md L38 ↔ L42-43 | controleur | — | controleur.md F05 |
| 197 | — | A present partial is a group that ran; a block absent from every field goes under `## Doubts` naming the group and what the partial lacks; L238's reason rewritten | controleur.md L237-238 ↔ L282, L289-292 | controleur | — | controleur.md F06 |
| 198 | NOTE | A sheet named and not there is not a sheet observing nothing: its intentions are `Doubtful`; L193 governs only what a read sheet fails to observe | controleur.md L85 ↔ L193 | controleur | — | controleur.md F07 |
| 199 | — | Route every line to `## Doubts` by its heading wherever the text sends a line somewhere; `Doubtful` kept as the outcome's name only | controleur.md L85, L281-282 ↔ L227, L255 | controleur | — | controleur.md F08 |
| 200 | — | Rename the register rule at L304 (language, not "prose") | controleur.md L233 ↔ L304 | controleur | — | controleur.md F09 |
| 201 | — | Name the unchanged block as the one case where a block gets a single line | controleur.md L104 ↔ L217, L195-197 | controleur | — | controleur.md F10 |
| 202 | settled | Assembly move 3 reads the opening `Blocks:` line: the prompt's list is authoritative, a difference is a line of the report naming the group | controleur.md L205-209 ↔ L246-248, L281-282 | controleur | — | controleur.md F11 |
| 203 | — | *a-trancher controleur F12* (with decisions.md): phase 1 marks `carried` the blocks a correction cycle built; the `B<n>` travels — the Product Owner writes it in `bug-list.md` when the gap comes from a control report, the Diagnostiqueur carries it into `desc-bug.md`, the Cadreur into the lot list; the mark gets a path from the map to the report (`tracabilite-full.md` format, grouping, an invocation-1 found line) | 9_controle.md L68-70, L130-131, L138-146 ↔ 8_code.md L25; diagnostiqueur.md L51, L254; grouper.py L36-55 | 9_controle | controleur (a `carried` block gets a found line), grouper.py, diagnostiqueur (`desc-bug.md` carries the `B<n>`), cadreur (the lot list carries it), Product Owner (`bug-list.md`) | controleur.md F12 · controleur To settle 1 — *added for diagnostiqueur, cadreur* |
| 204 | — | Extend L59-60 to both markers, `NEW` and `MODIFIED`, ignored alike | controleur.md L59-60 ↔ redacteur.md L99-105 | controleur | — | controleur.md F13 |
| 205 | — | Cite a criterion by its text, never by a counted position | controleur.md L215-216 ↔ detailleur.md L232-237 | controleur | — | controleur.md F14 |
| 206 | — | State the no-product-file stop once; L160 names the cut as L143-145 defines it | controleur.md L84, L160 ↔ L125-127, L143-145 | controleur | — | controleur plan part 2 D.12 · D.1 |
| 207 | — | `/9_controle` fixes the decisions line's shape (identifier first, greppable) and says a decision is translated at invocation 3 as an answer is at 2 | 9_controle.md L305-306 ↔ redacteur.md L674-705, L544 | 9_controle | redacteur (reads the identifier; translates) | passages-amont.md F08 (redacteur plan) |
| **Convertisseur · 6_convertit · 5_reclasse** | | | | | | |
| 208 | — | The resolving script (or its check) reports a `[B<n>:` whose `]` is not on the same line as a fault | 6_convertit.md L236-246 ↔ passes/convertisseur.md L125-150 | 6_convertit | — | convertisseur.md F01 |
| 209 | — | *a-trancher convertisseur 1*: invocation 2 alone reads `par-genre/transverses.md`; correct 5_reclasse.md L102 and modifications.md L547 to say so; rewrite the reason at L149-153 (cost and a single writer, never impossibility — L178-179 already derives a layer); F10, F11, D-16 stand | modifications.md L547; 5_reclasse.md L102 ↔ convertisseur.md L52, L146-153, L178-179 | convertisseur | 5_reclasse (L102), index (L547) | convertisseur.md F02 · F19 · passages-amont.md F07 · convertisseur To settle 1 |
| 210 | — | Replace the empty *settle* item with a choice a nature invocation faces (how a rule is cut into entries, where in its section); rest the *misplaced* contrast on it | convertisseur.md L363 ↔ L74, L494-496, L657; modifications.md L590 | convertisseur | — | convertisseur.md F03 · F12 |
| 211 | — | Remove "the product file, its text outside the blocks" from invocation 2's Reads | convertisseur.md L632 ↔ L717 | convertisseur | — | convertisseur.md F04 |
| 212 | — | Name invocation 2 in the `references.md` row and give it a move that opens the file and writes §9 Text before move 3 | convertisseur.md L52 ↔ L632, L88, L710-808 | convertisseur | — | convertisseur.md F05 |
| 213 | — | Narrow the headline at L3 and L18 to product matters | convertisseur.md L3, L18 ↔ L355-363, L602 | convertisseur | — | convertisseur.md F06 |
| 214 | — | State both exceptions to *never a number outside your own section* (move 2b transverse entry, move 4 *Resources* entry) | convertisseur.md L179-180 ↔ L774-778, L596-597 | convertisseur | — | convertisseur.md F07 |
| 215 | — | Count both question shapes the same way; align L474-475 | convertisseur.md L371-376 ↔ L410-416, L474-475 | convertisseur | — | convertisseur.md F08 |
| 216 | — | `Entries:` obeys the reference rule of L285-291; fix the example | convertisseur.md L374 ↔ L224-225, L285-291, L596 | convertisseur | — | convertisseur.md F09 |
| 217 | — | Move 2b records, for every transverse block, its entry or preamble part; move 3 resolves a reference to a transverse block from that record; transverse blocks excluded from the *fault of invocation 1* rule | convertisseur.md L746-748, L763-765 ↔ L146-147, L681, L722-734 | convertisseur | — | convertisseur.md F10 |
| 218 | — | Give the transverse block an ordinary `tracabilite.md` line at move 5; drop the "`## Trace` line in `tracabilite.md`" wording | convertisseur.md L183-185, L729-731 ↔ L795-797, L802-803 | convertisseur | — | convertisseur.md F11 |
| 219 | — | Add the technical questions file to invocation 2's Writes | convertisseur.md L340 ↔ L632 | convertisseur | — | convertisseur.md F13 |
| 220 | — | Add "the blocking file the prompt names" to both Reads columns | convertisseur.md L584-587 ↔ L631-632, L637 | convertisseur | — | convertisseur.md F14 |
| 221 | — | The transversal technical file takes a nature's route: answered, it forces the assembly and invocation 2, is named in the invocation-2 prompt, filed once consumed; the *No nature runs* row counts it | convertisseur.md L340, L385-386 ↔ 6_convertit.md L131-132, L154, L261-263 | 6_convertit | convertisseur (nothing) | convertisseur.md F16 · fichiers.md F02 · chemins-amont.md F14 |
| 222 | — | The command tells invocation 2's *No* from a fault (missing `tracabilite.md` beside a `questions-transversal.md` holding a question is the *No*); the *document stands* row never fires on a document left without preamble or traceability | convertisseur.md L453-457 ↔ 6_convertit.md L267-269, L154 | 6_convertit | convertisseur (L453-457 matches the test) | convertisseur.md F17 |
| 223 | — | Name the answered technical file as what makes the command run the nature again, the `<<ASSUMED` mark as what that rerun lifts | convertisseur.md L395-397 ↔ 6_convertit.md L130-132 | convertisseur | — | convertisseur.md F18 |
| 224 | — | State the *if nobody writes it* test once; exempt the technical file the prompt names from the never-do; say three cases at L473-474 and L527-528; remove the cross-cutting item from the notes' `## Preamble` | convertisseur.md L158, L608-609, L473-474, L527-528, L681, L693-694 ↔ L187-189, L385-386, L445-451, L146-153, L719 | convertisseur | — | convertisseur.md B-5 · c.20/D-3 · D-14 · D-16 |
| **Détailleur** | | | | | | |
| 225 | — | Index records `## Files` (as #C1 settles it), move 9's `spécifique` rule, the empty-body row, the `desc-bug.md` rule, C19-C21 applied through `8_code.md`, C1 met by the orchestration rename, the C4 count after #229, the `Not settled here.` row after conflict C2 | modifications.md L1013-1082, L1027-1031, L1038 ↔ detailleur.md L244-248, L259-265, L638-646, L109, L558-560, L443-444, L460, L438; 8_code.md L103-106, L395-397, L12-14, L170-173 | index | — | detailleur.md F01 · F02 · F03 · F04 · F05 · F06 · F07 · F10 |
| 226 | — | Drop the forward reference at move 2; move 4 carries the two-greps rule | passes/detailleur.md L214-234 ↔ detailleur.md L546-547, L580-581 | detailleur | — | detailleur.md F08 |
| 227 | — | Apply C17 to the `## Files` example — no platform extension (content rewritten under C1) | passes/detailleur.md L416-436 ↔ detailleur.md L246-248 | detailleur | — | detailleur.md F09 |
| 228 | — | Make the count match the shape (six fields) | detailleur.md L221-222 ↔ L224-257 | detailleur | — | detailleur.md F13 |
| 229 | — | The enumeration at L288-290 and the count at L460 agree with move 4's stop table | detailleur.md L288-290, L460 ↔ L103, L571-574, L590, L592 | detailleur | — | detailleur.md F14 |
| 230 | — | In divergence mode, run moves 1 and 2 on the named lots before moves 3-9 | detailleur.md L525-526 ↔ L680-681, L552, L628 | detailleur | — | detailleur.md F15 |
| 231 | — | Qualify L378 with the one exception move 4 names | detailleur.md L378-379 ↔ L571-578 | detailleur | — | detailleur.md F17 |
| 232 | — | The description of the Arbitre call names the block | detailleur.md L330 ↔ L332, L473-475 | detailleur | — | detailleur.md F18 |
| 233 | — | In divergence mode apply only a decision bearing on a lot the prompt names; say in the report which were not applied, so 4b does not rename | detailleur.md L668-670 ↔ L439, L679 | detailleur | 8_code (the rename after a divergence call waits for that report) | detailleur.md F19 |
| 234 | — | Keep `Edit` and bound it to the sheets a divergence prompt names; everything else is a Write | detailleur.md L4 ↔ L415-421, L682-685 | detailleur | — | detailleur.md F11 |
| 235 | — | Name the gesture — a Grep of `## Status` on `code/<lot>/verdict.md` with its following line, never a Read — and list the verdict in *What you read* with that restriction (`## Findings` of a false sheet arrive in the prompt, #171) | detailleur.md L45, L467-468 ↔ L60-89 | detailleur | — | detailleur.md F12 · D-3 |
| 236 | — | A request written in the walk is filed under the first lot of the block in the sequence | detailleur.md L571-574, L366 ↔ audit_conventions.md L92 | detailleur | — | detailleur.md D-7 |
| 237 | — | The `## Signatures` line marks each symbol *created* or *modified* (from `Produces`/`Modifies`); the Réalisateur's state-document grep and `## Symbols` key on the mark; L194 says `## Files` where it says `Modifies` | realisateur.md L123-125, L194, L555-557 ↔ detailleur.md L224-232, L397-398; relecteur.md L317-318; testeur.md L227 | detailleur | realisateur (L123-125, L194, L555-557), testeur (L227), relecteur (compares the marks) | realisateur F18 · renommages.md F03 — *added for detailleur* |
| 238 | — | The Réalisateur states one `## Outside the lot` rule keyed on `## Files`; the Détailleur's quotation at L261-262 follows it | realisateur.md L189-191 ↔ detailleur.md L261-262 | realisateur | detailleur (L261-262) | renommages.md F04 (detailleur, realisateur plans) |
| 239 | — | `audit_blocages.md`'s example reads `code/blocked_detailleur-01.md` | audit_blocages.md L156 ↔ detailleur.md L284-285; 8_code.md L170 | audit_blocages | — | detailleur.md F24 |
| 240 | — | The Réalisateur gains the row the Détailleur has: decision sending the lot back and `code/redecoupage.md` gone → the split was redone, carry on, report the decision applied | realisateur.md L500-506 ↔ detailleur.md L440-441 | realisateur | — | chemins-aval.md F23 (detailleur, realisateur plans) |
| 241 | settled | Every reader matches the `PASS` prefix (decisions.md passages-aval F15): relecteur L195-196, L219; detailleur L45, L467; 8_code L62-63; 9_controle L60; verificateur moot after #94; the Arbitre in #7 | relecteur.md L110, L222 ↔ detailleur.md L45, L466-467; verificateur.md L69-70; 8_code.md L62-63; 9_controle.md L60 | relecteur | detailleur, 8_code, 9_controle, arbitre (#7), verificateur (only if L70 stays) | passages-aval.md F15 (detailleur, relecteur, verificateur plans) |
| 242 | — | Drop the claim that `## Dependencies` carries the intra-lot order; the order is the one the signatures give | realisateur.md L567-569 ↔ detailleur.md L630-636 | realisateur | — | realisateur F26 |
| **Diagnostiqueur · diagnostique** | | | | | | |
| 243 | TO FIX | Rewrite the index's `diagnostiqueur.md` row to what the file carries; add a `diagnostique.md` entry to the index's command section | modifications.md L1601, L1320-1522 ↔ diagnostiqueur.md L38-45, L76-79, L311-313, L503-505; diagnostique.md L44-70, L157-158, L164-171 | index | — | diagnostiqueur.md F01 · F02 |
| 244 | NOTE | Name `Glob` as the gesture for the two existence checks and confine it to those | diagnostiqueur.md L4 ↔ L154-158, L503 | diagnostiqueur | — | diagnostiqueur.md F03 |
| 245 | TO FIX | *a-trancher diagnostiqueur F10*: keep the state document as a search aid — a recorded trap or dead symbol is named in `## Today` (dead state feeds move 3); the verdict is unchanged; name the reach gesture (grep on the two headings, then a bounded read) | diagnostiqueur.md L138 ↔ L144, L205-377, L238-246 | diagnostiqueur | — | diagnostiqueur.md F10 · F04 |
| 246 | TO FIX | An existing `desc-bug.md` is a stop (not a block) tested at the head of invocation 2, naming the file and saying what it holds is settled; the enumeration stays at four; `/diagnostique` does not issue phase 2 when the file exists and relays it as done | diagnostiqueur.md L76-79, L503-505 ↔ L173-180, L430-495; diagnostique.md L107 | diagnostiqueur | diagnostique (phase-2 skip) | diagnostiqueur.md F05 · F07 · F16 |
| 247 | TO FIX | Drop "The bearer is where it lands"; `Bearer: none` for a move | diagnostiqueur.md L311-313 ↔ L316-317 | diagnostiqueur | — | diagnostiqueur.md F06 |
| 248 | TO FIX | What can change while the bearer stays is always a second `## Bearer` block; `## Expected` keeps what the bearer's change cannot stand without | diagnostiqueur.md L333-335 ↔ L461-465, L328-331 | diagnostiqueur | — | diagnostiqueur.md F08 (absorbs D-11) |
| 249 | TO FIX | The nature is given per `## Bearer` block — per entry | diagnostiqueur.md L453-454 ↔ L459-460, L555-557 | diagnostiqueur | — | diagnostiqueur.md F09 |
| 250 | TO FIX | The widened search reaches the manifest, the build files and the resources with a path of their own; the path rule narrowed to `docs/` and the build output | diagnostiqueur.md L198-200 ↔ L210-223 | diagnostiqueur | architecte (only if the conventions name no folder for those) | diagnostiqueur.md F11 |
| 251 | TO FIX | `## Today` carries the set-aside reason, `## Searched` the paths beside the terms; invocation 2 copies `## Today` into `## Gaps set aside` | diagnostiqueur.md L226-228, L244-245 ↔ L384-410, L560 | diagnostiqueur | — | diagnostiqueur.md F12 |
| 252 | NOTE | Repeat `## Trigger` with `## Today` and `## Expected` under every `## Bearer` block; restate the heading count | diagnostiqueur.md L411-415 ↔ L392-393 | diagnostiqueur | — | diagnostiqueur.md F13 |
| 253 | NOTE | Declare the move-5 caller read in the description and in invocation 1's inputs row | diagnostiqueur.md L3, L138 ↔ L122-124 | diagnostiqueur | — | diagnostiqueur.md F14 |
| 254 | NOTE | Code locations are repository-root paths; only the bug-fix folder's own files are relative to it | diagnostiqueur.md L40-41 ↔ L390, L565-566 | diagnostiqueur | — | diagnostiqueur.md F15 |
| 255 | TO FIX | `/diagnostique` renames `investigation/blocked_<id>.md` to `-NN` once the investigation reports having applied its decision | diagnostiqueur.md L164-167, L71 ↔ diagnostique.md L164-171, L77-79, L168 | diagnostique | — | diagnostiqueur.md F17 · fichiers.md F05 |
| 256 | NOTE | `/diagnostique` also skips a gap whose `investigation/blocked_<id>.md` still carries an empty `## Decision`, relaying it as standing | diagnostique.md L77-79 ↔ diagnostiqueur.md L163, L433-434 | diagnostique | — | diagnostiqueur.md F18 |
| 257 | TO FIX | `/diagnostique` withholds phase 2 while a phase-1 block stands and relays the blocked identifiers from its own phase-1 results | diagnostique.md L107, L173-178 ↔ diagnostiqueur.md L163, L173-184 | diagnostique | diagnostiqueur (L182-184 stop routing through a decision on the assembly's file) | chemins-aval.md F12 |
| **Fusionneur · fusion commands · Rédacteur** | | | | | | |
| 258 | NOTE | Bring the index's `fusionneur.md` entry up to what changed — applied last, from the corrected file | modifications.md L806-810 ↔ fusionneur.md L3, L27-36, L88-89, L176-179, L191-204, L240, L289-290, L383-387, L473-480, L509-510 | index | — | fusionneur.md F01 – F08 |
| 259 | TO FIX | The role statement agrees with L431: the report is reviewed once the merge is done; the questions file is the manual step | fusionneur.md L24-25 ↔ L431 | fusionneur | — | fusionneur.md F10 |
| 260 | TO FIX | Add `desc-produit-fusion.md` to invocation 3's inputs row | fusionneur.md L473-480 ↔ L263, L270 | fusionneur | — | fusionneur.md F11 |
| 261 | TO FIX | The title question gets its own plan line and its own resolution at invocation 2 | fusionneur.md L159-162, L359-361 ↔ L136-149, L399-408 | fusionneur | — | fusionneur.md F12 |
| 262 | TO FIX | List the next questions file among invocation 2's outputs; a run that writes one holding a question applies nothing and writes no report | fusionneur.md L407-408 ↔ L262, L91 | fusionneur | fusion, fusion_applique (pass the number — #266) | fusionneur.md F13 |
| 263 | NOTE | Blocking files (unnumbered and numbered) are standing inputs of every invocation, outside "not one file more" | fusionneur.md L279-281, L295-296 ↔ L270 | fusionneur | — | fusionneur.md F16 |
| 264 | NOTE | Invocation 1 may open the feature's own answered `questions-fusionneur-*` files; L313-315 narrowed to other agents' files | fusionneur.md L181-182 ↔ L313-315 | fusionneur | — | fusionneur.md F17 |
| 265 | NOTE | Invocation 3's title check hangs on the moment a kept line enters a section as a new block | fusionneur.md L156-157 ↔ L509-510 | fusionneur | — | fusionneur.md F18 |
| 266 | BLOCKING | `/fusion`, `/fusion_compare`, `/fusion_applique` compute the next `questions-fusionneur-NN` number and pass it in the prompt at every invocation | fusionneur.md L88-89 ↔ fusion.md L157-162; fusion_compare.md L91-96, L45-46; fusion_applique.md L83-88 | commandes (fusion · fusion_compare · fusion_applique) | fusionneur (nothing) | fusionneur.md F19 · chemins-amont.md F24 |
| 267 | TO FIX | Invocation 3 gets the step that applies its own answered questions file to the global and writes the next one; that file is listed among its inputs | fusion.md L47 ↔ fusionneur.md L263, L487-519 | fusionneur | — | fusionneur.md F21 · chemins-amont.md F21 |
| 268 | TO FIX | `/fusion_compare` and `/fusion_applique` gain the blocking-file test before invoking and the rename once applied, in `/fusion`'s form | fusionneur.md L289-290 ↔ fusion_compare.md L18-22; fusion_applique.md L18-27; fusion.md L195-198 | commandes (fusion_compare · fusion_applique) | — | fusionneur.md F22 · chemins-amont.md F25 |
| 269 | TO FIX | When the plan holds `INIT` alone, `/fusion_applique` and `/fusion` copy `desc-produit-fusion.md` over the global before invoking; invocation 2 strips what belongs to the feature file by targeted edits (F14 resolved with it) | fusionneur.md L383-391 ↔ fusion.md L79-84; redacteur.md L689-690 | commandes (fusion_applique · fusion) | fusionneur (L383-391 rewritten around a global already holding the copy) | fusionneur.md F23 · F14 |
| 270 | TO FIX | Drop the `## Questions set aside` skip — no such section exists | fusionneur.md L306-308 ↔ redacteur.md L40-46 | fusionneur | — | fusionneur.md F24 · passages-amont.md F10 (fusionneur, redacteur plans) |
| 271 | settled | Invocation 3 reads every `bugfix-*/desc-bug.md`, never `bug-list.md`; one absent, it does not run and says so (decisions.md) | fusionneur.md L263, L489 ↔ diagnostiqueur.md L34-36, L44, L560-562 | fusionneur | fusion (row 8 unchanged) | fusionneur.md F25 |
| 272 | settled | `Genre:` read on every block at invocations 1 and 2, `INIT` included; `directive` and `hors périmètre` never enter the global; one drop-list (number, `Genre:`, `Global:`), the `NEW` clause at L426-427 dropped | fusionneur.md L337-353, L383-387, L240, L426-427 ↔ redacteur.md L698-708 | fusionneur | redacteur (nothing — the copy keeps `Genre:`) | passages-amont.md F11 (fusionneur, redacteur plans) · fusionneur.md F15 |
| 273 | — | *a-trancher redacteur F19*: the Fusionneur drops an empty `Nature:` line at merge, as it drops `Genre:` and `Global:` | redacteur.md L455, L702-705 ↔ fusionneur.md L386-387 | fusionneur | redacteur (nothing) | redacteur F19 |
| 274 | — | *a-trancher redacteur F01*: the `en anglais :` line is written on the `## Tranché` entry alone; the `## Relevé` clause at L169-170 and the sentence spliced into it go; no `## Relevé` sub-line is defined on the lexicographe's side; note in `todo.md` that a second English rendering of an unquestioned term goes uncaught | redacteur.md L168-173 ↔ modifications.md L205-208; lexicographe.md L163-166, L176-177, L199-200, L285-287 | redacteur | lexicographe (nothing — L176-177 stands; the sub-line of its F12 is not written) | redacteur F01 · F14 · passages-amont.md F02 (lexicographe, redacteur plans) · lexicographe.md F12 (superseded) |
| 275 | — | The invocation-2 route on a `blocked_*` file and the removed "250 KB" figure stay as they are; the index is the side out of date | modifications.md L143 ↔ redacteur.md L527-542, L414-416 | index | — | redacteur F03 · F04 |
| 276 | — | The sentence at L56-57 lists every line the example shows | redacteur.md L56-57 ↔ L59-62 | redacteur | — | redacteur F05 |
| 277 | — | Reword L119 so the rule covers both rows — grid or conversion | redacteur.md L119 ↔ L125, L553-555 | redacteur | — | redacteur F06 |
| 278 | — | Carve invocation 3 out of the two absolute prohibitions at L323-325 | redacteur.md L323-325 ↔ L707-708 | redacteur | — | redacteur F07 |
| 279 | — | Invocation 3 reads and edits `desc-produit-fusion.md`; `desc-produit.md` leaves what it opens; L668 reworded | redacteur.md L385 ↔ L668, L674, L687, L391 | redacteur | — | redacteur F08 |
| 280 | — | Declare `lexique.md`, its `en anglais` lines, among row 3's outputs | redacteur.md L385 ↔ L168-180 | redacteur | — | redacteur F09 |
| 281 | — | State the `NEW` precedence once, for every case | redacteur.md L99-100 ↔ L103-105 | redacteur | — | redacteur F10 |
| 282 | settled | `Global:` written when move 2's same-trigger test said yes, never on a title match; rewrite L83-85 | redacteur.md L83-85 ↔ L457-458, L442-451 | redacteur | — | redacteur F11 |
| 283 | — | Name the questions file as where what is still missing is said; drop "either branch" | redacteur.md L655-657 ↔ L541 | redacteur | — | redacteur F12 |
| 284 | — | Reword the frontmatter claim: the only agent that writes and rewrites the blocks' prose | redacteur.md L3 ↔ decoupeur.md L3; qualifieur.md L3 | redacteur | — | redacteur F22 |
| 285 | — | A decision invocation 3 cannot place goes into `blocked_redacteur.md`, Invocation 3 — never a flag in the copy, never a questions file (its routing under `/fusion` is conflict C15) | redacteur.md L262-266 ↔ L703-705, L474-495 ↔ fusion.md L42-43 | redacteur | — | redacteur D.4 |
| 286 | — | A block created at pass a row 3 goes through moves 2 and 3 as a pass-d block does | redacteur.md L598 ↔ L442-458, L650-651 | redacteur | — | redacteur D.7 |
| 287 | — | Name the qualifieur and the classeur among the readers of the markers at L116 and L323-325 | redacteur.md L116, L323-325 ↔ L71-73; 3b_nature.md L98 | redacteur | — | redacteur D.9 |
| **Lexicographe · 1_lexique** | | | | | | |
| 288 | — | Remove the duplicated clause from the description | lexicographe.md L3 ↔ modifications.md L22-23 | lexicographe | — | lexicographe.md F01 |
| 289 | — | Index records the numbering rule, invocation 3's `Défaut:` sweep and the `## Non tranché` widening | lexicographe.md L110-113, L417-423, L104, L454-458 ↔ modifications.md L22-23; passes/lexicographe.md L72-79 | index | — | lexicographe.md F02 · F03 · F04 |
| 290 | — | A `## Tranché` entry can say a replacement holds for one meaning only; such an entry is exempt from invocation 3's blanket swap — raised as a question instead | lexicographe.md L375-380 ↔ L431-439, L140-155; redacteur.md L167-170 | lexicographe | redacteur (a scoped entry carries two concepts, one `en anglais` each) | lexicographe.md F05 — *added for redacteur* |
| 291 | — | Extend to the `Défaut:` line of an entry whose `Answer:` is empty what invocations 3 and 4 do to an answer; widen the write permission of L66-68 | lexicographe.md L417-420 ↔ L66-68, L431-433, L523-524 | lexicographe | — | lexicographe.md F06 |
| 292 | — | Name `## Non tranché` in invocation 3's *What you write* and Outputs | lexicographe.md L104 ↔ L504-509 | lexicographe | — | lexicographe.md F07 |
| 293 | — | Invocation 4's move 3 moves each settled term out of `## Non tranché` into `## Tranché` | lexicographe.md L549-552 ↔ L191-193, L397-400, L457 | lexicographe | — | lexicographe.md F08 |
| 294 | — | Name invocation 2 among the lexicon's readers | lexicographe.md L211-212 ↔ L103, L354 | lexicographe | — | lexicographe.md F09 |
| 295 | — | Drop the rule that a sweep preserves the terms an answer brought; keep `(réponse)` as the mark | lexicographe.md L199-204, L285-287 ↔ L36-37; 1_lexique.md L87-91 | lexicographe | — | lexicographe.md F10 |
| 296 | — | Align L314-316 with L323-334 — every occurrence, grouped under the meaning read | lexicographe.md L314-316 ↔ L323-334 | lexicographe | — | lexicographe.md A/C3 |
| **Relecteur** | | | | | | |
| 297 | — | Renumber the index's relecteur section to the pass sheet's numbers; record `## Causes so far` (round-1 D-7/C8), the sheet-only ### 17 and the whole-file fallback of ### 13 as deliberate | modifications.md L1175-1240 ↔ passes/relecteur.md L358-543; relecteur.md L149-150, L171-174, L419-422, L66-68 | index | — | relecteur.md F01 · F02 · F03 · F05 |
| 298 | — | A sheet with no `## Signatures` or no `## Conventions` yields what no criteria does (`FAIL structurel`, `Cause: sheet`); point 3 on the `permanente` scope alone when `## Conventions` carries a dash; the `FAIL structurel` row lists this third thing | passes/relecteur.md L456-461 ↔ relecteur.md L112, L404-407 | relecteur | — | relecteur.md F04 · F11 |
| 299 | — | Name Grep as the tool of every read bounded to one line | relecteur.md L4 ↔ L60-61, L80-83, L194-195 | relecteur | — | relecteur.md F06 |
| 300 | — | Three words — `understanding`, `reasoning`, `sheet` | relecteur.md L114 ↔ L115 | relecteur | — | relecteur.md F07 |
| 301 | — | One definition of `reasoning`; "the sheet read wrongly" goes to `understanding` | relecteur.md L115-116 ↔ L176-178 | relecteur | — | relecteur.md F08 |
| 302 | — | The head-rule verdict carries all seven fields (`## Verified` with the red/not-run claim, `## Causes so far` copied plus `understanding`) | relecteur.md L312-315 ↔ L157-160, L171-174, L207-210; 8_code.md L159, L200 | relecteur | — | relecteur.md F09 · passages-aval.md F07 · chemins-aval.md F05 |
| 303 | — | Widen the read of the verdict being replaced to `## Attempts` and `## Causes so far` | relecteur.md L60-61 ↔ L171-173 | relecteur | — | relecteur.md F10 · passages-aval.md F08 · chemins-aval.md F04 |
| 304 | — | *a-trancher relecteur F12*: the reservation is written in `## Findings`, one line per reserved point; `/9_controle` reads it at phase 1 (it opens every `verdict.md`) and relays it — never a verdict, never a block, no new agent input | relecteur.md L110 ↔ L124-155; 9_controle.md L36, L60 | relecteur | 9_controle (one relay line) | relecteur.md F12 · relecteur To settle 2 |
| 305 | — | Point the reference at *What you write* | relecteur.md L46-47 ↔ L105-119, L124-155 | relecteur | — | relecteur.md F13 |
| 306 | — | The second way of seeing a test that does not run reads "a criterion listed under neither `## Tests` nor `## Criteria with no test`" | relecteur.md L409-411 ↔ L340-342 | relecteur | — | relecteur.md F14 |
| 307 | — | Move each rule under the point it governs | relecteur.md L404-416 ↔ L317-346 | relecteur | — | relecteur.md F15 |
| 308 | — | Extend the block to the four inputs the checklist cannot run without; `/8_code`'s Relecteur-block table gains a row for `conception.md` and `tests.md` | relecteur.md L58-59, L340 ↔ L236-239; 8_code.md L418-422 | relecteur | 8_code (the table) | relecteur.md F16 |
| 309 | — | State what the seven fields carry on a PASS | relecteur.md L114 ↔ L124-155 | relecteur | — | relecteur.md F17 |
| 310 | — | Use a word other than *report* for the return message at L295, L298 | relecteur.md L41 ↔ L295, L298 | relecteur | — | relecteur.md F18 |
| 311 | — | The Réalisateur's `FAIL mineur` row fixes every point `## Findings` names | relecteur.md L162-165 ↔ realisateur.md L520 | realisateur | — | relecteur.md F20 — *added for realisateur* |
| **Réalisateur** | | | | | | |
| 312 | — | A verdict judged wrong is a block like the two others; the never-do line says *block* | realisateur.md L524-525 ↔ L229-232, L457 | realisateur | — | realisateur F02 |
| 313 | — | Remove "a criterion no test can be made to read" from the wrong-sheet triggers | realisateur.md L215-216 ↔ testeur.md L274-276; relecteur.md L340-342; modifications.md L1103 | realisateur | — | realisateur F04 · F22 |
| 314 | — | *a-trancher realisateur F11*: `git restore` the non-compiling piece before stopping; `En chantier` says what was written and undone, and where; L475 and the command's removal step hold | realisateur.md L385-386 ↔ L475; 8_code.md L463-466 | realisateur | 8_code (nothing) | realisateur F11 |
| 315 | — | Move the `## Decision` sentence to the blocking-file section | realisateur.md L388-390 ↔ L370-380 | realisateur | — | realisateur F12 |
| 316 | — | Part 2 gains the reprise case, first thing: read `reprise_realisateur.md`, take `Fait` as done, start at `Non fait`, `En chantier` per #314; the file listed under *What you read* | realisateur.md L364-368 ↔ L61-88, L493-511; 8_code.md L134-136, L299 | realisateur | 8_code (prompt line stays) | realisateur F13 · fichiers.md F15 · chemins-aval.md F07 · passages-aval.md F09 |
| 317 | — | The run resuming after a reprise reads the previous `compte-rendu.md` and amends it | realisateur.md L320-322 ↔ L366-368, L521 | realisateur | — | realisateur F14 |
| 318 | — | Replace "one invocation per lot" with the rule it stands for | realisateur.md L31 ↔ L515, L366 | realisateur | — | realisateur F17 |
| 319 | — | The "still empty → call the Arbitre" row becomes a guard: stop and say the orchestration should not have invoked you; the Détailleur's L437 row follows | realisateur.md L503 ↔ 8_code.md L169; detailleur.md L437 | realisateur | detailleur (L437, same row) | realisateur F24 — *added for detailleur* |
| 320 | — | Index: C1 line corrected (`git restore` only), C3/C13/C14/C16/C17 marked passed on the `/8_code` side, the reprise lookup's removal and the four unlisted changes recorded | modifications.md L1085-1121 ↔ realisateur.md L425-427, L508-509, L364, L493-511, L258-270, L504-509, L215-216; 8_code.md L12-14, L48-51, L142-157, L164-175, L463-466 | index | — | realisateur F01 · F05 · F06 · F07 |
| **Sondeur** | | | | | | |
| 321 | — | Record C10 as applied | modifications.md L448-454 ↔ 4_grille.md L179, L299, L461 | index | — | sondeur.md F01 |
| 322 | — | *a-trancher sondeur 1*: the transverse rule is a *défaut*'s only ground; `GRILLE_CADRAGE_PRODUIT_V2.md` L38-41 and modifications.md L395 align to the agent; the `Défaut:` line carries the quoted words as today | modifications.md L395; GRILLE_CADRAGE_PRODUIT_V2.md L38-41 ↔ sondeur.md L398-400, L391, L394-395 | Product Owner (the grid) · index | sondeur (nothing) | sondeur.md F02 · F09 · sondeur To settle 1 |
| 323 | — | Drop the "two lists" count; say row by row which invocations receive each list | sondeur.md L48 ↔ L51-55 | sondeur | — | sondeur.md F04 |
| 324 | — | State the blocking-file target once, before the imperative | sondeur.md L111 ↔ L119-123 | sondeur | — | sondeur.md F05 |
| 325 | — | A feature block contradicting an out-of-scope block is raised by the global as an obligatory question, `Block:` naming the feature block; the case added to *The `Block:` line*; "not your business" struck | sondeur.md L346-348 ↔ L409-435 | sondeur | — | sondeur.md F06 |
| 326 | — | Restate stop 1 on what was asked for, with the three observables | sondeur.md L81-86 ↔ L43, L69 | sondeur | — | sondeur.md F07 |

### Entries added by consolidation

Each one is a side a plan lacked. The agent named applies the table line
it points at; the block says what, if anything, changes in its own file.

    ### architecte.md F20 — the Arbitre names the wrong meaning for the block   (added by consolidation)

    Decision: read what the architecte plan writes — arbitre.md L264-265 says what an Architecte block is (#17)
    Where: arbitre.md L264-265
    Owner: arbitre
    Follows: —

    ### architecte.md F19 — the prompt never says who called   (added by consolidation)

    Decision: the Arbitre's invocation-3 prompt at L418 gains the line "called by the Arbitre" (#18)
    Where: arbitre.md L418
    Owner: architecte
    Follows: arbitre

    ### realisateur F19 — a trap on a consumed symbol   (added by consolidation)

    Decision: arbitre.md L396-398 says the Réalisateur reads the two general sections whole and greps its lot's symbols (#19)
    Where: arbitre.md L396-398
    Owner: realisateur
    Follows: arbitre

    ### arbitre.md F13 — `architecte/arbitre-<lot>.md` on a multi-entry file   (added by consolidation)

    Decision: architecte.md L666 keys the Arbitre's request on the name the Arbitre now gives it — by the blocking file's scope (#12)
    Where: architecte.md L665-666
    Owner: arbitre
    Follows: architecte

    ### cadreur.md F02 · F08 — caller files go into `Touches`   (added by consolidation)

    Decision: read what the cadreur writes — the meaning of `Touches` widens to callers; the Vérificateur reads the five fields with that meaning (#61)
    Where: verificateur.md (its reading of `Touches`)
    Owner: cadreur
    Follows: verificateur

    ### verificateur.md F09 — the bearer's layer on a bug-fix   (added by consolidation)

    Decision: the lot list states each lot's layer on a bug-fix cycle — the Cadreur chooses where (the bearer's line in `## Symbols` changes no other reader) (#83)
    Where: cadreur.md L77-78 and the lot list's form
    Owner: cadreur
    Follows: verificateur

    ### verificateur.md F23 — the ceiling remark   (added by consolidation)

    Decision: the Cadreur relays the remark as it relays the archivable line (#84)
    Where: cadreur.md L926-927
    Owner: verificateur
    Follows: cadreur

    ### controleur.md F12 — the `B<n>` travels   (added by consolidation, from a-trancher)

    Decision: `desc-bug.md` carries the `B<n>` of the report line a gap comes from, when `bug-list.md` carries one; the lot list carries it in turn (#203)
    Where: diagnostiqueur.md (the entry's shape); cadreur.md (the lot list on a bug-fix)
    Owner: 9_controle
    Follows: diagnostiqueur, cadreur

    ### realisateur F18 · renommages.md F03 — the created/modified mark   (added by consolidation)

    Decision: the `## Signatures` shape marks each symbol *created* or *modified* (#237)
    Where: detailleur.md L224-232, L397-398
    Owner: detailleur
    Follows: realisateur, testeur, relecteur

    ### realisateur F24 — the still-empty row becomes a guard   (added by consolidation)

    Decision: read what the realisateur writes — the same row at detailleur.md L437 says stop, never call the Arbitre (#319)
    Where: detailleur.md L437
    Owner: realisateur
    Follows: detailleur

    ### concepteur.md F08 — "empty bodies"   (added by consolidation)

    Decision: read what the concepteur writes — testeur.md L19-20, L23-24 stop calling the deliverable "empty" (#181)
    Where: testeur.md L19-24
    Owner: concepteur
    Follows: testeur

    ### testeur.md F03 — no test command when the conventions name none   (added by consolidation)

    Decision: read what the testeur writes — the same one fallback at concepteur.md L212-221 and realisateur.md L423-427, L586 (#188)
    Where: concepteur.md L212-221; realisateur.md L423-427, L586
    Owner: testeur
    Follows: concepteur, realisateur

    ### concepteur To settle 3 — the commit message   (added by consolidation, from a-trancher)

    Decision: one line — commits read `<lot>: <what the commit carries>` (#177)
    Where: concepteur.md (move 5), testeur.md (move 6), realisateur.md (its commit rule)
    Owner: 8_code
    Follows: concepteur, testeur, realisateur

    ### lexicographe.md F05 — a meaning-scoped retirement   (added by consolidation)

    Decision: read what the lexicographe writes — a scoped `## Tranché` entry carries two concepts, and the `en anglais` line goes on each (#290)
    Where: redacteur.md L167-170
    Owner: lexicographe
    Follows: redacteur

    ### relecteur.md F20 — "fix the point reported", singular   (added by consolidation)

    Decision: the `FAIL mineur` row fixes every point `## Findings` names (#311)
    Where: realisateur.md L520
    Owner: realisateur
    Follows: —

---

## 2 — The conflicts

The Product Owner writes under `Arbitration:`. A defect below is absent
from the first table until she has.

### C1 · `## Files` — who declares the files a lot creates

Kind: divergent
Plans: cadreur (F19 · renommages F01 · passages-aval F01), detailleur (F20 · renommages F01 · renommages F02 · passages-aval F01), concepteur (passages-aval F01 · renommages F02), testeur (F12 · renommages F02 · passages-aval F01), realisateur (renommages F02 · passages-aval F01 · F25), relecteur (passages-aval F01)
What is wrong: every plan makes the Détailleur the owner of `## Files` and drops the dash, but they name two different writers for the files a production lot creates — the detailleur, concepteur, testeur and relecteur plans have the Détailleur derive them from the conventions' placement rules (the Concepteur then picks within `## Files`, detailleur.md L401-402 goes), while the cadreur and realisateur plans leave them to the Concepteur, which places the created symbols and names their files in `conception.md`, that file then counting as declared for the `## Outside the lot` checks — and the realisateur plan's F25 keeps L401-402 with the Concepteur named as the one who places.
Where: detailleur.md L259-265, L401-402 ↔ cadreur.md L753-754; concepteur.md L57-58, L186-191, L259-261; testeur.md L58-59, L282-284; realisateur.md L189-191, L533-535; relecteur.md L386-388
Quotations: —

Arbitration:

### C2 · The half-answered `## Decision` and the hand-back line

Kind: divergent (and owner, on the `/8_code` test)
Plans: arbitre (F09 · F16 · F17 · renommages F07 · passages-aval F11 · chemins-aval F20), detailleur (F16 · F22 · chemins-aval F20 · renommages F07 · passages-aval F11), realisateur (F10)
What is wrong: the arbitre plan reverses the empty-field rule — a product question is handed back with a `Not settled here.` line written under its number (or at file level), the empty-number signal of L165-167 is dropped, and every reader keys on that line (the Détailleur's L438 row becomes the hand-back row, `/8_code` 4b renames only when no entry carries it) — while the detailleur and realisateur plans keep the empty number as the Arbitre's signal (arbitre.md L165-167 "stands"), remove the `Not settled here.` row from the Détailleur as one that never fires, and have `/8_code` count the numbered answers against the `## Blocking N` headings; on that `/8_code` test the arbitre plan claims the Arbitre as owner of the field's form, the detailleur plan claims `8_code`. The a-trancher decision on the wait (arbitre 1) keeps the poll and does not say which signal the caller reads.
Where: arbitre.md L165-167, L178-187, L215-217, L456-462 ↔ 8_code.md L50-51, L167-170; detailleur.md L346, L434-441; realisateur.md L317-318, L503-505; audit_blocages.md L112-115
Quotations: —

Arbitration:

### C3 · One blocking-file shape — who owns it

Kind: owner
Plans: arbitre (F19 · renommages F05 · renommages F06 · passages-aval F13), detailleur (renommages F06), realisateur (F09 · renommages F05 · renommages F06 · passages-aval F13)
What is wrong: the three plans agree on the outcome — `## Blocking N` with `###` headings and one `## Decision` even for one entry, the Réalisateur's second shape at L272-288 deleted, the Arbitre's `##` single-entry reading at L129-130 and L180 dropped — but the arbitre plan names the realisateur as owner, the detailleur plan the arbitre, and the realisateur plan splits it by file.
Where: arbitre.md L129-130, L180 ↔ detailleur.md L292-293; realisateur.md L258-259, L272-288
Quotations: —

Arbitration:

### C4 · `## Traps` is not a heading of the state document — who aligns realisateur.md L135-137

Kind: owner
Plans: arbitre (F18), realisateur (F20)
What is wrong: both plans align realisateur.md L135-137 on the headings the Arbitre writes under (`## Traps — general`, or a subject's own `###`, as arbitre.md L391-393 says — the realisateur plan cites the same text at L401-403); the arbitre plan names the arbitre as owner (it loads the skill and writes the trap, "if the skill confirms it"), the realisateur plan names the realisateur.
Where: realisateur.md L133-137 ↔ arbitre.md L391-393
Quotations: —

Arbitration:

### C5 · The relay of `## Ce qui revient` and `## Ce que j'en fais`

Kind: divergent (and owner)
Plans: arbitre (fichiers F16), cadreur (fichiers F16 · chemins-aval F02)
What is wrong: the arbitre plan keeps the relay in `/8_code`, moved after `/7_lots` returns and read from the archived `code/redecoupage-NN.md` (owner `8_code`); the cadreur plan moves the relay into `/7_lots`, before it renames the file, drops it from `/8_code`, and has the Cadreur state the two sections in its report on every redécoupage, not only a third return (owner `7_lots`, cadreur L923 follows).
Where: 8_code.md L352-354 ↔ cadreur.md L907-909, L923; 7_lots.md L103, L240-253
Quotations: —

Arbitration:

### C6 · "a product decision" in the Architecte's two rows — does arbitre.md L431-432 change

Kind: divergent
Plans: arbitre (passages-aval F14), architecte (passages-aval F14)
What is wrong: both apply decisions.md on architecte.md L736-737; the arbitre plan then rewrites the Arbitre's two refusal rows to key on the two wordings (*Not a convention — here is where it belongs* → settle from that, *This is a product decision* → hand back), while the architecte plan says arbitre.md L431-432 already reads the two rows apart and nothing there changes (audit_conventions.md L126 follows instead).
Where: architecte.md L736-737 ↔ arbitre.md L431-432; audit_conventions.md L124-126
Quotations: —

Arbitration:

### C7 · The round count — who writes it, where

Kind: divergent (and owner)
Plans: cadreur (F18 · fichiers F14 · chemins-aval F19 · passages-aval F04), verificateur (F16 · chemins-aval F19 · passages-aval F04)
What is wrong: the cadreur plan has the Vérificateur write the round number in `code/sequence.md` (previous plus one when the previous `## Defects` carried lines, `1` otherwise) and the Cadreur count on that line, never on archived files (owner verificateur); the verificateur plan has the Cadreur archive each round's `code/sequence.md` as `code/sequence-NN.md` (by Read and Write) before calling the Vérificateur again, the count staying on the archived files and bounded to the current split (owner cadreur).
Where: cadreur.md L822-823 ↔ verificateur.md L96, L444-445, L105; 7_lots.md L101-103
Quotations: —

Arbitration:

### C8 · A re-cut lot and its `verdict.md`

Kind: divergent (and owner)
Plans: cadreur (chemins-aval F22), relecteur (chemins-aval F22)
What is wrong: to stop a re-cut lot inheriting its `## Attempts`, the cadreur plan gives a lot whose anchor or fields change on a redécoupage the next free number and retires its old number with its `code/<lot>/` folder (owner cadreur; `8_code` L344-354, L375 and the Vérificateur's L440-442 follow); the relecteur plan keeps the number and has `/8_code` delete `code/<lot>/verdict.md` alongside the stale sheet for every lot with no PASS (owner `8_code`).
Where: 8_code.md L344, L379-382 ↔ relecteur.md L157-158; cadreur.md L884-891
Quotations: —

Arbitration:

### C9 · `R<n>` in the sheet's `## Conventions` — who owns the change

Kind: owner
Plans: architecte (passages-aval F10), detailleur (F23 · passages-aval F10), relecteur (passages-aval F10)
What is wrong: the three plans agree the sheet cites rules by `R<n>` and shows `spécifique` rules in its example; the architecte and relecteur plans name the detailleur as owner (it writes the field), the detailleur plan names the architecte (it owns the rule key; the detailleur applies it).
Where: detailleur.md L250-254, L652 ↔ architecte.md L131-132, L144-152; relecteur.md L141
Quotations: —

Arbitration:

### C10 · realisateur F08 — the `permanente` grep rests on a line the architecte plan removes

Kind: cited
Plans: realisateur (F08), architecte (F10)
What is wrong: realisateur F08 names the gesture that locates the `permanente` rules as "a `Grep` on the marker at the end of the line", citing architecte.md L140; architecte F10 finds L140 contradicted by the rule line's own example at L121-122, where the mark is the third field and `mechanical` ends the line, and drops "at the end of the line" — so the gesture as decided finds nothing once #30 is applied.
Where: realisateur.md L66-70, L97-98, L551-552, L452-453 ↔ architecte.md L140, L119-128
Quotations: architecte.md L140 — "🔴 **`permanente` or `spécifique`, at the end of the line.**" · architecte.md L121-122 — "R12 · Every identifier that leaves a module is in English · permanente · mechanical"

Arbitration:

### C11 · An attempt that committed nothing — what the fresh Réalisateur is handed

Kind: divergent
Plans: commandes (chemins-aval F21), realisateur (chemins-aval F21)
What is wrong: both route the case as a FAIL with a fresh Réalisateur and give the FAIL table a row; the commandes plan has the orchestrator write the verdict with a `## Status` the table has a row for, the realisateur plan re-invokes with no verdict named and keys the row on "no `## Status`, or no verdict named".
Where: 8_code.md L129-132, L138, L149-151 ↔ realisateur.md L519-522
Quotations: —

Arbitration:

### C12 · realisateur.md L352-355 — is the worktree about to be removed

Kind: divergent
Plans: realisateur (F16 · chemins-aval F25), commandes (chemins-aval F01)
What is wrong: the realisateur plan corrects L352-355 as a false fact — the reason for writing no report is that the lot is about to be cut differently, not that the worktree is about to be removed — and corrects L336-338 (the blocking file and `code/redecoupage.md` are new files that stay and the orchestration commits them); the commandes plan's decision on chemins-aval F01 closes the loop's worktree before `/7_lots` and states that L352's reason "now holds" and the realisateur plan's F25 entry "reads against this decision".
Where: realisateur.md L335-338, L352-355 ↔ 8_code.md L357-358, L365-366; 7_lots.md L64, L224
Quotations: —

Arbitration:

### C13 · renommages F09 — the number the report cannot know, and whether the Relecteur resolves it

Kind: divergent
Plans: realisateur (renommages F09), relecteur (renommages F09)
What is wrong: both have the report name the blocking file at its unnumbered name; the realisateur plan adds the entry number (`blocked_realisateur.md — Blocking 2`) and has the Relecteur resolve it to the highest `blocked_realisateur-NN.md` in the lot folder, while the relecteur plan says the Relecteur reads the field and never opens a blocking file, so it greps no number and nothing on its side changes.
Where: realisateur.md L176-178 ↔ 8_code.md L170-171; relecteur.md L184-185
Quotations: —

Arbitration:

### C14 · A criterion whose behaviour the sheet removes — a block, or a `tests.md` field

Kind: divergent
Plans: testeur (F14 · F07 · passages-aval F12), realisateur (passages-aval F12), relecteur (passages-aval F12)
What is wrong: the testeur plan makes the case a block (`blocked_testeur.md` — only the Product Owner removes a behaviour; the report line at L233 goes); the realisateur and relecteur plans give `tests.md` a field for "a criterion gone with an adapted test" beside the green-by-declaration tests, which the Réalisateur's `## Red` read and the Relecteur's point 2 then take into account.
Where: testeur.md L230-233 ↔ 8_code.md L112-113, L479-488; testeur.md L268-291; realisateur.md L77-78; relecteur.md L333-334
Quotations: —

Arbitration:

### C15 · `blocked_redacteur.md` under `/fusion` — route by name, or an `## Invocation` heading

Kind: divergent
Plans: fusionneur (passages-amont F09), redacteur (F16 · chemins-amont F23 · passages-amont F09 · fichiers F06)
What is wrong: the fusionneur plan keeps the Rédacteur's four-heading blocking file and has `/fusion` row 3 route a filled `blocked_redacteur.md` to the Rédacteur's invocation 3 by its name (owner `fusion`); the redacteur plan adds an `## Invocation` heading to the Rédacteur's blocking file — five headings, as the Fusionneur's — so row 3 stands as written and `/2_structure` can tell an invocation-3 block from its own (owner redacteur). The fusionneur plan says only one of the two is applied.
Where: fusion.md L43 ↔ redacteur.md L343-359; fusionneur.md L200-205; 2_structure.md L103-110
Quotations: —

Arbitration:

### C16 · classeur.md L181 — "Split a block, or merge two — that is the decoupeur's"

Kind: owner
Plans: classeur (F11), decoupeur (F17)
What is wrong: the two plans rewrite the same line for two halves of it — the classeur plan (owner classeur) says a split that follows one of the classeur's answers is the Rédacteur's and the decoupeur's split is by trigger; the decoupeur plan (owner decoupeur, classeur and qualifieur following) says the line stops naming the decoupeur as the merger and names no owner for a merge, the qualifieur's L214 with it — and the a-trancher decision (decoupeur F17) settles that nobody merges. The decisions are complementary; the owner is claimed twice.
Where: classeur.md L181, L115 ↔ decoupeur.md L110; qualifieur.md L214
Quotations: —

Arbitration:

### C17 · fichiers.md F07 — the audit does not see `cadrage-produit/blocked_*-NN.md`

Kind: cited
Plans: sondeur (fichiers F07) — the convertisseur plan, also named, does not carry it
What is wrong: the finding is confirmed on the `/4_grille` side (L431-434 file the sondeurs' blocking files under `cadrage-produit/`, a folder audit_blocages.md L26-29 does not list) and carries no decision: the sondeur plan did not open `audit_blocages.md` L27, and no other plan decided it — the entry for `chemins-aval.md` F18 (#47) touches the same lines without adding the folder.
Where: audit_blocages.md L26-29 ↔ 4_grille.md L431-434
Quotations: audit_blocages.md L27-29 — "🔴 **Three places**: `code/**/`, the folder's own root *(`blocked_architecte`, `blocked_diagnostiqueur`)*, and `investigation/`" · 4_grille.md L433-434 — "git mv docs/features/<name>/cadrage-produit/blocked_par-bloc.md docs/features/<name>/cadrage-produit/blocked_par-bloc-NN.md"

Arbitration:

---

## 3 — Judged, nothing to apply

Findings the plans judged `wrong`, `overstated`, `stale` or as needing no
change; carried here so wave 3 does not look for them: cadreur.md F04 ·
decoupeur.md F05, F06, F07 · concepteur.md F05, D-11, D-12 ·
architecte.md D-22, C-6, C-7 · fusionneur.md F09 · redacteur F02, F15,
passages-amont F04, B.8 · convertisseur.md c.1 · sondeur.md F03,
fichiers.md F13 · controleur.md C1 NOTE, C5 NOTE · qualifieur.md F06
(void with #135) · detailleur.md renommages F16 (nothing of the
Détailleur moves, #49).

Not judged by any plan, for want of a text: lexicographe.md A/C15, B.1,
B.2 · diagnostiqueur.md D-12, D-19, D-22 · redacteur C18, B.2, B.6, D.1
note, D.14-D.17 · sondeur B-2, D-12 · classeur B-3, B-6 · fusionneur
D-12.
