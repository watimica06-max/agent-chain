## Signatures

enum class RaceOrigin { IMPORTED, RECORDED }

enum class RaceCompletion { COMPLETE, INCOMPLETE }

data class Race(
  id: Long,
  name: String,
  date: Instant,
  origin: RaceOrigin,
  isReference: Boolean,
  completion: RaceCompletion,
  segments: List<Segment>,
  retainedFactors: List<RetainedFactor>,
  rejectedCalibrations: List<RejectedCalibration>,
  currentSegmentIndex: Int?,
  currentSegmentOpenedAt: Long?
)

RaceRepository.setAsReference(raceId: Long) → Result<Unit>

RaceRepository.rename(raceId: Long, name: String) → Result<Unit>

RaceRepository.delete(raceId: Long) → Result<Unit>

RaceRepository.saveImportedRace(name: String, date: Instant, segments: List<Segment>) → Result<Race>

## Acceptance criteria

- Setting a race as reference while another race already holds it clears isReference on the previous holder, and only the new race is reference afterward
- Setting as reference a race when no race currently holds it leaves that race as the only one referenced
- Renaming a race to a name of 1 to 40 trimmed characters updates the stored name to the trimmed value
- Renaming a race to a value that trims to an empty string leaves the stored name unchanged and returns a failure
- Renaming a race to a value whose trimmed length exceeds 40 characters leaves the stored name unchanged and returns a failure
- Deleting a race removes it — it is no longer present among stored races
- Deleting the race currently marked as reference clears isReference app-wide, with no other race becoming reference
- Saving an imported race creates a new Race with origin IMPORTED, completion COMPLETE, isReference false, and the given 30 segments stored with their durationMs values
- Saving an imported race produces a Race with empty retainedFactors and empty rejectedCalibrations
- Saving an imported race produces a Race with no in-progress fields (currentSegmentIndex and currentSegmentOpenedAt both absent)
- Saving two imported races under the same name succeeds for both — no uniqueness constraint is enforced on name

## Dependencies

Segment — pre-existing (lot-01)
RetainedFactor — produced by lot-08
RejectedCalibration — produced by lot-08
