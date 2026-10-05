## What I need

What a screen-level caller does with a failure no text catalogue key
names and no entry gives a destination to — specifically:

- `ProfileSyncPushService.push` returning `ProfileSyncPushOutcome.Failure`
  from a handler on a screen carrying no sync state;
- `RaceRepository.setAsReference` returning a failed `Result` from a
  handler §9.4 does not list among its seven call sites.

R34 says a caller receiving a failure handles, propagates or reports it,
never drops it. R64 forbids inventing a user-facing literal, R2 forbids
settling a technical decision in silence, and no key exists for either
case. Whether "read the outcome and change no state" satisfies R34, or
whether such a failure must reach a log, a state or a new catalogue key,
is what I lack.

## Why the lot cannot proceed

It proceeds — the sheet is written against the conventions as they stand:
both outcomes are read, and neither changes a `RaceDetailUiState` field.
What is at stake is consistency: lot-20 and lot-21 both add a push after a
successful write (§6.10), on two screens neither of which carries a sync
state, and they will answer this the same way only if a rule says so.
lot-36's two `sync` call sites and lot-16's `markSyncSuccess` sit on the
same question.

## Where I met it

`code/lot-20/fiche-executable.md`, `RaceDetailViewModel` points 3 and 4 —
`onSetAsReferenceClicked`, `onRenameConfirmed` and `onDeleteConfirmed`,
each pushing after its write succeeds (§6.10 of `desc-bug.md`) and each
reading a `Result` (§9.4).

## What I think it is

update — R34 gains what "acts on it" means for a failure the corpus gives
no destination to, on a screen with no state for it.

## Verdict

**A convention. Written as R79 and R80, section 6 of
`docs/TECHNICAL_CONVENTIONS.md`.**

**The three filters leave it standing.** The platform imposes nothing —
Android has no opinion on what a handler does with an outcome. **No tool
carries it, and none could**: detekt's `IgnoredReturnValue` explicitly
excludes a value stored in a variable or property, so
`val outcome = service.push()` followed by nothing passes a clean
`./gradlew check`. R65 names detekt against R34 for the *syntactic* drop;
the semantic half — a value read and acted on by no one — is invisible to
it. It holds on no one machine. **It is a convention.**

**R34 was not silent, it was incomplete.** It names three destinations —
handled, propagated, reported — and the request's two cases are exactly
the ones where the first two are gone: a screen with no field to carry
the outcome cannot handle it, and a top-level handler returns to nobody
to propagate to. 🔴 **R79 writes down that the third is then not
optional**, and R53 already names the only channel there is. **What was
genuinely open is whether "read it and change no state" counts; it does
not.**

**R80 closes the workaround R64 leaves open.** R64 forbids inventing a
literal, which pushes a lot towards borrowing a key written for another
failure — the same invention wearing a key's name. **Consistency across
lot-20, lot-21, lot-36 and lot-16 was the stated worry, and one
destination for all four is what gives it.**

📌 **Whether the user is told a push failed is a product decision, and
is not settled here.** It needs an §10 key, and this agent invents none.
**Carry it back as a product question if the behaviour is wanted** — R79
holds in the meantime, and the sheet as written needs only the log added.

⚠️ **R79 does not reopen R35.** §6.1's refused push during a race stays
silent to the user; R79 governs the log, which no user reads. **The two
answer different questions and both stand.**
