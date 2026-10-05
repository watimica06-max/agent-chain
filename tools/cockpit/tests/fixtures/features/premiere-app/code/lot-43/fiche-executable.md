## Signatures

PhoneStringResources.RaceList.title → String
// "Mes courses"
PhoneStringResources.RaceList.referenceBadge → String
// "Référence"
PhoneStringResources.RaceList.incompleteBadge → String
// "Incomplète"
PhoneStringResources.RaceList.emptyTitle → String
// "Aucune course encore"
PhoneStringResources.RaceList.emptyBody → String
// "Colle un résultat officiel depuis hyresult pour importer ta première course."
PhoneStringResources.RaceList.emptyAction → String
// "Coller un résultat"

PhoneStringResources.RaceDetail.setReference → String
// "Définir comme référence"
PhoneStringResources.RaceDetail.rename → String
// "Renommer"
PhoneStringResources.RaceDetail.delete → String
// "Supprimer"

PhoneStringResources.DeleteConfirm.title(name: String) → String
// "Supprimer « {name} » ?" — name is never empty
PhoneStringResources.DeleteConfirm.body → String
// "Suppression définitive. La course disparaîtra aussi de l'historique sur la montre."
PhoneStringResources.DeleteConfirm.referenceNotice → String
// "C'est la course de référence. Après suppression, plus aucune course ne servira de comparaison."
PhoneStringResources.DeleteConfirm.cancel → String
// "Annuler"
PhoneStringResources.DeleteConfirm.confirm → String
// "Supprimer"

PhoneStringResources.Rename.title → String
// "Renommer la course"
PhoneStringResources.Rename.fieldLabel → String
// "Nom"
PhoneStringResources.Rename.cancel → String
// "Annuler"
PhoneStringResources.Rename.save → String
// "Enregistrer"

PhoneStringResources.Paste.title → String
// "Coller un résultat"
PhoneStringResources.Paste.placeholder → String
// "Colle ici les colonnes copiées depuis hyresult…"
PhoneStringResources.Paste.nameLabel → String
// "Nom de la course"
PhoneStringResources.Paste.namePlaceholder → String
// "ex. Marseille 2026"
PhoneStringResources.Paste.action → String
// "Importer"

PhoneStringResources.Preview.title → String
// "Aperçu avant enregistrement"
PhoneStringResources.Preview.totalLabel → String
// "Temps total reconnu"
PhoneStringResources.Preview.segmentsLabel → String
// "Segments détectés"
PhoneStringResources.Preview.correct → String
// "Corriger"
PhoneStringResources.Preview.save → String
// "Enregistrer"

PhoneStringResources.PasteError.back → String
// "Revenir au collage"

PhoneStringResources.PasteError.emptyTitle → String
// "Rien à lire"
PhoneStringResources.PasteError.emptyBody → String
// "Colle les quatre colonnes copiées depuis hyresult."

PhoneStringResources.PasteError.missingColumnsTitle(row: Int) → String
// "Colonnes manquantes — ligne {row}"
PhoneStringResources.PasteError.missingColumnsBody → String
// "Chaque ligne doit contenir quatre colonnes. Copie le tableau entier, en-tête compris."

PhoneStringResources.PasteError.invalidTimeTitle(row: Int) → String
// "Format de temps invalide — ligne {row}"
PhoneStringResources.PasteError.invalidTimeBody → String
// "Le temps doit être au format m:ss. Remplace l'espace par un deux-points."

PhoneStringResources.PasteError.tooFewTitle(count: Int) → String
// "{count} segments sur 30"
PhoneStringResources.PasteError.tooFewBody → String
// "Le collage est incomplet. Copie le tableau entier, de la première ligne jusqu'à « Total time »."

PhoneStringResources.PasteError.tooManyTitle(count: Int) → String
// "{count} segments au lieu de 30"
PhoneStringResources.PasteError.tooManyBody → String
// "Le collage contient des lignes en trop. Copie uniquement le tableau des temps."

PhoneStringResources.PasteError.unknownLabelTitle(row: Int) → String
// "Libellé inconnu — ligne {row}"
PhoneStringResources.PasteError.unknownLabelBody(label: String) → String
// "« {label} » n'est pas un point de passage attendu. Vérifie que tu as copié un résultat Hyrox complet."
// label truncated to exactly 20 characters when longer, unchanged otherwise, no ellipsis added

PhoneStringResources.PasteError.outOfSequenceTitle(row: Int) → String
// "Ordre inattendu — ligne {row}"
PhoneStringResources.PasteError.outOfSequenceBody(label: String) → String
// "« {label} » n'est pas à sa place dans la course. Copie le tableau sans le trier ni le réorganiser."
// label truncated to exactly 20 characters when longer, unchanged otherwise, no ellipsis added

PhoneStringResources.PasteError.inconsistentTimeTitle(row: Int) → String
// "Temps incohérents — ligne {row}"
PhoneStringResources.PasteError.inconsistentTimeBody → String
// "Le cumul ne correspond pas à la somme des temps. Vérifie que la ligne n'a pas été modifiée."

PhoneStringResources.Profile.title → String
// "Profil"
PhoneStringResources.Profile.hrMaxLabel → String
// "Fréquence cardiaque maximale"
PhoneStringResources.Profile.hrMaxSource → String
// "Maximum observé sur 12 mois"
PhoneStringResources.Profile.hrMaxEdit → String
// "Modifier"
PhoneStringResources.Profile.zonesLabel → String
// "Zones cardiaques (% FC max)"
PhoneStringResources.Profile.zoneRow(n: Int) → String
// "Zone {n}" — caller hides the row without a heart-rate reading
PhoneStringResources.Profile.distanceLabel → String
// "Distance d'un kilomètre"
PhoneStringResources.Profile.pressDurationLabel → String
// "Durée de l'appui long"
PhoneStringResources.Profile.syncAction → String
// "Synchroniser avec la montre"
PhoneStringResources.Profile.syncUnavailable → String
// "Synchronisation indisponible — l'accès aux appareils à proximité n'est pas autorisé."
PhoneStringResources.Profile.syncAllowAction → String
// "Autoriser"
PhoneStringResources.Profile.lastSync(date: String?) → String
// date present → "Dernière synchronisation réussie : {date}"; date null → "Jamais synchronisé"

PhoneStringResources.Sync.inProgress → String
// "Ne ferme pas l'application"
PhoneStringResources.Sync.failure → String
// "Synchronisation impossible — approche la montre du téléphone."
PhoneStringResources.Sync.retry → String
// "Réessayer."

## Acceptance criteria

- Every fixed key declared in §10.4's phone catalogue — including the parameter-free bodies of the failure catalogue — resolves to exactly its declared French text
- DeleteConfirm.title(name) interpolates the given name into "Supprimer « {name} » ?"
- Profile.zoneRow(n) interpolates the given zone number into "Zone {n}"
- Profile.lastSync(date) interpolates the given date into "Dernière synchronisation réussie : {date}" when date is present, and returns "Jamais synchronisé" when date is null
- PasteError.missingColumnsTitle, invalidTimeTitle, unknownLabelTitle, outOfSequenceTitle and inconsistentTimeTitle each interpolate the given row number into their own "— ligne {row}" wording
- PasteError.tooFewTitle and tooManyTitle each interpolate the given segment count into their own wording ("{count} segments sur 30" / "{count} segments au lieu de 30")
- PasteError.unknownLabelBody and outOfSequenceBody interpolate the given label unchanged when it is 20 characters or fewer, and truncated to exactly its first 20 characters when longer, with no ellipsis added
- Every key resolves to French text regardless of the device's system locale, since no other locale or switching mechanism exists

## Dependencies

None — all types are produced by this lot.
