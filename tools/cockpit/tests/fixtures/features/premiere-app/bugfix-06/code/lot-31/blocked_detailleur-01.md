## What blocks

lot-31 changes `RaceRepository`'s method set (§2.1 — every method
`suspend`) and its two flows' element type (§7.2 — `observeAll`/
`observeReference` carrying `RaceQueryFailure`), which breaks six call
sites no lot of the split declares as modified, and R73 makes a red
build no lot is named the owner of undeliverable.

## Where

`code/decoupage.md`, lot-31's `Modifies:` line, against these call sites
confirmed by grep:

- `:core-domain` — `ProfileSyncPushService.push` reads
  `raceRepository.observeReference().first()` and
  `raceRepository.observeAll().first()` (ProfileSyncPushService.kt:33-34),
  and `ProfileSyncPushServiceTest` holds a fake `RaceRepository`
  overriding all nine methods (:69-83). Both sit in the module
  `RaceRepository` itself lives in, so R74 puts them in lot-31's own
  scope by construction — the sheet can carry them, but lot-31's
  declaration does not, and `push`'s outcome on a query failure is not
  stated anywhere.
- `:app-phone` — fake `RaceRepository` implementations in
  `ProfileViewModelTest` (:112-125), `ProfileScreenTest` (:89-102),
  `ImportPreviewViewModelTest` (:72-88) and `ImportPreviewScreenTest`
  (:60-73). Their owning lots (lot-19, lot-21) are coded and passed.
- `:app-wear` — the fake `RaceRepository` in
  `ProfileSyncListenerServiceTest` (:131-145). Its owning lot (lot-16)
  is coded and passed.

lot-56, which adapts the five collectors of the guarded flows, names
`RaceListViewModelTest`, `RaceListScreenTest`, `RaceDetailViewModelTest`,
`RaceDetailScreenTest`, `HomeViewModelTest`, `HomeScreenTest`,
`PreparationViewModelTest` and `PreparationScreenTest` — the same job on
the same two modules — but not the five files above, and no later lot of
the sequence names them either.

## To resume

Two answers are needed:

1. Which lot adapts the five `:app-phone`/`:app-wear` fake
   `RaceRepository` implementations listed above — lot-56, lot-31, or a
   new lot. Without one, R72's deferral has no owner to name and R73
   leaves lot-31 undeliverable.
2. What `ProfileSyncPushService.push` returns when
   `observeReference()`/`observeAll()` hand it a
   `Result.failure(RaceQueryFailure)` instead of a value: it already
   returns `ProfileSyncPushOutcome.Failure` for a refused permission, a
   failed delivery and a failed `markSyncSuccess`, but §7.2 does not
   name `push` and no entry says whether a push must be attempted
   without the reference race or refused.

## Decision

Carry six of the seven call sites in lot-31's own sheet —
`ProfileSyncPushService` and `ProfileSyncPushServiceTest`
(`:core-domain`), and `ProfileViewModelTest`, `ProfileScreenTest`,
`ImportPreviewViewModelTest`, `ImportPreviewScreenTest`
(`:app-phone`) — defer `ProfileSyncListenerServiceTest` (`:app-wear`)
to lot-56 and name it, with lot-56, in lot-31's report under R73; and
have `push` return `ProfileSyncPushOutcome.Failure` without calling
`transport.send` when `observeReference()` or `observeAll()` emits a
`RaceQueryFailure`.

R74 puts the two `:core-domain` sites in lot-31's scope by
construction. The four `:app-phone` fakes get no deferral either:
lot-31 touches `:app-phone` through `RecordedRaceListenerService`, so
R72 requires `:app-phone:check` to exit 0, and those fakes compile in
the same test source set as `RecordedRaceListenerServiceTest`. lot-31
touches no `:app-wear` source, so R72's deferral does hold for the
fifth fake, and lot-56 — immediately after lot-31 in block-15
(`code/sequence.md`) — already adapts the `:app-wear` collectors of
these same two flows. `push`'s outcome rests on R75: a source failure
never takes the interface's ordinary success shape, and sending a
payload whose reference is absent and whose history is empty is that
substitution; R34's "acts on it" is met by propagating, the way `push`
already returns `Failure` at its three other failure points
(ProfileSyncPushService.kt:30, 39, 41) and `applyIncoming` at each of
its own (:63-73).

This does not extend beyond adapting those six files to the changed
method set, the changed flow element type and, for `push`, the outcome
above: the ViewModels and screens they exercise are not otherwise
touched, and the eight `:app-phone`/`:app-wear` test files lot-56
already names stay lot-56's. No new `ProfileSyncPushOutcome` variant
and no new text key — R80 leaves to §10 whether the user is told, and
`ProfileViewModel` and `ImportPreviewViewModel` keep the handling of
`Failure` they have.

## Applied

Applied on 2026-09-06 in `code/lot-31/fiche-executable.md`, and in
lot-56's sheet and `code/decoupage.md`'s lot-56 entry for the deferred
`ProfileSyncListenerServiceTest`. One file of the same kind the
enumeration does not name — `MainActivityTest` (`:app-phone`), calling
`raceRepository.saveImportedRace` from three non-suspend test bodies —
was carried into lot-31's sheet under the decision's own `:app-phone`
test-source-set rule, and raised as
`architecte/detailleur-lot-31.md`.
