## Signatures

    sealed class PhoneDestination {
        data object RaceList : PhoneDestination()
        data class RaceDetail(val raceId: Long) : PhoneDestination()
        data object Profile : PhoneDestination()
        data object PasteResult : PhoneDestination()
        data object ImportPreview : PhoneDestination()
        data object PasteError : PhoneDestination()
    }

    class PhoneNavigator {
        val current: PhoneDestination

        fun toRaceDetail(raceId: Long)
        fun toProfile()
        fun toPasteResult()
        fun toImportPreview()
        fun toPasteError()
        fun backToPasteResult()
        fun toRaceDetailAfterImport(raceId: Long)
        fun back(): Boolean
    }

## Acceptance criteria

- From RaceList, `toRaceDetail(raceId)` makes `current` a `RaceDetail` holding that raceId, with RaceList beneath it on the stack
- From RaceList, `toProfile()` makes `current` equal to `Profile`
- From RaceList, `toPasteResult()` makes `current` equal to `PasteResult`
- From PasteResult, `toImportPreview()` makes `current` equal to `ImportPreview`, with PasteResult still beneath it
- From PasteResult, `toPasteError()` makes `current` equal to `PasteError`, with PasteResult still beneath it
- From ImportPreview, `backToPasteResult()` makes `current` equal to `PasteResult`
- From PasteError, `backToPasteResult()` makes `current` equal to `PasteResult`
- From ImportPreview, `toRaceDetailAfterImport(raceId)` makes `current` a `RaceDetail(raceId)` whose only ancestor on the stack is `RaceList` — PasteResult and ImportPreview no longer appear
- After `toRaceDetailAfterImport(raceId)`, calling `back()` once returns `current` directly to `RaceList`
- From a `RaceDetail` reached by `toRaceDetail` (not after an import), calling `back()` once returns `current` to `RaceList`

## Dependencies

—
