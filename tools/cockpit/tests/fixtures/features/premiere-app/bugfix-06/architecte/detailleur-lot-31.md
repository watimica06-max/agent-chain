## What I need

Whether a module's *test* source set counts as "a module the lot
touches" under R72, and so whether a fake or a test call site broken by
a changed signature is deferrable the way a production call site in
another module is.

## Why the lot cannot proceed

It proceeds. R74 already settles the same-module case for production
sources, and the Arbitre's decision on this lot settles the concrete
list of files. What no rule states is the general answer, and the
question comes back on every signature change reaching a widely faked
interface.

The two readings differ on real files. Under "the lot touches the module,
so its whole check must exit 0", a lot changing an interface must adapt
every fake of that interface in every module it touches at all — here,
five test files in `:app-phone` that no entry of the technical document
names and that the split did not declare. Under "a test source set
follows its own lot", those files belong to whichever lot owns the
subject they exercise, and R72's deferral covers them.

`:app-phone` shows the two readings colliding inside one module: this
lot adapts four fakes and one direct call site there, while five other
`:app-phone` and `:app-wear` files — including two production
collectors, `RaceListViewModel` and `RaceDetailViewModel` — stay with
lot-56. `:app-phone:check` therefore does not exit 0 at the end of this
lot even though the lot carried the test files R72 was read as
requiring, so the criterion the enumeration was derived from is not the
one the enumeration satisfies.

## Where I met it

lot-31, §2.1 and §7.2 — `RaceRepository`'s nine methods becoming
`suspend` and its two flows changing element type. Confirmed by grep:
eleven fakes or direct call sites across `:core-domain`, `:app-phone`
and `:app-wear` test source sets, of which the split declared two.

`MainActivityTest` (`:app-phone`) is the one this lot's sheet added that
the decision's enumeration does not name: it calls
`raceRepository.saveImportedRace` from three non-suspend test bodies,
its owning lot (lot-27) is coded and passed, and no later lot of the
sequence names it.

## What I think it is        add · update · remove

update — R72 and R73, stating whether "every module it touches" reaches
that module's test source set, and which lot owns a fake broken by a
signature change no entry attributes to it.

## Verdict

**A convention. Written as R85 and R86, section 2 of
`docs/TECHNICAL_CONVENTIONS.md`.**

**The three filters leave it standing.** Gradle's own `check` task does
not distinguish a main source set's owner from a test source set's
owner — it compiles and runs both as one unit per module, and knows
nothing of lots at all; that coupling is a platform fact, but which lot
answers for which file inside it is not something Gradle, or any tool,
decides. It holds on no one machine. **It is a convention**, and R72/R74
did not yet reach it.

**The collision the request shows is real, and proves the enumeration's
own premise false.** The Arbitre's decision read R72's "every module it
touches" as requiring this lot to carry every `:app-phone`/`:app-wear`
test file broken by the `RaceRepository` signature change, so that
`:app-phone:check` and `:app-wear:check` would exit 0 at the end of this
lot. But five files stay with lot-56 regardless — two of them
production collectors, `RaceListViewModel` and `RaceDetailViewModel` —
so `:app-phone:check` does **not** exit 0 at the end of this lot even
with every enumerated test file carried. The criterion motivating the
enumeration is not the one the enumeration achieves; enumerating harder
cannot fix that, because carrying `RaceListViewModel` and
`RaceDetailViewModel` themselves would mean this lot absorbing lot-56's
own scope.

**R85 fixes the reading of "touches."** `RaceRepository` lives in
`:core-domain`; a fake or a direct call site in `:app-phone`'s or
`:app-wear`'s *test* source set is, under R74's own module-difference
test, exactly the deferrable case R72 was built for — a call site in a
module other than the signature's own. The only reason it looked
otherwise is that this lot also edits four fakes and one call site
*inside* that same module to keep its **own** tests compiling. R85 says
that edit does not extend the lot's `check` obligation to the rest of
the module: `:app-phone` and `:app-wear`'s production call sites —
`RaceListViewModel`, `RaceDetailViewModel`, `HomeViewModel`,
`PreparationViewModel`, `MainActivity`'s `WatchApp` — stay with lot-56
(or whichever lot's sheet names them), named under R73 exactly as an
ordinary cross-module deferral, undisturbed by this lot's presence in
the same module.

**R86 answers the general question directly**: a test file's owner is
the lot whose scope covers the subject it exercises — a fake of
`RaceRepository` used by `RaceListViewModelTest` belongs with whichever
lot owns `RaceListViewModel`, not with whichever lot happens to widen the
interface it fakes. A widely-faked interface change therefore adapts
only the fakes serving *its own* lot's tests; every other fake is the
consuming lot's to adapt, same as its production call site.

**`MainActivityTest` is not this and needs no third rule — R73 already
carries it.** Its owning lot, lot-27, is coded and passed, and no later
lot's sheet names it. "A red build no lot is named the owner of is not
deliverable" already says this is not resolved by wording; it is a hole
in `code/decoupage.md`'s enumeration — a call site the split never
attributed to anyone once lot-27 closed. 📌 **Not architecte's to
settle**: raise it back through the split, the same way lot-53's R74
finding was raised, so a lot is named to adapt it (very possibly this
one, since no later lot exists to inherit it, but that assignment is the
split's call).

Concretely, this lot proceeds carrying only the fakes and call sites
serving its own tests; the four fakes plus one direct call site already
adapted stand as R85 intends. The five files staying with lot-56 are
deferred under R72/R74/R85/R86 together, named in this lot's report per
R73. `MainActivityTest`'s orphaned break goes back through the split as
its own correction, not as a deferral this lot can claim under R72.

