## Signatures

WatchStringResources.Permission.title → String
// "Autoriser l'accès au capteur cardiaque"
WatchStringResources.Permission.explanation → String
// "Nécessaire pour afficher ta fréquence et tes zones pendant la course."
WatchStringResources.Permission.action → String
// "Autoriser"
WatchStringResources.Permission.reminder → String
// "⚠ Capteur cardiaque non autorisé"

WatchStringResources.Waiting.title → String
// "En attente du téléphone"
WatchStringResources.Waiting.explanation → String
// "Ouvre l'application sur ton téléphone pour envoyer ton profil."
WatchStringResources.Waiting.retry → String
// "Réessayer"

WatchStringResources.Home.start → String
// "Démarrer"
WatchStringResources.Home.history → String
// "Historique"
WatchStringResources.Home.sync → String
// "Synchroniser"
WatchStringResources.Home.referenceLine(name: String?) → String
// name present → "Réf. — {name}"; name null → "⚠ Aucune référence"

WatchStringResources.History.emptyTitle → String
// "Aucune course"
WatchStringResources.History.emptyAction → String
// "Synchronise depuis le téléphone."

WatchStringResources.Prep.hrLabel → String
// "Fréquence cardiaque"
WatchStringResources.Prep.launch → String
// "Lancer"
WatchStringResources.Prep.quit → String
// "Quitter"
WatchStringResources.Prep.referenceLoaded(name: String) → String
// "Référence chargée · {name}" — caller hides the line entirely without a reference

WatchStringResources.Projection.etaLabel → String
// "arrivée estimée"

WatchStringResources.Control.title → String
// "Contrôle"
WatchStringResources.Control.stop → String
// "Arrêter l'activité"
WatchStringResources.Control.undoLabel(segment: String) → String
// "Annuler : {segment}" — caller disables the control before the first marking

WatchStringResources.StopConfirm.title → String
// "Arrêter l'activité ?"
WatchStringResources.StopConfirm.body → String
// "Elle sera enregistrée telle quelle, marquée incomplète."
WatchStringResources.StopConfirm.cancel → String
// "Annuler"
WatchStringResources.StopConfirm.confirm → String
// "Arrêter"

WatchStringResources.ResumeDialog.title → String
// "Une autre activité est en cours"
WatchStringResources.ResumeDialog.body → String
// "Elle sera arrêtée pour démarrer le suivi Hyrox."
WatchStringResources.ResumeDialog.cancel → String
// "Annuler"
WatchStringResources.ResumeDialog.confirm → String
// "Continuer"

WatchStringResources.End.finish → String
// "Terminer"

WatchStringResources.Sync.inProgress → String
// "Ne ferme pas l'application"
WatchStringResources.Sync.failure → String
// "Synchronisation impossible — approche le téléphone de la montre."

WatchStringResources.RaceName.generated(dateTime: String) → String
// equals dateTime exactly — the whole template is the date-time format of §10.1 (e.g. "12 avr. 2026 · 09:14"), no surrounding text

## Acceptance criteria

- Every fixed key declared in §10.4's watch tables resolves to exactly its declared French text
- Home.referenceLine(name) interpolates the given name into "Réf. — {name}" when name is present, and returns "⚠ Aucune référence" when name is null
- Prep.referenceLoaded(name) interpolates the given name into "Référence chargée · {name}"
- Control.undoLabel(segment) interpolates the given segment description into "Annuler : {segment}"
- RaceName.generated(dateTime) returns exactly the given dateTime value, with no additional surrounding text
- Every key resolves to French text regardless of the device's system locale, since no other locale or switching mechanism exists

## Dependencies

None — all types are produced by this lot.
