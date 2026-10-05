## Signatures

    @Entity(tableName = "race_history_entries")
    data class RaceHistoryEntryEntity(
      @PrimaryKey(autoGenerate = true) val id: Long,   // 0 on insert requests a fresh id
      val name: String,
      val dateEpochMs: Long,                           // Instant.toEpochMilli(), mirrors RaceEntity.dateEpochMs (lot-01)
      val totalTimeMs: Long
    )

    interface RaceHistoryDao {
      fun observeAll(): Flow<List<RaceHistoryEntryEntity>>
      // ORDER BY id ASC — the order entries were inserted in, i.e. the
      // order they were passed to replaceAll; RaceHistoryEntryEntity
      // carries nothing else to order by, and this store never re-sorts
      // what it is given (§2.3: "persists the entries ... as a whole
      // block").

      fun replaceAll(entries: List<RaceHistoryEntryEntity>)
      // One transaction: deletes every existing row, then inserts
      // entries in the given order.
    }

    @Database(
      entities = [RaceHistoryEntryEntity::class],
      version = 1,
      exportSchema = true
    )
    abstract class WatchHistoryDatabase : RoomDatabase() {
      abstract fun raceHistoryDao(): RaceHistoryDao
    }
    // A database of its own, distinct from HyroxDatabase (lot-01) — the
    // lot declares WatchHistoryDatabase as its own produced piece, not an
    // addition to HyroxDatabase's entity list.

    class WatchHistoryStoreImpl(private val raceHistoryDao: RaceHistoryDao) : WatchHistoryStore {
      override fun replaceAll(entries: List<RaceHistoryEntry>)
      // Maps each RaceHistoryEntry to a RaceHistoryEntryEntity (id = 0)
      // and calls raceHistoryDao.replaceAll with the list in the same
      // order it was given — no re-sort.

      override fun observe(): Flow<List<RaceHistoryEntry>>
      // Maps raceHistoryDao.observeAll()'s emissions back to
      // RaceHistoryEntry, order preserved from the DAO query.
    }

## Acceptance criteria

- After `replaceAll(entries)`, `observe()`'s next emission is exactly `entries`, in the same order they were passed
- A second `replaceAll` call with a different, smaller list replaces the stored set wholesale: `observe()` no longer emits any entry from the first call that is absent from the second
- `observe()` re-emits on every `replaceAll` call, even when the same entries are passed again
- Entries stored through one `WatchHistoryStoreImpl` instance are present, in the same order, in `observe()`'s first emission from a freshly built `WatchHistoryStoreImpl` pointed at the same store — the history survives the store being recreated
- Before any `replaceAll` call on a freshly created store, `observe()`'s first emission is an empty list

## Dependencies

WatchHistoryStore — pre-existing, interface unchanged (`core-domain/src/main/kotlin/com/mgilli/core/domain/sync/WatchHistoryStore.kt`)
RaceHistoryEntry — pre-existing (`core-domain/src/main/kotlin/com/mgilli/core/domain/sync/RaceHistoryEntry.kt`)
Room runtime, Room ktx and the Room compiler, processed through the KSP plugin — pre-existing in `core-data/build.gradle.kts` and `gradle/libs.versions.toml`, added by lot-01; no further gradle change needed

## Conventions

§3 · a platform adapter lives in the module carrying its technology — Room in `:core-data`
§5 · the downward payload replaces the watch state wholesale — no merge, no comparison, no partial update
§8 · Room schemas are exported and versioned; every schema change ships with a migration, destructive fallback prohibited
§9 · Room entities are named `<Thing>Entity`, DAOs `<Thing>Dao` — carried over from the lot's own declared names
§14 · Room DAOs are tested with an in-memory database
