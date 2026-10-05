## What I need

A documented, working way to assert a rendered Compose node's actual
pixel opacity from this project's Robolectric-only unit tests — or
confirmation that no such way exists and a different technique is the
project's standard for this class of assertion.

## Why the lot cannot proceed

It does proceed — the FAIL mineur's criterion now has a compose-level
test in `MainRacePageScreenTest.kt`. What it does not use is pixel
capture, because none of the three techniques tried against this
project's test setup produces real pixels:

- `SemanticsNodeInteraction.captureToImage()` — the officially
  documented way — throws `ComposeTimeoutException` inside
  `WindowCapture_androidKt.forceRedraw`'s `waitUntil`: it waits on a
  window frame-commit callback this Robolectric runner never fires.
- Manually drawing the compose host view onto a software `Bitmap`
  (`view.draw(Canvas(bitmap))`, bypassing the window/`PixelCopy` path
  entirely) compiles and runs, but produces an all-black bitmap — not
  even the screen's own opaque background paints — so this app's
  `AndroidComposeView` does not render through a plain software
  `Canvas.draw()` call either.
- `SemanticsNode.layoutInfo.getModifierInfo()` does expose the
  `GraphicsLayerElement` `Modifier.Node` a rendered node carries (its
  `toString()` includes the real `alpha` value applied), but that
  element type is private to its declaring file, so a test cannot cast
  to it — only read its `toString()`, which is what the delivered test
  does.

## Where I met it

`code/lot-41/verdict.md`'s FAIL mineur, asking for "a compose test ...
asserting the opacity difference on a rendered node's opacity in
either mode" in
`app-wear/src/test/java/com/mgilli/app_wear/race/MainRacePageScreenTest.kt`.
There is no `androidTest` source set anywhere in this project — every
existing Compose UI test is a Robolectric unit test — so no
instrumented alternative was available to fall back to either.

## What I think it is

add — a trap on `CURRENT_TECHNICAL_STATE.md`: a Compose UI test in this
project cannot assert a rendered node's actual pixel opacity.
`captureToImage()` times out waiting on a window frame-commit callback
Robolectric never fires, and there is no `androidTest` source set to
run it on a real window instead. The nearest working substitute is
reading the `GraphicsLayerElement` `Modifier.Node`'s own `toString()`
off `SemanticsNode.layoutInfo.getModifierInfo()` — present only when a
`Modifier.alpha()` value differs from its default (full opacity) — since
the element type itself is private and cannot be cast to.

## Verdict

**Not a convention. It belongs to `CURRENT_TECHNICAL_STATE.md`, which
this agent does not write.** No rule added to
`docs/TECHNICAL_CONVENTIONS.md`.

It fails the same filter as `realisateur-lot-43.md`'s daemon-reliability
request:

- **This is a fact about the test framework's own limits, not a choice
  the project made.** No convention was picked between two working
  ways to assert rendered opacity; only one path exists, and it does
  not work here. Checked against Robolectric's own tracker rather than
  recalled: `captureToImage()` timing out inside
  `WindowCapture_androidKt.forceRedraw` on a frame-commit callback that
  never fires is a documented Robolectric/Compose interaction
  (robolectric/robolectric#8071, robolectric/robolectric#6756) — the
  screenshot-capable path Robolectric does support goes through a
  dedicated `captureRoboImage()` API and `@GraphicsMode(NATIVE)`, a
  different mechanism from `captureToImage()`, and adopting it is a
  tooling change (a new test dependency), not a rule about how this
  project's code is written.
- **No platform mechanism turns "this call times out here" into a
  project standard.** There is nothing to standardise on beyond what
  R56/R81 already require: a test does not reach a real window, and a
  Robolectric-shadowed `android.*` call is exercised under
  `RobolectricTestRunner` — both already rules of this file, and both
  already followed by the delivered test.
- **No tool of R65's table checks this either** — it is a report on
  what one API does inside this project's test setup, not a rule about
  the code.

**Where it belongs.** The request's own "What I think it is" already
names the right destination: a trap entry on
`CURRENT_TECHNICAL_STATE.md`, which the Détailleur and the Réalisateur
read and write — not this file, and not this agent. The substance to
carry there is exactly what the request states: `captureToImage()`
times out waiting on a frame-commit callback Robolectric never fires in
this project's setup, there is no `androidTest` source set to fall back
to, and the nearest working substitute is reading the
`GraphicsLayerElement` `Modifier.Node`'s `toString()` off
`SemanticsNode.layoutInfo.getModifierInfo()`.
