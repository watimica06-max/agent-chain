Settled and applied — `code/lot-19/fiche-executable.md` is written against
the `## Decision` below, not against §5.2 as the entry states it.

## What blocks

§5.2 asks `ProfileViewModel`/`ProfileUiState` for a state distinct from
"permission not yet granted" meaning "heart-rate history unavailable",
but nothing lot-19 consumes can tell the two apart, and the text
`ProfileScreen` must render it as has no resource key in any symbol
lot-19 may modify.

## Where

Lot lot-19 (`code/decoupage.md`), anchor §5.2 — "The phone crashes at
launch on a device without Health Connect", second gap.

Confirmed by grep:

- `core-domain/.../health/HrPermissionSystem.kt` — `suspend fun
  isGranted(): Boolean` and `suspend fun requestPermission(): Boolean`,
  nothing else.
- `app-phone/.../health/permission/ActivityBoundHrPermissionHost.kt`
  lines 33-35 — `delegate?.isGranted() ?: false` and
  `delegate?.requestPermission() ?: false`. lot-28 makes `MainActivity`
  skip `bind(...)` when the client is absent, so an absent Health
  Connect and a user refusal both surface as `false`.
- `core-domain/.../health/HrHistoryReader.kt` — `suspend fun
  bpmValuesOverLast12Months(): List<Int>`;
  `app-phone/.../health/HrHistoryReaderImpl.kt` lines 20-24 already
  report any failed read "as if no history existed", so an empty list
  cannot carry unavailability either.
- No `getSdkStatus`, availability type or `Unavailable` state exists in
  `core-domain/src/main` or `app-phone/src/main` outside
  `Profile.syncUnavailable`, which is §9.18's connectivity refusal.
- lot-28, which owns the absent-client wiring, runs in block-15 —
  after lot-19 — and its own `Needs` line names `ProfileUiState
  (lot-19)`.
- `app-phone/.../ui/text/PhoneStringResources.kt` carries no key for
  "heart-rate history unavailable"; lot-17's report lists the four keys
  it created and none is that one. lot-19's `Modifies` line does not
  include `PhoneStringResources`, and R64 forbids the literal.

## To resume

Two points, both outside this agent's authority:

1. Which symbol carries the unavailability signal into
   `ProfileViewModel`, and which lot declares that modification —
   `HrPermissionSystem` and `HrHistoryReader` both live in
   `:core-domain` and no lot of `decoupage.md` modifies either.
2. Which lot adds the `PhoneStringResources` key `ProfileScreen`
   renders for that state — lot-17 is already coded and lot-19 does not
   declare `PhoneStringResources` among the symbols it modifies.

⚠️ The five other anchors of lot-19 (§7.1, §9.1, §12.2, §12.4, and
§9.9 — whose `ProfileViewModel` half lot-17 already carried) are
derivable as they stand; only the §5.2 half blocks.

## Decision

Carry the signal on a new `:app-phone` symbol that lot-19 declares itself —
one that reads `HealthConnectClient.getSdkStatus`, injected into
`ProfileViewModel` — and add the `PhoneStringResources.Profile` key
`ProfileScreen` renders for that state, with its French text, in lot-19 as
well; name both additions in lot-19's report as scope its `Modifies` line
does not list.

R12 realises §5.2 in `:app-phone` alone, so neither `HrPermissionSystem` nor
`HrHistoryReader` in `:core-domain` gains anything and no lot needs to
modify either; R13 confines the Health Connect client to that same module,
where `getSdkStatus` — the check §5.2 already names as the one thing that
tells an absent provider from a refused permission — is reachable from a
`Context` without `PlatformModule`. R74 settles the lot: the carrier, the
key and `ProfileViewModel` all live in `:app-phone`, which Kotlin compiles
in one pass, so `./gradlew :app-phone:check` cannot exit 0 while lot-19
references a symbol a later lot would add — the definition is lot-19's own
scope by construction, and the split's silence is corrected here rather
than deferred to lot-28. The key half is solved the same way one block
earlier: `code/lot-17/fiche-executable.md` adds `Profile.lastSyncFuture`
and its resource text, and takes on `ProfileViewModel.syncStatusText`
though `decoupage.md` listed `PhoneStringResources` alone, recording the
divergence in the sheet. R64 keeps the text out of the code.

This does not extend to §5.2's other bearers: `PlatformModule`,
`MainActivity (:app-phone)`, `ActivityBoundHrPermissionHost`,
`HrPermissionSystemImpl` and `HrHistoryReaderImpl` stay lot-28's, and
lot-19 makes the injected client neither optional nor conditional. Nor does
it extend to any other `PhoneStringResources` key, nor to the five other
anchors of lot-19, which stand as they are.

## How it was applied

- `HealthHistoryAvailability` — new `:app-phone` class, `@Inject
  constructor(@ApplicationContext context: Context)`, `open suspend fun
  isAvailable(): Boolean` reading `HealthConnectClient.getSdkStatus`.
  Injected into `ProfileViewModel` as its eighth constructor parameter.
- `PhoneStringResources.Profile.hrHistoryUnavailable` and
  `R.string.profile_hr_history_unavailable` — added by lot-19.
- `ProfileUiState.isHealthHistoryUnavailable` — added, false while the
  answer is pending and false when the provider is present but the
  permission is not granted, which is what makes it distinct.
- `PlatformModule`, `MainActivity`, `ActivityBoundHrPermissionHost`,
  `HrPermissionSystemImpl`, `HrHistoryReaderImpl` — untouched, lot-28's.
