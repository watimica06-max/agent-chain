## Signatures

ProfileRepositoryImpl.observe(): Flow<Profile>
  — unchanged signature and unchanged emissions on success; a failure
    raised while collecting profileDao.observe() is caught inside the
    flow (a `.catch` on the existing map/flowOn chain) and never
    propagates as an uncaught exception to observe()'s own collector

## Acceptance criteria

- Collecting observe() while profileDao.observe() raises does not propagate an uncaught exception to the collector

## Dependencies

ProfileDao — pre-existing (observe(): Flow<ProfileEntity?>)
Profile — pre-existing

## Conventions

R30 · no empty and no generic catch — the failure is guarded against crossing the boundary uncaught, not silently absorbed
R33 · a call leaving the process (Room, here) returns its failure as a value, never a thrown exception crossing the boundary
R42 · cooperative coroutines / Flow execution model — `.catch` is the flow-native guard matching this model

## Requests

architecte/detailleur-lot-10.md
