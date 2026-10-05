## Signatures

    sealed class Freshness<out T> {
      data class Fresh<T>(val value: T) : Freshness<T>()
      object Stale : Freshness<Nothing>()
    }

    object SensorFreshnessWindow {
      const val WINDOW_MS: Long = 10_000

      fun <T> evaluate(value: T, lastReadingAt: Long, now: Long): Freshness<T>
      // lastReadingAt and now are monotonic instants in milliseconds
      // (SystemClock.elapsedRealtime()), per the timing convention.
    }

## Acceptance criteria

- `evaluate` with `now - lastReadingAt` at 9999ms returns `Fresh(value)`
- `evaluate` with `now - lastReadingAt` at exactly 10000ms returns `Fresh(value)`
- `evaluate` with `now - lastReadingAt` at 10001ms returns `Stale`
- `Stale` carries no value, so a caller past the window cannot keep rendering the last reading
- The evaluation applies identically whether the display is in normal or power-save mode — `evaluate` takes no mode parameter

## Dependencies

None — generic over the displayed value's type.
