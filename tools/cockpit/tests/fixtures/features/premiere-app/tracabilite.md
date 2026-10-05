# Traçabilité — desc-produit.md → spec-technique.md

Pour chaque bloc, les entrées §X.Y de `spec-technique.md` qui portent
au moins une de ses règles. — signifie qu'aucune entrée n'en porte
aucune. Seules les entrées §X.Y comptent (50 au total) ; le préambule
et les en-têtes §1..§12 eux-mêmes n'en sont pas.

    B1  Race segment structure                          §1.1
    B2  Color tokens                                     §1.2
    B3  Typography tokens                                 §1.2
    B4  Shape, spacing and zone-arc tokens                 §1.2
    B5  Idle display token variants                        §1.2
    B6  Race list screen                                   §9.1
    B7  Race detail screen                                 §9.2
    B8  Setting a race as the reference                    §2.1, §9.2
    B9  Renaming a race                                    §2.1, §9.2
    B10 Deleting a race                                    §2.1, §9.2
    B11 Paste-a-result screen                              §9.3
    B12 Reading and validating a pasted result              §5.1
    B13 Preview before saving                               §9.4
    B14 Saving an imported race                             §2.1, §8.2
    B15 Paste error screen                                  §9.5, §10.4
    B16 Profile screen                                      §9.6
    B17 Deriving maximum heart rate                          §5.2
    B18 Zone ranges from maximum heart rate                  §3.1, §9.6
    B19 Editing profile settings                             §2.2
    B20 Sensor permission request                            §4.1, §9.7
    B21 Waiting for the phone                                §9.8
    B22 Home screen                                          §9.9
    B23 Watch history screen                                 §9.10
    B24 Preparing and launching a race                       §4.2, §9.11
    B25 Starting when another app holds the sensor           §4.2, §9.11
    B26 Resuming our own already-active race                 §4.2
    B27 Marking a segment                                    §4.3, §8.1
    B28 Main page, adapting to the current segment           §9.12
    B29 Data freshness on the race pages                     §1.3
    B30 Projection page                                      §9.13
    B31 Control page                                         §9.14
    B32 Undoing the last marking                             §4.4, §9.14
    B33 Stopping the race                                    §4.5, §9.14
    B34 End-of-race screen                                   §9.15
    B35 Always-on display during the race                    §9.16
    B36 allure-segment and allure-lissee                     §3.2
    B37 Computing the correction factor                      §3.3
    B38 Starting factor and fallback                         §2.2, §3.3
    B39 Lap delta                                             §3.4
    B40 Cumulative delta and estimated arrival                §3.5
    B41 Trend arrow                                           §3.6
    B42 Zone switching hysteresis                             §3.1
    B43 Sending profile and reference to the watch            §6.1, §9.6, §9.9
    B44 Receiving recorded races from the watch               §6.2
    B45 Exercise session lifecycle                            §5.3, §9.17
    B46 Monotonic timing and recovery                         §2.3
    B47 Duration formats                                      §10.1
    B48 Delta format                                          §10.1
    B49 Pace, heart rate, position and zone formats           §10.1
    B50 Settings and range formats                            §10.1
    B51 Date formats                                          §10.1
    B52 Rounding rule                                         §3.7
    B53 Text resource rules                                   §10.2
    B54 Dynamic texts and fallbacks                           §10.3
    B55 Relative date wording                                 §10.1
    B56 Fixed text catalogue                                  §10.4
    B57 Phone navigation map                                  §8.2
    B58 Watch navigation map                                  §8.3, §8.1
    B59 Measured and displayed physiological data             —
    B60 Heart-rate data consent                               §11.1
    B61 Connectivity permission denied                        §11.2, §9.18

## Notes — règles isolées ne se retrouvant nulle part

- **B10**, la phrase « Once the deletion is confirmed, the app returns
  to the race list » : ni §2.1 (Delete), ni §9.2, ni §8.2 (carte de
  navigation) ne portent cette transition de retour.
- **B19**, « a short message states the constraint » lors d'un rejet
  de borne : §2.2 renvoie vers « §10.1's constraint message », mais
  §10.1 ne définit aucune entrée de ce nom — le texte du message
  n'existe nulle part.
- **B20**, le rappel sur l'écran d'accueil (« a reminder on the home
  screen asks the system for the permission again ») : §4.1 renvoie
  vers « §9.9's home-screen reminder », mais §9.9 ne décrit aucun
  élément de rappel — seul le badge « Aucune référence » y figure.
- **B59** lui-même : son contenu ne vit que dans le préambule
  (« Out of scope », annoté *(product: B59)*), jamais dans une entrée
  §X.Y.
