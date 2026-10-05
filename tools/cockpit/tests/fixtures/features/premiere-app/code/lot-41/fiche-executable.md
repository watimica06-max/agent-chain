## Signatures

WatchComplicationEntry.entryPoint(current: WatchDestination) → WatchComplicationEntry

## Acceptance criteria

- With MAIN as the current page, the complication's entry point targets MAIN
- With PROJECTION as the current page, the complication's entry point targets PROJECTION
- With CONTROL as the current page, the complication's entry point targets CONTROL
- With HOME as the current page (outside a race), the complication's entry point targets HOME

## Dependencies

WatchDestination — produced by lot-23
WatchRaceNavigator — produced by lot-23 (its `current` property is the input)
