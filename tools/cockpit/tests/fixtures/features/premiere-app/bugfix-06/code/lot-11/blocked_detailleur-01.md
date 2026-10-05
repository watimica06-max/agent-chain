## What blocks

Making `PayloadCodec.encode`, `decodeProfileSync` and
`decodeRecordedRace` suspend, as §6.2 states, stops four call sites
outside `:core-sync` from compiling, and the lots owning two of them are
already coded, so no lot is named to adapt them — R73 makes such a build
undeliverable.

## Where

lot-11 — `Modifies: PayloadCodec, PayloadCodecTest`. Confirmed by grep,
each call sitting in a plain non-suspend function:

- `app-phone/src/test/java/com/mgilli/hyroxtracker/connectivity/PayloadCodecCrossModuleTest.kt:33,50`
  — its subject is `PayloadCodec`, so under R86 it is this lot's own,
  in a module this lot's `Modifies` list does not name
- `app-wear/src/test/java/com/mgilli/app_wear/connectivity/PayloadCodecCrossModuleTest.kt:33,50`
  — same
- `app-phone/src/test/java/com/mgilli/hyroxtracker/sync/RecordedRaceListenerServiceTest.kt:202`
  — its subject is `RecordedRaceListenerService`, lot-31, coded and
  passed; no later lot of the sequence names this file
- `app-wear/src/test/java/com/mgilli/app_wear/sync/ProfileSyncListenerServiceTest.kt:239`
  — its subject is `ProfileSyncListenerService`, lot-16, and lot-56 also
  names the file; both are coded

This is the case `architecte/detailleur-lot-31.md`'s verdict describes
for `MainActivityTest` — a call site the split never attributed to
anyone once its owning lot closed — and it sends it back through the
split.

The two production decode call sites survive the change: both already
sit inside `serviceScope.launch`, and `:core-sync`'s two transports call
`encode` from a suspend `send`.

Second point on the same lot, entangled with the first: §9.5 asks
`toObject` to turn a mismatch into "the codec's own typed decoding
failure", and `code/decoupage.md`'s inventory calls
`PayloadDecodingFailure` "the type `PayloadCodec` returns on a decode it
cannot complete". R31 reads that as a thrown type the module declares,
which leaves the two production listener call sites compiling untouched;
R33 reads a deserialisation's failure as a returned value, which changes
the decode functions' return type and breaks those same two call sites —
`RecordedRaceListenerService.kt:49` and `ProfileSyncListenerService.kt:45`,
neither in this lot's `Modifies` list, both coded. The signature cannot
be written until that reading is settled;
`architecte/detailleur-lot-11.md` puts the conventions half of it to the
Architecte.

## To resume

Name the lot that adapts each of the four call sites — this one, under
R85 and R86, or a new one — and settle whether `PayloadCodec`'s two
decode functions keep their present return type and throw
`PayloadDecodingFailure`, or return the failure as a value with the two
listener services adapted alongside.

## Decision

Add the four test call sites to lot-11 —
`app-phone/src/test/java/com/mgilli/hyroxtracker/connectivity/PayloadCodecCrossModuleTest.kt`,
`app-wear/src/test/java/com/mgilli/app_wear/connectivity/PayloadCodecCrossModuleTest.kt`,
`app-phone/src/test/java/com/mgilli/hyroxtracker/sync/RecordedRaceListenerServiceTest.kt`
and `app-wear/src/test/java/com/mgilli/app_wear/sync/ProfileSyncListenerServiceTest.kt`
— and keep `decodeProfileSync` and `decodeRecordedRace` returning
`ProfileSyncPayload` and `RecordedRacePayload`, `toObject` throwing
`PayloadDecodingFailure` on a mismatch, with `suspend` the only change
to the three signatures.

R85 is the rule for the four: a module entered only to adapt an existing
test's direct call sites, so a signature changed in another module keeps
compiling, does not bind the lot to the rest of that module's `check` —
that is the whole of these four edits, and once they are made no call
site is left broken, so R73 has nothing to name. On the second point,
`PayloadCodec` is not a bearer of §7.2 — its bearers are
`RecordedRaceListenerService`, `ProfileSyncListenerService`,
`RaceRepositoryImpl`, `ProfileRepositoryImpl` and
`RaceRecordingRepositoryImpl` — and lot-52 delivered
`class PayloadDecodingFailure(message: String, cause: Throwable? = null) : Exception(message, cause)`
at `core-sync/src/main/kotlin/com/mgilli/core/sync/transport/PayloadDecodingFailure.kt:9`,
which `RecordedRaceListenerService.kt:53` and
`ProfileSyncListenerService.kt:49` already put into `Result.failure`
inside their own `serviceScope.launch`. R31 is what governs the codec —
the type crossing `:core-sync`'s boundary is the one `:core-sync`
declares — and R33's returned value is the `Result` those two services
already build.

This does not extend to the substance of the two listener-service tests:
under R86 their owners stay lot-31 and lot-16, so lot-11 changes nothing
in them beyond making the two event-building helpers reach a suspend
`encode`, and adds no assertion, fixture or test there. It does not touch
`RecordedRaceListenerService.kt`, `ProfileSyncListenerService.kt` or
`PayloadDecodingFailure.kt`, and under R85 it does not bind lot-11 to
`:app-phone`'s or `:app-wear`'s full `check`.

## Applied

Applied to lot-11's `fiche-executable.md`.
