## Signatures

    object DesignTokens {

      object Color {
        val surface: Color
        val surfaceRaised: Color
        val screenBlack: Color
        val textPrimary: Color
        val textBody: Color
        val textSecondary: Color
        val textTertiary: Color
        val border: Color
        val borderStrong: Color
        val ahead: Color
        val aheadText: Color
        val aheadBg: Color
        val behind: Color
        val behindText: Color
        val behindBg: Color
        val deltaZero: Color
        val link: Color
        val zone1: Color
        val zone2: Color
        val zone3: Color
        val zone4: Color
        val zone5: Color
      }

      object Typography {
        val fontLabel: FontFamily          // running text, labels, titles
        val fontData: FontFamily           // every timed value, always weight 700

        val letterSpacingLabel: TextUnit         // normal-size uppercase labels
        val letterSpacingGroupHeader: TextUnit   // group headers, small-size uppercase mentions
        val letterSpacingControlTitle: TextUnit  // Control page title only
        // running text and any fontData value carry no letter-spacing

        object Phone {
          val title: TextUnit
          val value: TextUnit
          val body: TextUnit
          val label: TextUnit
          val data: TextUnit
          val caption: TextUnit
        }

        object Watch {
          val display: TextUnit
          val displaySm: TextUnit
          val value: TextUnit
          val valueSm: TextUnit
          val badge: TextUnit
          val title: TextUnit
          val label: TextUnit
          val labelSm: TextUnit
          val caption: TextUnit
        }
      }

      object Shape {
        val radiusCard: Dp
        val radiusChip: Dp
        fun radiusPill(elementHeight: Dp): Dp   // half the element's own height
      }

      object Spacing {
        object Phone { val xs: Dp; val s: Dp; val m: Dp; val l: Dp; val xl: Dp }
        object Watch { val xs: Dp; val s: Dp; val m: Dp; val l: Dp; val xl: Dp }
      }

      object ZoneArc {   // watch only
        val radius: Dp
        val totalSpanDeg: Float
        val segmentSpanDeg: Float
        val gapDeg: Float
        val width: Dp             // inactive
        val widthActive: Dp
        val opacityIdle: Float
        val opacityActive: Float
        val activeSegmentRadius: Dp   // radius + width/2 - widthActive/2
      }

      object Idle {   // watch power-save variants only
        val textOpacity: Float           // text-primary and any timed value
        val secondaryTextOpacity: Float  // text-secondary and text-tertiary
        val deltaColorOpacity: Float     // ahead/behind/delta-zero, hue unchanged
        val arcWidthDim: Dp
        val arcWidthActiveDim: Dp
        val arcOpacityIdleDim: Float
      }
    }

Font weights use the framework's `FontWeight.Bold` (700), `FontWeight.SemiBold`
(600) and `FontWeight.Medium` (500) directly — no dedicated token.

## Acceptance criteria

- `DesignTokens.Color` exposes exactly: surface #121110, surface-raised #1C1A18, screen-black #000000, text-primary #F3EFE7, text-body #C9C4BA, text-secondary #9A958C, text-tertiary #6F6A62, border rgba(255,255,255,0.08), border-strong rgba(255,255,255,0.25), ahead #4FAE72, ahead-text #7FCB9C, ahead-bg rgba(79,174,114,0.16), behind #E2725F, behind-text #E2957F, behind-bg rgba(226,114,95,0.16), delta-zero #726D63, link #6FA3D8, zone-1 #4A90D9, zone-2 #35B0A4, zone-3 #4CAF63, zone-4 #E0A23A, zone-5 #E0503F
- `DesignTokens.Typography.fontLabel` is IBM Plex Sans and `DesignTokens.Typography.fontData` is IBM Plex Mono
- Only three font weights are ever used: 700 for titles, values and button labels; 600 for secondary labels and menu entries; 500 for detached units and low-emphasis actions
- `DesignTokens.Typography.letterSpacingLabel` is 0.04em, `letterSpacingGroupHeader` is 0.06em, `letterSpacingControlTitle` is 0.08em; running text and any `fontData` value carry no letter-spacing
- `DesignTokens.Typography.Watch` exposes exactly: display 110px, display-sm 80px, value 48px, value-sm 40px, badge 37px, title 33px, label 24px, label-sm 20px, caption 18px
- `DesignTokens.Typography.Phone` exposes exactly: title 22dp, value 20dp, body 15dp, label 13dp, data 12.5dp, caption 11dp
- `DesignTokens.Shape.radiusCard` is 12dp, `radiusChip` is 14dp, and `radiusPill(h)` equals `h / 2`
- `DesignTokens.Spacing.Phone` exposes xs 4dp, s 8dp, m 12dp, l 20dp, xl 32dp; `DesignTokens.Spacing.Watch` exposes the same scale multiplied by 1.83
- `DesignTokens.ZoneArc` exposes radius 229px, totalSpanDeg 140, segmentSpanDeg 25.6, gapDeg 3, width 13px, widthActive 33px, opacityIdle 0.30, opacityActive 1, and `activeSegmentRadius` equal to 219px (radius + width/2 - widthActive/2)
- `DesignTokens.Idle.textOpacity` is 0.55, `secondaryTextOpacity` is 0.45 (hue never changes for either), `deltaColorOpacity` is 0.55 applied to ahead/behind/delta-zero with their hue unchanged, `arcWidthDim` is 7px, `arcWidthActiveDim` is 22px, `arcOpacityIdleDim` is 0.25 — no other geometry changes in idle mode

## Dependencies

androidx.compose.ui.graphics.Color, androidx.compose.ui.unit.Dp,
androidx.compose.ui.unit.TextUnit, androidx.compose.ui.text.font.FontFamily,
androidx.compose.ui.text.font.FontWeight — framework (Jetpack Compose,
mandatory tech stack).
