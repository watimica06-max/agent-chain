## Signatures

EndOfRaceViewModel(
  finalRace: Race,
  referenceRace: Race?,
  exerciseSessionManager: ExerciseSessionManager,
  profileRepository: ProfileRepository,
  navigator: WatchRaceNavigator
)

Change: the constructor gains `profileRepository: ProfileRepository`.
On construction, when `finalRace.retainedFactors` is not empty, calls
`profileRepository.updateCorrectionFactor(value)` with the last entry
of `finalRace.retainedFactors`'s `factor`; when `finalRace.retainedFactors`
is empty, no call is made.

## Acceptance criteria

- A finished race whose `retainedFactors` is not empty calls
  `ProfileRepository.updateCorrectionFactor` with the last retained
  factor's `factor` value
- A finished race whose `retainedFactors` is empty never calls
  `ProfileRepository.updateCorrectionFactor`, leaving the profile's
  stored correction factor unchanged

## Dependencies

Race — pre-existing
ProfileRepository — pre-existing
ExerciseSessionManager — pre-existing
WatchRaceNavigator — pre-existing
