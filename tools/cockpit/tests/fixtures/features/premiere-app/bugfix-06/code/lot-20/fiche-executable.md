## Signatures

### SegmentRowUiState — modification (`:app-phone`)

After the change:

    data class SegmentRowUiState(
      name: LabelRef,
      duration: String?,
      cumulative: String?,
      delta: String?,
      deltaTone: DeltaTone?
    )

What changes:

- `index` is dropped, and the write populating it in
  `RaceDetailViewModel.buildRow` goes with it (§9.1). No screen reads it and
  `RaceDetailCycles`' `LazyColumn` keys on `CycleGroupUiState.cycleNumber`,
  not on it.

What each field is worth, after the change:

- `duration`, `cumulative` — never null; the missing-value glyph carries
  absence, never `"0:00"` and never an empty string (§3.4, §9.3, R20). The
  glyph is shown whenever the value cannot be computed:
  - the race carries no segment of that index at all (§9.3);
  - that segment's own `durationMs` is null;
  - `cumulativeDurationMs(race.segments, index)` returns null, or
    `cumulativeDurationMs(race.segments, index - 1)` returns null for an
    index above 1 — an earlier index absent, or carrying a null duration
    (§3.4). Both feed `DurationTruncationService.segmentDisplayedSeconds`,
    so neither can be replaced by a `0L` fallback (R29, R20).
  Index 1's previous cumulative is `0L` by definition, not a fallback.
- `delta` — non-null exactly when the row's own `durationMs` is non-null
  **and** the reference race carries a segment of the same `Segment.index`
  with a non-null `durationMs`; null on every other row, and the screen
  renders nothing in its place. Its value is
  `DisplayFormatter.formatDelta(DurationTruncationService.truncateToSeconds(durationMs - referenceDurationMs))`
  — the per-segment term of `CumulativeDeltaEstimator.finalDelta`, the
  calculation §9.10 asks the column to name, matched on `Segment.index`
  over every `SegmentType` with no `RUN` restriction. A missing reference
  duration never falls back to `0L` the way `finalDelta`'s own sum does
  (R20); the row shows nothing instead.
  ⚠️ `finalDelta` itself is never called from this file — it is a
  whole-race sum and carries no per-row signature.
- `deltaTone` — null exactly when `delta` is null; `AHEAD` when the
  truncated difference is negative, `BEHIND` when positive, `ZERO` when 0.

`DeltaTone` and `CycleGroupUiState` are unchanged.

### RaceDetailUiState — modification (`:app-phone`)

After the change:

    data class RaceDetailUiState(
      name: String,
      date: String,
      total: String,
      isReference: Boolean,
      isSetReferenceVisible: Boolean,
      isDeltaColumnVisible: Boolean,
      cycles: List<CycleGroupUiState>,
      renameFieldValue: String?,
      renameRejectionMessage: LabelRef?,
      isDeleteConfirmVisible: Boolean,
      deleteRejectionMessage: LabelRef?,
      isDeleteReferenceNoticeVisible: Boolean
    )

What changes:

- `raceId` is dropped, and both writes populating it in
  `RaceDetailViewModel.toUiState` go with it (§9.1). No screen reads it;
  the identity the ViewModel works on is its own `@Assisted raceId`.
- `renameRejectionMessage` is added (§9.4, §10.1) — non-null only after
  `RaceRepository.rename` has returned a failure for the value currently in
  `renameFieldValue`; null on a fresh state, null while the dialog is
  closed, and null again as soon as a rename succeeds or the dialog is
  cancelled. Its only value is `PhoneStringResources.Rename.rejected`,
  whose text names the one-to-forty trimmed-character bound.
- `deleteRejectionMessage` is added (§9.4) — non-null only after
  `RaceRepository.delete` has returned a failure; null on a fresh state,
  null while the confirmation is closed, and null again as soon as the
  confirmation is cancelled. Its only value is
  `PhoneStringResources.DeleteConfirm.rejected`.
- `isDeltaColumnVisible` keeps its present meaning — a reference race
  exists and is not the race being viewed (`blocked_detailleur-01.md`'s
  settled decision). The column is hidden on nothing else.

### RaceDetailViewModel — modification (`:app-phone`)

After the change:

    @HiltViewModel(assistedFactory = RaceDetailViewModel.Factory::class)
    class RaceDetailViewModel @AssistedInject constructor(
      @Assisted raceId: Long,
      raceRepository: RaceRepository,
      navigator: PhoneNavigator,
      profileSyncPushService: ProfileSyncPushService,
      clock: Clock,
      savedStateHandle: SavedStateHandle
    ) : ViewModel()

      @AssistedFactory
      interface Factory { fun create(raceId: Long): RaceDetailViewModel }
        — unchanged; `PhoneApp`'s `hiltViewModel<..., Factory>(key = …)`
          call site is unchanged, the three added parameters being supplied
          by Hilt

    val uiState: StateFlow<RaceDetailUiState>
      — never null. Its first value carries the empty name, date and total,
        no cycles, `isDeltaColumnVisible = false`, and the dialog state the
        `SavedStateHandle` holds — no repository read has happened yet.
      — carries the race as soon as `observeAll()`/`observeReference()`
        first emit.
      — keeps the last race it saw when `observeAll()` stops carrying
        `raceId` (the delete case), so the screen does not blank before the
        navigator leaves it.

    fun onSetAsReferenceClicked()
    fun onRenameClicked()
    fun onRenameTextChanged(text: String)
    fun onRenameCancelled()
    fun onRenameConfirmed()
    fun onDeleteClicked()
    fun onDeleteCancelled()
    fun onDeleteConfirmed()
      — the eight signatures are unchanged, `Unit` included.
      — the three that write (`onSetAsReferenceClicked`, `onRenameConfirmed`,
        `onDeleteConfirmed`) each return before their write completes: the
        write, the push and everything that follows run inside
        `viewModelScope.launch`, so `uiState` carries the outcome only once
        that coroutine ends (§7.1).

What changes:

1. Three constructor parameters are appended, in that order (§6.10, §12.2).
   `ProfileSyncPushService` and `Clock` are already provided app-wide —
   `SyncModule.provideProfileSyncPushService` and the `Clock` binding
   `ProfileViewModel` already injects. `SavedStateHandle` needs no
   `@Assisted`.

2. The constructor-time `raceRepository.findById(raceId)` no longer runs in
   a property initialiser (§7.1). It runs inside `viewModelScope.launch`,
   or is dropped in favour of the `observeAll()` collection that already
   carries the same race — either way, constructing the ViewModel performs
   no repository read before the constructor returns, and the last-known-race
   fallback described under `uiState` still holds.

3. The three write handlers each move their `raceRepository` call inside
   `viewModelScope.launch`, read the `Result` it returns and act on it
   (§7.1, §9.4, R34):
   - `onSetAsReferenceClicked` — on success, pushes; on failure, pushes
     nothing and changes no `uiState` field. No text resource names this
     refusal and §9.4 does not list this call site among its seven; see
     `## Requests`.
   - `onRenameConfirmed` — on success, closes the dialog
     (`renameFieldValue = null`), clears `renameRejectionMessage` and
     pushes; on failure, keeps the dialog open with the value the user
     typed, sets `renameRejectionMessage` and pushes nothing (§10.1).
   - `onDeleteConfirmed` — on success, pushes, then calls
     `navigator.back()`; on failure, keeps the confirmation open, sets
     `deleteRejectionMessage`, pushes nothing and does not navigate.
     🔴 The push is awaited *before* `navigator.back()`: leaving the
     destination clears this ViewModel and cancels `viewModelScope`, and a
     push started after that never completes (R25).

4. Each push is `profileSyncPushService.push(permissionGranted = true, at =
   clock.now())`, the shape `ProfileViewModel.pushProfile` already uses
   (§6.10). Its `ProfileSyncPushOutcome` is read, and neither outcome
   changes any `uiState` field: this screen carries no sync state, §6.10
   adds none, and no text catalogue key names a failed push here (R64).
   See `## Requests`.

5. What the `SavedStateHandle` holds, and what it does not (§12.2):
   - held — `renameFieldValue` (`String?`, the dialog open and its typed
     content), `isDeleteConfirmVisible` (`Boolean`), and one `Boolean` per
     rejection site, rename and delete. Both `LabelRef` values are
     constants with no args, so each is derived back from its `Boolean` on
     read and never stored: `LabelRef` is not Bundle-storable, and §12.2's
     second gap settles that the primitives a value is built from are what
     gets saved.
   - not held — the race itself, re-read from `observeAll()`; `raceId`,
     re-supplied by `PhoneApp` from the destination `PhoneNavigator`
     persists (§12.3, lot-25).

6. `buildRow` looks its segment up without assuming it is present (§9.3)
   and without falling a null cumulative back to `0L` (§3.4); what each
   case renders is stated under `SegmentRowUiState` above.

### RaceDetailScreen — modification (`:app-phone`)

    @Composable fun RaceDetailScreen(viewModel: RaceDetailViewModel)
      — signature unchanged

What changes:

- The header title rendering `uiState.name` sets `maxLines = 1` and
  `TextOverflow.Ellipsis` (§9.8) — a title on its own row, one line.
- The delete confirmation's title, built from the name through
  `PhoneStringResources.DeleteConfirm.title(uiState.name)`, sets
  `maxLines = 2` and `TextOverflow.Ellipsis` (§9.8) — a full sentence
  carrying the name.
- The rename dialog renders `uiState.renameRejectionMessage` when non-null
  and nothing in its place when null; the dialog stays open on a refusal
  because `renameFieldValue` stays non-null (§9.4, §10.1).
- The delete confirmation renders `uiState.deleteRejectionMessage` the same
  way (§9.4).
- Both new messages resolve through `stringResource(id)` — each `LabelRef`
  carries no args.

### RaceDetailViewModelTest — modification, RaceDetailScreenTest — production (`:app-phone`)

- No `RaceDetailScreenTest` exists at HEAD; `decoupage.md` lists it under
  `Modifies`. It is created here, on the terms `MainActivityTest` already
  uses in this module.
- `RaceDetailViewModel` is named in the state document's trap on
  `Dispatchers.Main`: both tests install
  `Dispatchers.setMain(UnconfinedTestDispatcher())` in `@Before` and
  `Dispatchers.resetMain()` in `@After`.
- `RaceDetailCycles` is a plain `LazyColumn`: the state document's trap says
  an item past the initial composition window is absent from the semantics
  tree entirely. A criterion bearing on a row beyond the first few needs
  `onNode(hasScrollToIndexAction()).performScrollToIndex(n)` first.
- `FakeRaceRepository` gains a settable `Result` for `rename` and
  `setAsReference`, as it already carries one for `delete`.

## Acceptance criteria

A missing or duplicate cumulative total (§3.4)

- A race whose segment 3 carries a null duration: row 3 and row 5 each show
  the missing-value glyph for cumulative, never `0:00`.
- That same race: row 5 shows the glyph for duration too, even though its
  own duration is present.
- A race whose segments all carry a duration: row 5 shows the sum of
  durations 1 to 5, truncated to the second, as its cumulative.

Pushing after a write (§6.10)

- A rename the repository accepts: `ProfileSyncPushService.push` is called
  once, with `permissionGranted = true` and the instant `Clock.now()`
  returns.
- A rename the repository refuses: `push` is never called.
- Set-as-reference the repository accepts: `push` is called once; refused:
  never called.
- A delete the repository accepts: `push` returns before
  `PhoneNavigator.current` leaves the race detail destination.
- A delete the repository refuses: `push` is never called and
  `PhoneNavigator.current` still carries the race detail destination.
- A push returning `ProfileSyncPushOutcome.Failure` after an accepted
  rename: the screen shows the renamed race and no additional message.

Repository calls from a coroutine (§7.1)

- Constructing `RaceDetailViewModel` calls no method of `RaceRepository`
  before the constructor returns.
- With the repository's `rename` suspended and not yet completed,
  `onRenameConfirmed` has returned and the rename dialog still shows the
  typed value with no rejection message.
- With the repository's `delete` suspended and not yet completed,
  `onDeleteConfirmed` has returned and `PhoneNavigator.current` still
  carries the race detail destination.

Dead UI-state fields (§9.1)

- `RaceDetailUiState` exposes no `raceId` member.
- `SegmentRowUiState` exposes no `index` member.
- The screen still shows the race the navigator's destination names, and
  each row still shows its own segment's name.

An incomplete race (§9.3)

- A race storing only segments 1 to 12: opening its detail screen renders
  the 8 cycle groups and all 30 rows without raising.
- That same race: row 20 shows the glyph for duration and for cumulative,
  and no delta value.
- That same race: row 7 shows its own duration and cumulative.

A dropped `Result` (§9.4)

- A rename the repository refuses: the rename dialog stays open, still
  carries the value the user typed, and shows the rename rejection text.
- A rename the repository accepts: the rename dialog closes, no rejection
  text is shown, and the title shows the new name.
- A rename refused, then the dialog cancelled and reopened: no rejection
  text is shown.
- A delete the repository refuses: the delete confirmation stays open and
  shows the delete rejection text.
- A delete the repository accepts: `PhoneNavigator.current` leaves the race
  detail destination.
- Set-as-reference refused by the repository: the screen shows no rejection
  text and still shows the race as not being the reference.

Bounded text (§9.8)

- A race named with 40 characters: the header title renders at the same
  height as the same screen showing a race named with 3 characters.
- That same race, delete confirmation open: its title renders at no more
  than twice the height of the same confirmation for a race named with 3
  characters.

The delta column (§9.10, `blocked_detailleur-01.md`)

- A reference race set, different from the one viewed, both carrying a
  duration at index 4, the viewed race 10 s faster: row 4 shows `-0:10`
  with the AHEAD tone.
- Same setup, the viewed race 10 s slower: row 4 shows `+0:10` with the
  BEHIND tone. Equal durations: `0:00` with the ZERO tone.
- Same setup at a `STATION` index and at a `ROXZONE_OUT` index: both rows
  show their difference, on the same rule as the `RUN` row.
- The reference race carrying no segment at index 9, or one whose duration
  is null: row 9 shows no delta value and no tone — never `0:00`.
- No reference race stored: the delta column is not rendered on any row.
- The race being viewed being itself the reference: the delta column is not
  rendered.

A bound violation's message (§10.1)

- `RaceRepository.rename` refusing a name of 41 trimmed characters: the
  dialog shows the text naming the one-to-forty bound.
- `RaceRepository.rename` refusing a name of spaces only: the dialog shows
  that same text and stays open.

ViewModel state across a rebuild (§12.2)

- The rename dialog open on a typed but unconfirmed value, then a
  `RaceDetailViewModel` rebuilt from the same `SavedStateHandle`: the
  dialog is open and carries that value.
- A rename rejection shown, then a rebuild from the same
  `SavedStateHandle`: the rejection text is shown again.
- The delete confirmation open, then a rebuild from the same
  `SavedStateHandle`: the confirmation is open.
- A fresh `SavedStateHandle` carrying nothing: neither dialog is open and
  no rejection text is shown.

## Dependencies

RaceRepository (`setAsReference`, `rename`, `delete`, `findById`,
  `observeAll`, `observeReference`) — pre-existing (`:core-domain`), already
  injected; not `suspend` at HEAD. ⚠️ lot-31 makes its methods `suspend`
  later in the sequence; wrapping these call sites in
  `viewModelScope.launch` compiles against either shape, and `decoupage.md`
  makes lot-20 a prerequisite of lot-31 for exactly that reason.
cumulativeDurationMs(segments, throughIndex): Long? — lot-02, already
  returning null on an absent index
CumulativeDeltaEstimator.finalDelta(raceSegments, referenceSegments): Long?
  — lot-03; named as the calculation backing the delta column, never called
  from this lot
DisplayFormatter.formatDelta / formatDurationSegment / formatDurationElapsed
  / formatDurationTotal / formatDate — pre-existing, `formatDurationTotal`
  corrected by lot-07
DurationTruncationService.truncateToSeconds / segmentDisplayedSeconds —
  pre-existing
PhoneStringResources.Rename.rejected, PhoneStringResources.DeleteConfirm.rejected
  — lot-17
ProfileSyncPushService.push(permissionGranted: Boolean, at: Instant):
  ProfileSyncPushOutcome — lot-16; provided app-wide by
  `SyncModule.provideProfileSyncPushService` (`:app-phone`)
Clock.now(): Instant — pre-existing (`:core-domain`), already injected into
  `ProfileViewModel` on this module's graph
PhoneNavigator.back(): Boolean — pre-existing, reshaped by lot-25; not
  `suspend`
LabelRef, Segment, Race, RaceCompletion, DeltaTone, CycleGroupUiState —
  pre-existing
SavedStateHandle — `androidx.lifecycle.SavedStateHandle`, framework;
  `decoupage.md` declares it pre-existing and lot-19 already injects it into
  a `@HiltViewModel`. ⚠️ No `lifecycle-viewmodel-savedstate` entry exists in
  `gradle/libs.versions.toml`; it is reachable as a transitive of
  `androidx.hilt.navigation.compose` — R77/R78 apply, and lot-19's report
  already names it. ⚠️ This is the first `@HiltViewModel(assistedFactory =
  …)` class in the project to take one alongside an `@Assisted` parameter;
  the state document's trap on `@HiltViewModel` + `@AssistedInject` bears on
  it.
TextOverflow, maxLines — Jetpack Compose; not project symbols, and no
  `Text` in this repository sets either one today

## Conventions

§2 · R4 — `./gradlew check` exits 0, the one definition of done
§2 · R74 — a same-module call site is this lot's own scope, never deferred
§4 · R12 — §9.x and §10.x on the phone are realised in `:app-phone`
§5 · R17 — no bare primitive carrying a unit or an identity in a public
  signature; the signatures above are what this lot delivers
§5 · R18 — data crossing a public boundary is immutable
§5 · R19, R24 — what blocks or reaches outside the process is `suspend`
§5 · R20 — missing data crosses as a nullable or a declared absence type; a
  fallback is never zero
§5 · R22 — what computes states what it returns for every input it cannot
  compute on
§5 · R25 — what a signature promises, the body delivers
§5 · R26 — no `!!` on a value coming from outside the function
§5 · R29 — a duration is carried in milliseconds and truncated only at
  display; a displayed segment duration is the difference of two truncated
  cumulative totals
§6 · R34 — a caller receiving a failure acts on it
§7 · R39 — dependencies passed as arguments, no mutable global state
§7 · R42 — cooperative async on Kotlin coroutines
§7 · R44 — one state holder per journey
§7 · R45 — a screen keeps what the user has in progress across a system
  rebuild
§7 · R46 — what must be found again after a process death is written where
  it survives
§7 · R47 — a screen reads a source once per entry, never in a composition
  body
§10 · R55 — one nominal and one failure test per public function
§10 · R56 — no test reaches I/O or the system clock; time is injected
§10 · R57 — the one-to-forty trimmed-character name bound has a test
  attempting to violate it
§11 · R62 — the lexicon: Race, Segment, Cycle, Reference, Delta,
  Cumulative, Duration, Total, Push, Sync
§11 · R63 — English identifiers, French only in the resource files, one doc
  line per exported symbol
§11 · R64 — no user-facing string is a literal in the code
§12 · R66, R77, R78 — no new dependency inside a lot; an artifact no build
  file declares is named in the report

## Requests

architecte/detailleur-lot-20.md
