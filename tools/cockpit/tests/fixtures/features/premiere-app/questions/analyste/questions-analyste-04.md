### Q1
Block: B42 — Zone switching hysteresis
Question: When a heart-rate reading places the raw value two or more zones away from the currently active zone — a jump spanning more than one boundary in a single reading, with no gap in readings in between — does the zone advance one boundary at a time under the hysteresis rule, or does it move directly to the zone containing the raw value?
Answer: La zone affichée est directement celle qui contient la valeur brute, sans passer par les zones intermédiaires.

L'hystérésis décale une frontière, elle ne limite pas la vitesse de changement. Seule la frontière entre la zone active et sa voisine immédiate est décalée de 3 bpm ; toutes les autres s'appliquent telles quelles. Une lecture qui franchit deux frontières d'un coup n'est pas une oscillation, c'est un vrai changement d'effort, et le retarder afficherait une zone fausse. [integrated: B42]

### Q2
Block: B61 — Connectivity permission denied
Question: What does tapping "Autoriser" do — does it reopen the system's connectivity permission request, or does it open the device's system settings, the way block B20's equivalent action does for the sensor permission?
Answer: Le bouton demande d'abord l'autorisation au système. Si le système n'affiche plus la boîte de demande — refus définitif ou autorisation révoquée — il ouvre la page des autorisations de l'application.

Un seul comportement à coder : le système indique lui-même si la demande peut encore être présentée. Envoyer systématiquement vers les réglages ferait faire un détour quand une simple boîte suffirait.

Le même comportement vaut pour le rappel d'autorisation du capteur cardiaque, dont la description actuelle ne mentionne que l'ouverture du réglage système : elle est à aligner sur celle-ci. [integrated: B61, B20]
