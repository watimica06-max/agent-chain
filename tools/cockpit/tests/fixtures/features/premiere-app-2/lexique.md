# Lexique — premiere-app-2

Vocabulaire de la fonctionnalité. `## Tranché` porte les termes qu'une
réponse a réglés ; `## Non tranché` porte ce que le balayage a trouvé et
qui attend une réponse.

## Tranché

### Course et découpage

    station — retenu
      remplace : atelier
      `STATION` : le segment, dans la table de correspondance de
      l'import (§A.3)

    RUN — retenu, le segment de course
      remplace : kilomètre (le segment), tour
      « kilomètre » reste l'unité de distance : « Distance d'un
      kilomètre », minutes par kilomètre

    course — retenu pour l'épreuve enregistrée
      concept anglais : race
      le fait de courir est RUN — deux choses distinctes

    course enregistrée — retenu, la course que la montre a enregistrée,
      par opposition à course importée (§2, §7.3, §9, §C.2)
      remplace : course enregistrée au sens de toute course sauvegardée,
      importée comprise (§4.4) — la phrase devient « Une course déjà
      créée est figée » : « créée » couvre les deux origines, sans être
      un terme
    course importée — retenu, la course venue de l'import

    ajoutée (§4.1), créée (§4.4) — des participes, pas des termes ; ni
      l'un ni l'autre ne nomme une entité (tour 10) ; §4.4 reste tel
      quel, §4.1 a depuis reçu un terme — voir rang d'entrée, tour 11
      « ajoutée » couvrait les deux origines, import et montre : le
      départage à date identique doit ordonner deux courses de la montre
      aussi bien que deux imports ; le mot empruntait à « bouton
      d'ajout » sans désigner le bouton

    rang d'entrée — retenu, la donnée que le départage à date identique
      suppose (§4.1) : une valeur par course, écrite une fois à son
      entrée dans la base locale, quelle qu'en soit l'origine — import
      ou envoi montant —, jamais affichée, jamais modifiée, lue seulement
      pour départager deux courses de même date ; le plus élevé passe en
      premier
      remplace : ordre d'insertion (nommait le classement plutôt que la
      donnée ; « insertion » est du vocabulaire de base de données,
      absent du fichier d'idées), « la course ajoutée le plus
      récemment » (§4.1, la périphrase — la phrase devient « À date
      identique, la course au rang d'entrée le plus élevé passe en
      premier — le rang d'entrée est interne, jamais affiché. », tour 11)
      identifiant croissant ou instant d'écriture en base : deux façons
      de tenir la même donnée, pas deux données — le lexique nomme ce
      qu'il faut tenir, pas comment
      « entrée » seule (§4.3, « L'entrée se fait par texte collé ») :
      autre sens, la saisie, sans conflit

    Roxzone — retenu, la zone de transition
      ROX_IN, ROX_OUT — retenus, deux moments distincts qu'elle contient :
      ROX_IN avant la station, ROX_OUT de la sortie de la station à la
      reprise de la course
      « transition » ne nomme qu'elle — l'autre emploi (§11) est le
      marquage

    station Wall Balls — retenu, le trentième segment
      remplace : bloc final, FINAL_BLOCK
      `STATION` du cycle 8 dans la table de correspondance de l'import
      le cycle 8 ne porte que deux segments : RUN 8 puis la station
      Wall Balls
      trentième segment (§6.2, « **Le trentième segment** — la station
      Wall Balls, … ») : un numéro, pas un nom — §2 numérote les trente
      segments et donne « 30. » à celui-ci, le code construit un index,
      pas un terme ; le même statut que « le huitième RUN » ; la phrase
      reste telle quelle, le numéro est le sujet, l'apposition le
      nomme (tour 14, Q1 — sorti de la liste des termes remplacés, où
      il figurait depuis le tour 1)

    segment — deux choses distinctes, même mot
      segment de course : un des 30, une des 30 lignes collées
      segment de l'arc : un des 5 éléments visuels (`arc-segment`) — un
      seul nom pour les cinq
      remplace : arcs (les cinq, au pluriel — §3.3 « cinq arcs
      concentriques » devient « cinq segments concentriques », §6.3
      « Cinq arcs `zone-1` à `zone-5` » devient « Cinq segments de
      l'arc, `zone-1` à `zone-5` » ; tour 8 — le jeton qui les mesure
      s'appelle déjà `arc-segment`)

    segment en cours — retenu, le segment ouvert
      remplace : segment courant

    destination — retenu, ce vers quoi la coureuse se dirige pendant
      une Roxzone, au centre de l'écran principal
      remplace : prochaine étape

    départ — retenu, l'instant où la course commence, vu comme un point
      dans le temps : « depuis le départ », « heure de départ »
      démarrage : l'action qui déclenche cet instant, par « Démarrer »
      coup de départ : ce qui se passe dans la salle
      trois facettes, trois termes, aucun ne remplace l'autre

    fin de la course — retenu, le moment où la course se termine,
      terminée ou arrêtée ; l'écart final s'y fige ; la session
      d'exercice s'y ferme (§10)
      « arrivée » ne nomme pas ce moment : une course arrêtée n'arrive
      jamais
      remplace : arrivée (§10 « fermée à l'arrivée » — un reliquat,
      tour 8 : §6.5 coupe le chrono et les mesures sur un arrêt, la
      session se ferme donc aussi sur une course qui n'arrive jamais) ;
      s'arrête (la course, §6.7 — devient « la course prend fin » :
      employer le verbe de l'arrêt sur une course terminée brouille ce
      que le lexique sépare, une course arrêtée est incomplète, une
      course qui prend fin au trentième marquage ne l'est pas)

    arrêt — retenu, l'événement ; la course est arrêtée
      remplace : interrompue, interrompre (§6.8, §5.4)
      « arrêtée en route » reste, c'est la course arrêtée
      incomplète : la marque que porte la course enregistrée, autre
      chose que l'arrêt

    incomplète — retenu, la marque de la course arrêtée
      « marquée incomplète » figure dans un texte affiché et ne change
      pas

    complète — un mot, deux sens, jamais la marque (tour 10)
      entièrement transférée : §9 — l'envoi montant, pas la marque ; une
      course arrêtée doit atteindre le téléphone pour y être marquée
      incomplète (§4.1), les deux phrases se contrediraient sous
      l'autre lecture
      remplace : complète (§9 « n'apparaît sur le téléphone que
      complète » — devient « qu'entièrement transférée », pour que la
      phrase ne puisse plus se lire comme la marque)
      une donnée entière : « la référence complète avec ses 30
      segments » (§9), « Le collage est incomplet », « un résultat Hyrox
      complet » (§C.5, textes affichés) — inchangés

    arrivée — retenu, la ligne d'arrivée : « sprint vers l'arrivée »
      remplace : ligne (dans ce sens, §2)
      ses emplois légitimes : le lieu (§2) et l'arrivée estimée, le
      temps prévu — jamais le moment où la course prend fin
      `arrivée` (§8.2) : identifiant de calcul, inchangé

    segment fermé — retenu, un segment clos par un marquage ; le
      segment ouvert au moment de l'arrêt n'en fait pas partie, il n'a
      pas de durée (§4.2, §6.7, §7.2, §8.2)
      remplace : segments réellement courus (§4.2) — trompeur : laissait
      entendre qu'un segment couru à moitié compte pour ce qu'il vaut
      §4.2 : « Le temps total affiché est celui des segments fermés. »

    nom du dernier segment fermé — retenu, la donnée que porte le
      bouton d'annulation (§13.2) ; `<segment fermé>` dans §C.2
      remplace : Nom du dernier marquage (§13.2) — un marquage n'a pas
      de nom

    redémarrage — retenu, l'application relancée (§11), seul sens
      recommencer la course à zéro : sans terme — §10 devient
      « reprendre là où elle en était, sans repartir de zéro »
      remplace : redémarrer (la course, §10)

    cycle, piste — retenus, sans rival

### Comparaison et mesure

    référence — retenu
      remplace : favori
      « Référence » : le badge affiché, texte distinct du concept
      course de référence : sa forme complète, admise là où le contexte
      pourrait faire hésiter (§4.1, §6.2) — une seule chose, la course
      choisie comme référence, pas seulement ses temps (§9)
      « C'est la course de référence. » : texte affiché, inchangé

    référence en cours — retenu, la référence désignée
      remplace : référence courante
      référence chargée : autre chose, l'état de la montre de l'avoir
      reçue — une référence peut être en cours sur le téléphone sans
      être chargée sur la montre
      « Référence chargée · <nom> » : texte affiché

    référence chargée — retenu, la référence telle que la montre la
      détient après un envoi descendant (§5.2, §13.2 ; tour 10)
      remplace : Référence synchronisée (§13.2, colonne Provenance du
      temps de référence du segment — devient « Référence chargée » :
      la provenance dit d'où vient la donnée, la consigne sous le tableau
      dit ce qui arrive quand elle manque, un seul nom pour que les deux
      se répondent)
      « Dernière synchronisation » (§13.3) : une autre provenance,
      l'événement qui est la source, pas la donnée qu'il a apportée —
      inchangée

    sans référence chargée — retenu, l'état de la montre : rien n'a été
      reçu (§5.2, §13.2 ; tour 12)
      « sans référence » nu, sur la montre (§5.2, §9, §13.3) : sa
      reprise, admise dans une section qui a déjà posé lequel des deux
      états elle traite — inchangé
    état sans référence — retenu, l'état du téléphone : aucune course
      n'est désignée comme référence en cours (§4.2, « n'en choisit
      aucune à la place »)
      deux états distincts, qui ne coïncident pas : une référence peut
      être en cours sur le téléphone sans être encore chargée sur la
      montre, tant qu'aucun envoi descendant n'a eu lieu — ce décalage
      est un état nominal, pas une anomalie
      la forme nue reste admise en reprise de chaque côté, dans une
      section qui a déjà posé lequel des deux elle traite — les quatre
      occurrences nues du fichier le sont

    écart — retenu · `delta`, `delta-zero` : ses jetons
    avance — retenu · `ahead` : son jeton
    retard — retenu · `behind` : son jeton

    couleurs de sens — retenu, trois jetons : `ahead`, `behind`,
      `delta-zero` ; `delta-zero` porte un sens comme les deux autres —
      ni avance ni retard (§3.4)
      la consigne de §3.1 ne vise que `ahead` et `behind`, jamais
      employées seules parce qu'elles opposent deux sens ; elle les
      nomme désormais sans passer par le terme

    écart sur le RUN, écart cumulé, écart par segment — trois écarts
      distincts, retenus ; ils se distinguent par leur portée — un RUN,
      le cumul, un segment — non par l'appareil qui les affiche

    écart par segment — retenu, des deux côtés : la différence entre la
      durée et le temps de référence sur un segment, la même mesure
      qu'on la somme en course, comme composante de l'écart cumulé, ou
      qu'on l'affiche en colonne après (tour 8)
      remplace : écarts de segment (§13.2 — devient « Somme des écarts
      par segment »), écart du segment en cours (§8.2 — devient « écart
      par segment du segment en cours »)
      écart de Roxzone (§8.5) : l'un d'eux, sur un segment de Roxzone —
      une désignation par le type de segment, pas un quatrième écart

    écart nul — retenu, l'état d'un écart à `+0:00`, ni avance ni
      retard ; ce que `delta-zero` colore (§3.1, §13.1)
      remplace : à égalité (§13.1 — devient « `+0:00` signifie un écart
      nul, pas un écart inconnu »)
      « nul », « à zéro » (§4.2, §B.2) restent des adjectifs de la
      valeur, pas des noms de l'état

    écart final — retenu, l'écart cumulé figé à la fin de la course ;
      pas un quatrième écart, la même mesure à un moment donné

    arrivée estimée — retenu
      remplace : estimation du temps d'arrivée, temps d'arrivée estimé,
      estimation d'arrivée
      seule forme affichée : « arrivée estimée »

    segments à venir — retenu, les segments après le segment en cours,
      ceux qui restent à courir ; ils comptent pour leur temps de
      référence dans l'arrivée estimée (§8.2, deux emplois — la formule
      fait foi, la colonne de provenance la résume ; tour 12)
      remplace : temps de référence restants (§13.2, colonne Provenance
      de l'arrivée estimée — devient « Écarts + temps de référence des
      segments à venir » : le raccourci déplaçait le sujet, « restants »
      qualifiait les temps là où ce sont les segments qui restent à
      courir)
      « les blocs restants » (§13.2, consigne) : les blocs, autre chose,
      inchangé
      segment jamais atteint (§4.2, §6.7) : après l'arrêt, autre chose —
      noté au tour 7

    allure — retenu · `pace` : son jeton
      vitesse : mesure distincte, la vitesse instantanée lissée, jamais
      affichée

    minutes par kilomètre — retenu en prose, l'unité de l'allure
      remplace : min/km
      `/km` : la forme affichée, l'unité détachée de la valeur :
      `6:00` `/km`

    durée — retenu, le temps mesuré d'un segment, par opposition à son
      temps de référence
      remplace : temps réel (§8.2, §13.2)
      `temps_réel` reste dans la formule : identifiant de calcul, comme
      `allure-segment`
      « temps du segment » (§6.1) disparaît, et n'était pas une durée :
      ce qui est relevé au doigt posé est l'instant où le segment se
      ferme, la durée s'en déduit — §6.1 devient « Le segment se ferme
      à l'instant où le doigt se pose, pas au relâchement. »

    temps cumulé — retenu en prose
      remplace : cumul (en prose)
      « cumul » reste admis où la place le commande — en-têtes de
      colonne, §B.6 — et dans le texte affiché « Cumul incohérent »

    heure de départ — retenu, l'heure du jour à laquelle la course a
      commencé
      remplace : heure réelle

    date et heure — retenu, la donnée
      remplace : horodatage
    nom généré — retenu, le nom d'une course enregistrée par la montre,
      formé de sa date et son heure
      remplace : nom automatique — « automatique » est pris par la
      synchronisation et le retour d'écran
      une valeur par défaut du nom, pas un second datum : il n'existe
      qu'un champ nom sur une course, « Renommer » écrit dans le même
      champ ; le code construit un seul nom, quelle qu'en soit
      l'origine (tour 14, Q2)

    distance_attendue — retenu, l'identifiant de calcul
      « Distance d'un kilomètre » : son libellé affiché, même réglage

    allure-segment, allure-lissee, distance_attendue, k_mesuré,
      temps_projeté — des concepts, pas des textes affichés : la chaîne
      les écrit en anglais à partir du fichier produit

    facteur initial — retenu, le facteur de correction avec lequel une
      course commence
      remplace : facteur de départ, valeur initiale
      titre §7.3 : « Facteur initial et repli »

    facteur en vigueur — retenu, le facteur de correction appliqué à
      cet instant, celui que `k_précédent` représente dans la formule
      remplace : facteur de correction courant (§7.1) — « courant »
      tombe une quatrième fois
      `k_précédent` reste tel quel : identifiant de calcul, pas un
      terme de prose

    calibration — retenu, le processus : produit un facteur à la fin de
      chaque RUN, en retient ou en rejette, met à jour la valeur du
      profil ; on réanalyse une calibration, les courses enregistrées
      l'alimentent (§7.2, §7.3)
      facteur de correction : la valeur que ce processus produit — deux
      choses distinctes

    distance mesurée — retenu, ce que le capteur rapporte sur le
      segment ; aucune autre source n'existe (§7.1, §7.2, §13.2)
      remplace : distance parcourue, mètres parcourus (§7.1) —
      trompeur : laisse entendre une distance réelle, alors que tout §7
      repose sur le fait qu'elle ne l'est pas
      distance attendue : distincte, la valeur de référence, 1000 m par
      défaut
      « chemin parcouru » (§12) : la navigation, autre sens, reste

    temps total écoulé — retenu, depuis le départ (§6.4, §13.2, §B.1)
      remplace : temps écoulé (seul, dans ce sens)
      `temps_écoulé` reste dans la formule §8.2 : identifiant de calcul,
      y désigne le total
    temps écoulé du segment — retenu, depuis le début du segment en
      cours, quel qu'il soit (§3.2, §6.2, §7.1, §13.2)
      remplace : temps écoulé (seul), temps écoulé depuis le début de la
      station, temps écoulé dans la transition (§6.2), Temps de Roxzone
      (§6.2, table de rendu — tour 5), temps déjà écoulé dans le segment
      (§8.1), temps depuis le début du segment (§13.2) — tour 8, les
      troisième et quatrième formes absorbées
      « temps écoulé » seul disparaît : c'est la forme qui ne dit pas
      laquelle des deux
      « Temps écoulé du segment en Roxzone » (§3.2) : la forme retenue
      suivie de son contexte, inchangée

    temps total — retenu, le temps d'une course terminée ; en entier,
      jamais sous sa forme nue
      remplace : durée totale (§B.1) — entrait en conflit avec
      « durée », le temps mesuré d'un segment
      remplace : total (nu — §11 ×2 « Le temps total est la somme des
      segments ; un segment n'est jamais le temps total moins les
      autres », §B.6 « ne retombe pas sur le temps total », légende de
      §A.1 « Temps total 1:37:25 » ; tour 14, Q3 : le cas de « temps
      écoulé » au tour 8, une forme qui ne dit pas laquelle des deux,
      dans des sections qui n'avaient jamais posé la forme longue)
      pas un nom commun d'arithmétique : la règle de §11 porte sur une
      donnée précise, celle qu'un segment ne doit jamais servir à
      déduire ; la somme est nommée par le verbe — « le temps total est
      la somme des segments »
      « 140° au total » (§3.3) : l'adverbe, hors vocabulaire ; « Total
      time » (§A.1, §A.3, §C.5) : la ligne du résultat collé, inchangée
      `duration-total` reste : identifiant

    temps de référence — retenu, celui de la référence sur un segment
      remplace : temps de la référence (§6.2)
    temps total de la référence — retenu, le temps total de la course
      de référence (§13.3)
      remplace : temps de la référence (dans ce sens, §13.3)

    valeurs vives (§6.9) — sans terme : « les valeurs qui changent en
      direct », une tournure ; le mot n'apparaissait qu'une fois
      donnée chronométrée reste, inchangée : un critère de composition,
      ce qui porte `font-data` — couvre aussi des durées figées, le
      temps total d'une course en liste par exemple

    marquage — retenu
      remplace : avancement (le bouton et ce qu'il enregistre sont une
      seule chose), transition (dans le sens de §11, « un marquage est
      atomique »)
    ouverture d'un segment — retenu, ce qui arrive au segment suivant ;
      le marquage est le geste et ce qu'il enregistre — deux facettes
      distinctes, les deux retenues, le même partage que départ,
      démarrage et coup de départ
      elles coïncident à chaque marquage, mais un segment s'ouvre aussi
      sans marquage : le premier au démarrage (§5.4), le segment rouvert
      à l'annulation (§6.5) ; « instant d'ouverture du segment en
      cours » (§11) inchangé

    annulation — retenu, l'annulation d'un marquage enregistré (§6.5) ;
      c'est elle qui vibre deux fois
      un relâchement avant la durée de l'appui long, ou un glissement
      de plus de 20 px, n'enregistre rien — il n'y a rien à annuler
      (§6.1 reformulé)
      « Annuler » : texte affiché, le bouton de toutes les boîtes de
      confirmation — suppression, renommage, arrêt, reprise de session

    marquer (au sens de signaler) — retenu, cohabite avec marquage
      « marquée incomplète » : dans un texte affiché, ne change pas
      badge « Référence » — retenu, ce que porte la course de référence
      remplace : marque visible

    position — deux choses distinctes, même mot
      position dans la course : « 14/30 », en temps réel
      position d'un élément : son emplacement à l'écran

    ligne — deux sens distingués, même mot
      une rangée : du résultat collé, de l'écran de détail, de la liste
      de la montre — un seul sens, le contexte suffit
      une ligne de texte en mise en page : « sur trois lignes maximum »,
      « Lignes de segment »
      la ligne d'arrivée disparaît : « sprint vers l'arrivée »

    délai de péremption — retenu, le délai au-delà duquel une donnée de
      capteur repasse au repli (§13.1)
      remplace : seuil (dans ce sens)

    chiffres à chasse fixe — retenu, la propriété de `font-data` : des
      chiffres de largeur égale (§3.2)
      remplace : chiffres tabulaires (§3.2)

    valeur interpolée — retenu, la part d'un texte dynamique qui change
      (§C.1, colonne de §C.2)
      remplace : Valeur variable (§C.2)

    repli — retenu, l'état d'une donnée qui n'est pas montrée, quelle
      qu'en soit la cause ; « en repli » (§5.4, §7.1, §8.3, §13.1,
      §13.2)
      remplace : indisponible (§13.2 « Allure indisponible », colonne
      Repli de la distance mesurée — devient « Allure en repli » : la
      ligne décrit une conséquence, pas un second état, et la ligne
      suivante donne à `allure-segment` son repli `—:—` ; tour 10)
      la distinction « calculée mais non montrée » contre « pas
      calculable » n'existe nulle part dans le document
      « Synchronisation indisponible » (§4.4, §C.4, texte affiché), « la
      synchronisation devient indisponible » (§4.4) : autre chose, une
      action empêchée, pas une donnée en repli — inchangés

    facteur de correction, garde-fou, hystérésis, zone morte, fenêtre,
      zone extrême, compteur de marquages, case d'écart, échantillon,
      morceaux — retenus, sans rival

### Cardiaque

    fréquence cardiaque — retenu en prose
      remplace : FC
      « fréquence » seule : admise en reprise seulement — forme
      complète à la première mention d'un passage, « la fréquence »
      ensuite
      `bpm` : l'unité de mesure, dans les textes affichés seulement

    battements par minute — retenu en prose, l'unité
      `bpm` : la forme affichée

    fréquence cardiaque maximale — retenu en prose
      remplace : FC max
      « fréquence maximale » : admise en reprise seulement, même règle
      « Fréquence cardiaque maximale », « Zones cardiaques (% FC max) » :
      textes affichés, inchangés

    mesure — retenu, une valeur livrée par un capteur ; le verbe suit :
      « fréquence mesurée », « valeur mesurée »
      remplace : lecture (dans ce sens), lue
      « lecture » ne garde que le sens de l'import (§A.4)

    dérivation — retenu, l'opération : lire l'historique de santé pour
      en tirer la fréquence cardiaque maximale (§4.4, §13.4)
      remplace : lecture automatique (§13.4), lecture de l'historique de
      santé (§4.4)
      « proposée automatiquement » (§4.4) : une description de l'effet,
      pas un nom — c'est le résultat de la dérivation
      remplace aussi : proposition automatique (réponse du Rédacteur,
      Q1 — « demande la proposition automatique de la fréquence
      cardiaque maximale » devient « demande la dérivation de la
      fréquence cardiaque maximale » ; tour 15 : le nom là où §4.4
      n'avait que le participe — la proposition est ce que la
      dérivation produit, pas un second nom de l'opération)
      « lecture » garde son seul sens, celui de l'import ; « lecture
      seule » (§5.3) est la locution, pas le terme

    historique de santé — retenu, la source de la dérivation, sur le
      téléphone (§4.4, §13.4) ; confirme l'entrée « historique » du
      tour 1
      remplace : historique de fréquence cardiaque (§4.4)

    seuil — retenu, la limite entre deux zones
      remplace : borne, frontière (dans ce sens)
      « borne » reste la borne d'un réglage (min et max) et les bornes
      d'une plage affichée
      pourcentage : son unité, comme `bpm` l'est de la fréquence
      cardiaque — pas une seconde donnée (tour 10)
      remplace : pourcentage (§4.4 Rendu, nommant la valeur — « libellé,
      pourcentage et plage » devient « libellé, seuil et plage », « La
      zone 1 n'a pas de pourcentage à elle » devient « n'a pas de seuil à
      elle » : c'est bien un seuil qui lui manque, pas une unité)
      « en pourcentage de la fréquence cardiaque maximale » (§4.4),
      « Pourcentage de zone » (§B.4, un format nommé par son unité,
      comme « Durée de l'appui long » par ses millisecondes) : inchangés

    zone active — retenu, la zone où tombe la mesure
      remplace : zone courante
      segment actif : l'élément d'arc qui la dessine, distinct et
      conservé — le segment actif dessine la zone active

    segment inactif — retenu, l'état des quatre segments de l'arc qui ne
      sont pas le segment actif ; `arc-opacity-idle`, `arc-width`,
      `arc-width-dim` le portent (§3.3, §3.4, §6.3, §13.2)
      remplace : atténués (les quatre autres, §6.3 — devient « les
      quatre autres restent inactifs »), style atténué (§13.2 — devient
      « les cinq restent inactifs »)
      pas « inactif » au sens du bouton : aucun segment de l'arc ne
      répond jamais — même mot, autre chose, comme « segment »,
      « position » et « ligne »
      pas le mode atténué non plus : deux axes indépendants — actif ou
      inactif d'une part, affichage normal ou mode atténué d'autre
      part, les quatre combinaisons existent

    durée de l'appui long — retenu, le délai à maintenir pour marquer,
      en entier partout, la table de §B.4 comprise
      remplace : seuil (dans ce sens), Durée d'appui (§B.4)
      la forme courte reste réservée aux emplacements réellement
      contraints — aucun aujourd'hui

    saisie manuelle — retenu, l'acte de taper la valeur soi-même — la
      fréquence cardiaque maximale (§4.4, §13.4)
      remplace : modification manuelle (§13.4), saisie à la main
      (§13.4 — devient « saisie manuellement »), modifiable à la main
      (§4.4 — devient « modifiable manuellement »)

    repos actif — retenu, sans rival (§4.4)

    zone cardiaque — retenu, sans rival

    arc — retenu, le tout : les cinq segments de l'arc ensemble ; au
      singulier seulement
      remplace : arcs (au pluriel, pour les cinq — voir segment de
      l'arc, tour 8)

### Appareils, échanges, session

    session d'exercice — retenu, partout
      remplace : activité (l'exercice ouvert sur la montre), exercice
      (§10), capteur d'exercice (§12 — un lapsus, ce qui est occupé
      n'est pas un capteur), session capteur (§10 — le même lapsus,
      tour 4)
      « Arrêter l'activité », « Une autre activité est en cours » :
      textes affichés, inchangés

    base locale — retenu, le stockage local d'un appareil, la seule
      provenance interne (§10, §11, §13.2, §13.4)
      remplace : journal local (§13.4), journal des marquages (§13.2),
      « en base » (§11 — devient « dans la base locale »)
      un journal est un contenu de cette base, pas un stockage à part :
      la colonne demande d'où vient la donnée, non ce que la base
      contient

    reprise — retenu, la reprise d'une session d'exercice en cours, la
      nôtre comme celle d'une autre application
      la relance d'une demande d'autorisation est une autre chose

    rappel — retenu, la relance d'une demande d'autorisation, sur
      l'écran d'accueil de la montre (§5.1)
      remplace : reprise (dans ce sens)
      sur le téléphone aussi, pour l'autorisation d'accès à
      l'historique de santé (réponse du Rédacteur, Q1 ; tour 15) : ce
      que le système n'autorise plus après un refus, c'est le rappel
      remplace : redemander (réponse du Rédacteur, Q1 — « ne permet
      plus de la redemander » devient « ne permet plus le rappel » : le
      rappel dit comme verbe)

    synchronisation — retenu, l'ensemble des échanges ; depuis la
      montre, « Synchroniser » échange dans les deux sens
      envoi descendant — retenu, du téléphone vers la montre
      envoi montant — retenu, de la montre vers le téléphone
      remplace : transfert montant, remontée
      « envoi » seul, dans §9, désigne l'envoi descendant par son
      contexte

    en cours, échec, réussite — retenus, les trois états d'une
      synchronisation, un nom chacun
      remplace : Échouée (§4.4), succès (§12)
      « succès │ échec » du schéma téléphone (§12) qualifie le résultat
      de l'import, pas d'une synchronisation — même paire de mots,
      autre contexte, autre état

    résultat d'une synchronisation — retenu, l'issue d'une tentative,
      qui prend l'un des trois états tranchés : « en cours » pendant,
      « réussite » ou « échec » après, et la date de la dernière
      synchronisation réussie que la réussite écrit — rien au-delà
      (§5.2, §12 ; tour 12)
      autre chose que résultat, le tableau collé — deux choses
      distinctes, toutes deux construites par le code ; le complément
      est obligatoire dans ce sens, comme pour confirmation de réception
      (tour 8)
      remplace : son résultat (§5.2 — « affiche son résultat sur place »
      devient « affiche le résultat de la synchronisation sur place » :
      la forme nue se lisait en contexte, la forme complète ne se lit
      que d'une façon)

    indicateur de progression — retenu, le témoin qui tourne pendant une
      synchronisation, sur les deux appareils
      remplace : indicateur d'activité, pictogramme rotatif
      « activité » reste à la session d'exercice

    date de la dernière synchronisation réussie — retenu, en entier,
      partout : « réussie » n'est pas un ornement, une synchronisation
      échouée n'écrit pas cette date (§4.4, §12, §13.4)
      remplace : date de dernière réussite (§4.4), date de dernière
      synchronisation (§4.4), date de la dernière réussite (§12), Date
      de dernière synchronisation (§13.4), Dernière synchronisation
      (§B.5, colonne Usage de la table des dates — tour 6 : « partout »
      atteint cette ligne, une colonne de tableau n'est pas un
      emplacement contraint ; la forme courte y laisserait croire à une
      donnée distincte)
      `Dernière synchronisation réussie : <date>` : texte affiché
      « Dernière synchronisation » comme provenance (§13.3) :
      l'événement, pas la date — les deux occurrences ne changent pas

    liaison — retenu, le lien établi entre les deux appareils (§9),
      sans rival

    liste des courses — retenu, les courses de l'utilisatrice
      remplace : historique (dans ce sens)
      « Historique » : le titre affiché sur la montre ; « Mes courses » :
      le titre affiché sur le téléphone

    liste des courses résumée — retenu, la liste de la montre, à la
      première mention d'un passage ; « liste résumée » en reprise
      remplace : liste des courses en version résumée

    historique — retenu pour l'historique de santé du téléphone
      seul sens conservé pour ce mot

    résultat — retenu, le tableau collé depuis hyresult, une fois
      reconnu
      remplace : export ; tableau (§A.4, en prose — « en cours de
      résultat » ; le résultat nommé par sa forme)
      « Copie le tableau entier », « le tableau des temps » : textes
      affichés, inchangés
      résultat d'une synchronisation : autre chose, l'issue d'une
      tentative — voir cette entrée, sous les trois états (tour 12)
    texte collé — retenu, ce qui se trouve dans la zone de texte avant
      toute validation ; peut n'être rien du tout (« Rien à lire »,
      « Colonnes manquantes ») — deux choses distinctes : nommer
      résultat ce qui n'a pas passé la validation préjugerait de l'issue
      (§A.5) ; §4.3, §C.5
    sélection (§4.3) — sans terme, une occurrence : la phrase devient
      « L'utilisatrice corrige à la source et recolle. »

    import — retenu, l'opération entière : coller, valider, enregistrer
      remplace : collage, saisir (dans ce sens, §1 — « importer les
      anciennes courses »)
      saisir, saisie restent à la frappe d'une valeur — un nom, une
      date, la fréquence cardiaque maximale
      « Coller un résultat », « Revenir au collage », « Importer » :
      textes affichés, inchangés
      le verbe « coller » et le participe « collé » restent libres
      zone de texte — le champ où l'on colle, terme déjà employé par
      §4.3 ; remplace : zone de collage

    table de correspondance — retenu, la table des noms collés vers les
      segments
      remplace : mapping
      titre §A.3 : « Table de correspondance des noms »

    échec de lecture — retenu, l'import refusé, en prose
      remplace : erreur de lecture (en prose), rejet (§C.5) ; « cause de
      rejet » devient « cause d'échec »
      écran d'erreur — retenu, le nom de l'écran qui l'affiche ;
      « Erreur de lecture » n'est pas un texte affiché, aucun des huit
      titres de §C.5 ne le porte
      « rejeté », « rejet » restent au garde-fou du facteur (§7.2),
      autre sens
      remplace aussi : erreur (nue, §4.3 « En cas d'erreur, le message
      indique la ligne qui pose problème » — devient « En cas d'échec de
      lecture, … » ; tour 13 : la trace du renommage du tour 3, le grep
      cherchait « erreur de lecture » et la forme nue lui a échappé ; le
      bouton « Importer » inactif est traité sans message, « erreur » ne
      couvrait donc rien de plus large que le refus de l'import)
      « erreur » garde ses deux emplois légitimes : les noms — Écran
      d'erreur, Messages d'erreur d'import — et le mot courant de §13.1,
      « Un repli n'est pas une erreur », qui ne parle pas de l'import

    anomalie — retenu, la faute trouvée dans une ligne, celle qui
      provoque l'échec de lecture — autre chose que l'échec (§C.5, §A.4)
      remplace : défaut (§A.4)
      « Cause » (colonne de §C.5) : la catégorie d'anomalie — collage
      vide, colonnes manquantes, cumul incohérent — là où l'anomalie
      est l'occurrence rencontrée dans une ligne donnée ; pas un doublon

    mode terminal — retenu, sans rival (§A.4)

    point de passage — retenu
      `Split` : sa colonne dans le tableau collé

    nom — retenu, le nom d'un segment, d'une station, d'un point de
      passage, d'une course
      remplace : libellé (dans ce sens)
      remplace : nom libre (§14, une occurrence — « Une course est
      identifiée par son nom libre » devient « par son nom » ; tour 14,
      Q2 : il n'existe qu'un champ nom sur une course, le nom généré en
      est une valeur par défaut ; l'adjectif portait le contraste avec
      les divisions Pro / Doubles / Relay que §14 écarte deux lignes
      plus haut — le contexte le donne, le mot n'a pas à le répéter)
      « libellé » reste le libellé d'un élément d'interface (§3.2, §4.4)
      et les textes affichés « Libellé inconnu — ligne <n> »,
      « <libellé> » restent tels quels

    libellé — retenu, le texte attaché à un élément : un bouton, un
      champ, une ligne de réglage
    mention — retenu, un texte secondaire autonome, qui n'étiquette
      rien : « arrivée estimée » sous le chrono, la phrase d'une
      confirmation, la date sous le bouton de synchronisation
      deux choses distinctes : « libellés secondaires » (graisse 600) et
      « mentions secondaires » (`w-label`) de §3.2 nomment deux choses
      tour 7 : la phrase sous un titre — liste vide, écran d'erreur,
      autorisation, confirmation — et la phrase sous un champ sont une
      seule chose, la mention ; expliquer quoi faire ou énoncer un fait
      est une différence de contenu, pas de composant — même
      emplacement, même rôle, mêmes jetons
      remplace : explication (§4.3, §C.5 — la colonne devient
      « Mention »), phrase d'explication (§4.1, §5.1), phrase expliquant
      (§5.1), message au sens de cette phrase (§4.1 liste vide ; §4.4
      « un message court, sous le champ » ; et ses reprises §C.2 « le
      message n'existe que sur un refus », §C.4 « le message borné »)
      remplace aussi : message expliquant (réponse du Rédacteur, Q1 —
      « un message expliquant pourquoi elle en a besoin » devient « une
      mention expliquant pourquoi elle en a besoin » ; tour 15 : la
      forme retirée « phrase expliquant » avec « message » à la place
      de « phrase » — la phrase sous le titre, pas le message entier)
    message — retenu, l'ensemble de ce qu'un écran dit, titre et
      mention réunis ; ne nomme jamais la seule phrase
      « le message indique la ligne qui pose problème » (§4.3), « Aucun
      message » (§4.3, §13.1), « Un seul message à la fois », « Aucun
      message générique », « Messages en §C.5 », « Messages d'erreur
      d'import » : inchangés
      « *Échec* — message en `behind` » (§4.4) : l'ensemble de ce que
      l'état affiche, inchangé

    entrées de menu (§3.2) — un reliquat, retiré : aucun menu n'existe
      dans ce produit ; §3.2 devient « 600 pour les libellés
      secondaires. »

    réglage — retenu, un des quatre réglages du profil
    réglages système — retenu, toujours avec son adjectif : le lieu où
      vit la page des autorisations, sur le téléphone comme sur la
      montre (§4.4, §5.1)
      remplace : les réglages (seul, dans ce sens — « vers les
      réglages »)
      deux choses distinctes, même mot

    profil — retenu, la donnée : ce que le téléphone envoie à la montre
      dans l'envoi descendant, stocké des deux côtés, qui porte les
      quatre réglages et le facteur de correction (§7.3, §9, §12, §13.2 ;
      texte affiché « envoyer ton profil » §5.1, §C.4) ; tour 13
      écran Profil : l'écran du téléphone, autre chose — voir Écrans et
      états ; le même partage que Historique (l'écran) et liste des
      courses résumée (la donnée)
      le critère : le code construit les deux, séparément — la montre
      construit la donnée et ne connaîtra jamais l'écran
      icône profil (§4.1, §12) : l'icône qui ouvre l'écran, notée au
      tour 7, inchangée

    capteur, autorisation, hyresult — retenus, sans rival

    supprimer, suppression — retenu, l'acte de l'utilisatrice, sur le
      téléphone, dans Détail d'une course, seul endroit (§4.2) ; la
      course cesse d'exister des deux côtés (§4.2, §5.3, §12, §C.4)
    effacer — retenu, autre chose : la montre retire sa propre copie
      d'une course une fois la réception confirmée (§9) ; la course
      survit sur le téléphone et revient à la montre dans la liste des
      courses résumée descendante
      deux opérations distinctes, chacune avec son verbe (tour 13) :
      sous un seul verbe, « le seul endroit de l'application où une
      course se supprime » deviendrait faux — §9 décrit un autre endroit
      où une course disparaît de la montre
      disparaître (§9, texte affiché §C.4 « La course disparaîtra aussi
      de l'historique sur la montre ») : la conséquence visible d'une
      suppression, de la prose — pas une troisième opération

    configuration — retenu, une chose distincte et plus large que le
      profil : tout ce que le téléphone décide et que la montre reçoit
      sans pouvoir le modifier — le profil, la référence, la liste des
      courses (§5.3, une occurrence — tour 8)
      remplacer « configuration » par « profil » rendrait la phrase de
      §5.3 fausse : elle énumère la référence et les courses à côté des
      réglages, trois choses dont une seule est le profil

    autorisation — un mot, trois autorisations distinctes (tour 7) :
      autorisation d'accès aux capteurs — retenu, sur la montre (§5.1)
      autorisation d'accès aux appareils à proximité — retenu, sur le
        téléphone (§4.4)
      autorisation d'accès à l'historique de santé — retenu, celle qui
        permet au téléphone de lire l'historique de santé ; §13.4
        l'emploie en entier
        remplace : autorisation (nue, §13.4 — ni les capteurs de la
        montre ni l'accès aux appareils à proximité ne gouvernent cette
        lecture)
      « L'autorisation est vérifiée chaque fois que l'application
        s'ouvre » (§4.4, §5.1) : le mot nu, chacun dans sa section, la
        sienne — inchangé

### Chrono

    chrono — retenu en prose, le compteur qui tourne
      remplace : chronomètre (le substantif — §5.4, §13.2)
      « chronomètre » reste le verbe : « la montre chronomètre
      normalement » (§9) — imposer le substantif ferait collision
    chronométrage — retenu, l'activité de chronométrer ; titre de §11
    chronométrage officiel — retenu, le chronométrage de la course
      qu'hyresult publie
      remplace : chrono officiel

### Écrans et états

    écran — retenu
      remplace : page
      « page » ne subsiste que pour la page système des autorisations
      de l'application (§4.4, §5.1)

    écran — deux choses distinctes, même mot
      l'afficheur physique de la montre (1,5 pouce, 480 × 480) — c'est
      lui qui porte la géométrie de l'arc : « centrés sur l'écran »,
      « centré sur le bas de l'écran »
      un écran de l'application

    cadran — retenu, la face de la montre où le système dessine son
      raccourci (§10) ; terme grand public de Wear OS
      remplace rien — le cadran comme repère de l'arc (§3.3, §6.3) est
      l'écran, retiré dans ce sens

    Projection — retenu, nom de l'écran qui affiche l'arrivée estimée
      pendant la course ; ni bouton ni texte affiché

    liste vide — retenu, un état de l'écran Liste des courses, pas un
      cinquième écran : §4 compte quatre écrans sur le téléphone
      remplace : écran de liste vide (§13.4)
      Historique vide (§C.4) : le même état sur l'écran Historique de
      la montre, nommé par l'écran qu'il concerne — reste

    Historique — retenu, nom de l'écran de la montre qui affiche la
      liste des courses résumée (§5.3 en titre de section, §C.4 pour
      son état vide, §12 — tour 8)
      remplace : Liste des courses résumée (nom d'écran, nœud de §12 —
      un glissement : la liste des courses résumée est la donnée que
      cet écran affiche, pas l'écran ; le nœud devient « « Historique »
      ────────► écran Historique », l'action et l'écran écrits
      distinctement)
      « Historique » : le texte affiché, bouton de l'accueil et titre
      de l'écran — entrée distincte, voir Textes affichés

    écran principal — retenu, en entier partout où l'écran est nommé,
      même règle qu'au tour 7 (§3.2, §6.1, §6.2, §6.6, §7.1, §8, §12,
      §15)
      remplace : Principal (§6.6, une abréviation d'un seul endroit —
      devient « Écran principal → Projection → Contrôle » ; tour 8)

    écran Profil — retenu, l'écran du téléphone, nommé en entier partout
      où il est nommé, comme les six écrans du tour 8 (tour 13) ; une
      destination de navigation, autre chose que profil, la donnée —
      voir Appareils, échanges, session
      remplace : profil (nommant l'écran — §5.2 « depuis le profil »
      devient « depuis l'écran Profil », §12 le nœud « Profil » devient
      « écran Profil », §13.4 « au premier affichage du profil » devient
      « au premier affichage de l'écran Profil », §5.1 « du bouton
      « Autoriser » du profil » devient « de l'écran Profil ») ; écran de
      profil (§4.4 — devient « l'écran Profil affiche »)
      §4.4 garde son titre de section « Profil » ; §C.4 conserve ses
      lignes « Profil » — la colonne y nomme des écrans, le contexte est
      posé
      « Profil » : le titre affiché de l'écran (§C.4)
      que les deux ne se rencontrent jamais sur le même appareil ne
      suffit pas : le Rédacteur écrit un seul document pour les deux
      applications

    Autorisation capteurs — retenu, nom du premier écran de la montre,
      dans le diagramme (§12) comme au catalogue (§C.4)
      remplace : Autorisation (§C.4, nom d'écran) — la colonne « Écran »
      ne dispense pas de nommer l'écran
      Première ouverture : la séquence — autorisation, attente du
      téléphone, accueil — et non l'un de ces écrans

    Liste des courses, Détail d'une course, Import d'un résultat,
      Confirmation de suppression, Écran d'erreur, Écran de fin —
      retenus en entier partout où un écran est nommé : le catalogue
      nomme les écrans, il ne les abrège pas (tour 7, même règle que
      « Autorisation capteurs »)
      remplace : Liste, Détail, Import, Suppression, Erreur, Fin (§C.4,
      colonne « Écran ») ; Import (§12, cible de « Corriger » dans le
      diagramme) ; Erreur (§4.3, en-tête du paragraphe de rendu) ;
      Détail de la course importée (§12, nœud final du diagramme
      téléphone — tour 8 : le même écran ouvert sur la course qu'on
      vient d'importer, §4 en compte quatre ; le nœud le nommait par ce
      qu'il montre à ce moment-là, une description, pas un nom — la
      flèche dit déjà qu'on y arrive depuis l'import)
      « la liste », « le détail », « le détail de la course importée »
      (§4.3, §12 en prose) : des reprises, pas des noms — inchangées

    Première ouverture — retenu, la séquence de la montre, avec sa
      majuscule (§5.1, §12) ; écran d'ouverture — retenu, le premier
      écran du téléphone ; ouvrir un écran ou une boîte — le verbe, le
      complément suffit à séparer les emplois, comme pour « en-tête »
      remplace : première ouverture du profil (§13.4 — devient
      « Proposée au premier affichage du profil » : réutiliser le nom
      d'une séquence en minuscule sur un autre objet coûte une
      hésitation pour rien ; depuis le tour 13, « au premier affichage
      de l'écran Profil »)
      extrémités ouvertes (§4.4, §8.4), la zone qu'il ouvre (§B.4) :
      prose mathématique, pas des termes

    Attente du téléphone — retenu, nom d'écran ; `En attente du
      téléphone` : son titre affiché
      « pendant l'attente » (§5.4, préparation) : de la prose, pas un
      second nom de la préparation ni cet écran, que la montre a quitté
      deux écrans plus tôt — un complément de temps, remplaçable par
      « pendant ce délai » sans rien changer au sens ; la phrase reste
      telle quelle (tour 12) ; le critère : Attente du téléphone nomme
      un écran que le code construit, « l'attente » ne nomme rien
    écran d'ouverture — retenu, le premier écran du téléphone, la liste
      des courses (§4.1, §12) ; sans rival
    écran secondaire — retenu, Projection et Contrôle (§6.1) ; sans
      rival
    aperçu, sélecteur de date, texte indicatif, pile — retenus, sans
      rival

    en-tête — trois emplois, un seul mot, distingués par le contexte
      l'en-tête d'un écran, sur le téléphone (§4.1, §4.2, §4.4, §12)
      l'en-tête de cycle, au-dessus d'un groupe de segments (§3.1,
      §3.3, §4.2) — il n'existe qu'un seul type de groupe, le cycle
      la ligne d'en-tête du tableau collé (§A.4)
      en-tête de cycle remplace : en-tête de groupe, en-têtes de groupe
      (§3.1, §3.3) — un rôle générique sans second cas n'est pas un
      rôle

    geste de retour du système — retenu, la forme complète (§6.6, §12)
      geste de retour : sa reprise (§12)
      remplace : geste système (§12) — ne dit pas ce que le geste fait

    retour — retenu, l'acte générique de revenir à l'écran précédent,
      par quelque moyen que ce soit — un geste ou un bouton (§12, nu
      dans le diagramme montre ; « retour automatique à l'écran
      principal » §6.1, §12 ; « retour écran principal » §12 ; tour 10)
      ne se confond pas avec le geste de retour du système, qui est
      l'un de ces moyens : sous Préparation, la flèche « retour » du
      diagramme couvre « Quitter », que le diagramme ne dessine nulle
      part ailleurs — les deux flèches restent telles quelles

    pilule — retenu, la forme de tous les boutons ; aucun bouton d'une
      autre forme n'existe dans le document
      plein, bordé : ses deux remplissages — pilule pleine, pilule
      bordée
      remplace : bouton plein, bouton bordé (§4.2), boutons principaux
      (§3.3 — l'usage de `radius-pill` devient « Boutons, badges »)
      cercle (§4.1 Rendu, « cercles de 36–38 dp bordés
      `border-strong` ») : la même forme, ce que `radius-pill` produit
      sur un bouton carré — la moitié de 36 dp donne un rayon de 18 dp,
      un disque ; la géométrie obtenue, pas une troisième forme ; les
      deux éléments sont bordés comme une pilule bordée — reste tel quel,
      « pilules de 36–38 dp » serait plus exact et moins clair (tour 10)

    texte seul — retenu, un bouton sans conteneur : « Supprimer »,
      « Quitter », « Arrêter l'activité », « Modifier » — la destination
      et la couleur séparent deux emplois du même composant, pas deux
      composants ; graisse 500 (§3.2)
      remplace : lien (§4.4 — « ouverte par « Modifier », en texte seul
      `link` ») ; actions discrètes (§3.2 — devient « 500 pour les
      unités détachées et les textes seuls » ; tour 8 : nommer un
      composant par sa discrétion plutôt que par sa forme laissait
      croire à un troisième type de bouton)
      `link` : le jeton, inchangé — un jeton nomme une couleur, pas un
      composant

    accent — retenu, le rôle du jeton `link` : le seul accent du thème,
      ni couleur de sens, ni gris de texte, ni couleur de zone ; il
      porte l'action « Modifier » (§4.4) et le badge « Référence »
      (§4.1, §4.2) — deux emplois sur trois ne sont pas des liens
      remplace : Liens (§3.1, colonne Usage de la table des jetons)
      la colonne devient « Accent — action « Modifier », badge
      « Référence » » ; ni « Liens » ni « Textes seuls » — « Supprimer »
      et « Quitter » sont des textes seuls et ne portent pas `link`
      lien : retiré partout, aucun emploi restant

    bouton d'arrêt — retenu, le concept (§5.4, §6.6, §12) ; `Arrêter
      l'activité` : son libellé affiché, le bouton de Contrôle qui
      ouvre la confirmation
      remplace : Arrêter (§12, nœud du diagramme montre — le bouton de
      Contrôle nommé court ; devient « Contrôle ── bouton d'arrêt ──►
      confirmation ──► Écran de fin », tour 8)
      `Arrêter` : un autre texte affiché, le bouton de la confirmation
      d'arrêt, qui mène à l'écran de fin — les deux boutons du chemin
      portent le même mot, seule la forme longue les sépare
    bouton d'annulation — retenu, le concept (§6.5, §12, §13.2) ;
      `Annuler : <segment fermé>` : son libellé affiché (§6.5, §C.2)
      remplace : Annuler le dernier marquage (§12, nœud du diagramme —
      devient « Contrôle ── bouton d'annulation ──► retour écran
      principal », tour 8)
      remplace aussi : Annuler le dernier marquage (§6.5, en gras — la
      description prenait la place du libellé ; tour 9 : les deux puces
      de §6.5 prennent la même construction, le texte affiché en gras
      puis ce que le bouton fait — « **« Annuler : <segment fermé> ».**
      Annule le dernier marquage. […] » et « **« Arrêter l'activité ».**
      Avec confirmation. »)
      dans ce passage, le gras garde un seul sens : il porte le texte
      affiché, jamais la description ; le cas est isolé — §6.1 n'en
      porte pas d'autre, ses gras sont de l'emphase — et se traite
      localement, sans règle d'emphase pour tout le fichier
    bouton d'ajout — retenu, le concept (§4.1, §4.4) ; `+` : son
      libellé affiché

    point d'actionnabilité — retenu, le point de 9 px en haut de
      l'écran principal qui signale que la surface est actionnable
      (§6.2, §6.9) ; §6.2 le nomme désormais, pour que §6.9 ait un
      antécédent

    lancement — retenu, le passage à la préparation, par le bouton
      « Lancer » ; il aboutit toujours (tour 7 : l'ancienne entrée,
      « l'ouverture de la session d'exercice », était un raccourci)
    ouverture de la session d'exercice — retenu, l'acte technique tenté
      au lancement ; il peut échouer, et « Démarrer » le retente (§5.4)
      deux choses distinctes : une préparation affichée sans session
      ouverte est un état nominal (§5.4, fréquence en repli)
    démarrage — retenu, le départ de la course, par le bouton
      « Démarrer » ; le chrono part
      les deux libellés ont été échangés dans le corpus
      §10 « Au démarrage, trois cas » : bien le départ de la course,
      cohérent avec §12 (l'écran de reprise entre « Démarrer » et le
      départ) et §5.4 (« Démarrer » retente d'ouvrir la session) ; le
      contrôle des trois cas a lieu à chaque tentative d'ouverture de la
      session, au lancement comme au démarrage — confirmé au tour 4

    préparation — retenu
      remplace : sas
      la session d'exercice s'ouvre à la préparation, fermée à la fin
      de la course (§10 aligné sur §5.4 ; « fermée à l'arrivée » retiré
      au tour 8)

    mode atténué — retenu
      remplace : mode veille, mode économie ; écran non interactif (§10
      « Quand l'écran n'est pas interactif » — devient « En mode
      atténué, les données sont livrées par paquets plutôt qu'en
      continu » : le vocabulaire de la plateforme, jamais défini par le
      document ; §13.2 donne à la fréquence cardiaque une cadence de
      10 s « en mode atténué », c'est cette livraison par paquets ;
      tour 10)
      affichage permanent : la contrainte d'affichage, retenue aussi —
      deux états, mode atténué ou affichage normal
      jetons `*-dim` inchangés

    affichage normal — retenu, l'état opposé au mode atténué
      remplace : mode normal (§13.1), plein régime (§6.9)

    mise à jour — retenu, une propriété de chaque donnée : le moment où
      sa valeur change ; varie d'une ligne à l'autre des tableaux de
      §13 — colonne et titre de §13, §7.3 (tour 13)
    rafraîchissement — retenu, autre chose : la cadence à laquelle
      l'écran est redessiné en mode atténué, une seule valeur pour tout
      l'affichage, posée contre le défaut de la plateforme (§6.9, §13.1)
      deux choses distinctes, le code construit les deux séparément ;
      « Continu, ou 10 s en mode atténué » (§13.2, fréquence cardiaque)
      est bien la mise à jour de la donnée, et si elle vaut dix
      secondes c'est que le rafraîchissement la borne — une conséquence,
      pas une identité : le rafraîchissement est un réglage, la mise à
      jour une observation ; les deux valeurs coïncident et pourraient
      cesser de coïncider
      « à jour » (§5.2), « mise à jour possible vers Wear OS 6 » (§15) :
      le sens courant, hors vocabulaire

    bloc — retenu, une région de l'écran, et rien d'autre
      « Ligne masquée » pour le temps de référence du segment (§13.2) :
      un lapsus, devient « Bloc masqué » — le temps de référence occupe
      la position Haut, un bloc, et la consigne sous le tableau le
      compte parmi les quatre blocs qui disparaissent (tour 8)
      les deux « Ligne masquée » de §C.2 — « Référence chargée · <nom> »
      et « Zone <n> » — sont justes et restent : ni l'une ni l'autre
      n'occupe une des trois positions d'un écran de course

    carte — retenu, le conteneur en relief (`surface-raised`,
      `radius-card`), partout
      remplace : encart

    badge — retenu, l'étiquette de texte teintée : « Référence »,
      « Incomplète », l'écart en course — toujours du texte sur fond
      teinté, `radius-chip`

    pastille — retenu, l'icône ronde en tête d'une confirmation : `!`
      sur `behind`, `✓` sur `ahead` — jamais de texte, toujours un
      symbole
      remplace : pictogrammes (§3.1, usage de `ahead` et `behind`)

    inactif — retenu, l'état d'un bouton ou d'un geste qui ne répond
      pas ; par symétrie avec « actif », la forme positive employée
      partout (§4.3, §4.4, §6.6, §13.2, §C.2)
      remplace : désactivé (§6.6, §13.2, §C.2)
      segment inactif : autre chose, même mot — voir Cardiaque

    action — retenu, un élément d'interface que l'on actionne :
      « Définir comme référence », « Renommer », « Supprimer »,
      « Autoriser » (§4.1, §4.2, §4.4)
      remplace : option (§4.1)
      « action » au sens d'un comportement (« Synchroniser est une
      action, pas un écran ») : même mot, le contexte suffit

    carré de couleur — retenu, le repère de chaque ligne de zone sur
      l'écran Profil
      remplace : pastille carrée

    raccourci système — retenu, l'élément que le système affiche
      pendant une course et qui ramène à l'application ; dessiné par le
      système, pas par l'application, sur le cadran
      remplace : pastille sur le cadran

    l'ouverture de l'application (§4.4, §5.1) — sans terme : « chaque
      fois que l'application s'ouvre », une tournure verbale
      « lancement » reste à la session d'exercice, « démarrage » à la
      course
      remplace : lancement (dans ce sens — réponse du Rédacteur, Q1,
      « jamais au lancement » devient « jamais à l'ouverture de
      l'application » ; tour 15 : l'ouverture de l'application sur le
      téléphone, « lancement » reste à la montre)

    tiret cadratin `—` — retenu, le glyphe d'absence, un seul glyphe
      sous un seul nom ; §13.1, qui pose la règle générale, le nomme en
      entier : « L'absence s'affiche par un tiret cadratin `—` »
      ailleurs en prose, « tiret » nu reste admis (§4.2, §6.9) : le
      contexte ne laisse aucun doute
      `—:—` : ce même glyphe posé dans la forme de la valeur qu'il
      remplace, pas un second caractère
    tiret demi-cadratin `–` — retenu, le séparateur de plage (§B.4)
    tiret ASCII `-` — retenu, le caractère écarté (§B.2)
      trois caractères distincts, le qualificatif dit lequel ; le mot nu
      ne désigne jamais l'un des deux qualifiés
      signe moins `−` (U+2212, §B.2) : un quatrième trait horizontal,
      déjà nommé autrement, sans conflit

    accueil, vibration — retenus, sans rival

    flèche de tendance — retenu, l'élément que le code construit : une
      direction, une couleur de sens, une zone morte, un masquage (§3.1,
      §6.2, §7.1, §8.3, §13.2, §15) ; « flèche » seule : sa reprise —
      la seule flèche du document (tour 10)
      remplace : flèche (§6.2, rendu de la destination — « la flèche
      seule à 0,85 d'opacité » devient « le caractère `→` à 0,85
      d'opacité ») : pas deux termes, un terme et un caractère — le `→`
      vit dans la chaîne `→ SkiErg`, en ressource ; le code n'en
      construit rien, ne le colore pas, ne le masque pas ; le
      rapprochement avec « segment », « position » et « ligne » ne
      tient pas, ces trois-là portent deux choses réelles chacune

    confirmation — deux choses distinctes sous un mot, comme
      « segment », « position » et « ligne » (tour 8)
      confirmation : la boîte qui demande avant un acte irréversible —
        « demande une confirmation » (§4.2), Confirmation de
        suppression, Confirmation d'arrêt (§6.5, §C.4), « demander
        confirmation » (§10), §12 — neuf emplois
      confirmation de réception : l'accusé qu'un appareil envoie à
        l'autre, un emploi (§9) ; le complément est obligatoire dans ce
        sens, et §9 l'emploie déjà — « après confirmation explicite de
        réception »

    boîte de demande — retenu, la boîte que le système montre quand une
      autorisation est demandée (§4.4, §5.1) ; notée au tour 7 sans
      rival, tranchée au tour 15
      remplace : boîte de dialogue du système (réponse du Rédacteur,
      Q1 — « ouvre la boîte de dialogue du système » devient « ouvre la
      boîte de demande »)
      boîte de saisie numérique (§4.4) : une autre boîte, notée au
      tour 7 ; les confirmations ne sont jamais appelées boîtes

### Textes affichés

    « Lancer » — texte affiché, français, accueil de la montre
      le concept : lancement de la session d'exercice
    « Démarrer » — texte affiché, français, écran de préparation
      le concept : démarrage de la course
    « Réf. <nom> » — texte affiché, français, sans tiret, partout :
      « Réf. Bordeaux 2025 · 1:37:25 » sur l'accueil, « Réf. 4:26 »
      pendant la course
      remplace : « Réf. — <nom> »

    « ⚠ Aucune référence » — texte affiché, français, avec le signe
      partout : c'est un badge d'alerte et le signe porte l'alerte
      remplace : « Aucune référence » (§4.4, §5.2, §13.3)
      un texte de la montre seulement : le téléphone n'affiche rien de
      ce genre — l'état sans référence (§4.2) est un état interne, sans
      guillemets ; remplace : « aucune référence » (§4.2, entre
      guillemets)

    à égalité, inconnu (§13.1) — des concepts, pas des textes affichés :
      les guillemets étaient de l'emphase, retirés
      tour 8 : « à égalité » disparaît, remplacé par écart nul — voir
      Comparaison et mesure ; « inconnu » reste, adjectif de l'écart

    `→ Run 3` — texte affiché, la destination pendant une Roxzone vers
      un RUN, avec sa capitale unique — comme `Réf.` l'est pour
      référence ; le concept : RUN (§6.2)

    « Ouvre l'application sur ton téléphone pour envoyer ton profil. »
      — texte affiché, français ; avec ou sans point final en prose,
      même texte

    « Maximum observé sur 12 mois » — texte affiché, français, la
      mention sous la fréquence cardiaque maximale (§4.4)
    « Modifier » — texte affiché, français, le texte seul en `link`
      deux textes, comme §C.4 les liste ; le point médian entre eux est
      un séparateur de mise en page, jamais un caractère de l'un ou de
      l'autre (§C.1 : les valeurs ne sont jamais concaténées)
      remplace : « Maximum observé sur 12 mois · Modifier » (§4.4, une
      seule chaîne entre guillemets — devient « la mention « Maximum
      observé sur 12 mois » et le texte seul « Modifier » en `link` »)

    « Annuler » — texte affiché, français, le bouton de toutes les
      boîtes de confirmation
      le concept : annulation, l'annulation du dernier marquage (§6.5)

    « Quitter », « Terminer », « Synchroniser », « Historique »,
      « Contrôle » — textes affichés, français
      dans le corpus, ils s'écrivent en gras ou nus : tranché au tour 1,
      les guillemets ne sont pas exigés dans `idees.md`
    « Référence », « Incomplète », « Historique », « Contrôle »,
      « CYCLE n », « Réf. 4:26 », « → SkiErg », « 14/30 » — textes
      affichés ; dans le corpus entre accents graves, tranché au tour 1 ;
      les concepts portant le même mot sont des entrées distinctes
    `RUN`, `STATION`, `ROX_IN`, `ROX_OUT` — des concepts, entre accents
      graves dans la table de correspondance (§A.3) ; tranché au tour 1

    noms de stations affichés, dans l'ordre :
      SkiErg · Sled Push · Sled Pull · Burpee Broad Jump · Rowing ·
      Farmers Carry · Sandbag Lunges · Wall Balls
      remplace : Rameur (par Rowing)
    leurs abréviations dans le résultat collé, jamais affichées :
      SkiErg · Sled Push · Sled Pull · Burpee BJ · Row · F. Carry ·
      S. Lunges · Wall Balls

## Non tranché

### 1. Termes du domaine — balayés et comparés, sans paire trouvée

Tour 15 (réponse du Rédacteur, Q1 — les termes de la réponse, pas du
fichier d'idées) :

    proposition automatique 1, dérivation (Tranché) — posé, Q1,
      tranché : la même chose, la proposition est le résultat — voir
      Tranché, sous dérivation
    lancement 1 (« jamais au lancement »), l'ouverture de l'application
      (Tranché) — posé, Q2, tranché : l'ouverture de l'application sur
      le téléphone, « lancement » reste à la montre — voir Tranché
    boîte de dialogue du système 1, boîte de demande 2 (§4.4, §5.1) —
      posé, Q3, tranché : la même boîte, boîte de demande — voir
      Tranché ; sorti de la ligne du tour 7
    message expliquant 1, mention (Tranché) — posé, Q4, tranché : la
      mention, la phrase sous le titre — voir Tranché, sous mention
    redemander 1, rappel (Tranché) — posé, Q5, tranché : le rappel dit
      comme verbe, sur le téléphone aussi — voir Tranché, sous rappel

Tour 14 :

    trentième segment 1 (§6.2) — posé, Q1, tranché : un numéro en
      apposition au nom, pas un terme ; sorti de la liste des termes
      remplacés sous station Wall Balls — voir Tranché
    nom libre 1 (§14), nom 30+, nom généré 3 (§6.7, §C.2) — posé, Q2,
      tranché : une seule chose, §14 devient « par son nom » ; le nom
      généré est une valeur par défaut du même champ — voir Tranché,
      sous nom et sous nom généré
    total 3 (§11 ×2, §B.6), Total 1 (§A.1) — posé, Q3, tranché : la
      forme nue de temps total, écrite en entier aux quatre endroits —
      voir Tranché, sous temps total ; deux règles générales posées en
      tête de `## Tranché`
    Course 2 (§12, nœud et titre du diagramme montre — le groupe des
      trois écrans de course), course en cours 2 (§6.6, §11), pendant
      la course (§6, §13.2, §C.4 « Montre — course »), hors course (§5,
      §13.3, §3.2) — le même moment, nommé par un nœud et par la prose ;
      le nœud abrège comme « Accueil » et « Préparation » le font ; noté
      au tour 12 sous course en cours, sans rival — non posé
    écran de préparation 1 (§6.6), Préparation 6 (§5.4, §12 nœud, §C.4
      ligne, Rendu de la préparation), la préparation 5 (§5.4, §10 —
      l'état) — l'écran et l'état sous un mot, le même partage que
      Historique ; « écran de préparation » est déjà la forme que le
      Tranché emploie sous « Démarrer » ; pas une paire
    Chrono ou allure central 1 (§6.2, table de rendu), `w-display`
      « Chrono ou allure au centre de l'écran principal » (§3.2) — le
      chrono tranché, le compteur qui tourne ; au centre de l'état
      station il montre le temps écoulé du segment, la donnée ; le
      compteur et sa valeur, deux entrées du Tranché, pas une paire
    Durée vs référence 1 (§13.2, provenance de l'écart sur le RUN) — un
      raccourci de colonne : §8.1 calcule sur `temps_projeté`, la durée
      n'est là qu'une fois le RUN fermé ; un point de fond sur le
      contenu de la cellule, pas un second nom
    champ multiligne 1 (§4.3, Rendu, « Zone de texte : champ multiligne
      haut ») — la description du rendu de la zone de texte, derrière
      les deux-points ; champ noté au tour 12 comme le composant
      générique ; pas un second nom
    proposition initiale 1 (§13.4), proposée automatiquement 1 (§4.4),
      Proposée au premier affichage 1 (§13.4) — le résultat de la
      dérivation, en nom et en participe ; le Tranché dit déjà que ce
      n'est pas un nom ; une forme grammaticale, pas une paire
    facteur retenu 3 (§7.2, §7.3 ×2), rejeté 2 (§7.2, §7.3) — l'état
      d'un facteur de correction passé ou non par le garde-fou ; des
      participes, sans rival
    valeur du profil 1 (§7.3) — le facteur conservé dans le profil,
      reprise ; sans rival
    Roxzone vers la station 1, Roxzone vers la piste 1 (§2, liste
      numérotée), ROX_IN, ROX_OUT (§A.3 ; Tranché) — la description de
      §2 et l'identifiant de §A.3, tranchés ensemble au tour 1 sous
      Roxzone ; pas une paire
    donnée de capteur 1 (§5.4), donnée capteur 1 (§10), donnée issue
      d'un capteur 1 (§13.1) — trois formes grammaticales, notées au
      tour 8 ; une seule chose
    réglages numériques 1 (§4.4 Rendu, « Les deux réglages
      numériques ») — la distance d'un kilomètre et la durée de l'appui
      long, les deux réglages en ligne libellé/valeur hors zones ; une
      reprise, sans rival
    perte de focus 1 (§4.4), incrémenteur 1, curseur 1 (§4.4, exclus),
      lever de poignet 1, toucher de l'écran 1 (§6.9), fournisseur de
      localisation 1 (§7, exclu), sélecteur de fichier 1 (§4.3, exclu)
      — événements et composants, sans rival
    date du jour 1 (§4.3), jour même 3 (§4.3, §B.5, §C.3),
      `aujourd'hui` (affiché) — le même jour, prose et forme affichée ;
      sans rival
    heure du jour 1 (§A.2, la colonne `Time of Day`), heure de départ
      (Tranché), heure passée 1 (§B.1, l'unité) — trois emplois du mot,
      le complément dit lequel
    Distance 2 (§13.2 « Distance ÷ temps écoulé du segment », §B.4
      ligne de format) — reprises de distance mesurée et de la distance
      d'un kilomètre, chacune dans sa table ; le contexte suffit
    bloc central 1 (§15) — le centre de l'écran principal, bloc tranché
      comme région ; sans rival
    état de la montre 1 (§9), envoi unique 1 (§9) — l'envoi descendant
      et ce qu'il remplace, prose
    autorisations système 1 (§10) — les trois autorisations ensemble,
      prose
    appareil 6 — générique, le complément dit lequel
    hr, position, zone (§B.3), duration-segment, duration-elapsed
      (§B.1) — identifiants de format, comme `pace` et `delta` ; pas des
      termes de prose
    Synchronisation (§C.4, ligne « Écran » des deux tables) — l'état
      affiché sur l'accueil et sur l'écran Profil, rangé sous une
      colonne qui nomme des écrans ; la grille en demande l'emplacement,
      pas le lexique

Tour 13 :

    profil 17 — l'écran du téléphone (§4.4, §5.1, §5.2, §12, §13.4,
      §C.4) et la donnée que le téléphone envoie (§7.3 ×3, §9, §12,
      §13.2 ×2, texte affiché §5.1) — posé, Q1, tranché : profil la
      donnée, écran Profil l'écran — voir Tranché ; icône profil 2 :
      l'icône qui ouvre l'écran, notée au tour 7
    supprimer, suppression 13 (§4.2, §5.3, §12, §C.4), effacer 1 (§9),
      disparaître 2 (§9, texte affiché §C.4) — posé, Q2, tranché : deux
      opérations, chacune son verbe — voir Tranché
    mise à jour 5 (titre §13, colonne ×3, §7.3 « mise à jour à la fin de
      chaque course »), rafraîchissement 2 (§6.9, §13.1), à jour 1
      (§5.2, prose) — posé, Q3, tranché : deux choses — voir Tranché ;
      « mise à jour possible vers Wear OS 6 » (§15) : le sens courant,
      hors vocabulaire
    erreur 1 (§4.3, « En cas d'erreur »), échec, échec de lecture 6
      (§A.4, §A.5, §A.6, §C.5, §12) — posé, Q4, tranché : échec de
      lecture, §4.3 remplacé — voir Tranché ; « Un repli n'est pas une
      erreur » (§13.1) : le mot commun, hors import
    trentième segment 1 (§6.2) — le reliquat noté au tour 12, toujours
      présent, toujours non reposé ; le tour 13 ne l'a pas remplacé :
      « Le trentième segment — la station Wall Balls, Roxzone puis Wall
      Balls puis sprint — est traité comme une station » met le terme
      retenu en apposition, et le remplacer nu donnerait « La station
      Wall Balls — la station Wall Balls, … » ; aucune réponse n'a dit
      si l'ordinal reste une description admise ici — à poser au
      prochain balayage, pas à trancher par le lexicographe
    sprint 2 (§2 « sprint vers l'arrivée », §6.2 « puis sprint ») — la
      troisième partie de la station Wall Balls, décrite, jamais un
      segment (§14 l'exclut) ; sans rival
    écrans de course 1 (§3.4), écrans hors course 1 (§3.2), « pendant
      la course » (§6, titre), « hors course » (§5, §13.3) — la
      partition des écrans de la montre ; sans rival.
    sortie 1 (§6.6, « la seule sortie est le bouton d'arrêt ») — la
      façon de quitter la course, prose ; §5.4 dit la même chose avec
      « la seule façon d'arrêter une course » ; « sortie de la station »
      dans le Tranché : autre chose
    dérivée 1 (§7, « l'allure est dérivée des capteurs de la montre ») —
      le verbe au sens commun, calculée à partir de ; dérivation tranché
      ne nomme que l'opération sur l'historique de santé ; pas une paire,
      aucun second nom de l'allure
    intervalle 1 (§7.2, « hors de l'intervalle [0,70 ; 1,40] ») — les
      bornes du garde-fou, une constante ; plage nomme une plage
      affichée, borne la borne d'un réglage ; trois choses, le mot le
      dit
    brute 2 (§7.3 « Allure affichée brute », §8.4 « la valeur brute ») —
      l'allure sans facteur, la fréquence sans hystérésis ; un
      adjectif, deux contextes
    corrigée 4 (§7.2, §7.3, §13.2 ×2) — l'allure multipliée par le
      facteur en vigueur ; sans rival
    seuils simples 1 (§8.4) — les seuils sans le décalage de
      l'hystérésis, prose
    forcer 1 (§9, « Un bouton sur le téléphone permet de forcer »),
      déclencher 2 (§5.2, §9) — les verbes du déclenchement manuel
      d'une synchronisation ; génériques, notés au tour 12 sous
      déclenchement
    carte 1 (§14, « Toute carte, tout tracé de parcours ») — la carte
      géographique, hors périmètre ; autre chose que carte, le
      conteneur — même mot, le voisin « tracé » suffit
    pause 1 (§5.4, « Pas de mise en pause ») — exclu, sans rival
    copier-coller 1 (§A, en tête) — l'acte qui produit le résultat,
      prose ; « coller » reste libre
    ligne de base 1 (§6.2) — la ligne de base typographique, un
      composé, pas un troisième sens de « ligne »
    marge intérieure 1, interligne 1, diamètre 1, repère 1 (§3.3,
      §6.2) — géométrie de rendu, hors balayage
    Samsung Health 1 (§4.4) — le produit où vivent les zones
      inaccessibles ; historique de santé reste la source de la
      dérivation ; deux choses
    Aperçu 5 — l'écran (§12, §C.4) et « Un aperçu avant enregistrement »
      (§4.3, prose) ; sans rival.
    changement d'écran 1 (§6.1) — ce que devient un glissement pendant
      l'appui ; sans rival
    pris en compte 1 (§6.1, « chaque marquage pris en compte ») — le
      marquage validé, prose ; validation notée au tour 7
    segment concerné 1 (§6.5, rendu) — reprise du segment rouvert ;
      prose

Tour 12 :

    trentième segment 1 (§6.2, « **Le trentième segment** — la station
      Wall Balls, Roxzone puis Wall Balls puis sprint — est traité
      comme une station. ») — un terme que `## Tranché` retire sous
      station Wall Balls, encore présent ; pas une paire nouvelle, non
      reposé : le Tranché ne note aucune exception pour cette phrase,
      un tour 2 tranchera s'il faut remplacer ou si l'apposition le
      garde comme description ; trentième marquage 1 (§6.7), 30ᵉ
      marquage 1 (§12) : le marquage, pas le segment — conformes
    surface 3 (§6.1, §6.2, §6.5 — la surface de l'écran, celle qu'on
      touche), `surface` 3 (§3.1, §4.1 — le jeton de couleur, entre
      accents graves) — deux choses, le jeton est un identifiant ; même
      mot, la forme l'écrit
    tronqué, troncature 3 (§B.6 — une durée ramenée à la seconde),
      tronqué 2 (§C.2, §C.5 — un nom ou un libellé coupé) — deux
      opérations, même mot ; le complément dit laquelle
    refus, refusée 3 (§4.4, §C.2 ×2 — une valeur de réglage ou un nom
      vide), refus, refusée 5 (§4.4 ×2, §5.1 ×3, §13.4 — une
      autorisation) — le mot générique de ce qui n'est pas accepté ;
      « rejet » reste au garde-fou ; le complément dit lequel
    ligne fautive 2 (§4.3, §A.5), ligne qui pose problème 1 (§4.3) — la
      même ligne, la seconde forme est de la prose ; ligne <n> : sa
      forme affichée
    course en cours 2 (§6.6, §11) — la course entre le démarrage et la
      fin ; sans rival
    tri 1 (§4.1) — sans rival
    au retour 1 (§2, « traversée à l'aller et au retour ») — la
      traversée de la Roxzone au retour de la station ; autre chose que
      retour, l'acte de revenir à l'écran précédent — même mot, le
      contexte suffit
    Renommer 2 (§4.2 en tête du paragraphe de rendu, §C.4 en nom
      d'écran) — la boîte de renommage, nommée par son bouton ; sans
      rival
    champ 12 — le composant de saisie : zone de texte, nom, date, champ
      numérique en ligne ; boîte de saisie numérique (§4.4) est autre
      chose, notée au tour 7 ; sans rival
    titre 15 — le composant en tête d'un écran ou d'une confirmation ;
      sans rival
    jeton 8, icône 3, ressource 3, clé 1, machine à états 1, moyenne
      glissante 1, numéro de zone 3 (+ `Zone n`, son format) — sans
      rival
    comparaison 7 (§4.2 ×2, §6.2, §8, §9, §14, §A.3), déclenchement 1,
      déclenche 1 (§9, §5.2) — génériques
    historique 1 (§C.4, `Suppression définitive. La course disparaîtra
      aussi de l'historique sur la montre.`) — dans un texte affiché,
      inchangé ; cohérent avec « Historique », titre de l'écran de la
      montre

Tour 10 :

    bouton de synchronisation 1 (§4.4), bouton sur le téléphone 1 (§9),
      bouton pour réessayer 1 (§5.1) — des boutons nommés par leur
      fonction, comme bouton d'arrêt, bouton d'annulation, bouton
      d'ajout ; sans rival, les textes affichés « Synchroniser avec la
      montre », « Réessayer » les portent
    bouton de marquage 2 (§6.1, §6.5), surface actionnable 2 (§6.2) —
      la surface est le bouton, le texte le dit lui-même ; sans rival
    paquets 1 (§10), morceaux 1 (§9) — les données de capteur livrées
      par lots, l'envoi montant découpé : deux choses
    entièrement transférée 1 (§9) — la forme que Q6 du tour 10 donne à
      « complète » dans ce sens ; une tournure, pas un terme
    écart assumé 1 (§6.9) — le sens courant du mot, l'écart à une
      recommandation ; pas la mesure
    groupe 2 (§B.1 « premier groupe », « groupe des heures ») — un
      groupe de chiffres d'un format ; autre chose que le groupe d'un
      cycle (§4.2), noté au tour 7 — même mot, le contexte suffit
    échelle 5 — l'échelle typographique (§3.2 ×3), l'échelle des zones
      (§3.1, §8.4), l'échelle d'un format de temps (§A.4) ; mot
      générique, le complément dit laquelle
    sens 3 (§9 ×2, §8.4) — la direction d'un envoi, d'une bascule ;
      autre chose que les couleurs de sens, l'avance ou le retard —
      même mot, le contexte suffit
    chaîne visible 1 (§C.1), comparaison de chaînes 1 (§A.3) — le mot
      technique de la ressource et du calcul ; « texte » reste le nom
      de ce qui est affiché (annexe C)
    enregistrement 4 (§4.3 ×2, §6.7, §7.2) — la troisième étape de
      l'import, l'écriture d'une course, celle d'un rejet ; générique
    tentative 4 (§5.4 ×2 : ouverture de la session ; §9 ×2 :
      synchronisation) — générique, le contexte suffit
    plage 6 — plage de zone (§4.4 ×2, §13.4 ×2, §B.4) et plage du
      sélecteur de date (§4.3) ; même mot, deux compléments
    cadence 3 — de l'allure (§8.1), de rafraîchissement (§13.1), de
      foulée (§14, hors périmètre) ; générique
    Écrans conditionnels 1 (§12) — titre de section, une catégorie de
      deux écrans ; sans rival
    Fréquence cardiaque de préparation 1 (§13.3) — la fréquence
      cardiaque affichée pendant la préparation ; sans rival
    état d'affichage 1 (§6.2), état 3 (§6.2, les trois de l'écran
      principal) — la forme complète et sa reprise
    segments reconnus 1 (§4.3, prose), `Segments détectés` (affiché) —
      le concept et le texte affiché, deux entrées
    Nom de la station 1 (§6.2), Nom du segment 1 (§13.2) — la même
      donnée, le nom du segment en cours, nommée par le type de segment
      dans le rendu de l'état station
    ligne libellé/valeur 2 (§4.3, §4.4) — une disposition, sans rival
    forme attendue 1 (§4.3) — ce que la carte d'erreur montre en
      `ahead` ; sans rival
    interruption 2 — des mesures (§8.4), de l'affichage (§13.1) — déjà
      noté au tour 8 ; un envoi interrompu (§9), idem

Tour 7 :

    boîte de demande 2 — tranché au tour 15 (Q3), voir Tranché ;
      boîte 2, boîte de saisie numérique 1 (§4.4, §5.1) — trois boîtes,
      une confirmation : les confirmations ne sont jamais appelées
      boîtes dans le fichier
    vibration 2, impulsion 2 (§6.1) — l'événement et son unité, le
      texte les distingue lui-même
    session (reprise de session d'exercice) 2 (§5.4) — reprise du même
      mot
    validation 4 (§4.4 ×2, §6.1, §A.2, §A.5) — d'un marquage, d'une
      valeur, de l'import ; mot générique, le contexte suffit
    colonne d'écart 1, case d'écart 1 (§4.2) — la colonne et sa case
    segment jamais atteint 2 (§4.2, §6.7), segments à venir 2 (§8.2) —
      après l'arrêt, pendant la course : deux choses
    chrono monotone 1 (§13.2), chronométrage monotone 1 (§11) — le
      compteur et l'activité, conformes au Tranché
    utilisatrice 1 (§4.3) — « coureuse » n'apparaît pas dans le fichier
    icône profil 2, icône 1 — même mot
    groupe 1 (§4.2) — le groupe visuel d'un cycle, déjà noté sous
      en-tête
    constante de domaine 1, recommandation officielle 1, date relative
      2, appareils à proximité 3, suivi Hyrox (affiché) 1 — sans rival

Tour 8 :

    interruption des mesures 1 (§8.4), sans nouvelle mesure 1 (§13.1),
      donnée capteur manquante 1 (§10), donnée absente 1 (§13.1) — la
      cause, décrite en prose ; repli 12 reste l'état affiché : deux
      choses
    interrompu (envoi, §9) 1, interruption (§13.1) 1 — pas le sens
      retiré (la course interrompue) : l'envoi, l'affichage
    phrase 2 (§4.2, §C.5) — le nom commun, en prose, pour ce que la
      colonne nomme mention ; pas un composant
    bascule 4 (§6.3, §8.4 ×2 ; §C.1 « mécanisme de bascule », autre
      sens), changement 2 (§8.4) — le passage d'une zone à l'autre ;
      sans rival
    glissement 4 (§6.1, §6.6, §12 ×2), appui long 6, appui 3,
      relâchement 2 — les gestes ; sans rival
    bouton d'action 1 (§5.1) — un bouton en pilule, prose de rendu
    mesures cardiaques 1 (§4.4), donnée cardiaque 1 (§10) — les
      mesures d'une course ; « mesure » tranché couvre les deux
    Reprise de session d'exercice (§C.4), Reprise de session d'exercice
      en cours (§6.5), Reprise d'une session d'exercice en cours (§12)
      — un nom, trois formes grammaticales, pas une paire
    écran d'import 2 (§4.1, §12) — reprise en prose de « Import d'un
      résultat », comme « la liste », « le détail »
    capteur cardiaque 3 (§5.4, §C.4 ×2), capteurs 5 — le capteur et
      l'ensemble ; l'autorisation vise les capteurs, le texte affiché
      nomme le cardiaque
    course créée 1 (§4.4), course écrite 1 (§13.4) — tournures, le
      Tranché dit déjà que « créée » n'est pas un terme ; « écrire »
      reste le verbe de la base locale (§11, §A.5)
    résultat officiel 3, résultat 14 — la forme complète et sa reprise
    fenêtre 1, zone morte 3, garde-fou 2, hystérésis 3, échantillon 1,
      morceaux 1, pile 1, gouttières 1, ellipse 1 — sans rival
    temps projeté 1 (§8.1 prose), `temps_projeté` 1 — le concept et
      son identifiant
    unité détachée 3 (§3.2, §B.3), unité 9 — même chose, l'adjectif
      dit la mise en page
    accueil normal 1 (§5.2) — l'accueil, prose

    écart segment par segment 1 (§8, table des trois écarts) — une
      locution de prose (« segment par segment » sert aussi §1, §2,
      §5.3), pas une forme de « écart par segment » ; non posée, notée
      pour mémoire

    Pour mémoire, sans doute (tour 7) :
    tiret (§4.2, §6.9) — le nom du glyphe, pas le glyphe ; §13.1 le
      nomme et le montre, §13.2 porte le glyphe entre accents graves
    « — jamais absent » (§13.2, §13.4, §C.2) — prose de tableau, sans
      accents graves, à distinguer du `—` affiché : cohérent
