# Questions — Architecte, invocation 1

> Seven questions. Each names the entries and the anomaly, and stops
> there. 🔴 **Fill the `Answer:` field of each; leave nothing blank.**

---

## Q1 — The `Consumes:` graph holds a cycle around §9.18

**Kind**: coverage

**Entries**: §9.6, §9.9, §9.18, §11.2

**The anomaly**: §9.6 declares `Consumes: … §9.18/§11.2` and §9.18
declares `Consumes: §9.6, §9.9, §11.2, §10.4`; §9.9 and §9.18 consume
each other the same way; §11.2 declares `Consumes: … §9.18` while §9.18
declares `Consumes: … §11.2`. Three two-entry cycles. Nothing settles
which of §9.18 and §9.6/§9.9 owns the rendering of the
connectivity-denied state, so the direction of the dependency between
them cannot be read. The rule fixing the import graph on the declared
adjacency (G4.1) is not written while this stands.

**Answer**:

---

## Q2 — `Consumes:` is declared on 19 entries out of 50

**Kind**: coverage

**Entries**: §9.1–§9.18 and §11.2 declare one; §1.1–§8.3, §10.1–§10.4
and §11.1 declare none.

**The anomaly**: thirty-one entries declare no `Consumes:` line while
their own prose states a dependency — §3.4 computes from §3.2's
`allure-segment`, §3.5 from §3.4, §3.3 from §2.2's
`expectedDistanceM`, §6.1 from §2.1 and §2.2. Read as declared, those
entries are roots that consume nothing; read as written, they are not.
The set of root entries cannot be established from the document, and
the rule forbidding a root module to import anything (R10) is written
in its class form only, naming no entry.

**Answer**:

---

## Q3 — The segment names are displayed but hold no resource key

**Kind**: conjunction

**Entries**: §5.1, §9.2, §9.12, §10.2, §10.4

**The anomaly**: §5.1's mapping table produces domain segment names —
"SkiErg", "Rameur", "Farmers Carry", "Wall Balls" — which §9.2 renders
in each segment row and §9.12 renders as the station name and as the
Roxzone destination. §10.2 states that no visible string is ever
hard-coded and that every one comes from a resource file, and §10.4's
catalogue holds no key for any segment name. A segment name is
therefore both a domain value produced by §5.1 and a visible string
§10.2 forbids in code, and no entry says which it is.

**Answer**:

---

## Q4 — §9.2 consumes §3.4 for a delta §3.4 does not produce

**Kind**: conjunction

**Entries**: §3.4, §9.2

**The anomaly**: §9.2 declares `Consumes: … §3.4` for its delta column,
shown on all 30 rows of a stored race against the reference. §3.4
defines `écart = temps_projeté − temps_référence_du_segment`, projected
from a live `allure-segment`, recomputed continuously, and states it
"exists only on `RUN` segments". The per-segment delta of a finished
race on a `STATION`, `ROXZONE_OUT`, `ROXZONE_IN` or `FINAL` segment is
defined by neither entry.

**Answer**:

---

## Q5 — §1.3's freshness window and §9.16's refresh cadence coincide

**Kind**: conjunction

**Entries**: §1.3, §9.12, §9.16

**The anomaly**: §1.3 gives every sensor-derived value a 10-second
freshness window, "in both normal and power-save display mode", past
which it "returns to its fallback state" and "renders as a dash"
(§9.12). §9.16 sets the power-save refresh cadence to exactly 10
seconds and states that in power-save "values stay shown, dimmed,
rather than replaced with a dash — a deliberate departure". In
power-save every value reaches the freshness boundary at each refresh,
and whether it renders dimmed or as a dash there is settled by neither
entry.

**Answer**:

---

## Q6 — B59 carries a dash in `tracabilite.md`

**Kind**: coverage

**Entries**: none — product block B59, and the preamble's "Out of
scope"

**The anomaly**: `tracabilite.md` maps B59 to a dash: no §X.Y entry
carries its rules. Its content — pace and heart rate are the only
physiological measures, and calorie count, step count, displayed stride
cadence, altitude and any route or map are out of scope — lives only in
the preamble. The section split has no entry to cut a lot from, and no
rule of the conventions file cites it.

**Answer**:

---

## Q7 — Two entries point at texts that do not exist

**Kind**: coverage

**Entries**: §2.2 → §10.1 ; §4.1 → §9.9

**The anomaly**: §2.2 states that on a bound violation "§10.1's
constraint message shows", and §10.1 defines display formats only — no
entry of that name, and §10.4's catalogue holds no key for it. §4.1
states that "§9.9's home-screen reminder re-requests it", and §9.9
describes no reminder element — only the "Aucune référence" badge —
though §10.4 does hold `watch.permission.reminder`. The rule forbidding
a literal user-facing string (R64) requires a key for both, and neither
key can be named.

**Answer**:
