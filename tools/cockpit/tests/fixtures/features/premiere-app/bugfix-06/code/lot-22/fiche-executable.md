## Signatures

PasteResultViewModel @Inject constructor(
  navigator: PhoneNavigator,
  clock: Clock,
  savedStateHandle: SavedStateHandle
) : ViewModel()
  — modification; `savedStateHandle` is the added parameter, the two
    others unchanged. Hilt supplies it to a `@HiltViewModel`; the class
    stays `@HiltViewModel` with a plain `@Inject` constructor, no
    assisted factory
  — the handle carries the three fields the user enters: the pasted
    text, the race name, the race date. It carries nothing else

PasteResultViewModel.uiState: StateFlow<PasteResultUiState>
  — type unchanged. Its value at construction:
    · `pastedText` and `raceName` — what the handle carries, `""` each
      when it carries nothing
    · `raceDate` — what the handle carries, the clock's own current
      local date otherwise
    · `maxSelectableDate` — always the clock's own current local date,
      read at construction, never taken from the handle
    · `isImportEnabled` — recomputed from the `pastedText` and
      `raceName` above, never taken from the handle
    · `lastParseResult` — always null; it is never written to the
      handle and never restored from it

PasteResultViewModel.onPastedTextChanged(text: String) → Unit
  — modification: sets `pastedText` in the state and writes it to the
    handle in the same call, and recomputes `isImportEnabled`

PasteResultViewModel.onRaceNameChanged(name: String) → Unit
  — modification: sets `raceName` in the state and writes it to the
    handle in the same call, and recomputes `isImportEnabled`

PasteResultViewModel.onRaceDateChanged(date: LocalDate) → Unit
  — modification: sets `raceDate` in the state and writes it to the
    handle in the same call

PasteResultUiState.isImportEnabled: Boolean
  — modification of the rule producing it: true when `pastedText` and
    `raceName` are both non-blank, false as soon as either is blank —
    a value of spaces alone included. Emptiness no longer decides it

PasteResultViewModel.onImportClicked() → Unit
  — modification: the whole body — the `HyresultResultParser.parse`
    call, the `lastParseResult` update and the navigation that follows
    it — runs inside `viewModelScope.launch`, so the call returns
    before any of the three happens
  — the order inside that body is unchanged: `lastParseResult` carries
    the parse outcome before `navigator.toImportPreview()` /
    `navigator.toPasteError()` is called
  — which navigation follows which outcome is unchanged: `Success` →
    `toImportPreview()`, `Failure` → `toPasteError()`
  — the constructor-time `clock.now()` read stays where it is: it
    reaches no repository, controller or manager

  ⚠ The state document's trap *"`viewModelScope` … needs a stubbed Main
  dispatcher outside Robolectric"* lists `PasteResultViewModel` among
  those touching no coroutine scope; this lot makes that false, and its
  tests need `Dispatchers.setMain` / `resetMain` from here on.

## Acceptance criteria

- A pasted text of `"a"` and a race name of `"   "` leave
  `uiState.isImportEnabled` false
- A pasted text of `"   "` and a race name of `"Race"` leave
  `uiState.isImportEnabled` false
- A pasted text of `"a"` and a race name of `"Race"` leave
  `uiState.isImportEnabled` true
- With `Dispatchers.Main` set to a dispatcher that runs nothing until
  its scheduler is advanced, `onImportClicked()` returns with
  `uiState.lastParseResult` still null and no navigation performed;
  after the scheduler runs, `lastParseResult` carries the outcome and
  the navigation has happened
- `onImportClicked()` on a paste the parser accepts navigates to
  `ImportPreview`, and `uiState.lastParseResult` is a
  `HyresultParseResult.Success` at the moment that navigation is
  observed
- `onImportClicked()` on a paste the parser rejects navigates to
  `PasteError`, and `uiState.lastParseResult` is a
  `HyresultParseResult.Failure` at the moment that navigation is
  observed
- A ViewModel built from a fresh empty `SavedStateHandle` exposes
  `pastedText` `""`, `raceName` `""`, `raceDate` equal to the clock's
  current local date, `isImportEnabled` false and `lastParseResult`
  null
- A pasted text typed on one instance, then a second instance built
  from that same `SavedStateHandle`, exposes that pasted text
- A race name typed on one instance, then a second instance built from
  that same `SavedStateHandle`, exposes that race name and
  `isImportEnabled` computed from the restored pair, not the false it
  started at
- A race date selected on one instance, then a second instance built
  from that same `SavedStateHandle`, exposes that race date
- A second instance built from a `SavedStateHandle` a first instance
  ran a successful `onImportClicked()` on exposes `lastParseResult`
  null
- A second instance built from a `SavedStateHandle` a first instance
  filled, but against a clock on a later day, exposes that later day as
  `maxSelectableDate`
- `PasteResultScreen` driven by a ViewModel whose `isImportEnabled` is
  false ignores a tap on the import action

## Dependencies

PhoneNavigator — pre-existing, modified by lot-25 (earlier in the
  sequence); `toImportPreview()` and `toPasteError()` stay non-suspend
Clock — pre-existing
HyresultResultParser.parse(pastedText: String) → HyresultParseResult —
  pre-existing, behaviour modified by lot-01 (earlier in the sequence);
  the signature is unchanged and is not suspend
HyresultParseResult, .Success, .Failure — pre-existing
PasteResultUiState — pre-existing, this lot's own
SavedStateHandle — androidx.lifecycle, framework type already used by
  ProfileViewModel, RaceDetailViewModel and ImportPreviewViewModel

## Conventions

R45 · every screen keeps what the user has in progress across a system
  rebuild — the pasted text, the name being typed, the field being
  edited
R44 · the state of a journey is held by one state holder — the import
  journey stays this ViewModel's, no screen holds another's
R42 · cooperative async on Kotlin coroutines, one UI thread per
  application
R26 · no `!!` on a value coming from outside the function — a read out
  of `SavedStateHandle` is nullable and is handled as such
R57 · each fact stated as always true has a test attempting to violate
  it — a name of 1–40 trimmed characters, blank included
R55 · every public function has at least one nominal and one failure
  test, delivered in this lot
R56 · no test reads the system clock — the clock is injected
R62 · the code's vocabulary: Paste, Import, Preview, Race — no synonym
  and no abbreviation outside it
R63 · identifiers, comments and documentation in English; one line per
  exported symbol saying what it guarantees and when it fails
R74 · a call site in the same module is this lot's own scope —
  `PasteResultScreenTest` (`:app-phone`) constructs
  `PasteResultViewModel` directly at three places and no other lot
  claims it

## Requests

—
