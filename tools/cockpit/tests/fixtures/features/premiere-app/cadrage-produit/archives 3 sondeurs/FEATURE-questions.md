## Answers

C1.1              | Non rétroactif : chaque réglage du profil (FC max, seuils de zone, distance attendue, durée d'appui long) s'applique à partir de la prochaine course ; une course déjà enregistrée reste figée (B19). Le facteur de correction suit la même règle : jamais recalculé rétroactivement, seul l'affichage à venir est corrigé (B37).
C1.2              | Calories, pas, cadence affichée, altitude, carte/tracé du parcours (B59) ; formule d'âge et accès à la configuration Samsung Health pour dériver la FC max (B17) ; GPS/position pour l'allure (B36) ; import par fichier — collage uniquement (B11) ; luminosité forcée en continu (B35).
C1.3              | gap: le document ne dit pas si cette fonctionnalité s'appuie sur une version antérieure de l'app ou sur des règles déjà en place ; impossible de dire, règle par règle, ce qui serait conservé, changé ou supprimé.
C1.4              | Chaque terme technique est réglé à sa première occurrence : segment/cycle/Roxzone (B1) ; allure-segment/allure-lissee (B36) ; k, k_mesuré, k_précédent (B37–B38) ; écart, écart_cumulé, temps_projeté, arrivée (B39–B40) ; formats de durée, delta, allure, FC, position, zone, réglages, dates, arrondi (B47–B52) ; aucun terme n'est laissé indéfini.
C1.5              | Les termes affichés sont ceux du produit : textes français catalogués (B56) et gabarits dynamiques (B54), toujours issus d'un fichier de ressources (B53). Les notations de calcul (distance_attendue, k_mesuré, k_précédent, écart_cumulé, allure-segment, allure-lissee…) sont la notation du document, jamais affichées telles quelles — seules leurs valeurs le sont.
C1.6.sante        | Oui — fréquence cardiaque, via le capteur pendant la course et via l'historique santé du téléphone pour dériver la FC max. Consentement porté uniquement par les permissions système (capteur B20, historique santé B17), sans étape de consentement propre à l'app (B60) ; donnée jamais transmise hors téléphone/montre (B60).
C1.7.capteur      | Permission capteur cardiaque (montre, B20) : un refus laisse l'app utilisable — horloge, segments et deltas continuent de fonctionner ; FC et arc de zone restent en repli permanent. La demande n'est jamais répétée automatiquement ; un rappel sur l'accueil relance la demande système ou ouvre les réglages système si celle-ci n'est plus proposée.
C1.7.historique   | Permission historique santé (téléphone, B17) : un refus ou une indisponibilité laisse la FC max à saisir à la main, jamais devinée, et les plages de zones restent masquées tant qu'elle n'est pas saisie.
C1.7.connectivite | Permission de connectivité / appareils à proximité (B61) : un refus permanent rend la synchronisation durablement indisponible sans affecter le reste — chaque app reste pleinement utilisable seule. Le téléphone affiche un message dédié et un bouton "Autoriser" ; la montre affiche "Aucune référence" ; la demande n'est jamais répétée automatiquement.

## Questions

### Q1
Block: -
Question: Does this feature build on an existing app or an existing set of product rules, and if so, for each rule it touches, is it kept, changed, or removed?
Answer:
