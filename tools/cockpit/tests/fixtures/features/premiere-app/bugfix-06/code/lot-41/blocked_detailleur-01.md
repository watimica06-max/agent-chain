## What blocks

§9.6 has `WatchApp` pass `refreshIntervalMs` on to `MainRacePageScreen`
without saying what the screen does with it, and §9.11 keeps "a value
whose freshness has just lapsed" shown and dimmed without naming how long
"just lapsed" lasts — two readings of the pair produce different screens,
and choosing between them is not this agent's to settle.

## Where

`desc-bug.md` §9.6 (*Ambient mode is computed and thrown away*) and §9.11
(*Every sensor value hits its freshness boundary on every power-save
refresh*), against `code/decoupage.md` lot-41 (`Modifies:
MainRacePageViewModel, MainRacePageUiState, MainRacePageScreen, …`) and
lot-49 (`Needs: … MainRacePageScreen (lot-41) …`).

The two readings, and what separates them:

- **(a) `refreshIntervalMs` stops at `WatchApp`.** `MainRacePageScreen`
  takes `displayMode: DisplayMode` and nothing else new;
  `MainRacePageViewModel` receives the display mode alone, as §9.11's own
  sentence says, and in `POWER_SAVE` every value that has ever been
  received but is no longer fresh is shown dimmed, for as long as it stays
  stale. A sensor that stops delivering for a minute keeps its last value
  on screen, dimmed.
- **(b) `refreshIntervalMs` is the bound §9.11 leaves unnamed.**
  `MainRacePageScreen` takes both, forwards the interval, and a value
  stale by no more than one refresh interval is shown dimmed while a
  staler one falls back to the dash. The same sensor stopping for a minute
  falls back to the dash after one interval.

Reading (a) leaves `refreshIntervalMs` a parameter no callee reads, which
R25 forbids and which is the very defect §9.1 reports elsewhere; reading
(b) reads it, but rests on a bound neither entry states. Nothing in
`desc-bug.md`, in `CURRENT_TECHNICAL_STATE.md` or in the code decides
between them: `AlwaysOnDisplayController.refreshIntervalMs` is
`SensorFreshnessWindow.WINDOW_MS` in `POWER_SAVE` and null in `NORMAL`,
and `SensorFreshnessWindow` states it takes no display-mode input. The
whole lot's `MainRacePageScreen` signature turns on the answer, and lot-49
calls that signature.

## To resume

State which of (a) and (b) holds — that is, whether `MainRacePageScreen`
takes `refreshIntervalMs` at all, and what it does with it.

If (b): say whether the bound is inclusive at `refreshIntervalMs`, the way
`SensorFreshnessWindow`'s own window and R27 are, and whether the same
bound governs the heart-rate value and the pace value alike.

Either answer leaves the rest of lot-41 unchanged: §5.3's collection of
`SensorReadingsSource.heartRate()` / `.distance()` / `.speed()` and
`RaceTicker.ticks` on `viewModelScope`, §7.1's call sites (already carried
by lot-43), §9.11's three-way `MainRacePageUiState` block distinguishing a
fresh value, a shown-but-dimmed value and an absent one, and §12.2's
`SavedStateHandle`.

## Decision

Take reading (a)'s behaviour, with `refreshIntervalMs` read for what it
already is: `MainRacePageScreen` takes both `displayMode: DisplayMode`
and `refreshIntervalMs: Long?`, forwards `displayMode` alone to
`MainRacePageViewModel` as §9.11's own sentence says, and reads
`refreshIntervalMs` as the cadence at which it refreshes its power-save
layout while in `POWER_SAVE` — never as a freshness bound. In
`POWER_SAVE` a value already received and no longer fresh is shown
dimmed for as long as it stays stale.

§9.6 states that `WatchApp`'s `MAIN` branch passes `displayMode` *and*
`refreshIntervalMs` on to `MainRacePageScreen`, so dropping the
parameter is not open; `AlwaysOnDisplayController.refreshIntervalMs`'s
own KDoc states what it is — "The refresh interval to apply while in
[DisplayMode.POWER_SAVE]", overriding the platform's once-per-minute
ambient default "so a sensor-derived value never goes stale-looking
while frozen" — and reading it for that satisfies R25 without inventing
a bound. No expiry on the dimmed value exists: §9.11 states the dimming
unconditionally for power-save and names no bound, and R27 fixes the
inclusivity of a bound an entry states rather than creating one.

This does not extend to `NORMAL`, which keeps `computeState`'s existing
dash fallback untouched; nor to `SensorFreshnessWindow`, which keeps
`WINDOW_MS` and its display-mode-free signature; nor to `RaceTicker`,
whose `TICK_INTERVAL_MS` stays as it is. The dimmed state applies
uniformly to every sensor-derived value `computeState` already evaluates
for freshness — the heart-rate value through
`SensorFreshnessWindow.evaluate` and the pace value through
`distanceFresh` — with no per-value distinction.

## How it was applied

`code/lot-41/fiche-executable.md` is written against this decision:

- `MainRacePageScreen(viewModel, displayMode: DisplayMode = NORMAL,
  refreshIntervalMs: Long? = null)`; it forwards `displayMode` alone to
  `MainRacePageViewModel.onDisplayModeChanged`, and reads
  `refreshIntervalMs` as its power-save refresh cadence, never as a
  freshness bound. Both parameters carry a default so `WatchApp`'s call
  site — same module, lot-49's scope — keeps compiling, which keeps R74
  from ever triggering on this lot.
- `SensorValueDisplay` (`Fresh` / `Stale` / `Fallback`) is added to
  `MainRacePageUiState.kt` for §9.11's second gap. `Stale` is reachable in
  `POWER_SAVE` only, never expires, and applies uniformly to the
  heart-rate value and the pace value; `NORMAL` keeps today's fallback.
- The criteria pin the no-expiry reading — a value still shown dimmed a
  full minute after its window lapsed — and the cadence reading, on what
  becomes visible after `refreshIntervalMs` has elapsed.
