## Signatures

PhoneNavigationStateStore(context: Context) — :app-phone
  fun save(serializedStack: String) — persists the given string, overwriting
    whatever was previously saved
  fun restore(): String? — returns the string last given to `save`, or null
    when `save` was never called

## Acceptance criteria

- `save(x)` followed by `restore()` on a `PhoneNavigationStateStore` built
  from the same `Context` returns `x`
- `restore()` on a `PhoneNavigationStateStore` that has never had `save`
  called on it (or on its stored state) returns null
- `save(x)` then `save(y)` then `restore()` returns `y`, never `x`

## Dependencies

Context — pre-existing (android.content.Context)

## Conventions

R46 · anything the application must find again after the process dies is written where it survives, as it changes, and read back from there
R39 · no mutable global state outside the entry point — the persisted value lives behind this instance, not a top-level property
R63 · identifiers and doc line in English, stating what the symbol guarantees and when it fails

## Requests

—
