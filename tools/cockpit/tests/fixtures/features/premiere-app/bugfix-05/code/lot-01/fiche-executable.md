## Signatures

DesignTokens.Typography.Watch.display: TextUnit
DesignTokens.Typography.Watch.displaySm: TextUnit
DesignTokens.Typography.Watch.value: TextUnit
DesignTokens.Typography.Watch.valueSm: TextUnit
DesignTokens.Typography.Watch.badge: TextUnit
DesignTokens.Typography.Watch.title: TextUnit
DesignTokens.Typography.Watch.label: TextUnit
DesignTokens.Typography.Watch.labelSm: TextUnit
DesignTokens.Typography.Watch.caption: TextUnit

Each becomes a `@Composable` getter (today a fixed `val`), resolving at
render time as base-pixels × (current watch face width in pixels ÷
480), converted to the `sp` a `Text`'s `fontSize` expects. Base pixels
per token are unchanged from today's constants: display 110, displaySm
80, value 48, valueSm 40, badge 37, title 33, label 24, labelSm 20,
caption 18. Call sites keep the same property-access syntax — none of
them changes.

## Acceptance criteria

- At a watch face width of 480px (density 1, fontScale 1), each of the
  nine tokens resolves to its base pixel value in sp: display 110.sp,
  displaySm 80.sp, value 48.sp, valueSm 40.sp, badge 37.sp, title
  33.sp, label 24.sp, labelSm 20.sp, caption 18.sp
- At a watch face width of 240px (density 1, fontScale 1), each of the
  nine tokens resolves to half its base pixel value in sp: display
  55.sp, displaySm 40.sp, value 24.sp, valueSm 20.sp, badge 18.5.sp,
  title 16.5.sp, label 12.sp, labelSm 10.sp, caption 9.sp

## Dependencies

None — `TextUnit` and the px→sp conversion are framework types
(`androidx.compose.ui.unit`), not project symbols.

## Conventions

§14 · Compose UI tests are written in `src/test`, with Robolectric —
DesignTokensTest now exercises a `@Composable` getter and needs a
compose test rule, not a plain JUnit assertion on a static value
