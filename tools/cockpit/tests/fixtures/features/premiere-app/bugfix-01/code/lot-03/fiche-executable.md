## Signatures

LinkStateMonitor.observeLinkEstablished(): Flow<Unit>

Emits once on every transition of the phone-watch link from
not-established to established. Emits nothing at subscription time
when the link is already established, and nothing while the link
stays not-established.

## Acceptance criteria

- The link transitioning from not-established to established emits
  once
- Subscribing while the link is already established produces no
  emission at subscription time
- The link transitioning to established, then lost, then established
  again emits a second time on the second transition

## Dependencies

— (new symbol, no pre-existing dependency)
