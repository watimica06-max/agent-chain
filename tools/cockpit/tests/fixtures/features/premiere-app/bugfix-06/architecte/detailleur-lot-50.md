## What I need

A rule saying what keeps a read-modify-write consistent when it spans a
suspension: which of the read and the write may interleave with another
coroutine's, and what the boundary does when they do.

## Why the lot cannot proceed

It proceeds — the signatures are written against the conventions as they
stand — but nothing decides this point, and the two rules that come
closest pull apart. R43 bars holding anything across the suspending
database read, so two concurrent calls can each read the same stored race
and each write its own result, the second silently discarding the first.
R37 covers a *pair of writes* holding one invariant, which one Room
`@Transaction` already satisfies; it says nothing about a read and a
later write separated by a suspension. R42's "no shared mutable state
between coroutines" describes memory, not a row two coroutines both read
and both rewrite.

## Where I met it

`code/lot-50/fiche-executable.md` — `RaceRecordingRepositoryImpl`'s
`markSegment`, `undoLastMark`, `stopRace` and `markSent`, each of which
reads the stored race, derives a new one from it and writes it back,
with the lock released across the read. Reached concurrently by the watch
UI, `WatchRaceComplicationDataSourceService` and
`ProfileSyncListenerService`.

## What I think it is

add

## Verdict

**A convention, and a genuine gap between R37, R42 and R43. Written as R91
and R92, section 6 of `docs/TECHNICAL_CONVENTIONS.md`.**

Checked in this order:

- **Does the platform impose it?** No. Kotlin coroutines and Room leave
  both an application-held lock and a database transaction equally
  available around a read-modify-write cycle; nothing about the platform
  picks one on its own. What Room imposes once a transaction is chosen is
  serialization — checked against Room's own transaction-dispatcher
  behaviour and SQLite's single-writer semantics, not recalled: a
  suspending `androidx.room.withTransaction` block takes a thread of the
  transaction executor for its whole body, and the underlying SQLite
  connection admits one write transaction at a time regardless of
  executor size, so a second concurrent transaction cannot start — let
  alone read — until the first has committed.
- **Does a tool already check it?** No tool of R65's table reads meaning
  into where a transaction boundary sits; this is architecture, not a
  mechanical property.
- **Does the project already declare it?** Not this exact case. R37
  already trusts a Room `@Transaction` to make a *pair of writes* atomic
  against a concurrent reader, but only for that shape. R43 bars holding
  anything across the very suspension that stands between the read and
  the later write here. R42's "no shared mutable state between
  coroutines" describes memory, not a stored row two coroutines both read
  and both rewrite. **Each of the three is complete on its own** — the
  conflict only appears where a read and a later write meet across one
  suspension, exactly the edge a framing grid sweeping subject by subject
  cannot see, and `Consumes:` does not encode "reads, then later writes."

**R91 extends R37's own established technique — a Room transaction, not
an application lock — from a pair of writes to a read-then-derive-then-
write cycle.** `markSegment`, `undoLastMark`, `stopRace` and `markSent`
fold their read and their derived write into one `withTransaction` block
instead of releasing a `Mutex` across the read and reacquiring it to
write.

**R92 says why this satisfies R43 rather than reopening it.** No
application lock is held across the suspension — the atomicity is Room's
own transaction serialization. A second concurrent call's read is never
stale: its transaction cannot begin until the first commits, so it reads
what the first wrote, and the two calls never interleave. No separate
conflict-resolution rule is needed, because the interleaving the request
describes does not occur once both calls share a transaction boundary —
the second's write derives from the first's result, never discards it.

**Both off-grid, citing §7.2** — the entry R75, R76, R87 and R88 already
cite for `RaceRecordingRepositoryImpl`'s own contract: no C-entry of the
grid reaches what keeps a read and a later write consistent across a
suspension.

The four methods this request names proceed under R91/R92. 📌 The same
pair governs any later method of this repository, or of another
store-backed repository, whose write derives from a read a suspension
separates it from — the recurrence the request anticipates is why this
is written as a rule rather than settled for these four methods alone.
