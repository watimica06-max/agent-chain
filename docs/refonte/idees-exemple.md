# Application Hyrox — description

Description de ce que fait l'application. Deux applications : une sur
le téléphone, une sur la montre.

Les encadrés **⚙️ Consigne** portent une contrainte technique qui doit
être respectée au développement.

---

## 1. Objet

Suivre sa performance pendant une course Hyrox, segment par segment, en
se comparant à une course précédente prise comme référence.

Pendant la course, tout se passe sur la montre. Le téléphone sert avant
et après : saisir les anciennes courses, consulter l'historique,
choisir la référence.

---

## 2. Structure d'une course

Une course Hyrox est identique partout : huit kilomètres de course,
chacun suivi d'un atelier, dans un ordre fixe — SkiErg, Sled Push,
Sled Pull, Burpee Broad Jump, Rameur, Farmers Carry, Sandbag Lunges,
Wall Balls. Entre la piste et les ateliers, la Roxzone : la zone de
transition traversée à l'aller et au retour.

**Une course est découpée en 30 segments.**

Pour chacun des sept premiers cycles, quatre segments :

1. le kilomètre de course
2. la Roxzone vers l'atelier
3. l'atelier
4. la Roxzone vers la piste

Soit 28 segments. Puis :

29. le huitième kilomètre
30. le bloc final — Roxzone, Wall Balls, sprint vers la ligne

> **⚙️ Consigne.** Ce découpage est celui du chrono officiel. Une
> course importée et une course enregistrée par la montre se comparent
> segment par segment, sans reconstruction.

---

## 3. Thème

Jetons de conception, nommés en anglais. Les descriptions d'écran s'y
réfèrent par leur nom, jamais par une valeur brute.

### 3.1 Couleurs

| Jeton | Valeur | Usage |
|---|---|---|
| `surface` | `#121110` | Fond général du téléphone |
| `surface-raised` | `#1C1A18` | Cartes, encarts, champs |
| `screen-black` | `#000000` | Fond de la montre — noir pur, OLED |
| `text-primary` | `#F3EFE7` | Valeurs, titres |
| `text-body` | `#C9C4BA` | Texte courant |
| `text-secondary` | `#9A958C` | Unités, dates, libellés |
| `text-tertiary` | `#6F6A62` | Mentions, en-têtes de groupe |
| `border` | `rgba(255,255,255,0.08)` | Séparations, contours de carte |
| `border-strong` | `rgba(255,255,255,0.25)` | Contours de bouton |
| `ahead` | `#4FAE72` | Avance — flèches, pictogrammes |
| `ahead-text` | `#7FCB9C` | Avance — texte sur fond teinté |
| `ahead-bg` | `rgba(79,174,114,0.16)` | Fond des badges d'avance |
| `behind` | `#E2725F` | Retard — flèches, pictogrammes |
| `behind-text` | `#E2957F` | Retard — texte sur fond teinté |
| `behind-bg` | `rgba(226,114,95,0.16)` | Fond des badges de retard |
| `delta-zero` | `#726D63` | Écart nul — ni avance ni retard |
| `link` | `#6FA3D8` | Liens |
| `zone-1` | `#4A90D9` | Zone cardiaque 1 |
| `zone-2` | `#35B0A4` | Zone cardiaque 2 |
| `zone-3` | `#4CAF63` | Zone cardiaque 3 |
| `zone-4` | `#E0A23A` | Zone cardiaque 4 |
| `zone-5` | `#E0503F` | Zone cardiaque 5 |

> **⚙️ Consigne.** Les couleurs de sens — `ahead` et `behind` — ne sont
> **jamais employées seules** : toujours doublées d'un signe et d'une
> flèche.
>
> L'échelle des zones suit le code bleu → rouge de la fréquence
> cardiaque.

### 3.2 Typographie

Deux familles seulement :

| Jeton | Police | Usage |
|---|---|---|
| `font-label` | IBM Plex Sans | Libellés, titres, texte courant |
| `font-data` | IBM Plex Mono, chiffres tabulaires | **Toute donnée chronométrée** |

> **⚙️ Consigne.** `font-data` impose des chiffres à chasse fixe : un
> chrono ne change jamais de largeur en défilant.

Trois graisses, jamais d'autres. 700 pour les titres, les valeurs et
les libellés de bouton. 600 pour les libellés secondaires et les
entrées de menu. 500 pour les unités détachées et les actions
discrètes. `font-data` n'emploie que 700, quelle que soit la taille.

**Échelle montre** — en pixels sur un écran de 480 × 480 :

| Jeton | Taille | Usage |
|---|---|---|
| `w-display` | 110 | Chrono ou allure au centre de la page principale |
| `w-display-sm` | 80 | Temps total de la page de fin |
| `w-value` | 48 | Fréquence cardiaque, destination de Roxzone |
| `w-value-sm` | 40 | Temps écoulé en Roxzone |
| `w-badge` | 37 | Écart en badge |
| `w-title` | 33 | Titres des écrans hors course |
| `w-label` | 24 | Unités, mentions secondaires |
| `w-label-sm` | 20 | Unité `bpm` |
| `w-caption` | 18 | Numéro de zone |

**Échelle téléphone** — en dp :

| Jeton | Taille | Usage |
|---|---|---|
| `p-title` | 22 | Titre d'écran |
| `p-value` | 20 | Temps total d'une course |
| `p-body` | 15 | Texte courant |
| `p-label` | 13 | Libellés de réglage |
| `p-data` | 12.5 | Lignes de segment |
| `p-caption` | 11 | Dates, mentions, badges |

### 3.3 Formes et espacements

| Jeton | Valeur | Usage |
|---|---|---|
| `radius-pill` | moitié de la hauteur | Boutons principaux, badges |
| `radius-card` | 12 | Cartes, encarts, champs |
| `radius-chip` | 14 | Badges d'écart |
| `space-xs` `space-s` `space-m` `space-l` `space-xl` | 4 · 8 · 12 · 20 · 32 | Gouttières |

Rayons et espacements sont **en dp sur le téléphone**. Sur la montre,
ils sont multipliés par 1,83 pour rester dans le repère 480 × 480 des
échelles `w-*`.

L'espacement des lettres varie selon le rôle, pas selon la taille.
0,04em sur les libellés en capitales de taille normale, dont le numéro
de zone. 0,06em sur les en-têtes de groupe et les mentions en capitales
de petite taille — en-tête de cycle, nom d'atelier, « arrivée
estimée », titre d'écran de la montre. 0,08em sur le titre Contrôle. Ni
le texte courant ni aucune donnée chronométrée n'en portent.

**Arc des zones cardiaques** — cinq arcs concentriques au cadran, même
centre que l'écran, longueur angulaire identique, extrémités coupées
net. Valeurs en pixels sur un écran de 480 × 480.

| Jeton | Valeur |
|---|---|
| `arc-radius` | 229 — soit 95 % du rayon de l'écran |
| `arc-span` | 140° au total, centré sur le bas du cadran |
| `arc-segment` | 25,6° par segment |
| `arc-gap` | 3° entre deux segments |
| `arc-width` | 13 — les quatre segments inactifs |
| `arc-width-active` | 33 — le segment actif |
| `arc-opacity-idle` | 0,30 |
| `arc-opacity-active` | 1 |

> **⚙️ Consigne.** Le segment actif s'épaissit **vers l'intérieur**,
> bord extérieur aligné sur celui des quatre autres. Son rayon vaut
> `arc-radius + arc-width/2 − arc-width-active/2`.

### 3.4 Mode veille

Décline les écrans de course sans changer aucune position.

| Jeton | Effet |
|---|---|
| `dim-text` | Valeurs atténuées, position inchangée |
| `arc-width-dim` | 7 au lieu de 13 — segments inactifs affinés |
| `arc-width-active-dim` | 22 au lieu de 33 |
| `arc-opacity-idle-dim` | 0,25 au lieu de 0,30 |

`dim-text` n'est pas une couleur mais une opacité posée sur les
couleurs existantes : 0,55 sur `text-primary` et sur toute donnée
chronométrée, 0,45 sur `text-secondary` et `text-tertiary`. Les
couleurs de sens — `ahead`, `behind`, `delta-zero` — gardent leur
teinte et prennent la même opacité 0,55. Aucun texte ne change de
couleur, seulement d'opacité.

> **⚙️ Consigne.** En veille, l'arc s'allège **par amincissement** :
> les segments restent pleins, plus fins et plus sombres. La géométrie
> ne change pas.

---

## 4. Application téléphone

Quatre écrans.

### 4.1 Liste des courses

Écran d'ouverture. Une carte par course : nom, date, temps total. La
course de référence porte une marque visible.

- Tri par date, la plus récente en haut. À date identique, la course
  ajoutée le plus récemment passe en premier — le critère est interne,
  jamais affiché.
- Bouton d'ajout dans l'en-tête, qui ouvre l'écran de collage.
- Liste vide : un message indique qu'il faut coller un résultat depuis
  hyresult.
- Une course incomplète est marquée comme telle, et l'option d'en faire
  la référence n'apparaît pas.

**Rendu.** Fond `surface`. En-tête : titre `p-title` en `text-primary`,
icône profil et bouton `+` alignés à droite, cercles de 36–38 dp bordés
`border-strong`. Une carte par course en `surface-raised`,
`radius-card` : nom en `p-body`/`text-primary` à gauche, temps total en
`p-value`/`font-data` à droite, date en `p-caption`/`text-secondary`
sous le nom. Badge `Référence` en `link` sur fond teinté, badge
`Incomplète` en `behind-text` sur `behind-bg`, tous deux en
`p-caption`, `radius-chip`.

**Liste vide.** Bloc centré : titre `p-title`, phrase d'explication en
`p-body`/`text-secondary` sur largeur contrainte, bouton
« Coller un résultat » en pilule bordée `border-strong`.

### 4.2 Détail d'une course

Les 30 segments dans l'ordre, avec leur durée et leur temps cumulé,
regroupés visuellement par cycle (kilomètre, Roxzone, atelier,
Roxzone).

Les trente lignes restent affichées même pour une course incomplète,
structure des cycles comprise : un segment jamais atteint porte un
tiret en durée comme en cumul, et sa case d'écart reste vide. Le temps
total affiché est celui des segments réellement courus.

Une colonne d'écart contre la référence, affichée quand la course n'est
pas elle-même la référence.

Trois actions, accessibles depuis l'en-tête de l'écran : **définir
comme référence**, **renommer**, **supprimer**.

« Définir comme référence » est masqué quand la course consultée est
déjà la référence, et masqué aussi quand elle est incomplète.

La suppression demande une confirmation. Supprimer la course de
référence est autorisé : la confirmation le dit, et après suppression
aucune course ne sert plus de comparaison — l'application retombe sur
l'état « aucune référence » et n'en choisit aucune à la place. Une fois
la suppression confirmée, on revient à la liste des courses : le détail
qu'on quittait décrivait la course supprimée.

> **⚙️ Consigne.** C'est le seul endroit de l'application où une course
> se supprime.

**Rendu.** En-tête : nom de la course en `p-title`, date en
`p-caption`/`text-secondary`, temps total en `p-value`/`font-data`,
badge de la référence courante en `link`. Les trois actions en ligne
sous l'en-tête : « Définir comme référence » en bouton plein,
« Renommer » en bouton bordé, « Supprimer » en texte seul `behind`.

Les segments sont groupés par cycle, chaque groupe précédé d'un
en-tête `CYCLE n` en `p-caption`/`text-tertiary`, lettres espacées.
Chaque ligne : nom en `p-data`/`text-primary`, durée et cumul en
`font-data`/`text-secondary`, écart en `font-data` coloré `ahead`, `behind`, ou
`delta-zero` quand il est nul — colonnes alignées à largeur fixe.

**Confirmation de suppression.** Pastille `!` sur fond `behind`, titre
nommant la course, mention que la suppression est définitive et se
répercute sur la montre, boutons « Annuler » bordé et « Supprimer »
plein `behind`. Quand la course est la référence, une phrase
s'intercale avant la mention habituelle — « C'est la course de
référence. Après suppression, plus aucune course ne servira de
comparaison. » Le titre et les deux boutons ne changent pas.

**Renommer.** Champ `radius-card` bordé, pré-rempli avec le nom
actuel, boutons « Annuler » et « Enregistrer ».

### 4.3 Collage d'un résultat

Une zone de texte et un bouton. On colle les quatre colonnes copiées
depuis hyresult ; l'application vérifie et enregistre.

- En cas d'erreur, le message indique la ligne qui pose problème.
- Un aperçu avant enregistrement montre le temps total et le nombre de
  segments reconnus.
- Le nom de la course se saisit ici.
- **La date de la course aussi** : l'export ne porte aucune date, et
  rien ne permet de la déduire. Le champ est pré-rempli avec la date du
  jour, par commodité seulement — une course importée est presque
  toujours antérieure, et la valeur pré-remplie est à corriger. Il se
  modifie par un sélecteur de date standard, dont la plage s'arrête au
  jour même : une date postérieure ne peut pas être choisie, il n'y a
  donc aucun message pour ce cas. Aucune borne basse.
- Le bouton « Importer » reste inactif tant que la zone de collage, le
  nom ou la date ne sont pas renseignés. Aucun message : l'écran
  empêche plutôt qu'il ne refuse.
- Après un enregistrement réussi, on arrive sur le **détail de la
  course importée**, pas sur la liste.

> **⚙️ Consigne.** L'entrée se fait par collage de texte, jamais par
> sélecteur de fichier : les résultats officiels ne s'exportent pas.
>
> **Format, mapping, validation et échantillon réel : annexe A.**

**Rendu.** Zone de collage : champ multiligne haut, `radius-card`,
bordé `border`, texte indicatif en `text-tertiary`. Sous elle, le champ
« Nom de la course », puis le champ « Date de la course ». Bouton
« Importer » pleine largeur, pilule.

**Aperçu.** Pastille `✓` sur fond `ahead`, titre `p-title`, puis deux
lignes libellé/valeur — « Temps total reconnu » et « Segments
détectés » — libellé en `text-secondary`, valeur en `font-data`
`p-value`. Boutons « Corriger » bordé et « Enregistrer » plein.

**Erreur.** Pastille `!` sur fond `behind`, titre nommant la ligne
fautive, explication en `p-body`/`text-secondary`, puis un encart
`surface-raised` montrant la ligne telle qu'elle a été lue en `behind`
et la forme attendue en `ahead`, toutes deux en `font-data`. Bouton
« Revenir au collage ».

L'encart est une illustration, pas une proposition : aucune correction
automatique n'existe, aucun bouton ne l'applique. L'utilisatrice
corrige sa sélection à la source et recolle.

### 4.4 Profil

Accessible par une icône dans l'en-tête de la liste des courses, à côté
du bouton d'ajout.

Quatre réglages :

- **Fréquence cardiaque maximale** — proposée automatiquement, le
  maximum observé sur douze mois dans l'historique de santé du
  téléphone, modifiable à la main.
- **Quatre seuils de zone**, en pourcentage de la FC max. Par défaut
  60, 70, 80 et 90 %. Chaque seuil est la borne **basse** de sa zone :
  la zone *n* va du seuil *n* inclus au seuil *n+1* exclu, la zone 1
  couvre tout ce qui est sous le premier seuil, la zone 5 tout ce qui
  est au-dessus du quatrième. Cinq zones demandent quatre frontières :
  les deux extrémités sont ouvertes.

  Pour une FC max de 187 : zone 1 sous 112, zone 2 de 112 à 130,
  zone 3 de 131 à 149, zone 4 de 150 à 167, zone 5 à partir de 168.

  Le repos actif, que la littérature situe sous 50 %, est absorbé par
  la zone 1 plutôt que de former une catégorie à part : sur une course
  Hyrox cet état ne se produit pas pendant l'effort, et le distinguer
  ajouterait un réglage, un état visuel et un repli sans rien apporter.
- **Distance d'un kilomètre** — la `distance_attendue` du §7.2. 1000 m
  tant qu'elle n'a jamais été modifiée.
- **Durée de l'appui long.** 700 ms par défaut.

Plus un bouton de synchronisation et la date de la dernière
synchronisation réussie.

La fréquence cardiaque maximale s'édite dans une boîte de saisie
numérique, ouverte par le lien « Modifier ». Les seuils de zone, la
distance d'un kilomètre et la durée de l'appui long s'éditent dans un
champ numérique en ligne sur l'écran, validé à la perte de focus.
Aucun incrémenteur, aucun curseur.

Chaque réglage est borné : la fréquence cardiaque maximale de 100 à
230 bpm, un seuil de zone de 30 à 99 % et strictement supérieur au
précédent, la distance d'un kilomètre de 500 à 2000 m, la durée de
l'appui long de 300 à 2000 ms. Tous sont des entiers. Une valeur hors
bornes, non entière, ou qui romprait l'ordre croissant des seuils est
refusée à la validation : le champ reprend sa valeur précédente et un
message court, sous le champ concerné, indique la contrainte —
« Valeur attendue entre <min> et <max>. », « Nombre entier attendu. »,
« Chaque seuil doit être supérieur au précédent. »

Aucun réglage ne s'applique rétroactivement. Une course enregistrée est
figée : ses durées, son facteur de correction et ses mesures cardiaques
ne sont jamais recalculés. Chaque réglage prend effet à partir de la
course suivante — la fréquence maximale et les seuils déterminent l'arc
affiché en course, la distance attendue entre dans le facteur de
correction et dans l'écart sur le tour, la durée de l'appui long agit
sur le marquage. Conséquence à retenir : un réglage modifié sur le
téléphone n'atteint la montre qu'à la synchronisation suivante.
Modifier sa fréquence maximale juste avant de partir, sans
synchroniser, laisse la montre travailler avec l'ancienne valeur.

> **⚙️ Consigne.** Ni les zones configurées dans Samsung Health, ni la
> FC max ne sont accessibles par une application tierce. La FC max se
> dérive de l'historique de fréquence cardiaque, les zones se
> calculent.
>
> **Pas de formule sur l'âge.** La FC max est le maximum observé sur
> douze mois. L'âge n'est ni connu ni demandé.
>
> La lecture de l'historique de santé se fait sur le téléphone
> uniquement.

---

**Rendu.** FC max en `p-value`/`font-data` suivie de l'unité en
`p-caption`/`text-secondary`, avec dessous « Maximum observé sur
12 mois · Modifier », le lien en `link`. Les cinq zones en lignes :
pastille carrée `zone-1` à `zone-5`, libellé, pourcentage et plage en
`font-data`/`text-secondary`, colonnes alignées. La zone 1 n'a pas de
pourcentage à elle — elle commence là où le premier seuil s'arrête — et
sa ligne ne montre que sa plage. Les deux réglages
numériques en lignes libellé/valeur. Bouton « Synchroniser avec la
montre » pleine largeur, pilule bordée, et sous lui la date de
dernière réussite en `p-caption`/`text-tertiary`.

**États de synchronisation.** *En cours* — pictogramme rotatif et
« Ne ferme pas l'application ». *Échouée* — message en `behind` et
bouton « Réessayer ».

**Autorisation d'accès aux appareils à proximité.** Sans elle, la
synchronisation devient indisponible et rien d'autre n'est affecté :
les deux applications restent pleinement utilisables séparément. À la
place de la date de dernière synchronisation, l'écran de profil affiche
« Synchronisation indisponible — l'accès aux appareils à proximité
n'est pas autorisé. », et juste en dessous l'action « Autoriser ». Le
bouton « Synchroniser avec la montre » reste affiché, inactif tant que
l'autorisation manque. La montre, elle, ne dit rien de particulier :
elle affiche « Aucune référence » tant qu'elle n'a rien reçu.

« Autoriser » demande d'abord l'autorisation au système ; si le système
n'affiche plus la boîte de demande — refus définitif ou autorisation
révoquée — il ouvre la page des autorisations de l'application. Le
système indique lui-même si la demande peut encore être présentée :
envoyer systématiquement vers les réglages ferait faire un détour quand
une simple boîte suffirait.

L'autorisation est vérifiée à chaque lancement. Révoquée depuis les
réglages système, elle produit exactement le même état qu'un refus
initial, et aucune nouvelle demande n'est déclenchée automatiquement.

---

## 5. Application montre — hors course

### 5.1 Première ouverture

1. Demande d'autorisation d'accès aux capteurs, une seule fois, avec
   une phrase expliquant à quoi elle sert.
2. Attente du téléphone : « Ouvre l'application sur ton téléphone pour
   envoyer ton profil », avec un bouton pour réessayer.

> **⚙️ Consigne.** Autorisation refusée : l'application reste
> utilisable. Chrono, segments et écarts fonctionnent ; la fréquence
> cardiaque et l'arc des zones sont en repli permanent. La demande
> n'est jamais rejouée d'elle-même — un rappel sur l'écran d'accueil
> est la seule reprise, et c'est une action.
>
> Ce rappel demande d'abord l'autorisation au système ; si le système
> n'affiche plus la boîte de demande — refus définitif ou autorisation
> révoquée — il ouvre la page des autorisations de l'application.
> Exactement le comportement du bouton « Autoriser » du profil (§4.4) :
> le système indique lui-même si la demande peut encore être présentée,
> et envoyer systématiquement vers les réglages ferait faire un détour
> quand une simple boîte suffirait.
>
> L'autorisation est vérifiée à chaque lancement. Révoquée depuis les
> réglages système plutôt que refusée dans l'application, elle produit
> exactement le même comportement qu'un refus initial, et aucune
> nouvelle demande n'est déclenchée automatiquement.

**Rendu.** Titre en `w-title`, phrase d'explication en
`w-label`/`text-secondary`, bouton d'action en pilule. Écrans centrés,
texte sur trois lignes maximum.

### 5.2 Écran d'accueil

De haut en bas :

- **La référence en cours**, en petit : « Réf. — Bordeaux 2025 ·
  1:37:25 ». Sans référence chargée : « Aucune référence ».
- **Démarrer**, un gros bouton au centre.
- En faisant défiler : **Historique** et **Synchroniser**.

Démarrer reste actif même sans référence.

**Synchroniser** est une action, pas un écran : elle déclenche l'envoi
et affiche son résultat sur place. Même principe sur le téléphone,
depuis le profil.

Les trois mêmes états qu'au téléphone, affichés sur l'accueil sans le
quitter. *En cours* — indicateur d'activité et « Ne ferme pas
l'application ». *Échec* — « Synchronisation impossible — approche le
téléphone de la montre. » et « Réessayer ». *Réussite* — retour à
l'accueil normal, avec la référence et l'historique à jour.

**Rendu.** Référence en haut : « Réf. — <nom> » en
`w-label`/`text-secondary`, temps en dessous en `font-data`. Sans
référence, un badge « ⚠ Aucune référence » en `behind-text` sur
`behind-bg`, `radius-chip`. Bouton **Démarrer** en pilule pleine largeur, **bordé et non plein** :
bordure de 2 px en `text-primary`, fond `text-primary` à 7 %
d'opacité, libellé en `text-primary`. En dessous, « Historique » et
« Synchroniser » en pilules bordées `border-strong`, libellé en
`text-body`.

### 5.3 Historique

La liste des courses en version résumée : nom, date, temps total. Le
détail segment par segment n'existe que sur le téléphone.

> **⚙️ Consigne.** Aucune saisie ni aucun réglage sur la montre : elle
> est en lecture seule sur toute la configuration. Le favori ne s'y
> change pas, une course ne s'y supprime ni ne s'y renomme.

**Rendu.** Titre `Historique` en `w-label`/`text-tertiary`, lettres
espacées. Une ligne par course : nom en `w-label`/`text-primary`, date
et temps total sur la ligne suivante en `font-data`/`text-secondary`.

### 5.4 Démarrage, en deux temps

- **Préparation**, dans le sas. La session d'exercice s'ouvre, les
  capteurs montent en régime, l'application vérifie qu'elle a une
  référence. La fréquence cardiaque s'affiche pendant l'attente.
- **Lancement**, au coup de départ. Le chrono part, le premier segment
  s'ouvre.

Un bouton **Quitter** ferme la préparation et revient à l'accueil.
Tant que le chrono n'est pas parti, rien n'est enregistré.

> **⚙️ Consigne.** La session d'exercice s'ouvre à la **préparation**,
> pas au lancement : le capteur cardiaque a besoin de ce délai pour
> accrocher. Le chronomètre ne démarre qu'au lancement.
>
> Si l'ouverture de la session échoue, la préparation reste affichée
> avec la fréquence en repli, et **Lancer** demeure actif.
>
> Appuyer sur **Lancer** retente alors d'ouvrir la session. Si cette
> tentative échoue à son tour, la course démarre sans donnée de capteur
> pour toute sa durée : aucune nouvelle tentative n'a lieu en cours de
> course.

> **⚙️ Consigne.** Pas de mise en pause. Le seul moyen d'interrompre
> une course est le bouton d'arrêt.

---


**Rendu de la préparation.** Libellé « Fréquence cardiaque » en
`w-caption`/`text-tertiary`, valeur en `font-data`/`w-display-sm`.
Badge « Référence chargée · <nom> » en `ahead-text` sur `ahead-bg`.
Bouton **Lancer** en pilule pleine, et « Quitter » en texte seul
`text-secondary`.

---

## 6. Application montre — pendant la course

### 6.1 Principes d'interaction

- **Toute la surface de l'écran est le bouton d'avancement.** L'appui
  long se fait n'importe où, sur toutes les pages sauf la page
  Contrôle.
- **Une vibration** confirme chaque marquage pris en compte.
- **Retour automatique à la page principale** après chaque marquage, et
  après **8 secondes** sans interaction sur une page secondaire.

> **⚙️ Consigne.** Le temps du segment est relevé au moment où le doigt
> se pose, pas au relâchement. Un relâchement avant le seuil annule le
> marquage et n'écrit rien.
>
> Un **glissement de plus de 20 px** pendant l'appui annule le
> marquage : le geste devient un changement de page.
>
> Aucun délai minimum entre deux marquages.
>
> **Vibration** : une impulsion courte unique à la validation d'un
> marquage, deux impulsions brèves à l'annulation d'un marquage. Rien
> pendant l'appui.

### 6.2 Page principale — trois états

Le bloc du bas ne change jamais : fréquence cardiaque et arc des zones.
Seuls le haut et le centre s'adaptent au segment en cours.

**Pendant un kilomètre**

| Position | Contenu |
|---|---|
| Haut | L'écart sur ce tour par rapport à la référence |
| Centre, en gros | `allure-segment` en min/km, avec une flèche de tendance |
| Bas | Fréquence cardiaque et arc des zones |

La comparaison est **tour par tour**, pas cumulée : la référence donne
6:30 sur ce kilomètre, on court à 6:00, l'écran affiche 30 secondes.

La flèche compare `allure-lissee` à `allure-segment`, avec une zone
morte (§8.3).

**Pendant un atelier**

| Position | Contenu |
|---|---|
| Haut | Le temps de la référence sur cet atelier |
| Centre, en gros | Le temps écoulé depuis le début de l'atelier |
| Bas | Fréquence cardiaque et arc des zones |

Pas d'écart calculé.

**Pendant une Roxzone**

| Position | Contenu |
|---|---|
| Haut | Le temps écoulé dans la transition |
| Centre, en gros | La prochaine étape : `→ SkiErg` pour un atelier, `→ Run 3` pour un kilomètre |
| Bas | Fréquence cardiaque et arc des zones |

Pas d'écart calculé.

**Le trentième segment** — le bloc final, Roxzone puis Wall Balls puis
sprint — est traité comme un atelier. Le nom affiché est Wall Balls, le
temps de référence est celui du bloc final de la course de référence,
et le centre montre le temps écoulé depuis le début du bloc. Aucun
quatrième état d'affichage n'est créé.

> **⚙️ Consigne.** L'écran fait 1,5 pouce en 480 × 480 et il est rond.
> Trois blocs lisibles au maximum, pas quatre.


**Rendu commun aux trois états.** Fond `screen-black`. Les trois blocs
sont répartis verticalement, espacés régulièrement, avec une marge
intérieure de 12 % en haut et 11 % en bas du diamètre.

Un **point de 9 px** en `rgba(255,255,255,0.35)`, centré à 6 % du haut
de l'écran, signale que la surface est actionnable. Aucun bouton n'est
dessiné.

| Élément | Jetons |
|---|---|
| Badge d'écart | `font-data`, `w-badge`, `radius-chip`, `ahead-text` sur `ahead-bg` ou `behind-text` sur `behind-bg` |
| Chrono ou allure central | `font-data`, `w-display`, `text-primary`, interligne 1 |
| Unité `/km` | `font-label`, `w-label`, `text-secondary` |
| Flèche de tendance | `ahead` ou `behind`, alignée sous l'unité |
| Nom de l'atelier | `font-label`, `w-label`, `text-tertiary`, lettres espacées, capitales |
| Temps de référence `Réf. 4:26` | `font-data`, `w-label`, `text-secondary` |
| Temps de Roxzone | `font-data`, `w-value-sm`, `text-primary` |
| Destination `→ SkiErg` | `font-label`, `w-value` — la flèche seule à 0,85 d'opacité, le nom en `text-primary` à pleine opacité |
| Fréquence cardiaque | `font-data`, `w-value`, `text-primary` |
| Unité `bpm` | `w-label-sm`, `text-secondary` |
| Numéro de zone | `w-caption`, `text-tertiary`, lettres espacées |

L'unité et la flèche de tendance sont empilées à droite du chrono,
alignées sur sa ligne de base. La fréquence, son unité et le numéro de
zone forment un bloc centré unique, posé au-dessus de l'arc.

### 6.3 Arc des zones cardiaques

Cinq segments de même taille suivant la courbure basse de l'écran,
chacun d'une couleur. Le segment de la zone courante est plus épais et
pleinement saturé, les quatre autres sont atténués. Au-dessus, la
fréquence en battements par minute.

> **⚙️ Consigne.** Hystérésis de 3 bpm à la bascule (§8.4).

**Rendu.** Cinq arcs `zone-1` à `zone-5` de `arc-segment` chacun,
séparés de `arc-gap`, couvrant `arc-span` centré sur le bas du cadran,
au rayon `arc-radius`, extrémités coupées net. Le segment actif prend
`arc-width-active` et `arc-opacity-active` ; les quatre autres gardent
`arc-width` et `arc-opacity-idle`.

### 6.4 Page Projection

| Position | Contenu |
|---|---|
| Haut | L'écart cumulé depuis le départ |
| Centre, en gros | L'estimation du temps d'arrivée |
| Bas | Le temps total écoulé et la position, « 14/30 » |

L'appui long reste actif sur cette page.

> **⚙️ Consigne.** Calcul en §8.2.

**Rendu.** Badge d'écart cumulé en haut, mêmes jetons que sur la page
principale. Temps d'arrivée estimé en `font-data`/`w-display`. Sous
lui, la mention « arrivée estimée » en `w-caption`/`text-tertiary`,
lettres espacées. En bas, temps écoulé et position sur une seule
ligne en `font-data`/`w-label`/`text-secondary`.

### 6.5 Page Contrôle

Deux boutons :

- **Annuler le dernier marquage.** Le bouton nomme le segment rouvert,
  celui que le dernier marquage a fermé : « Annuler : Roxzone →
  SkiErg ».
- **Arrêter l'activité.** Avec confirmation.

> **⚙️ Consigne.** C'est le seul écran où la surface n'est pas le
> bouton d'avancement.
>
> L'annulation est à un seul niveau et porte sur le dernier marquage
> uniquement, sans limite de temps.
>
> Arrêter coupe le chrono et les mesures. Une session d'exercice
> continue de tourner quand l'application n'est plus à l'écran :
> quitter l'application n'arrête rien.

**Rendu.** Titre `Contrôle` en `w-label`/`text-tertiary`, lettres
espacées. Bouton d'annulation en pilule pleine largeur nommant le
segment concerné. « Arrêter l'activité » en dessous, en texte seul `behind`, moins
saillant que le premier.

**Confirmation d'arrêt.** Titre, mention que la course sera enregistrée
telle quelle et marquée incomplète, puis « Annuler » bordé et
« Arrêter » plein `behind`.

**Reprise d'activité en cours.** Même structure : titre, mention que
l'activité en cours sera arrêtée, « Annuler » et « Continuer ».

### 6.6 Navigation

Principale → Projection → Contrôle, toutes vers la droite.

> **⚙️ Consigne.** Aucune page vers la gauche. Le glissement depuis le
> bord gauche est le geste de retour du système.
>
> Ce geste est **désactivé pendant toute la course** — page principale,
> Projection, Contrôle et écran de fin. Quitter une course en cours par
> un geste accidentel n'est pas acceptable : la seule sortie est le
> bouton d'arrêt. Sur l'écran de préparation et partout hors course, il
> fonctionne normalement.

### 6.7 Page de fin

Après le trentième marquage, la course s'arrête. L'écran affiche le
temps total, l'écart final à la référence, et le nom automatique de la
course — sa date et son heure.

L'enregistrement est automatique, sans validation. Un bouton
**Terminer** ramène à l'écran d'accueil.

Le même écran sert à une course arrêtée en route. Son écart final est
l'écart cumulé au dernier segment fermé, et l'écran indique que la
course est incomplète. Les segments jamais atteints n'entrent dans
aucun calcul.

**Rendu.** Bloc centré : temps total en `font-data`/`w-display-sm`,
badge d'écart final en dessous, puis date et heure en
`font-data`/`w-caption`/`text-tertiary`. Bouton **Terminer** en bas.

### 6.8 Course interrompue

Une course arrêtée en route est enregistrée telle quelle et marquée
incomplète.

> **⚙️ Consigne.** Une course incomplète ne peut pas devenir la
> référence.

### 6.9 Affichage permanent

L'écran reste visible pendant toute la course, sans avoir à lever le
poignet. En mode économie, les valeurs sont visuellement atténuées.

> **⚙️ Consigne.** Rafraîchissement en mode économie : **dix
> secondes**, et non la valeur par défaut d'une fois par minute. Retour
> au plein régime au lever de poignet **comme au toucher de l'écran**.
>
> Forcer l'écran allumé en pleine luminosité est exclu.
>
> Les valeurs vives restent affichées, atténuées. **Écart assumé** par
> rapport à la recommandation officielle, qui prévoit un tiret.
>
> L'écran reste très majoritairement noir. L'arc s'allège par
> amincissement (§3.4).

**Rendu.** Applique `dim-text` et les variantes `*-dim` de l'arc
(§3.4). **Aucune position ni aucune taille de texte ne change** :
seules l'épaisseur de l'arc et les opacités varient. Le point
d'actionnabilité reste visible.

---

## 7. Allure et distance

La course se déroule en intérieur. Le GPS est inutilisable ; l'allure
est dérivée des capteurs de la montre.

### 7.1 Les deux allures

| Nom | Définition | Usage |
|---|---|---|
| `allure-segment` | Distance parcourue depuis le début du segment ÷ temps écoulé depuis le début du segment | **Affichée au centre** de la page principale ; base de l'écart sur le tour |
| `allure-lissee` | Moyenne glissante de la vitesse instantanée sur **10 secondes** | **Jamais affichée.** Sert uniquement à orienter la flèche de tendance |

Les deux sont multipliées par le facteur de correction courant, puis
converties en minutes par kilomètre.

> **⚙️ Consignes.**
>
> - Aucun usage du GPS ni d'un fournisseur de localisation.
> - `allure-segment` est remise à zéro à chaque marquage : elle ne
>   porte que sur le segment en cours.
> - `allure-segment` n'est calculée que sur les segments `RUN`.
> - `allure-lissee` : tant que la fenêtre de 10 secondes n'est pas
>   pleine, le calcul porte sur ce qui est disponible ; sous
>   **3 secondes** de données, elle est en repli.
> - Sous **50 mètres** parcourus dans le segment, `allure-segment` est
>   en repli.

### 7.2 Facteur de correction

À la fin de chaque kilomètre :

```
k_mesuré = distance_attendue / distance_mesurée_sur_le_segment_RUN
k        = 0,6 × k_mesuré + 0,4 × k_précédent
```

> **⚙️ Consignes.**
>
> - **Poids 0,6 sur le dernier kilomètre**, 0,4 sur le facteur en
>   vigueur. Au premier calcul, `k_précédent` est la valeur initiale.
> - **Garde-fou** : un `k_mesuré` hors de l'intervalle **[0,70 ; 1,40]**
>   est rejeté. Le facteur en vigueur est conservé et le rejet
>   enregistré avec la course. Cet enregistrement est purement interne :
>   il sert à réanalyser une calibration après coup et n'apparaît sur
>   aucun écran.
> - Une distance mesurée nulle ou absente ne produit aucun facteur.
> - Le facteur **ne s'applique jamais rétroactivement** : les durées
>   des segments déjà fermés ne sont pas recalculées. Seule l'allure
>   affichée est corrigée, à partir du kilomètre suivant.
> - Le facteur s'applique aux deux allures (§7.1).
> - Chaque facteur retenu est conservé avec la course, avec le numéro
>   du kilomètre dont il vient.

### 7.3 Valeur initiale et repli

Le facteur de départ d'une course est **le dernier facteur retenu, tous
historiques confondus**, conservé dans le profil.

| Situation | Facteur initial | Effet au 1ᵉʳ kilomètre |
|---|---|---|
| Un facteur a déjà été retenu | Ce facteur | Allure corrigée |
| Aucun facteur n'a jamais été retenu | **1** | Allure affichée brute |

> **⚙️ Consignes.**
>
> - Le facteur est stocké **dans le profil**, pas rattaché à une
>   course : une seule valeur, mise à jour à la fin de chaque course.
> - Une course **importée** ne produit aucun facteur. Seules les
>   courses enregistrées par la montre alimentent la calibration.
> - Si tous les facteurs d'une course ont été rejetés par le garde-fou
>   (§7.2), la valeur du profil reste inchangée.
> - Supprimer une course ne modifie pas le facteur.
> - Un facteur à 1 **n'est pas signalé à l'écran**.

---

## 8. Comparaison et écarts

Trois écarts distincts, à ne pas confondre :

| Où | Quoi |
|---|---|
| Page principale, kilomètre | Écart sur le tour en cours uniquement |
| Page Projection | Écart cumulé depuis le départ |
| Détail d'une course, téléphone | Écart segment par segment, après course |

### 8.1 Écart sur le tour

```
temps_projeté = distance_attendue / allure-segment
écart         = temps_projeté − temps_référence_du_segment
```

> **⚙️ Consignes.**
>
> - Recalculé en continu, à la cadence de l'allure.
> - Repose sur `allure-segment`, jamais sur `allure-lissee` (§7.1).
> - **Le temps projeté ne descend jamais sous le temps déjà écoulé**
>   dans le segment.
> - Ce calcul n'existe que sur les segments `RUN`.

### 8.2 Écart cumulé et arrivée estimée

```
écart_cumulé  = Σ (temps_réel − temps_référence) sur les segments fermés
                + écart du segment en cours

arrivée       = temps_écoulé
                + reste_du_segment_en_cours
                + Σ temps_référence des segments à venir
```

> **⚙️ Consignes.**
>
> - Le **segment en cours** compte pour son temps de référence tant
>   qu'il n'est pas dépassé, puis pour son temps réel une fois dépassé.
> - Les segments **à venir** comptent pour leur temps de référence,
>   sans pondération.
> - Recalculé à chaque marquage, et en continu pour la part du segment
>   en cours.

### 8.3 Flèche de tendance

Compare `allure-lissee` à `allure-segment` (§7.1).

> **⚙️ Consignes.**
>
> - **Zone morte de 2 %** : en deçà de 2 % d'écart entre les deux
>   allures, aucune flèche n'est affichée. La flèche demande
>   strictement plus de 2 % — à exactement 2 %, rien.
> - Flèche vers le haut quand `allure-lissee` est **plus rapide** que
>   `allure-segment`, donc quand le nombre en minutes par kilomètre
>   **diminue**.
> - Aucune flèche tant que l'une des deux allures est en repli.

### 8.4 Zones cardiaques

> **⚙️ Consignes.**
>
> - La bascule vers la zone supérieure demande de dépasser sa borne de
>   **3 bpm**. Le retour vers la zone inférieure demande de descendre
>   de **3 bpm** sous cette même borne. Le seuil est inclusif dans les
>   deux sens : à exactement 3 bpm, la bascule a lieu.
> - L'hystérésis décale une frontière, elle ne limite pas la vitesse de
>   changement. Seule la frontière entre la zone active et sa voisine
>   immédiate est décalée ; une lecture qui en franchit deux d'un coup
>   affiche directement la zone qui contient la valeur brute, sans
>   passer par les zones intermédiaires. Ce n'est pas une oscillation,
>   c'est un vrai changement d'effort, et le retarder afficherait une
>   zone fausse.
> - Après une interruption des lectures, la zone est établie à neuf sur
>   la première lecture qui revient, par les seuils simples et sans
>   hystérésis ; celle-ci s'applique de nouveau à partir de cette zone.
>   La fréquence a pu changer beaucoup entre-temps : se référer à la
>   zone d'avant afficherait une zone périmée.
> - **Toute fréquence lue tombe dans une zone.** Les deux extrémités
>   de l'échelle sont ouvertes (§4.4) : un segment de l'arc est donc
>   toujours actif dès qu'une valeur est lue, si basse ou si haute
>   soit-elle.
> - Sans fréquence cardiaque, aucune zone n'est active. C'est le seul
>   cas sans zone.

### 8.5 Roxzones

> **⚙️ Consigne.** La durée d'une Roxzone dépend de la disposition de
> la salle — de 1 seconde à 1 min 33 selon l'atelier. Un écart de
> Roxzone n'est jamais présenté comme une contre-performance.

---

## 9. Synchronisation montre ↔ téléphone

Chaque sens ne transporte qu'une seule chose.

**Du téléphone vers la montre** — un envoi unique contenant le profil,
la référence complète avec ses 30 segments, et l'historique résumé.

**De la montre vers le téléphone** — uniquement les courses
enregistrées.

**Déclenchement** — automatique dès que la liaison entre les deux
appareils est établie, dans les deux sens. Un bouton sur le téléphone
permet de forcer.

**Sans référence**, la montre chronomètre normalement, sans écart ni
estimation d'arrivée.

> **⚙️ Consigne.**
>
> - L'envoi descendant **remplace intégralement** l'état de la montre.
>   Aucune fusion, aucune comparaison. Une course supprimée sur le
>   téléphone disparaît de la montre à l'envoi suivant.
> - L'historique résumé descendant est **borné aux 20 courses les plus
>   récentes**. La référence part toujours en entier.
> - Le transfert montant se fait en morceaux. La course n'apparaît sur
>   le téléphone que complète ; un transfert interrompu reprend depuis
>   le début.
> - La montre n'efface une course qu'après confirmation explicite de
>   réception. Elle réapparaît ensuite dans l'historique résumé
>   descendant.
> - Une tentative échouée est retentée à la prochaine liaison établie,
>   sans nouvelle tentative entre-temps.
> - **Rien ne se synchronise pendant la course.** Un téléphone absent
>   ou déchargé n'a aucun effet sur le chrono.

---

## 10. Capteurs

> **⚙️ Consignes.**
>
> - **Une seule session d'exercice pour toute la course**, ouverte au
>   départ, fermée à l'arrivée. Les 30 segments sont des marquages à
>   l'intérieur.
> - **Le système n'autorise qu'un exercice à la fois**, toutes
>   applications confondues. Au démarrage, trois cas :
>   - *une autre application occupe la place* → demander confirmation,
>     en indiquant que l'activité en cours sera arrêtée ;
>   - *c'est notre propre course* → reprendre là où elle en était, ne
>     pas redémarrer. L'état repris vient de la base locale, pas de la
>     session capteur ;
>   - *rien en cours* → démarrer normalement.
> - **Vérifier la disponibilité de chaque type de donnée** avant de s'y
>   fier : elle varie selon l'appareil.
> - **Une donnée capteur manquante est un cas normal.** Le chrono
>   continue.
> - Quand l'écran n'est pas interactif, les données sont livrées par
>   paquets plutôt qu'en continu.
> - Une pastille sur le cadran permet de revenir à l'application
>   pendant toute la course.
> - **Aucune donnée cardiaque ne quitte les deux appareils** : rien
>   n'est transmis à un serveur, rien n'est partagé, rien n'est
>   exporté. Les autorisations système suffisent — l'application
>   n'ajoute aucune étape de consentement propre.

---

## 11. Chronométrage

> **⚙️ Consignes.**
>
> - **Chronométrage monotone**, insensible à un changement d'heure
>   système. L'heure réelle n'est enregistrée qu'une fois, au départ.
> - **Un segment est mesuré, jamais déduit.** Le total est la somme des
>   segments ; un segment n'est jamais le total moins les autres.
> - **Une transition est atomique** : fermer le segment précédent et
>   ouvrir le suivant se font en une seule écriture.
> - **Une course en cours survit à un redémarrage** de l'application.
>   L'instant d'ouverture du segment courant est écrit en base au
>   marquage ; au redémarrage, le segment reprend à cet instant.

---

## 12. Navigation

### Téléphone

```
Liste des courses  ──── appui sur une carte ────►  Détail d'une course
   (écran d'ouverture)                                    │
   │  │                                                   │
   │  └── icône profil (en-tête) ──►  Profil              │
   │                                    │                 │
   │                                    └── Synchroniser (action, sur place)
   │
   └── bouton + (en-tête) ──►  Collage d'un résultat
              ou bouton de la liste vide      │
                                              ▼
                                        « Importer »
                                          │        │
                                    succès │        │ échec
                                          ▼        ▼
                                      Aperçu    Erreur de lecture
                                        │  │        │
                            Enregistrer │  │        └── « Revenir au collage »
                                        │  └── « Corriger » ──► Collage
                                        ▼
                              Détail de la course importée
```

Depuis le **détail d'une course** : définir comme référence, renommer,
supprimer (avec confirmation). Retour à la liste par le geste système.

Le geste de retour remonte pas à pas, dans l'ordre inverse du chemin
parcouru. Une exception : après un enregistrement réussi, l'écran de
collage et l'aperçu sortent de la pile, et le retour depuis le détail
de la course importée ramène à la liste.

### Montre

```
Première ouverture
   Autorisation capteurs ──►  Attente du téléphone ──►  Accueil

Accueil
   ├── Démarrer ──────────►  Préparation (sas)
   │                            │  │
   │                            │  └── retour ──► Accueil
   │                            ▼
   │                         Lancer ──►  Course
   │
   ├── Historique ────────►  Liste résumée ──► retour ──► Accueil
   └── Synchroniser ──────►  action sur place, reste sur l'accueil

Course
   Page principale  ◄──glissement──►  Projection  ◄──glissement──►  Contrôle
        (trois états selon le segment)

   Depuis n'importe quelle page sauf Contrôle : appui long ──► segment suivant
   Après un marquage, ou après 8 s sans interaction :
        retour automatique à la page principale

   Contrôle ── Annuler le dernier marquage ──► retour page principale
   Contrôle ── Arrêter ──► confirmation ──►  Page de fin

   30ᵉ marquage ────────────────────────────►  Page de fin

Page de fin ── « Terminer » ──►  Accueil
```

### Écrans conditionnels

- **Reprise d'une activité en cours** — s'intercale entre « Lancer » et
  le démarrage de la course, uniquement si une autre application occupe
  le capteur d'exercice.
- **Attente du téléphone** — s'affiche à la place de l'accueil tant
  qu'aucun profil n'a été reçu.

> **⚙️ Consigne.** Le résultat d'une synchronisation est visible sur
> les deux appareils : succès, échec, et date de la dernière réussite.

---

## 13. Provenance, mise à jour, repli

### 13.1 Règles transverses

> **⚙️ Consignes.**
>
> - **Une donnée absente n'est jamais remplacée par zéro** — `+0:00`
>   signifie « à égalité », pas « inconnu ». L'absence s'affiche par un
>   tiret ou par le masquage du bloc.
> - **Une valeur périmée n'est jamais figée en silence.** Au-delà de
>   **10 secondes** sans nouvelle mesure en mode normal, une donnée
>   issue d'un capteur — fréquence cardiaque, distance — repasse au
>   repli plutôt que de conserver la dernière valeur reçue. En mode
>   économie, le seuil est celui de la cadence de rafraîchissement,
>   soit 10 secondes également.
> - **Un repli n'est pas une erreur.** Aucun message, aucune
>   interruption.
> - **Le chrono ne se replie jamais.**

### 13.2 Montre — pendant la course

| Donnée | Provenance | Mise à jour | Repli |
|---|---|---|---|
| Temps écoulé du segment | Chronomètre monotone | Continu | — jamais absent |
| Temps total écoulé | Chronomètre monotone | Continu | — jamais absent |
| Position `14/30` | Compteur de marquages | À chaque marquage | — jamais absent |
| Nom du segment, destination | Constante de domaine | À chaque marquage | — jamais absent |
| Fréquence cardiaque | Capteur | Continu, ou 10 s en veille | `—`, aucun segment actif : les cinq restent au style atténué |
| Zone cardiaque | FC + profil | Suit la FC | Aucun segment actif |
| Distance mesurée | Capteur | Continu | Allure indisponible |
| `allure-segment` | Distance ÷ temps depuis le début du segment, corrigée | Continu | `—:—` |
| `allure-lissee` | Vitesse instantanée lissée sur 10 s, corrigée | Continu | Flèche masquée |
| Facteur de correction | Profil au départ, puis calcul en fin de kilomètre | Après chaque kilomètre | Vaut 1 tant qu'aucun facteur n'a jamais été retenu |
| Flèche de tendance | `allure-lissee` vs `allure-segment` | Continu | Masquée |
| Temps de référence du segment | Référence synchronisée | À chaque marquage | Ligne masquée |
| Écart sur le tour | Temps réel vs référence | Continu pendant le segment | Bloc masqué |
| Écart cumulé | Somme des écarts de segment | À chaque marquage | Bloc masqué |
| Arrivée estimée | Écarts + temps de référence restants | À chaque marquage | Bloc masqué |
| Libellé du dernier marquage | Journal des marquages | À chaque marquage | Bouton d'annulation désactivé avant le 1ᵉʳ marquage |

> **⚙️ Consigne.** Sans référence chargée, **quatre blocs
> disparaissent** : temps de référence, écart sur le tour, écart
> cumulé, arrivée estimée. La page n'est pas réorganisée — les blocs
> restants gardent leur position.

### 13.3 Montre — hors course

| Donnée | Provenance | Mise à jour | Repli |
|---|---|---|---|
| Nom et temps de la référence | Dernière synchronisation | À chaque synchronisation | Badge « Aucune référence » |
| Historique résumé | Dernière synchronisation | À chaque synchronisation | Liste vide avec mention |
| FC de préparation | Capteur | Continu | `—`, le lancement reste possible |
| Temps total, écart final, horodatage | Course qui vient de finir | Une fois | Écart masqué s'il n'y avait pas de référence |

### 13.4 Téléphone

| Donnée | Provenance | Mise à jour | Repli |
|---|---|---|---|
| Liste des courses | Base locale | À chaque import ou remontée | Écran de liste vide |
| Durée et cumul par segment | Base locale | Fixe une fois la course écrite | — jamais absent |
| Écart par segment | Course vs référence | Recalculé à l'affichage | Colonne masquée si la course consultée est la référence, ou s'il n'y en a aucune |
| FC max | Maximum observé sur 12 mois, ou saisie manuelle | Proposée à la première ouverture du profil | Saisie manuelle demandée |
| Plages de zones en bpm | FC max × les quatre seuils | Suit la FC max | Plages masquées tant que la FC max est inconnue |
| Date de dernière synchronisation | Journal local | À chaque synchronisation réussie | « Jamais synchronisé » |

> **⚙️ Consignes.**
>
> - Si l'historique de santé est vide, inaccessible, ou si
>   l'autorisation est refusée, la FC max **n'est pas devinée** :
>   aucune formule sur l'âge, aucune valeur par défaut. Le champ reste
>   à remplir et les plages de zones restent masquées jusque-là.
> - **Une valeur saisie à la main n'est jamais écrasée** par une
>   lecture automatique ultérieure, et une valeur observée plus élevée
>   n'est **pas signalée**. La dérivation ne sert qu'à la proposition
>   initiale ; ensuite, seule une modification manuelle change la FC
>   max.

---

## 14. Hors périmètre

- Écran de comparaison de deux courses côte à côte.
- Divisions Pro / Doubles / Relay. Une course est identifiée par son
  nom libre.
- Découpage plus grossier en 24 ou 16 segments.
- Décomposition du bloc final en trois segments distincts.
- Nombre de calories, nombre de pas, cadence de foulée affichée,
  altitude. L'allure et la fréquence cardiaque sont les seules mesures
  physiologiques affichées.
- Toute carte, tout tracé de parcours.

---

## 15. À vérifier sur l'appareil

- La fiabilité de l'allure en intérieur. Elle conditionne le bloc
  central de la page principale pendant les kilomètres.
- Le sens de la flèche de tendance : accélérer fait baisser le nombre
  affiché en min/km.
- La lisibilité de l'arc des zones en plein soleil.

Matériel cible : Galaxy Watch Ultra, écran 1,5 pouce en 480 × 480,
Wear OS 5 avec One UI Watch 6, mise à jour possible vers Wear OS 6.

---

## Annexe A — Format du résultat officiel

Ce que produit un copier-coller depuis hyresult, et comment le lire.

### A.1 Échantillon réel

Colonnes séparées par des tabulations. Total 1:37:25.

```
Split	Time of Day	Time	Diff
Rox In	15:56:42	6:36	6:36
SkiErg In	15:56:44	6:37	0:01
SkiErg Out	16:01:10	11:03	4:26
Rox Out	16:02:27	12:20	1:17
Rox In	16:07:52	17:46	5:26
Sled Push In	16:08:04	17:57	0:11
Sled Push Out	16:10:59	20:52	2:55
Rox Out	16:12:34	22:27	1:35
Rox In	16:18:07	28:01	5:34
Sled Pull In	16:18:32	28:25	0:24
Sled Pull Out	16:23:59	33:53	5:28
Rox Out	16:25:31	35:25	1:32
Rox In	16:30:55	40:48	5:23
Burpee BJ In	16:31:40	41:34	0:46
Burpee BJ Out	16:37:12	47:05	5:31
Rox Out	16:37:52	47:46	0:41
Rox In	16:43:07	53:01	5:15
Row In	16:43:30	53:24	0:23
Row Out	16:48:38	58:31	5:07
Rox Out	16:50:09	1:00:03	1:32
Rox In	16:55:33	1:05:26	5:23
F. Carry In	16:57:05	1:06:59	1:33
F. Carry Out	16:59:04	1:08:58	1:59
Rox Out	16:59:48	1:09:42	0:44
Rox In	17:05:32	1:15:25	5:43
S. Lunges In	17:06:40	1:16:33	1:08
S. Lunges Out	17:12:21	1:22:14	5:41
Rox Out	17:13:14	1:23:08	0:54
Wall Balls In	17:19:28	1:29:21	6:13
Total time	17:27:31	1:37:25	8:04
```

### A.2 Colonnes

| Colonne | Contenu | Usage |
|---|---|---|
| `Split` | Libellé du point de passage | Identifie le segment |
| `Time of Day` | Heure du jour, `h:mm:ss` | Donne l'heure de départ |
| `Time` | Temps cumulé depuis le départ | Sert à la validation |
| `Diff` | **Durée du segment** | C'est la valeur stockée |

### A.3 Mapping des libellés

Le cycle se répète sept fois, puis le format change.

| Libellé | Segment |
|---|---|
| `Rox In` | `RUN` du cycle n |
| `<Atelier> In` | `ROX_IN` du cycle n |
| `<Atelier> Out` | `STATION` du cycle n |
| `Rox Out` | `ROX_OUT` du cycle n |
| `Wall Balls In` | `RUN` du cycle 8 |
| `Total time` | `FINAL_BLOCK` |

**Noms d'ateliers tels qu'ils apparaissent**, dans l'ordre :

`SkiErg` · `Sled Push` · `Sled Pull` · `Burpee BJ` · `Row` ·
`F. Carry` · `S. Lunges` · `Wall Balls`

> **⚙️ Consigne.** Quatre de ces huit noms ne correspondent pas aux
> noms de segments du domaine. La table de correspondance est
> explicite, jamais déduite d'une comparaison de chaînes.

### A.4 Lecture

> **⚙️ Consignes.**
>
> - **Machine à états sur le cycle**, pas recherche par libellé : `Rox
>   In` apparaît sept fois à l'identique. Le numéro de cycle vient de
>   l'atelier qui suit. `Wall Balls In` fait basculer en mode terminal.
> - **Ligne d'en-tête ignorée** si elle est présente : la première
>   ligne est écartée quand sa quatrième colonne n'est pas un temps
>   lisible. Une seule ligne peut l'être de cette façon — si une autre
>   présente le même défaut, c'est une erreur de lecture.
> - **Séparateur** : tabulation, ou toute suite d'espaces multiples.
>   Les noms d'ateliers contiennent des espaces simples.
> - **Format des temps** : le nombre de composantes détermine
>   l'échelle. Deux composantes = `m:ss`, trois = `h:mm:ss`. La
>   colonne `Time` passe de l'un à l'autre en cours de tableau.
> - **Heure de départ** = `Time of Day` de la première ligne moins son
>   `Diff`. Sur l'échantillon : 15:56:42 − 6:36 = 15:50:06.

### A.5 Validation

> **⚙️ Consignes.** Un collage n'est accepté que si les trois
> conditions sont réunies :
>
> 1. **Exactement 30 lignes** de données.
> 2. **La somme des `Diff` retombe sur `Time`** à chaque ligne.
> 3. **Les libellés se succèdent dans l'ordre attendu** du cycle.
>
> Un échec nomme la ligne fautive. Rien n'est écrit — jamais d'import
> partiel. Messages en §C.5.

### A.6 Fragilité

> **⚙️ Consigne.** Ce format vient d'un site externe : libellés,
> abréviations et ordre des colonnes peuvent changer. Un échec de
> lecture est un cas normal — jamais un plantage, jamais une
> interprétation approximative.

---

## Annexe B — Formats d'affichage

### B.1 Durées

| Format | Motif | Usage | Exemple |
|---|---|---|---|
| `duration-segment` | `m:ss` | Durée d'un segment — toujours sous l'heure | `6:36`, `0:01` |
| `duration-total` | `h:mm:ss` | Durée totale d'une course | `1:37:25`, `0:52:18` |
| `duration-elapsed` | `m:ss` sous 60 min, `h:mm:ss` à partir de 60:00 | Temps écoulé en course | `52:10`, puis `1:02:10` |

> **⚙️ Consignes.**
>
> - Pas de zéro de tête sur le premier groupe : `6:36`, jamais `06:36`.
> - `duration-total` **conserve le groupe des heures même à zéro** —
>   `0:52:18` — pour aligner les colonnes en liste.
> - `duration-elapsed` ne l'affiche qu'une fois l'heure passée.

### B.2 Écarts

| Format | Motif | Exemple |
|---|---|---|
| `delta` | signe + `m:ss` | `+1:12`, `−0:30`, `+0:00` |

> **⚙️ Consignes.**
>
> - **Le signe est toujours présent**, y compris à zéro : `+0:00`.
>   Positif ou nul donne `+`, négatif donne `−`.
> - Le signe négatif est le **caractère moins `−` (U+2212)**, jamais le
>   tiret ASCII.
> - La **couleur** distingue les trois cas : `ahead`, `behind`, ou
>   `delta-zero` à zéro. Le format reste unique.
> - Un écart dépassant l'heure reste en `m:ss` : `+72:14`, pas
>   `+1:12:14`.

### B.3 Allure, fréquence, position

| Format | Motif | Exemple |
|---|---|---|
| `pace` | `m:ss` + unité détachée | `6:00` `/km` |
| `hr` | entier + unité détachée | `168` `bpm` |
| `position` | `n/30`, sans espaces | `14/30` |
| `zone` | `Zone n` | `Zone 4` |

> **⚙️ Consigne.** L'unité est un élément distinct, plus petit et en
> `text-secondary`, jamais concaténée à la valeur.

### B.4 Réglages et plages

| Donnée | Format | Exemple |
|---|---|---|
| Pourcentage de zone | entier + espace insécable + `%` | `60 %` |
| Plage de zone | bornes séparées par un tiret demi-cadratin | `112–130 bpm` |
| Zone extrême | opérateur + espace | `< 112 bpm`, `≥ 168 bpm` |
| Distance | entier + espace + `m`, sans séparateur de milliers | `1000 m` |
| Durée d'appui | entier + espace + `ms` | `700 ms` |

> **⚙️ Consigne.** Les deux opérateurs des zones extrêmes ne sont pas
> symétriques, et c'est voulu : un seuil appartient à la zone qu'il
> ouvre (§4.4). La zone 1 s'arrête donc strictement avant le premier
> seuil, la zone 5 commence au quatrième, celui-ci compris. Les
> exemples valent pour une FC max de 187.

### B.5 Dates

| Usage | Format | Exemple |
|---|---|---|
| Date d'une course | jour, mois abrégé, année | `12 avr. 2026` |
| Date et heure | date + `·` + `h:mm` | `12 avr. 2026 · 09:14` |
| Dernière synchronisation | relatif si le jour même | `aujourd'hui à 09:02` |

### B.6 Arrondi

> **⚙️ Consignes.**
>
> - Les durées sont stockées en millisecondes et affichées à la
>   seconde, **par troncature** — jamais par arrondi.
> - **La durée affichée d'un segment se calcule par différence de deux
>   cumuls tronqués**, jamais par troncature de sa propre durée : sans
>   quoi la somme des segments ne retombe pas sur le total.
> - Un écart se calcule sur les valeurs en millisecondes, puis se
>   tronque à l'affichage.

---

## Annexe C — Textes

### C.1 Règles

> **⚙️ Consignes.**
>
> - **Aucune chaîne visible n'est écrite en dur**, sur aucune des deux
>   applications. Tout passe par les fichiers de ressources.
> - **Une seule langue : le français.** Aucune autre locale n'est
>   fournie ; aucun mécanisme de bascule n'est prévu.
> - Les deux applications ont **des fichiers de ressources distincts**.
>   Une clé présente des deux côtés y est dupliquée, jamais partagée.
> - Les valeurs interpolées sont passées en paramètre de la ressource,
>   jamais concaténées.

### C.2 Textes dynamiques et replis

| Texte | Valeur variable | Repli |
|---|---|---|
| `Réf. — <nom>` | Nom de la référence | Badge `⚠ Aucune référence` (le texte entier est remplacé) |
| `Référence chargée · <nom>` | Nom de la référence | Ligne masquée |
| `Annuler : <segment fermé>` | Nom du segment | Bouton désactivé avant le 1ᵉʳ marquage |
| `Dernière synchronisation réussie : <date>` | Date relative | `Jamais synchronisé` |
| `Supprimer « <nom> » ?` | Nom de la course | — le nom n'est jamais vide |
| `Zone <n>` | Numéro de zone | Ligne masquée sans fréquence cardiaque |
| `Valeur attendue entre <min> et <max>.` | Bornes du réglage édité | — le message n'existe que sur un refus |

> **⚙️ Consignes.**
>
> - **Un nom de course n'est jamais vide.** À la saisie, le champ
>   refuse une valeur vide une fois les espaces de bord retirés. Sur la
>   montre, le nom est généré automatiquement.
> - **Longueur maximale d'un nom : 40 caractères**, appliquée à la
>   saisie.
> - **Aucune contrainte d'unicité.** Deux courses peuvent porter le
>   même nom ; la date les distingue dans la liste. Rien n'est refusé,
>   rien n'est signalé.
> - À l'affichage, un nom trop long pour son emplacement est **tronqué
>   en fin avec une ellipse**, jamais réduit sur plusieurs lignes.
> - Le nom généré d'une course enregistrée par la montre suit le format
>   date et heure de l'annexe B.5 : `12 avr. 2026 · 09:14`.

### C.3 Date relative

| Cas | Forme |
|---|---|
| Le jour même | `aujourd'hui à 09:02` |
| La veille | `hier à 09:02` |
| Au-delà | `14 sept. 2025 à 09:02` |

### C.4 Textes fixes

**Montre — hors course**

| Écran | Texte |
|---|---|
| Autorisation | `Autoriser l'accès au capteur cardiaque` · `Nécessaire pour afficher ta fréquence et tes zones pendant la course.` · `Autoriser` |
| Autorisation refusée, rappel sur l'accueil | `⚠ Capteur cardiaque non autorisé` |
| Attente du téléphone | `En attente du téléphone` · `Ouvre l'application sur ton téléphone pour envoyer ton profil.` · `Réessayer` |
| Accueil | `Démarrer` · `Historique` · `Synchroniser` · `⚠ Aucune référence` |
| Historique vide | `Aucune course` · `Synchronise depuis le téléphone.` |
| Préparation | `Fréquence cardiaque` · `Lancer` · `Quitter` |
| Synchronisation | `Ne ferme pas l'application` · `Synchronisation impossible — approche le téléphone de la montre.` · `Réessayer` |

**Montre — course**

| Écran | Texte |
|---|---|
| Projection | `arrivée estimée` |
| Contrôle | `Contrôle` · `Arrêter l'activité` |
| Confirmation d'arrêt | `Arrêter l'activité ?` · `Elle sera enregistrée telle quelle, marquée incomplète.` · `Annuler` · `Arrêter` |
| Reprise d'activité | `Une autre activité est en cours` · `Elle sera arrêtée pour démarrer le suivi Hyrox.` · `Annuler` · `Continuer` |
| Fin | `Terminer` |

**Téléphone**

| Écran | Texte |
|---|---|
| Liste | `Mes courses` · `Référence` · `Incomplète` |
| Liste vide | `Aucune course encore` · `Colle un résultat officiel depuis hyresult pour importer ta première course.` · `Coller un résultat` |
| Détail | `Définir comme référence` · `Renommer` · `Supprimer` |
| Suppression | `C'est la course de référence. Après suppression, plus aucune course ne servira de comparaison.` (seulement si c'est le cas) · `Suppression définitive. La course disparaîtra aussi de l'historique sur la montre.` · `Annuler` · `Supprimer` |
| Renommer | `Renommer la course` · `Nom` · `Annuler` · `Enregistrer` |
| Collage | `Coller un résultat` · `Colle ici les colonnes copiées depuis hyresult…` · `Nom de la course` · `ex. Marseille 2026` · `Date de la course` · `Importer` |
| Aperçu | `Aperçu avant enregistrement` · `Temps total reconnu` · `Segments détectés` · `Corriger` · `Enregistrer` |
| Erreur | Messages en §C.5 · `Revenir au collage` |
| Profil | `Profil` · `Fréquence cardiaque maximale` · `Maximum observé sur 12 mois` · `Modifier` · `Zones cardiaques (% FC max)` · `Distance d'un kilomètre` · `Durée de l'appui long` · `Synchroniser avec la montre` |
| Profil — refus d'une valeur | `Nombre entier attendu.` · `Chaque seuil doit être supérieur au précédent.` (et le message borné de §C.2) |
| Profil — autorisation manquante | `Synchronisation indisponible — l'accès aux appareils à proximité n'est pas autorisé.` · `Autoriser` |
| Synchronisation | `Ne ferme pas l'application` · `Synchronisation impossible — approche la montre du téléphone.` · `Réessayer` |

### C.5 Messages d'erreur de collage

Structure constante : un titre qui nomme le problème et situe la ligne,
puis une phrase qui dit quoi faire.

| Cause | Titre | Explication |
|---|---|---|
| Collage vide | `Rien à lire` | `Colle les quatre colonnes copiées depuis hyresult.` |
| Moins de quatre colonnes | `Colonnes manquantes — ligne <n>` | `Chaque ligne doit contenir quatre colonnes. Copie le tableau entier, en-tête compris.` |
| Temps illisible | `Format de temps invalide — ligne <n>` | `Le temps doit être au format m:ss. Remplace l'espace par un deux-points.` |
| Moins de 30 segments | `<n> segments sur 30` | `Le collage est incomplet. Copie le tableau entier, de la première ligne jusqu'à « Total time ».` |
| Plus de 30 segments | `<n> segments au lieu de 30` | `Le collage contient des lignes en trop. Copie uniquement le tableau des temps.` |
| Libellé non reconnu | `Libellé inconnu — ligne <n>` | `« <libellé> » n'est pas un point de passage attendu. Vérifie que tu as copié un résultat Hyrox complet.` |
| Libellé hors séquence | `Ordre inattendu — ligne <n>` | `« <libellé> » n'est pas à sa place dans la course. Copie le tableau sans le trier ni le réorganiser.` |
| Cumul incohérent | `Temps incohérents — ligne <n>` | `Le cumul ne correspond pas à la somme des temps. Vérifie que la ligne n'a pas été modifiée.` |

> **⚙️ Consignes.**
>
> - **Un seul message à la fois** : celui de la première anomalie
>   rencontrée dans l'ordre de lecture.
> - **Aucun message générique n'existe.** Ces huit causes couvrent
>   tous les rejets et chacune porte son propre titre : il n'y a pas
>   de repli attrape-tout derrière elles.
> - Le bouton est toujours `Revenir au collage`, et le texte collé est
>   conservé.
> - `<libellé>` reprend la valeur lue telle quelle, tronquée à
>   20 caractères si nécessaire.

---

## Documents liés

- **`TECHNICAL_CONVENTIONS.md`** — comment coder : pile technique,
  découpage en modules, nommage, tests.
- **`TUTORIEL_PROJET.md`** — créer le projet, Git et GitHub.
- **`TUTORIEL_DEPLOIEMENT.md`** — installer l'application sur le
  téléphone et sur la montre.
