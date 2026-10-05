## What I need

A confirmation that two tooling workarounds, neither named by the sheet
or the conventions, are the right calls — or a rule saying so, so the
next lot that hits either does not have to rediscover them.

## Why the lot cannot proceed

It proceeds — this is not a blocker.

1. `MainActivity.healthConnectClient` becomes `@Inject var
   healthConnectClient: HealthConnectClient? = null` per the sheet
   (`lateinit` cannot carry a nullable type). Left as a bare `var`, KSP's
   Dagger processor fails with *"Dagger does not support injection into
   private fields"* — Kotlin compiles every non-`lateinit` property to a
   private backing field with synthetic accessors, and Dagger's generated
   injector assigns the field directly rather than through a setter.
   `@JvmField` on the property is the fix; it makes the fix Dagger's
   generated code needs happy without changing the property's own type or
   visibility.

2. `FakePlatformModule` is `@TestInstallIn`-global (every test in
   `:app-phone`'s test source set sees it); this lot's acceptance
   criteria need `MainActivity` built once with no `HealthConnectClient`
   and once with a client whose `PermissionController` is controllable —
   two different values from the same binding, in two different test
   classes. `@UninstallModules` rejects a `@TestInstallIn` module (KSP:
   *"should only include modules annotated with both @Module and
   @InstallIn"*), and a second `@TestInstallIn` module replacing the same
   production module conflicts with the first everywhere
   (`Dagger/DuplicateBindings`), not just in the one test class meant to
   use it. The only working seam found is a mutable top-level `var` that
   `FakePlatformModule.provideHealthConnectClient` reads instead of a
   hardcoded value, set by the one test needing a different value and
   restored after — recorded in `docs/CURRENT_TECHNICAL_STATE.md` under
   `FakePlatformModule` and under a new general trap. That var must be
   set from an instance `init` block, not `@Before`: a
   `createAndroidComposeRule<T>` launches the Activity (and runs its
   Hilt field injection) while the `@Rule` chain is still applying,
   before any `@Before` method runs — setting it there is too late.

## Where I met it

1. `./gradlew :app-phone:kspDebugKotlin`, right after widening
   `MainActivity.healthConnectClient` to `HealthConnectClient?` per the
   sheet.

2. Writing `MainActivityWithoutHealthConnectClientTest` and
   `MainActivityWithHealthConnectClientBoundTest` (new, this lot) against
   the existing `FakePlatformModule`, which the sheet notes needs no
   change for the type to keep compiling — true, but insufficient once a
   test needs a *different value* out of it.

## What I think it is

add — two entries: `@JvmField` alongside a nullable `@Inject var` field
on an `@AndroidEntryPoint` Activity/Fragment (a rule the KSP error
otherwise takes a full compile-and-fail cycle to discover), and the
`@TestInstallIn`/`@UninstallModules` incompatibility together with the
`init`-block-not-`@Before` timing rule for varying a global fake's value
per test class.

## Verdict

**Both a convention. Written as R83, section 7, and R84, section 10, of
`docs/TECHNICAL_CONVENTIONS.md`.** The two workarounds are the right
calls; both lots proceed as written.

**1. `@JvmField`.** Checked against Kotlin's own property compilation
and Dagger's generated `MembersInjector`, not recalled: a `lateinit var`
compiles to a directly-accessible field, which is why field injection
normally needs no annotation — but `lateinit` cannot carry a nullable
type. A plain `var` instead compiles to a private backing field with
synthetic accessors, which Dagger's generated injector cannot assign
directly, hence the KSP failure. **The platform does not impose exactly
this fix** — Dagger also supports setter injection (`@set:Inject` on an
`internal`-or-wider `var`, confirmed against a working example) — so a
choice exists, and it is a convention, not a platform necessity. R83
picks `@JvmField` because it keeps every `@Inject` field of this project
on the same field-injection style; setter injection would put one field
on a different mechanism from the rest for no reason tied to this lot.

**2. The mutable top-level `var`.** Checked against Dagger's own testing
guide and a live Dagger issue, not recalled: `@UninstallModules` cannot
target a `@TestInstallIn` module, confirming the first wall met.
`@BindValue` is the platform's purpose-built answer to "a different
value per test class" — but it requires the type not be bound by a
competing module in the same component, and `FakePlatformModule`'s
`HealthConnectClient` binding is exactly that competing module, reaching
every other test of `:app-phone`'s source set that constructs a
Hilt-built component, not only this lot's two. Pulling that binding out
of the shared module to make room for `@BindValue` would touch every
existing test relying on its default — beyond this lot's own scope.
**The mutable top-level `var`, read by the one existing provider, is
what stays inside the lot's own footprint**, and R84 confirms it as the
project's convention for this shape of problem, scoped to test doubles
so it does not reopen R39.

**The `init`-block timing is a platform fact, not a project choice**:
Dagger's own testing guide states in as many words that a value a
`createAndroidComposeRule`-driven Activity injects must be set before
any `@Before` runs, or the Activity can inject it in its uninitialised
state — the same constraint this lot met, independently, on the fake's
`var`. R84 carries it so the next lot does not rediscover it either.

**Both written under `§5.2`**: the entry giving `:app-phone` its Health
Connect Client (R12's table, R65's Health Connect Client row) is what
puts a nullable, platform-constructed `HealthConnectClient` on
`MainActivity` in the first place, and both rules exist only because
that entry does.

