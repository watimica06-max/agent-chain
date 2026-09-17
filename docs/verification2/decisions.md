# decisions.md — the second round's fourteen `QUESTION` findings, settled

🔴 **A question in this list is settled.** 📌 **Apply the decision, never
reopen it** — ⚠️ **and if the plan you are building contradicts one, it
is the plan that is wrong.**

📌 **The key is `<report> <id>`**, exactly as the report writes it.

---

## `assembleur.md` F05 — resuming on a question that cannot be placed

🔴 **The decision carries the value of the `Block:` line, and the agent
writes it.**

📌 **L190 forbids editing a `Block:` line *to merge two questions*** —
⚠️ **not writing one the decision gives you.**

🔴 **The blocking file says so**: `## To resume` asks for the value, not
for an opinion.

---

## `cadreur.md` F23 — resuming through `/7_decoupe`

🔴 **Moot.** 📌 **`cycle.md` is deleted** — ⚠️ **the command is gone and
so is the row.**

🔴 **Remove every mention of `/cycle` and `cycle.md`** wherever you meet
one.

---

## `chemins-amont.md` F16 — a nature waiting on a product answer

🔴 **An answer that changes no block leaves the document standing.** 📌
**That is an outcome, not a wait** — ⚠️ **a relay row was missing, not a
rule.**

📌 **The command says it**: the nature does not run, its part stays as
it is, and the turn closes.

---

## `classeur.md` F02 — a « tap → state change + visible feedback » block

🔴 **Restore what C2 intended: the block takes the nature of what the
action produces.**

📌 **`presentation` only when the block describes the perceived part
alone.** ⚠️ **A block describing both is not badly split** — 🔴 **it is
not a Product Owner question.**

⚠️ **The frontier as written turns every « tap → state + feedback »
into a question** — 📌 **exactly the cost C2 named as its defect.**

---

## `controleur.md` F11 — the partial's opening `Blocks:` line

🔴 **The prompt's list is authoritative.**

📌 **The opening line says which blocks the group actually treated** —
🔴 **a gap between the two is a finding of the report**, ⚠️ **never a
reason to pick one over the other.**

---

## `controleur.md` F12 — the sheets a correction cycle wrote

🔴 **Mark `carried` the blocks a correction cycle built**, like the four
genres that produce no lot.

📌 **They are not missing intentions** — ⚠️ **they were built,
elsewhere**, and the map has to say so instead of letting them fall
through.

---

## `fichiers.md` F09 — resuming a Vérificateur block

🔴 **Moot.** 📌 **Same reason as `cadreur.md` F23** — `cycle.md` is
deleted.

---

## `fusionneur.md` F25 — what invocation 3 reads

🔴 **Invocation 3 reads `desc-bug.md`, never `bug-list.md`.**

📌 **A gap the diagnosis set aside produced no code** — ⚠️ **carrying it
into the global would describe a behaviour the application does not
have**, which is what the global exists to prevent.

📌 **The intent is not lost**: a `set aside` stays in `desc-bug.md` with
its reason, 🔴 **and comes back through a later `bug-list.md`** if the
Product Owner takes it up again.

⚠️ **`desc-bug.md` absent** — 🔴 **invocation 3 does not run, and says
so.** 📌 **Never fall back on `bug-list.md`.**

---

## `passages-amont.md` F11 — which genres enter the global

🔴 **The Fusionneur reads `Genre:` on every block**, not only at `INIT`.

| Genre | |
|---|---|
| `comportement` | ✅ **Enters** |
| `transverse` | ✅ **Enters** — 📌 **a rule over a category is product** |
| `recette` | ✅ **Enters** — 📌 **behaviour checked by hand**: the global says what the application does, not how it is checked |
| `référence` | ✅ **Enters** — 📌 **data the product cites** |
| `directive` | 🔴 **Does not enter** — ⚠️ **a means imposed**: 📌 **it lives in the conventions** |
| `hors périmètre` | 🔴 **Does not enter** — ⚠️ **set aside explicitly**: 📌 **describing it would describe a product that does not exist** |

---

## `passages-aval.md` F14 — « a product decision » in two rows

🔴 **Two distinct wordings, and the Arbitre reads them differently:**

| The verdict says | The Arbitre |
|---|---|
| **Not a convention — here is where it belongs** *(the code, the tooling, the machine)* | 🔴 **Settles from that** |
| **This is a product decision** | 🔴 **Waits for the Product Owner** |

⚠️ **The *Not a convention* row must no longer end on « a product
decision »** — 📌 **that is what makes the two rows indistinguishable.**

---

## `passages-aval.md` F15 — `PASS with reservation`

🔴 **Every reader matches the `PASS` prefix.** 📌 **A lot with a
reservation is coded** — ⚠️ **the reservation is a note for what
follows, not a failure.**

📌 **The readers concerned**: `relecteur`, `detailleur`, `verificateur`,
`8_code`, `9_controle`.

---

## `redacteur.md` F11 — what « found » means at move 2

🔴 **The same trigger**, never a title that resembles another.

📌 **A close title says nothing** — ⚠️ **two sections can carry the same
name and describe two different behaviours.**

---

## `renommages.md` F16 — the Concepteur and the Architecte

🔴 **The Concepteur writes an `architecte/` request, like the Détailleur
and the Réalisateur.**

⚠️ **Its exception was unjustified** — 📌 **a placement the conventions
do not settle is exactly a missing rule**, which is what the route is
for.

📌 **Meanwhile it places the symbol in the module of the one it depends
on most**, and says so in its report.

---

## `verificateur.md` F19 — six layers against twelve sections

🔴 **Match on what the section is about**, never on its title.

📌 **No match, the default row** — ⚠️ **and the agent says so**, so that
a ceiling never applies in silence.

---

## What is not in this list

⚠️ **A question you meet while building a plan and that is not here is
not settled.**

🔴 **Do not settle it.** 📌 **Write it into the plan under
`## To settle`**, with what each option costs — ⚠️ **and stop the plan
where it bites.**

🔴 **Above all when it turns on intent, scope, or user-facing
behaviour** — 📌 **those belong to the Product Owner, always.**
