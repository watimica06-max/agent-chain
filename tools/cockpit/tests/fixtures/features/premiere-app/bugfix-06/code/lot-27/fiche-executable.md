## Signatures

🔴 Written against `code/lot-27/blocked_detailleur-01.md`'s `## Decision`,
not against §9.5's silence on what the guarded branches show.

PhoneApp(navigator: PhoneNavigator)
  — `@Composable` in `MainActivity.kt` (`:app-phone`), parameter list and
    return unchanged. Its three casts stop throwing:

    1. the host context — a checked conversion to `ComponentActivity`
       yielding an absent host instead of raising. `BackHandler` keeps
       calling `navigator.back()` first; when that returns false and the
       host is absent, nothing is finished and nothing is raised. With a
       `ComponentActivity` host the gesture still finishes it, unchanged.

    2. `PhoneDestination.ImportPreview` — renders `ImportPreviewScreen`
       only when `PasteResultViewModel.uiState.value.lastParseResult` is a
       `HyresultParseResult.Success`, with the same `raceName`/`raceDate`
       snapshot it reads today. On any other value — null after a rebuild,
       or a `Failure` — it renders nothing, builds no
       `ImportPreviewViewModel`, and calls
       `PhoneNavigator.backToPasteResult()` from a side effect entered
       with the branch, once per entry into the branch and never from the
       composition body.

    3. `PhoneDestination.PasteError` — the same, mirrored: renders
       `PasteErrorScreen` only for a `HyresultParseResult.Failure`; on any
       other value it renders nothing, builds no `PasteErrorViewModel`, and
       calls `PhoneNavigator.backToPasteResult()` the same way.

    The `RaceList`, `RaceDetail`, `Profile` and `PasteResult` branches are
    unchanged, `key = current.raceId.toString()` included. Whether
    `PhoneApp` stays private is the Réalisateur's call, bounded by the
    guarded-host criterion below having to be observable from
    `MainActivityTest`; its contract is the one above either way.

MainActivity.onCreate / onDestroy — unchanged. No new injected field, no
  new binding, no manifest change.

MainActivityTest (`:app-phone`) — this lot's own scope, `Modifies` names
  it. Two things: the guarded behaviours above, and the stale fixture
  lot-21 and lot-22 deferred here under R72 — its 30-row
  `VALID_HYRESULT_PASTE` constant is written on the label vocabulary
  `HyresultResultParser` expected before lot-01, so it now parses to
  `Failure(UNKNOWN_LABEL, …)` and the import-preview test fails. The
  fixture becomes a paste the current parser accepts, on the vocabulary
  `core-domain/src/test/resources/hyresult/valid_result_no_header.txt`
  carries.

## Acceptance criteria

- Pasting a well-formed Hyresult export, naming the race and tapping
  import renders the import preview showing that paste's total time and
  its 30 segments
- Reaching the import-preview destination while `lastParseResult` is null
  renders no import preview and leaves the phone on the paste screen, its
  pasted text and name still shown
- Reaching the import-preview destination while `lastParseResult` is a
  `HyresultParseResult.Failure` renders no import preview and leaves the
  phone on the paste screen
- Pasting text the parser refuses and tapping import renders the paste
  error screen for that failure
- Reaching the paste-error destination while `lastParseResult` is null
  renders no paste error screen and leaves the phone on the paste screen
- Reaching the paste-error destination while `lastParseResult` is a
  `HyresultParseResult.Success` renders no paste error screen and leaves
  the phone on the paste screen
- No branch of `PhoneApp` raises while reaching any of the six
  destinations, whatever `lastParseResult` carries
- The back gesture on the race list, with nothing beneath it on the back
  stack, finishes the hosting activity
- The back gesture with a composition host that is not a
  `ComponentActivity` finishes nothing and raises nothing

## Dependencies

PhoneNavigator — pre-existing, modified this cycle by lot-25.
  `current: StateFlow<PhoneDestination>`; `back(): Boolean` false when the
  stack holds one entry; `backToPasteResult()` pops until the top is
  `PhoneDestination.PasteResult` or one entry is left, then publishes.
  Reused as it stands, never redeclared — no signature change here
PhoneDestination, PhoneDestination.isRestorable — pre-existing,
  `isRestorable` created this cycle by lot-25. Untouched
HyresultParseResult — pre-existing `:core-domain` sealed interface,
  `Success(totalTimeMs, segmentDurationsMs)` and
  `Failure(rowNumber, cause, rawRow, …)`
PasteResultViewModel, PasteResultUiState — pre-existing, modified this
  cycle by lot-22. `uiState.value.lastParseResult: HyresultParseResult?`
  is null on every rebuild of the ViewModel, by lot-22's own contract
ImportPreviewViewModel(.Factory), ImportPreviewScreen — pre-existing,
  modified this cycle by lot-21. Untouched
PasteErrorViewModel(.Factory), PasteErrorScreen — pre-existing, modified
  this cycle by lot-23. Untouched
HyresultResultParser — pre-existing, modified this cycle by lot-01; its
  post-lot-01 label vocabulary is what the test fixture must match
ComponentActivity, BackHandler, LocalContext — androidx.activity /
  Jetpack Compose, R65

## Conventions

R4 · `./gradlew check` exits 0
R12 · the phone's screens are realised in `:app-phone`
R20 · missing data crosses as a nullable or a declared absence, never an
  invented default
R26 · nothing outside the function is force-unwrapped; what can be missing
  is declared and handled
R34 · a caller that receives a failure acts on it
R47 · a screen reads a source once per entry, never in a composition body
R53 · `android.util.Log`, ERROR for what needs a human
R54 · no data attached to a person in a log message — a race name, a race
  date, a pasted row
R55 · one nominal and one failure test per public function, same lot
R56 · no test reaching the network, the file system, the data layer or the
  system clock
R62 · the lexicon — Paste, Import, Preview
R63 · English identifiers and comments; one guarantee line per exported
  symbol
R64 · no user-facing string literal in the code
R71 · Compose only, no XML layout
R72 · the deferral lot-21 and lot-22 named this lot the owner of
R79 · a failure neither carried into a state the caller owns nor
  propagated is logged at ERROR
R80 · no failure reported through a catalogue key written for another one

## Requests

—
