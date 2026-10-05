## What I need

Which of R31 and R33 governs an in-process deserialisation helper whose
own module already converts the failure at the boundary that leaves the
process: does its failure cross as a type the module declares and
throws, or as a value it returns?

## Why the lot cannot proceed

The lot is blocked on a split defect of its own
(`code/lot-11/blocked_detailleur.md`), but this question stands
independently of that, and the signature cannot be written either way
until it is answered.

R31 says an error crossing a module boundary is of a type that module
declares and that a dependency's own exception never crosses — read that
way, `PayloadCodec.toObject` throwing `PayloadDecodingFailure` instead
of letting `ClassCastException` or an `ObjectInputStream` exception
escape satisfies §9.5, and every caller compiles unchanged.

R33 names "a deserialisation" among the calls that return their failure
as a value, never as a thrown exception crossing the boundary — read
that way, `decodeProfileSync` and `decodeRecordedRace` return
`Result<ProfileSyncPayload>`/`Result<RecordedRacePayload>`, and the two
production listener services that call them stop compiling. Both are in
lots already coded, and both wrap the caught exception into a
`PayloadDecodingFailure` of their own today, so the second reading also
duplicates a conversion the receiving module already performs.

The two readings produce two different signatures for the same function,
and nothing in the file separates the process-leaving call R33 was
written for from a helper that reads bytes already in memory.

## Where I met it

lot-11, §9.5 and §6.3 — `PayloadCodec.toObject` and the two decode
functions, `:core-sync`. Confirmed by grep:
`RecordedRaceListenerService.kt:49` and `ProfileSyncListenerService.kt:45`
each call the decode inside a `try` and wrap what they catch as
`PayloadDecodingFailure`; `PayloadDecodingFailure` itself is an
`Exception` subclass declared by `:core-sync` (lot-52).

## What I think it is        add · update · remove

update — R33, stating whether a deserialisation of bytes already held in
memory is one of the process-leaving calls it governs, and where the
failure-as-a-value obligation sits when the module that receives the
bytes from outside is not the module that decodes them.

## Verdict

**A convention, and a genuine gap between R31 and R33. Written as R89,
section 6 of `docs/TECHNICAL_CONVENTIONS.md`.**

**The three filters leave it standing.** Kotlin imposes neither a thrown
type nor a `Result` return on a private helper — both compile, both run;
there is no other way the platform prefers. No tool of the R65 table
reads meaning into a function's failure style: detekt's exception checks
(R30) fire on an empty or generic catch, not on the choice between
throwing a declared type and returning one. It holds on no one machine.
**It is a convention**, and neither R31 nor R33 as worded settles it
alone — each reads as complete on its own, and the conflict only
surfaces at the point one call nests inside the other, exactly the shape
a framing grid sweeping subject by subject cannot see.

**The two readings are not equally supported.** R33's list — "the store,
a sensor, the data layer, a deserialisation" — names operations sharing
one property: each is *itself* the act of reaching outside the process,
so each can fail for a reason outside the module's control at the moment
it is called. `PayloadCodec.toObject` does not reach anywhere: the bytes
it decodes already sit in memory, handed to the listener service by the
platform's own callback before `toObject` is ever invoked. That callback
delivery — not the decode that follows it — is the point R32 already
names: "a sync payload" is in R32's own list of "data entering from
anywhere outside the process," validated and converted "at the module
that receives it." `:core-sync` is that module, and it already performs
that conversion, exactly as the request's grep shows: the two listener
services catch what `toObject`'s dependency throws (`ClassCastException`,
an `ObjectInputStream` exception) and wrap it into `PayloadDecodingFailure`
— R31's own form, a dependency's exception stopped at the boundary and
replaced by a type `:core-sync` declares.

**R33's obligation does not disappear — it sits one level up.** The
process-leaving event is the listener service's own receipt of the
payload; R33 binds *that* boundary — the listener service's public
method — to hand its failure back as a value to whatever calls it, not
to the in-process helper it delegates decoding to. Reading R33 as
reaching into `toObject` and `decodeProfileSync`/`decodeRecordedRace`
would make the module perform the same conversion twice — once inside
the decode helper (to satisfy a literal "never thrown" on every internal
call) and once again at the service boundary — for no caller's benefit,
and would break the two already-coded, already-passed production call
sites for a distinction their own code already drew correctly.

**Concretely**: `PayloadCodec.toObject` throws `PayloadDecodingFailure`,
as do `decodeProfileSync` and `decodeRecordedRace` — R31 governs all
three, and every existing caller compiles unchanged. R33 continues to
govern the listener services' own boundary-facing methods, unaffected by
where inside `:core-sync` the decode step itself lives. The lot proceeds
on that signature.

📌 **This will recur.** Any module receiving bytes over a callback and
decoding them through an internal helper meets the same shape; R89 is
written generally rather than for this pair of functions alone.
