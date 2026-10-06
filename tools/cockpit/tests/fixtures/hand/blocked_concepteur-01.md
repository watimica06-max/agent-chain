## What blocks

The sheet's `RaceClock.now()` returns `Instant`, and the module has no `java.time` on its classpath.

## Where

`RaceClock.now`, code/lot-12/fiche-executable.md, `## Signatures` line 3

## To resume

Say which type the signature takes.

Options:
- La signature rend un `Long`, des millisecondes depuis l'époque.
- Le module reçoit `java.time` et la signature reste telle quelle.

## Decision

La signature rend un `Long`, des millisecondes depuis l'époque.
