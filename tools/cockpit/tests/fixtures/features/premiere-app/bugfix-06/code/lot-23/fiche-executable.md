## Signatures

PasteErrorViewModel @AssistedInject constructor(
  @Assisted failure: HyresultParseResult.Failure,
  navigator: PhoneNavigator,
  savedStateHandle: SavedStateHandle
) : ViewModel()
  — modification; `savedStateHandle` is the added parameter, an
    ordinary one and never `@Assisted`. The two others are unchanged,
    `Factory.create(failure: HyresultParseResult.Failure)` is
    unchanged, and the class stays
    `@HiltViewModel(assistedFactory = PasteErrorViewModel.Factory::class)`
    — the state document's trap on that annotation still applies
  — `HyresultParseResult.Failure` cannot cross the handle as a value;
    what crosses is the four primitives it is built from — its
    `rowNumber`, its `cause`, its `rawRow` and its `label`
  — at construction, the handle carrying none of them is written the
    four the `@Assisted` failure carries; the handle already carrying
    them is left as it is

PasteErrorViewModel.uiState: StateFlow<PasteErrorUiState>
  — type unchanged, `PasteErrorUiState` unchanged (`title`, `body`,
    `rawRow`, `expectedRow`)
  — its value is built from the four values the handle carries when it
    carries them, and from the `@Assisted` failure otherwise. The two
    agree on every construction that writes the handle, so the
    mapping from a cause to its title and body, and the rule tying
    `expectedRow` to a non-null `rawRow`, are both unchanged

PasteErrorViewModel.onBackToPasteClicked() → Unit
  — unchanged, including on an instance built from a restored handle:
    it calls `navigator.backToPasteResult()` and nothing else

## Acceptance criteria

- A ViewModel built with a failure whose cause is `EMPTY_PASTE` and a
  fresh empty `SavedStateHandle` exposes the empty-paste title and
  body, `rawRow` null and `expectedRow` null
- A ViewModel built with a failure whose cause is `UNKNOWN_LABEL`, a
  row number, a raw row and a label, and a fresh empty
  `SavedStateHandle`, exposes the unknown-label title carrying that row
  number, the body carrying that label, that raw row and a non-null
  `expectedRow`
- After that same construction, the `SavedStateHandle` carries the
  failure's row number, its cause, its raw row and its label
- A second ViewModel built from that same `SavedStateHandle`, and given
  a `@Assisted` failure of a different cause and a different row
  number, exposes the saved failure's title, body and raw row — never
  the ones its `@Assisted` failure carries
- A second ViewModel built from a `SavedStateHandle` a first instance
  wrote a `rawRow`-less failure into exposes `rawRow` null and
  `expectedRow` null
- `onBackToPasteClicked()` on a ViewModel built from a restored
  `SavedStateHandle` navigates back to the paste screen

## Dependencies

HyresultParseResult.Failure(rowNumber: Int, cause:
  HyresultParseFailureCause, rawRow: String?, label: String?) —
  pre-existing, its shape modified by no lot of this cycle; lot-01
  (earlier in the sequence) changes only what `parse` puts in it
HyresultParseFailureCause — pre-existing, eight constants
PhoneNavigator — pre-existing, modified by lot-25 (earlier in the
  sequence); `backToPasteResult()` stays non-suspend
PhoneStringResources.PasteError — pre-existing
PasteErrorUiState — pre-existing, this lot's own, unchanged
SavedStateHandle — androidx.lifecycle, framework type already used by
  ProfileViewModel, RaceDetailViewModel and ImportPreviewViewModel

## Conventions

R45 · every screen keeps what the user has in progress across a system
  rebuild — what they have opened and not yet left
R44 · the state of a journey is held by one state holder — this
  ViewModel holds the error screen's state and no other screen's
R26 · no `!!` on a value coming from outside the function — a read out
  of `SavedStateHandle` is nullable and is handled as such
R64 · no user-facing string is a literal in the code: a key and a
  resource table — the titles and bodies stay `PhoneStringResources`
  references
R55 · every public function has at least one nominal and one failure
  test, delivered in this lot
R62 · the code's vocabulary: Paste, Import, Race — no synonym and no
  abbreviation outside it
R63 · identifiers, comments and documentation in English; one line per
  exported symbol saying what it guarantees and when it fails

## Requests

—
