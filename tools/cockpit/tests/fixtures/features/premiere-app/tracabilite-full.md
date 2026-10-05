# Traçabilité — bloc produit → lots

Croisement de `tracabilite.md` (bloc → entrées) et `tracabilite-2.md`
(entrée → lots). Union des lots de toutes les entrées d'un bloc,
dédoublonnée. — signifie qu'aucun lot n'en découle.

    B1  Race segment structure                     lot-01
    B2  Color tokens                                lot-02
    B3  Typography tokens                            lot-02
    B4  Shape, spacing and zone-arc tokens            lot-02
    B5  Idle display token variants                   lot-02
    B6  Race list screen                              lot-25
    B7  Race detail screen                            lot-26
    B8  Setting a race as the reference               lot-04, lot-26
    B9  Renaming a race                               lot-04, lot-26
    B10 Deleting a race                               lot-04, lot-26
    B11 Paste-a-result screen                         lot-27
    B12 Reading and validating a pasted result         lot-18
    B13 Preview before saving                          lot-28
    B14 Saving an imported race                        lot-04, lot-24
    B15 Paste error screen                             lot-29, lot-43, lot-44
    B16 Profile screen                                 lot-30
    B17 Deriving maximum heart rate                     lot-19
    B18 Zone ranges from maximum heart rate             lot-07, lot-30
    B19 Editing profile settings                        lot-05
    B20 Sensor permission request                       lot-13, lot-31
    B21 Waiting for the phone                           lot-32
    B22 Home screen                                     lot-33
    B23 Watch history screen                            lot-34
    B24 Preparing and launching a race                  lot-14, lot-35
    B25 Starting when another app holds the sensor      lot-14, lot-35
    B26 Resuming our own already-active race            lot-14
    B27 Marking a segment                               lot-15, lot-23
    B28 Main page, adapting to the current segment      lot-36
    B29 Data freshness on the race pages                lot-03
    B30 Projection page                                 lot-37
    B31 Control page                                    lot-38
    B32 Undoing the last marking                        lot-16, lot-38
    B33 Stopping the race                               lot-17, lot-38
    B34 End-of-race screen                              lot-39
    B35 Always-on display during the race               lot-40
    B36 allure-segment and allure-lissee                lot-08
    B37 Computing the correction factor                 lot-08
    B38 Starting factor and fallback                    lot-05, lot-08
    B39 Lap delta                                       lot-09
    B40 Cumulative delta and estimated arrival          lot-10
    B41 Trend arrow                                     lot-11
    B42 Zone switching hysteresis                       lot-07
    B43 Sending profile and reference to the watch      lot-21, lot-30, lot-33
    B44 Receiving recorded races from the watch         lot-22
    B45 Exercise session lifecycle                      lot-20, lot-41
    B46 Monotonic timing and recovery                   lot-06
    B47 Duration formats                                lot-42
    B48 Delta format                                    lot-42
    B49 Pace, heart rate, position and zone formats     lot-42
    B50 Settings and range formats                      lot-42
    B51 Date formats                                    lot-42
    B52 Rounding rule                                   lot-12
    B53 Text resource rules                             lot-43, lot-44
    B54 Dynamic texts and fallbacks                     lot-43, lot-44
    B55 Relative date wording                           lot-42
    B56 Fixed text catalogue                            lot-43, lot-44
    B57 Phone navigation map                            lot-24
    B58 Watch navigation map                            lot-23
    B59 Measured and displayed physiological data       —
    B60 Heart-rate data consent                         —
    B61 Connectivity permission denied                  lot-45, lot-30, lot-33
