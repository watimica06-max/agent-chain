# Analyse de la chaîne — orchestration

Tu orchestres une analyse de notre chaîne d'agents, en quatre phases
autonomes. **Je n'interviens pas de bout en bout.**

🔴 **Chaque passe est un sous-agent lancé sous `fable-5.1`.** Tu ne
fais aucun travail d'analyse toi-même : tu lances, tu attends, tu
vérifies, tu commites, tu enchaînes.

⚠️ **Tu attends entre chaque passe**, sans exception — crédits.
📌 **Combien : voir *L'attente entre deux passes*.**

---

## Avant de commencer

🔴 **Crée un worktree pour ce travail** et lances-y toutes les passes.
📌 **Rien ne s'écrit sur `master` en cours de route.**

**Crée les dossiers de sortie :**

    mkdir -p docs/refonte/agents docs/refonte/groupes

**Dépose le fichier d'idées que la phase 1 lit** — 🔴 **la version
d'origine, avant tout balayage du lexicographe :**

    git show c3bfa80:docs/features/premiere-app-2/idees.md \
      > docs/refonte/idees-exemple.md

⚠️ **Vérifie qu'il n'est pas vide.** 📌 **Sinon, arrête et dis-le-moi.**

🔴 **Vérifie que les quatre fichiers de consigne sont là** :
`docs/refonte/01_conception.md`, `02_analyse.md`, `03_agent.md`,
`04_frontiere.md`. ⚠️ **Un manquant arrête tout.**

---

## Après chaque passe, sans exception

🔴 **Commite ce que la passe a produit**, dans le worktree, avec un
message qui nomme la phase et l'agent ou le groupe traité.

🔴 **Puis merge sur `master` et pousse.** ⚠️ **Une passe qui n'est pas
mergée avant la suivante est un travail qu'un incident perd** — et
elles s'étalent sur plusieurs jours.

📌 **Le worktree reste** jusqu'à la fin de toutes les passes.

---

## L'attente entre deux passes

🔴 **L'analyse doit être finie le 14 septembre à 6 h 30**, heure de
Singapour. 📌 **Vingt-cinq passes en tout** : une en phase 1, une en
phase 2, dix-huit en phase 3, et celles de la phase 4.

⚠️ **Ne dors pas une durée fixe** — 📌 **une passe plus longue ou plus
courte que prévu décale tout ce qui suit.** 🔴 **Recalcule après chaque
passe :**

    cible=$(date -d '2026-09-14 06:30:00' +%s)
    reste=$(( cible - $(date +%s) ))
    duree=$(( reste / passes_restantes ))
    [ $duree -gt 0 ] && sleep $duree

📌 **`passes_restantes` compte les passes qui n'ont pas encore
tourné**, celle qui vient de finir exclue. ⚠️ **Zéro ou négatif :
n'attends pas, enchaîne.**

🔴 **Adapte la commande à ta plateforme** — 📌 **`date -d` est la
syntaxe GNU**, et ce qui compte est la règle : **le temps restant
divisé par les passes restantes.**

⚠️ **Si une attente calculée tombe sous cinq minutes**, note-le pour ton
compte rendu final : l'analyse aura pris plus de temps que prévu.

---

## Phase 1 — la conception en aveugle

Lance un sous-agent `fable-5.1` avec ce prompt :

    Lis `docs/refonte/01_conception.md` en entier et fais ce qu'il
    demande.

**Attends la fin.** 🔴 **Vérifie que `docs/refonte/proposition.md`
existe et n'est pas vide.** Sinon, arrête tout et dis-le-moi.

**Commite, merge, pousse.** Puis attends, selon *L'attente entre deux passes*.

---

## Phase 2 — le jugement macro

Lance un sous-agent `fable-5.1` avec ce prompt :

    Lis `docs/refonte/02_analyse.md` en entier et fais ce qu'il
    demande.

**Attends la fin.** 🔴 **Vérifie que `docs/refonte/verdict.md` existe,
n'est pas vide, et porte ses sept sections.** Sinon, arrête tout et
dis-le-moi.

**Commite, merge, pousse.** Puis attends, selon *L'attente entre deux passes*.

---

## Phase 3 — une passe par agent

🔴 **Un agent = une passe.** 📌 **Tous les agents de
`.claude/agents/`**, sans exception — ⚠️ **y compris ceux que le
verdict juge sains.**

**Dans l'ordre de la chaîne** : lexicographe, redacteur, decoupeur,
classeur, sondeur, assembleur, convertisseur, architecte, cadreur,
verificateur, detailleur, realisateur, relecteur, controleur, arbitre,
diagnostiqueur, extracteur, fusionneur.

**Pour chacun**, lance un sous-agent `fable-5.1` avec ce prompt, en
remplaçant `<nom>` :

    Lis `docs/refonte/03_agent.md` en entier et fais ce qu'il demande.
    L'agent sur lequel tu travailles est : <nom>

**Après chaque passe** : 🔴 **vérifie que
`docs/refonte/agents/<nom>.md` a été écrit.** ⚠️ **Un fichier manquant
arrête tout** — dis-moi lequel et pourquoi.

📌 **Un fichier qui ne porte aucun commentaire est un résultat
valable** — ⚠️ **ne relance pas la passe.**

**Commite, merge, pousse.** Puis attends, selon *L'attente entre deux passes*.

---

## Phase 4 — une passe par frontière

🔴 **Ne commence qu'une fois les dix-huit passes de la phase 3
faites.**

📌 **Un groupe = les agents qui se partagent un même artefact**, celui
que l'un écrit et que l'autre lit.

| Groupe | Agents | Artefact partagé |
|---|---|---|
| `lexique` | lexicographe, redacteur | `lexique.md` |
| `produit` | redacteur, decoupeur, classeur, sondeur, assembleur | `desc-produit.md` |
| `technique` | convertisseur, cadreur | `spec-technique.md` |
| `decoupage` | cadreur, verificateur | `decoupage.md` |
| `fiches` | detailleur, realisateur, relecteur, arbitre | `code/<lot>/fiche-executable.md` |
| `intention` | redacteur, controleur | `desc-produit.md`, relu en fin de cycle |

⚠️ **Le verdict a pu nommer une frontière que cette table ignore** —
🔴 **lis sa section 4 avant de commencer**, et ajoute un groupe si elle
en désigne un que personne ne couvre. 📌 **Dis-moi lequel et pourquoi.**

**Pour chaque groupe**, lance un sous-agent `fable-5.1` avec ce
prompt, en remplaçant les trois valeurs :

    Lis `docs/refonte/04_frontiere.md` en entier et fais ce qu'il
    demande.
    Ton groupe est : <groupe>
    Les agents de ton groupe sont : <liste>
    L'artefact qu'ils se partagent est : <artefact>

**Après chaque passe** : 🔴 **vérifie que
`docs/refonte/groupes/<groupe>.md` a été écrit.** ⚠️ **Un fichier
manquant arrête tout.**

**Commite, merge, pousse.** Puis attends, selon *L'attente entre deux passes*.

---

## Quand tout est fini

**Retire le worktree.**

**Dis-moi**, en quelques lignes :

- Combien de passes ont tourné, et sur quels agents et groupes
- Quels fichiers ont été produits, et lesquels sont vides
- Tout ce qui s'est arrêté ou a échoué en route

🔴 **Ne fais aucune synthèse du contenu** — je lis les fichiers
moi-même.

⚠️ **Ne modifie rien sous `.claude/`.** 📌 **Tout ce qui est produit
vit dans `docs/refonte/`.**
