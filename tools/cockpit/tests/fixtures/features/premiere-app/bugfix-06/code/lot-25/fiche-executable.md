## Signatures

PhoneDestination
  gains `val isRestorable: Boolean`, a computed property (no new
  constructor field): false on `ImportPreview` and `PasteError`, true
  on every other destination (`RaceList`, `RaceDetail`, `Profile`,
  `PasteResult`) — the predicate PhoneNavigator's restoration walks
  against; `RaceDetail`'s existing `raceId: Long` is unchanged

PhoneNavigator @Inject constructor(stateStore: PhoneNavigationStateStore)
  — at construction, reads `stateStore.restore()`; a null result (never
    saved) seeds the back stack at `[RaceList]`, unchanged from today.
    A non-null result deserializes to the back stack it was saved from,
    then that stack's trailing entries are dropped, from the top down,
    for as long as the top one's `isRestorable` is false — so a saved
    stack whose current destination was `ImportPreview` or `PasteError`
    restores to the nearest destination beneath it whose
    `isRestorable` is true instead. `RaceList` is always the stack's
    first entry and is always restorable, so this always terminates on
    at least it.
  — every mutating call (`toRaceDetail`, `toProfile`, `toPasteResult`,
    `toImportPreview`, `toPasteError`, `backToPasteResult`,
    `toRaceDetailAfterImport`, `back`) persists the back stack through
    `stateStore.save(...)`, in addition to publishing `current`, same
    as today otherwise
  — `current: StateFlow<PhoneDestination>` and every method's own
    behaviour (what it pushes, what `back()` pops, what
    `toRaceDetailAfterImport` clears) are unchanged

## Acceptance criteria

- A `PhoneNavigator` built against a `stateStore` whose `restore()`
  returns null starts on `current = RaceList`
- Driving one `PhoneNavigator` to `RaceDetail(raceId)` (a restorable
  destination), then building a second `PhoneNavigator` against the
  same `stateStore`, restores its `current` to that same
  `RaceDetail(raceId)`
- Driving one `PhoneNavigator` to `PasteResult` then `ImportPreview`,
  then building a second `PhoneNavigator` against the same
  `stateStore`, restores its `current` to `PasteResult`, never
  `ImportPreview`
- Driving one `PhoneNavigator` to `PasteResult` then `PasteError`, then
  building a second `PhoneNavigator` against the same `stateStore`,
  restores its `current` to `PasteResult`, never `PasteError`
- Driving one `PhoneNavigator` to `RaceDetail(raceId)` then `back()` to
  `RaceList`, then building a second `PhoneNavigator` against the same
  `stateStore`, restores its `current` to `RaceList`, not
  `RaceDetail(raceId)` — `back()` persists too, not only a push

## Dependencies

PhoneDestination — pre-existing, modified here (computed property
  only, no new field)
PhoneNavigationStateStore — produced by lot-26 (same block)

## Conventions

R46 · anything the application must find again after the process dies
  is written where it survives, as it changes, and read back from
  there
R39 · dependencies passed as arguments, never read from a top-level
  property or an object — `stateStore` is constructor-injected, not a
  singleton PhoneNavigator reaches for on its own
R63 · identifiers, comments and docs in English; one line per exported
  symbol saying what it guarantees and when it fails

## Requests

—
