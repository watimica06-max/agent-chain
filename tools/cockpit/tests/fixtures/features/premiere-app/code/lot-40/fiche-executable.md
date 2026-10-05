## Signatures

enum class DisplayMode { NORMAL, POWER_SAVE }

AlwaysOnDisplayController.mode → DisplayMode
// starts NORMAL

AlwaysOnDisplayController.refreshIntervalMs → Long?
// SensorFreshnessWindow.WINDOW_MS (10 000) while POWER_SAVE, null while NORMAL
// (continuous refresh, no fixed interval)

AlwaysOnDisplayController.enterPowerSave() → DisplayMode
// sets mode to POWER_SAVE

AlwaysOnDisplayController.exitPowerSave() → DisplayMode
// called on a wrist raise or a screen touch; sets mode to NORMAL

## Acceptance criteria

- A newly created controller reports mode NORMAL and a null refreshIntervalMs
- enterPowerSave() sets mode to POWER_SAVE and refreshIntervalMs to SensorFreshnessWindow.WINDOW_MS (10 000ms), overriding the platform's once-per-minute default
- exitPowerSave(), called after a wrist raise or a screen touch, returns mode to NORMAL and clears refreshIntervalMs to null

## Dependencies

SensorFreshnessWindow — produced by lot-03 (WINDOW_MS supplies the power-save refresh interval)
DesignTokens — produced by lot-02 (Idle token variants; applied downstream by the screens that read `mode`, not referenced directly by this signature)
