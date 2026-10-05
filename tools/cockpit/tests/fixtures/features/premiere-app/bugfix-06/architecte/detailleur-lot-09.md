## What I need

Whether R16 ("a field the code searches on carries an index … and any
lookup a lot adds") requires this lot to add a Room migration indexing
`RaceEntity.currentSegmentIndex`, given that lot-09's declared scope
(Modifies: RaceDao, RaceDaoTest; Produces: —) excludes RaceEntity,
HyroxDatabase and RaceDatabaseMigrations.

## Why the lot cannot proceed

It is not blocked — RaceDao.findInProgress()'s signature and its
acceptance criteria hold with or without the index, so the sheet is
written regardless. What is missing is a decision on whether adding the
index is this lot's job, since the file it would live in is outside the
lot's declared scope.

## Where I met it

lot-09, §2.7's second gap — the new RaceDao.findInProgress() query,
`WHERE currentSegmentIndex IS NOT NULL`.

## What I think it is        add · update · remove

update — either R16 states an exception for a small, non-identifying
filter field, or a convention amendment schedules a follow-up lot to
retrofit the missing indices in one migration. The same gap already
exists, unaddressed, for `RaceEntity.isReference` — named by R16
itself — and for `date`/`origin`, none of which carry an index despite
being searched on by pre-existing queries; this is not new to lot-09.

## Verdict

Not a convention. R16 already answers the technical half without
exception: "any lookup a lot adds" covers
`RaceDao.findInProgress()`'s filter on `currentSegmentIndex` — no carve-out
for a small or non-identifying field, so no amendment to R16 is
warranted.

The half that is actually open — whether lot-09 itself writes the
migration — is a lot-boundary matter, and R9 already governs it: "ask
first before touching any file whose change reaches beyond the lot that
touches it." Raising this request *is* that ask; it is not answered by
carving a new rule. R2 covers what happens next: the lot goes on
against this file as it stands, and the open point is carried in
lot-09's own report — exactly as it already stands, unaddressed, for
`isReference`, `date` and `origin`.

Concretely: write the sheet without touching RaceEntity, HyroxDatabase
or RaceDatabaseMigrations. `RaceDao.findInProgress()` proceeds without
the index. R16's test is a review, not a wired mechanical check (no
tool in section 12's table names it), so nothing in R4's `./gradlew
check` gate is put at risk by the deferral — lot-09 is deliverable as
scoped. Note the missing index on `currentSegmentIndex` in lot-09's
report, for whichever later lot's scope covers the schema files.

