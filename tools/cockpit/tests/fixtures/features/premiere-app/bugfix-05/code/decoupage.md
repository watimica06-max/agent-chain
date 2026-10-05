## Symbols

DesignTokens.Typography.Watch
  display, displaySm, value, valueSm, badge, title, label, labelSm, caption —
  fixed .sp constants, must resolve at render time from the watch face's
  own width instead                                          §3.1

DesignTokensTest
  asserts the nine `DesignTokens.Typography.Watch` values against fixed
  sp constants — those assertions no longer hold once the values are
  computed from the face width                               §3.1

RaceListViewModel
  onProfileClicked() — opens the profile screen via
  PhoneNavigator.toProfile()                                 §8.1

RaceListHeader
  renders only the title and the "+" action — needs a profile icon next
  to it, wired to RaceListViewModel.onProfileClicked          §8.1

RaceListScreen
  wires RaceListHeader's new profile-icon callback; exposes its
  empty-state switch as a standalone, testable criterion (mirrors
  WatchHistoryScreen.isHistoryEmpty), true when RaceListUiState.races is
  empty                                                       §8.1, §9.3

PhoneNavigator
  toProfile() — already exists and already opens the profile
  destination; nothing to build                               §8.1

PhoneStringResources.RaceList
  needs a new entry for the profile icon's glyph, absent today  §8.1

RaceListUiState
  races — read by the new empty-state criterion                §9.3

PasteResultScreen
  pastedText TextField — grows with content instead of keeping a fixed,
  scrollable height, pushing the "Importer" action off screen  §9.1

ProfileViewModel
  onHrMaxUpdated / onExpectedDistanceChanged / onLongPressChanged /
  onZoneThresholdChanged — call ProfileRepository's updater but discard
  the returned Result; must inspect it, revert the field on rejection
  and surface the constraint message, cleared on the next successful
  edit of the same field                                      §9.2

ProfileRepository
  updateHrMaxBpm / updateExpectedDistanceM / updateLongPressMs /
  updateZoneThreshold — already return Result<Unit>; nothing to build
  there                                                        §9.2

ProfileUiState
  carries no field for a per-field rejection message — needs one  §9.2

ProfileScreen
  must revert each field's displayed value to the profile's last
  stored value and show the rejection message on failure       §9.2

PhoneStringResources.Profile
  needs new entries naming the violated constraint for each of the
  four settings                                                §9.2

EndOfRaceViewModel
  computeState never reads Race.completion                     §9.4

Race.completion / RaceCompletion
  already exists and already carries COMPLETE/INCOMPLETE; nothing to
  build there                                                  §9.4

EndOfRaceUiState
  carries no field for an incomplete race — needs one           §9.4

EndOfRaceScreen
  needs to render a dedicated message when the race is incomplete  §9.4

WatchStringResources.End
  needs a new entry for the incomplete-race message              §9.4

## lot-01

Anchor: §3.1 — Watch typography renders at scaled-pixel size instead of the spec's pixel scale
Needs: —
Produces: —
Modifies: DesignTokens.Typography.Watch, DesignTokensTest

## lot-02

Anchor: §8.1 — The profile screen is unreachable from the race list; §9.3 — The race list's empty state has no standalone, testable criterion
Needs: PhoneNavigator (pre-existing), PhoneDestination.Profile (pre-existing), RaceListUiState (pre-existing)
Produces: RaceListViewModel.onProfileClicked (called by RaceListHeader, within this lot); the race list's empty-state criterion, mirroring WatchHistoryScreen.isHistoryEmpty (called by RaceListScreen, within this lot)
Modifies: RaceListViewModel, RaceListHeader, RaceListScreen, PhoneStringResources.RaceList

## lot-03

Anchor: §9.1 — The paste screen's growing text field pushes the Importer action off screen
Needs: —
Produces: —
Modifies: PasteResultScreen

## lot-04

Anchor: §9.2 — A rejected zone-threshold or other profile setting is never reverted or explained
Needs: ProfileRepository (pre-existing)
Produces: —
Modifies: ProfileViewModel, ProfileUiState, ProfileScreen, PhoneStringResources.Profile

## lot-05

Anchor: §9.4 — The end-of-race screen never states a race is incomplete
Needs: Race.completion / RaceCompletion (pre-existing)
Produces: —
Modifies: EndOfRaceViewModel, EndOfRaceUiState, EndOfRaceScreen, WatchStringResources.End

## Entries with no lot

None — every numbered entry is cited above.
