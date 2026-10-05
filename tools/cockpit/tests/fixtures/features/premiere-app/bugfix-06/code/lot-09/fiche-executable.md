## Signatures

RaceDao.findInProgress(): RaceEntity?
  — the race carrying a non-null currentSegmentIndex, or null when
    none does; at most one is ever expected to match

RaceDao.insertSegments(segments: List<SegmentEntity>): Unit
  — unchanged parameters and return type; @Insert(onConflict =
    OnConflictStrategy.ABORT) replaces the current REPLACE, so
    inserting a segment whose (raceId, index) is already stored
    raises instead of silently overwriting the stored row

RaceDao.upsertAndFind(
  race: RaceEntity,
  segments: List<SegmentEntity>,
  retainedFactors: List<RetainedFactorEntity>,
  rejectedCalibrations: List<RejectedCalibrationEntity>
) → RaceEntity?
  — one @Transaction: writes race and its children exactly as the
    existing upsert() does (calling it internally), then reads the
    resulting row back inside the same transaction; null only if the
    row is absent at the read, which nothing inside the transaction
    can cause

RaceDao.findOrSaveRecordedRace(
  sourceRaceId: Long,
  race: RaceEntity,
  segments: List<SegmentEntity>,
  retainedFactors: List<RetainedFactorEntity>,
  rejectedCalibrations: List<RejectedCalibrationEntity>
) → RaceEntity?
  — one @Transaction: returns the existing row already carrying
    sourceRaceId, writing nothing, when findBySourceRaceId(sourceRaceId)
    finds one; otherwise writes race — with sourceRaceId set to the
    given value, overriding whatever race.sourceRaceId already
    carries — and its children via upsertAndFind, and returns that
    result. The lookup and the write happen inside one transaction, so
    no concurrent call can interleave between them.

RaceDao.replaceReference(
  race: RaceEntity?,
  segments: List<SegmentEntity>,
  retainedFactors: List<RetainedFactorEntity>,
  rejectedCalibrations: List<RejectedCalibrationEntity>
) → RaceEntity?
  — one @Transaction: clears isReference on every race, then, only
    when race is non-null, writes it and its children via
    upsertAndFind and returns that result; returns null when race is
    null. Both the clear and the write happen inside one transaction,
    so no reader ever observes the flag cleared without the new
    reference already present.

## Acceptance criteria

- findInProgress() returns null when no stored race carries a non-null currentSegmentIndex
- findInProgress() returns the race carrying a non-null currentSegmentIndex, when one is stored
- insertSegments raises when a segment's (raceId, index) is already stored, and the previously stored row for that (raceId, index) is unchanged afterwards
- upsertAndFind returns the row it just wrote, its fields matching what was passed in
- findOrSaveRecordedRace returns the existing row unchanged, and inserts nothing, when sourceRaceId is already stored on another row
- findOrSaveRecordedRace writes and returns a new row carrying sourceRaceId, when sourceRaceId is not yet stored on any row
- replaceReference(race, ...) with a non-null race clears isReference on every previously-referenced race and returns the given race written with isReference = true, and it alone is referenced afterwards
- replaceReference(null, ...) clears isReference on every race, returns null, and writes no new row

## Dependencies

RaceEntity — carries the unique index on sourceRaceId since lot-08; unchanged further by this lot
SegmentEntity, RetainedFactorEntity, RejectedCalibrationEntity — pre-existing
RaceDao.upsert, RaceDao.findById, RaceDao.findBySourceRaceId, RaceDao.clearReferenceFlag — pre-existing, called by the new transactional methods above

## Conventions

R8 · no committed migration is modified — this lot adds no migration, no schema change
R16 · a field the code searches on carries an index — findInProgress's new lookup on currentSegmentIndex has none; see architecte/detailleur-lot-09.md
R26 · no !! on a value coming from outside the function — every new method returns its absence as null instead
R30 · no empty and no generic catch — the SQLiteConstraintException insertSegments now raises is left to propagate uncaught here, not swallowed
R37 · a write holding an invariant is atomic against a concurrent reader — the basis for upsertAndFind, findOrSaveRecordedRace and replaceReference each being one @Transaction
R55 · every public function has at least one nominal and one failure test — RaceDaoTest does not exist yet and is created by this lot
R57 · "at most one reference race" has a test attempting to violate it — replaceReference is where that invariant is now held atomically

## Requests

architecte/detailleur-lot-09.md
