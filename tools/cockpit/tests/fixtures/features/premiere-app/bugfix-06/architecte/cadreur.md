## What I need

R12's module table to name `:core-platform` as the module realising §11.1,
in place of `:core-sync`.

## Why the lot cannot proceed

R12 assigns §11.1 to `:core-sync` — the only module lot-14 could build
`ConnectivityPermissionSystemImpl` in under the conventions as written.
`core-sync/build.gradle.kts` declares neither `androidx.activity` nor
`androidx.core`, and R66 forbids adding a dependency inside a lot; the
Détailleur blocked on exactly this (`code/lot-14/blocked_detailleur.md`).
The Product Owner's filled Decision on that sheet moves the realisation to
a new module, `:core-platform`, created on its own lot before lot-14,
carrying those two dependencies so `:core-sync` — the Data Layer module —
does not gain either. `code/decoupage.md` is now cut against that
decision; R12 itself still names `:core-sync` for §11.1.

## Where I met it

`docs/TECHNICAL_CONVENTIONS.md` R12 (module table); `code/lot-14/blocked_detailleur.md`
(the Decision); `code/decoupage.md` lot-14 and lot-54.

## What I think it is        update

R12's table: `:core-platform` replaces `:core-sync` as the module
realising §11.1; `:core-sync` keeps §6.1, §6.2 alone.

## Verdict

**A convention, and R12 already carried its form — only its table was
stale.** Neither the platform nor a tool settles which module realises
an entry; `settings.gradle.kts` confirms `:core-platform` does not exist
yet and `core-sync/build.gradle.kts` confirms it declares neither
`androidx.activity` nor `androidx.core`, matching the sheet's account.
R12's table is corrected: `:core-sync` keeps §6.1, §6.2 alone;
`:core-platform` is added as the module realising §11.1. Written into
`docs/TECHNICAL_CONVENTIONS.md`, section 4.

