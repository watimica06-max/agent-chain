## Signatures

HapticFeedbackImpl (Modification)
  @Inject constructor(@ApplicationContext context: Context)         — unchanged
  private val vibrator: Vibrator?                                   — was `Vibrator` (unchecked `as`); now obtained through `context.getSystemService(Context.VIBRATOR_SERVICE) as? Vibrator`
  override fun confirmMarking(): Unit                               — unchanged signature; no-ops when `vibrator` is null, same as it already no-ops when `vibrator.hasVibrator()` is false
  override fun cancelMarking(): Unit                                — unchanged signature; same no-op rule

## Acceptance criteria

- `confirmMarking()` does not throw when `getSystemService(VIBRATOR_SERVICE)` returns something other than a `Vibrator` (or null)
- `cancelMarking()` does not throw under the same condition

## Dependencies

HapticFeedback — pre-existing
Vibrator — pre-existing (android platform)

## Conventions

§5 R20 · missing data crosses a boundary as a nullable, never an invented default
§6 R33 · a call leaving the process (`getSystemService`) is handled as a value, not left to throw
§10 R55 · every public function has a nominal and a failure test
§10 R56 · no test reaches a real `Vibrator`; the system service is faked

## Requests

—
