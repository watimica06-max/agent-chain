## Signatures

    enum class WatchDestination { HOME, PREPARATION, MAIN, PROJECTION, CONTROL, END }

    class WatchRaceNavigator {

        /** Starts at HOME. */
        val current: WatchDestination

        /** Whether the system back gesture is enabled on [current] (§8.3). */
        val backGestureEnabled: Boolean

        /** Home's "Démarrer" (§9.9 → §9.11). */
        fun toPreparation()

        /** Preparation's "Quitter" (§9.11 → §9.9). */
        fun quitPreparation()

        /** Preparation's "Lancer", once the race's clock has started (§9.11 → §9.12). */
        fun launchRace()

        /**
         * A rightward swipe during the race (§8.3): MAIN → PROJECTION →
         * CONTROL. Returns whether [current] moved — false from CONTROL,
         * the chain's last page.
         */
        fun swipeForward(): Boolean

        /** A marking taken on Main or Projection (§4.3, §8.1): returns to MAIN. */
        fun onMarked()

        /** The 30th marking (§8.3): straight to END, bypassing CONTROL. */
        fun onFinalMarking()

        /** Control's undo control tap (§4.4, §9.14 → §9.12). */
        fun onUndo()

        /** Control's stop confirmation "Arrêter" (§4.5, §9.14 → §9.15). */
        fun onStopConfirmed()

        /** End's "Terminer" (§9.15 → §9.9). */
        fun finish()

        /**
         * Records an interaction on the current page, rearming the
         * inactivity timer as of [atElapsedRealtime] (§8.1).
         */
        fun onInteraction(atElapsedRealtime: Long)

        /** A confirmation dialog opens on Control: suspends the inactivity timer (§8.1). */
        fun onDialogOpened()

        /**
         * The confirmation dialog closes: resumes the inactivity timer,
         * rearmed as of [atElapsedRealtime] (§8.1).
         */
        fun onDialogClosed(atElapsedRealtime: Long)

        /**
         * Called while on a secondary page (PROJECTION, CONTROL). Moves
         * [current] to MAIN, and returns it, when at least 8000ms have
         * elapsed since the last interaction and no dialog is open (§8.1).
         * Otherwise returns [current] unchanged. A call while [current]
         * is HOME, PREPARATION, MAIN or END never changes it.
         */
        fun checkInactivity(nowElapsedRealtime: Long): WatchDestination
    }

## Acceptance criteria

- `toPreparation` moves `current` from HOME to PREPARATION
- `quitPreparation` moves `current` from PREPARATION to HOME
- `launchRace` moves `current` from PREPARATION to MAIN
- `swipeForward` moves `current` from MAIN to PROJECTION and returns true
- `swipeForward` moves `current` from PROJECTION to CONTROL and returns true
- `swipeForward` called while `current` is CONTROL leaves it unchanged and returns false
- `backGestureEnabled` is false while `current` is MAIN, PROJECTION, CONTROL or END
- `backGestureEnabled` is true while `current` is HOME or PREPARATION
- `onMarked` called while `current` is PROJECTION moves it to MAIN
- `onMarked` called while `current` is MAIN leaves it at MAIN
- `onFinalMarking` moves `current` to END whether called from MAIN or PROJECTION, never passing through CONTROL
- `onUndo` moves `current` from CONTROL to MAIN
- `onStopConfirmed` moves `current` from CONTROL to END
- `finish` moves `current` from END to HOME
- `checkInactivity`, called while `current` is PROJECTION at least 8000ms after the last interaction with no dialog open, moves `current` to MAIN and returns MAIN
- `checkInactivity`, called while `current` is CONTROL at least 8000ms after the last interaction with no dialog open, moves `current` to MAIN and returns MAIN — the timer fires on Control exactly as on Projection
- `checkInactivity`, called less than 8000ms after the last interaction, leaves `current` unchanged
- `checkInactivity`, called while `current` is HOME, PREPARATION, MAIN or END, leaves `current` unchanged however much time has elapsed
- `onInteraction` resets the elapsed-time baseline: a `checkInactivity` call just under 8000ms after it leaves `current` unchanged
- while a dialog is open (`onDialogOpened` called, `onDialogClosed` not yet called), `checkInactivity` leaves `current` unchanged even past 8000ms since the last interaction
- `onDialogClosed(atElapsedRealtime)` rearms the timer as of that instant: a `checkInactivity` call just under 8000ms later leaves `current` unchanged; at or past 8000ms later it moves `current` (PROJECTION or CONTROL) to MAIN

## Dependencies

SegmentMarkingController — pre-existing (lot-15)
