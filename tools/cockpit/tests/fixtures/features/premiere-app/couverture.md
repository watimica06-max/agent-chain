# Coverage — spec-technique.md → conventions-5.md

One line per entry of the technical document, in its order.

    §1.1    N1   → R12, R16, R17, R57, R60
    §1.2    N1   → R12, R64
    §1.3    N1   → R12, R20, R27 ; Q5
    §2.1    N2   → R8, R12, R16, R21, R23, R37, R46, R57, R61
    §2.2    N2   → R12, R21, R46, R50, R57 ; Q7
    §2.3    N2   → R12, R29, R37, R46, R49, R61
    §3.1    N3   → R12, R27, R28, R41, R57, R59
    §3.2    N3   → R12, R22, R27, R41, R59 ; Q2
    §3.3    N3   → R12, R22, R41, R59
    §3.4    N3   → R12, R22, R41, R57, R59 ; Q2, Q4
    §3.5    N3   → R12, R41, R59
    §3.6    N3   → R12, R27, R41, R59
    §3.7    N3   → R12, R29, R41, R59
    §4.1    N4   → R12, R33, R36, R52, R58 ; Q7
    §4.2    N4   → R12, R33, R35, R48, R58
    §4.3    N4   → R12, R35, R37, R58, R61
    §4.4    N4   → R12, R35, R58
    §4.5    N4   → R12, R35, R37, R58, R61
    §5.1    N5   → R12, R13, R22, R32, R33, R62 ; Q3
    §5.2    N5   → R12, R13, R20, R32, R33
    §5.3    N5   → R12, R13, R33, R48, R52
    §6.1    N6   → R12, R13, R19, R23, R32, R37, R38, R61, R68
    §6.2    N6   → R12, R13, R19, R23, R32, R38, R48, R61, R68
    §7      N7   → no entry (nature empty)
    §8.1    N8   → R12, R44
    §8.2    N8   → R12, R44
    §8.3    N8   → R12, R35, R44, R58
    §9.1    N9   → R12, R14, R45, R47, R64
    §9.2    N9   → R12, R14, R20, R45, R47, R64 ; Q3, Q4
    §9.3    N9   → R12, R14, R45, R64
    §9.4    N9   → R12, R14, R45, R64
    §9.5    N9   → R12, R14, R45, R64
    §9.6    N9   → R12, R14, R21, R45, R47, R64 ; Q1
    §9.7    N9   → R12, R14, R64
    §9.8    N9   → R12, R14, R52, R64
    §9.9    N9   → R12, R14, R47, R64 ; Q1, Q7
    §9.10   N9   → R12, R14, R47, R62, R64
    §9.11   N9   → R12, R14, R48, R64
    §9.12   N9   → R12, R14, R20, R47, R64 ; Q3, Q5
    §9.13   N9   → R12, R14, R47, R64
    §9.14   N9   → R12, R14, R64
    §9.15   N9   → R12, R14, R48, R64
    §9.16   N9   → R12, R14, R47 ; Q5
    §9.17   N9   → R12, R14, R48
    §9.18   N9   → R12, R14, R64 ; Q1
    §10.1   N10  → R12, R29, R64 ; Q7
    §10.2   N10  → R12, R15, R64 ; Q3
    §10.3   N10  → R12, R64
    §10.4   N10  → R9, R12, R64 ; Q3, Q7
    §11.1   N11  → R12, R54, R68
    §11.2   N11  → R12, R33, R36, R52 ; Q1
    §12     N12  → no entry (nature empty)

📌 Fifty §X.Y entries, all present above. §7 and §12 carry no entry.

📌 Entries that fired no rule of their own: none. Rules the sweep did
not write: G3.1 (no entry describes a derived artefact), G4.1 (V2 holds
a cycle — Q1), G4.7 (raises Q1 rather than a rule), G8.1 (§12 empty —
covered off-grid by R52), G12.4 (N5 non-empty — covered off-grid by
R68).

---

## Rules, their grid entry, and how each is tested

    R1    G1.1       none — the only rule of the file with no test
    R2    G1.2       review
    R3    G1.3       review
    R4    G2.1       mechanical
    R5    G2.2       mechanical
    R6    G2.3       review
    R7    G3.2       mechanical
    R8    G3.3       review
    R9    G3.4       review
    R10   G4.2       mechanical
    R11   G4.3       mechanical
    R12   G4.4       review
    R13   G4.5       mechanical
    R14   G4.6       mechanical
    R15   G4.8       review
    R16   G4.9       test on the exported schema
    R17   G5.1       review
    R18   G5.2       review
    R19   G5.3       review
    R20   G5.4       review
    R21   G5.11      test per entry point of each bounded value
    R22   G5.10      test per uncomputable input
    R23   G5.5       review
    R24   G5.8       review
    R25   G5.9       review
    R26   G5.6       mechanical
    R27   G5.7       review
    R28   off-grid   test
    R29   off-grid   test
    R30   G6.1       mechanical
    R31   G6.2       review
    R32   G6.3       review
    R33   G6.8       failure-injection test per boundary
    R34   G6.9       mechanical
    R35   G6.4       review
    R36   G6.5       review
    R37   G6.6       failure-injection test per write
    R38   G6.7       review
    R39   G7.1       review
    R40   G7.2       mechanical
    R41   G7.3       mechanical
    R42   G7.4       review
    R43   G7.9       review
    R44   G7.5       review
    R45   G7.6       test per screen holding state
    R46   G7.10      test per surviving thing, killing between two steps
    R47   G7.7       mechanical
    R48   G7.8       review
    R49   off-grid   review
    R50   G8.2       mechanical
    R51   G8.3       review
    R52   off-grid   start-up test per prerequisite
    R53   G9.1       mechanical
    R54   G9.2       mechanical
    R55   G10.1      review
    R56   G10.2      mechanical
    R57   G10.3      test per fact
    R58   G10.4      test per transition
    R59   G10.5      test per entry
    R60   G10.6      one test
    R61   G10.7      test per write
    R62   G11.1      review
    R63   G11.2      review
    R64   G11.3      mechanical
    R65   G12.1      mechanical
    R66   G12.2      mechanical
    R67   G12.3      review
    R68   off-grid   review

📌 Sixty-eight rules, of which five carry `off-grid` (R28, R29, R49,
R52, R68). ⚠️ Twenty are mechanical and must be wired into
`./gradlew check` for R6 to hold.
