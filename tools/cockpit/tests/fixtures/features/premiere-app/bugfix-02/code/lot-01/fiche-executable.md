## Signatures

    @Entity(tableName = "races")
    data class RaceEntity(
      @PrimaryKey(autoGenerate = true) val id: Long,   // 0 on insert requests a fresh id; non-zero reuses that id
      val name: String,
      val dateEpochMs: Long,                           // Instant.toEpochMilli()
      val origin: RaceOrigin,
      val isReference: Boolean,
      val completion: RaceCompletion,
      val currentSegmentIndex: Int?,
      val currentSegmentOpenedAt: Long?
    )

    // Per §4: a segment row stores a duration against an index only —
    // type, station and cumulativeMs are never persisted, they are
    // derived on read (SegmentBlueprint / buildSegments).
    @Entity(tableName = "segments", primaryKeys = ["raceId", "index"])
    data class SegmentEntity(
      val raceId: Long,
      val index: Int,
      val durationMs: Long?
    )

    @Entity(tableName = "retained_factors", primaryKeys = ["raceId", "kilometre"])
    data class RetainedFactorEntity(val raceId: Long, val kilometre: Int, val factor: Double)

    @Entity(tableName = "rejected_calibrations", primaryKeys = ["raceId", "kilometre"])
    data class RejectedCalibrationEntity(val raceId: Long, val kilometre: Int, val value: Double)

    @Entity(tableName = "profile")
    data class ProfileEntity(
      @PrimaryKey val id: Int,             // always 0 — one row
      val hrMaxBpm: Int?,
      val zoneThresholds: List<Int>,       // 4 entries
      val expectedDistanceM: Int,
      val longPressMs: Int,
      val correctionFactor: Float,
      val lastSyncSuccessAt: Long?
    )

    interface RaceDao {
      fun observeAll(): Flow<List<RaceEntity>>
      // date DESC, id DESC as insertion-order tiebreak — mirrors
      // RaceRepository.observeAll's existing order (§9.1)

      fun observeReference(): Flow<RaceEntity?>
      fun findById(raceId: Long): RaceEntity?
      fun findSegments(raceId: Long): List<SegmentEntity>              // ordered by index ascending
      fun findRetainedFactors(raceId: Long): List<RetainedFactorEntity>
      fun findRejectedCalibrations(raceId: Long): List<RejectedCalibrationEntity>

      fun upsert(
        race: RaceEntity,
        segments: List<SegmentEntity>,
        retainedFactors: List<RetainedFactorEntity>,
        rejectedCalibrations: List<RejectedCalibrationEntity>
      ): Long
      // One transaction: deletes any existing segments/retainedFactors/
      // rejectedCalibrations rows for race.id, replaces the race row
      // (REPLACE on id conflict; id 0 autogenerates), inserts the given
      // children. Returns the resulting race id.

      fun update(race: RaceEntity)   // race.id must already exist
      fun clearReferenceFlag()       // isReference = false on every stored race
      fun delete(raceId: Long)       // one transaction: the race row and its segments/retainedFactors/rejectedCalibrations
    }

    interface ProfileDao {
      fun observe(): Flow<ProfileEntity?>   // null until the row is first written
      fun upsert(profile: ProfileEntity)    // single row, id fixed at 0
    }

    @Database(
      entities = [RaceEntity::class, SegmentEntity::class, RetainedFactorEntity::class,
                  RejectedCalibrationEntity::class, ProfileEntity::class],
      version = 1,
      exportSchema = true
    )
    abstract class HyroxDatabase : RoomDatabase() {
      abstract fun raceDao(): RaceDao
      abstract fun profileDao(): ProfileDao
    }

    class RaceRepositoryImpl(private val raceDao: RaceDao) : RaceRepository
    class ProfileRepositoryImpl(private val profileDao: ProfileDao) : ProfileRepository
    // Both keep every method of RaceRepository / ProfileRepository with
    // the same signature and the same validation/ordering contracts
    // already in place; only the storage backing changes, from the
    // in-memory LinkedHashMap / MutableStateFlow to raceDao / profileDao.
    // Reconstructing a domain Race from RaceEntity + its children reuses
    // SegmentBlueprint / buildSegments-style derivation for type, station
    // and cumulativeMs — never stored.

## Acceptance criteria

- A race saved through `saveImportedRace` is returned unchanged by `findById` from a `RaceRepositoryImpl` built against a newly reopened `HyroxDatabase` pointed at the same store — it survives the repository being recreated
- A race saved through `saveRecordedRace` with `completion` INCOMPLETE is returned by `findById`, after the repository is recreated, with exactly the same segments present (and the same ones absent) as when it was saved
- Deleting a race removes its segments, retained factors and rejected calibrations from storage: after `delete`, no `findSegments`/`findRetainedFactors`/`findRejectedCalibrations` call for that id returns any row, from a recreated repository
- `observeAll`'s order (date descending, ties by most-recently-inserted) still holds after the repository is recreated, not only within one instance
- A race set as reference via `setAsReference`, or stored as reference via `replaceReference`, is still the sole reference (`observeReference`) after the repository is recreated
- A value set through any `ProfileRepository` updater (e.g. `updateCorrectionFactor`) is present in `observe()`'s first emission from a `ProfileRepositoryImpl` built against a newly reopened `HyroxDatabase` pointed at the same store
- Before any updater has ever run against a freshly created store, `observe()`'s first emission is still the default profile: `hrMaxBpm` unset, `zoneThresholds` [60, 70, 80, 90], `expectedDistanceM` 1000, `longPressMs` 700, `correctionFactor` 1, `lastSyncSuccessAt` unset

## Dependencies

RaceRepository, ProfileRepository — pre-existing, interfaces unchanged
RaceRepositoryImpl, ProfileRepositoryImpl — pre-existing, modified by this lot
Race, Segment, RaceOrigin, RaceCompletion, RetainedFactor, RejectedCalibration, Profile — pre-existing domain types
SegmentBlueprint, buildSegments — pre-existing, used to re-derive type/station/cumulativeMs on read
Room runtime, Room ktx and the Room compiler, processed through the KSP plugin — added by this lot to `core-data/build.gradle.kts` and to `gradle/libs.versions.toml` (no Room dependency exists in the project yet)

## Conventions

§3 · a platform adapter lives in the module carrying its technology — Room in `:core-data`
§4 · a segment row stores a duration against an index — nothing about the shape of the race
§8 · Room schemas are exported and versioned; every schema change ships with a migration, destructive fallback prohibited
§8 · cumulative values are computed on read, never stored
§8 · the calibration factor lives on the profile row, not on a race
§13 · a repository returns a result type, never null on failure
§13 · a failed import writes nothing, never a partial race
§14 · Room DAOs are tested with an in-memory database
