# Étape 2 — Protocole d'analyse et de correction des demandes

> Entrée : verbatims bruts (avis, bugs, suggestions) collectés à l'étape 1.
> Sortie : tickets classés par sévérité **et** specs techniques Luau prêtes à coder.

## A. Pipeline de traitement

```
Verbatims bruts
   │  1. Nettoyage (langue, dédup, anti-spam/bot)
   ▼
Verbatims normalisés
   │  2. Classification automatique (mots-clés + LLM de catégorisation)
   ▼
┌───────────────────────────┬───────────────────────────┐
│  BUGS                      │  FRUSTRATIONS GAMEPLAY     │
│  (sévérité technique)      │  (demande latente)        │
└───────────────────────────┴───────────────────────────┘
   │  3. Scoring (sévérité × fréquence × portée)
   ▼
Backlog priorisé → 4. Traduction en specs Luau
```

## B. Classification par sévérité

On sépare d'abord ce qui **casse l'expérience** de ce qui **déçoit** — la réponse business n'est pas la même (l'un protège le revenu existant, l'autre crée du revenu nouveau).

### B.1 Bugs bloquants (priorité défensive — ils détruisent le revenu déjà acquis)
| Niveau | Type | Exemples de signaux texte | SLA cible |
|---|---|---|---|
| **S0 — Critique** | Crash, perte de progression/données, exploit de triche, faille économique (duplication d'items/Robux) | « le jeu crash quand… », « j'ai perdu tout mon stuff », « des gens dupliquent », « exploiteurs partout » | Hotfix < 24 h |
| **S1 — Majeur** | Fonctionnalité achetée cassée (gamepass inopérant), achat non délivré | « j'ai payé le gamepass et rien », « le boost marche pas » | < 72 h |

> **Règle d'or :** tout ce qui touche un **achat non délivré** ou un **exploit économique** passe S0 — c'est à la fois un risque de remboursement, un risque de modération Roblox, et le tueur de confiance n°1.

### B.2 Frustrations de gameplay (priorité offensive — elles débloquent du revenu futur)
| Niveau | Type | Exemples de signaux texte |
|---|---|---|
| **G1 — Équilibrage** | Difficulté, grind excessif, méta cassée, pay-to-win ressenti | « trop long pour débloquer », « impossible sans payer », « X est cheaté » |
| **G2 — Manque de contenu** | Lassitude, fin de contenu, peu de nouveautés | « rien à faire après le niveau max », « toujours pareil », « besoin de nouvelles maps/skins » |
| **G3 — Confort / QoL** | UX, contrôles mobile, tutoriel, lisibilité | « les contrôles sur tel sont nuls », « on comprend rien au début » |

### B.3 Formule de scoring (priorisation objective)
```
Score = Sévérité(poids) × Fréquence(occurrences) × Portée(audience touchée)

Poids sévérité : S0=100, S1=60, G1=25, G2=20, G3=10
```
Le score tranche les arbitrages : un G2 très récurrent et large peut dépasser un S1 rare. Mais **aucun S0 n'attend** — il court-circuite la file.

## C. Extraction de la demande latente → spécifications Luau

Le cœur du métier : traduire une plainte floue en quelque chose de **codable et testable**. Chaque demande devient une fiche.

### Gabarit de fiche

```
ID            : LAT-001
Verbatim brut : « on rame trop longtemps avant d'avoir un truc cool,
                  je me suis lassé au bout de 20 min »
Catégorie     : G2 (manque de contenu) + G1 (courbe de progression)
Demande latente: la première récompense significative arrive trop tard
                 → l'onboarding ne « hook » pas avant le décrochage (~20 min)
Spec technique : avancer la 1re récompense forte à < 5 min de jeu ;
                 ajouter un palier de progression court terme visible en HUD
Implémentation Luau (esquisse) :
  - DataStore : champ `firstRewardClaimed` (anti-rejeu)
  - Server script : à `PlayerAdded` + ~150 s de session cumulée,
    accorder une récompense d'accueil via un RemoteEvent sécurisé serveur
  - GuiObject : barre de progression « prochain palier » mise à jour
    par un RemoteEvent (calcul côté serveur, jamais côté client)
Validation    : A/B test — cohorte avec récompense précoce vs. témoin ;
                KPI = rétention D1 et durée de 1re session (Open Cloud Analytics)
Sécurité      : toute attribution de valeur (Robux, items) est calculée et
                validée SERVEUR — le client ne fait que demander/afficher
```

### Règles de traduction (les invariants)
1. **Autorité serveur.** Toute mécanique touchant à de la valeur (monnaie, items, scores classés) est **calculée et validée côté serveur**. Le client propose, le serveur dispose — c'est la parade structurelle aux exploits (cf. S0).
2. **RemoteEvent/RemoteFunction avec validation stricte** des arguments (type, bornes, fréquence anti-spam). Un exploit vient presque toujours d'un Remote qui fait confiance au client.
3. **Idempotence des récompenses** via DataStore (clé `*_claimed`) pour empêcher le rejeu.
4. **Mesurabilité d'abord.** Pas de spec sans KPI de validation rattaché (Open Cloud Analytics). Si on ne peut pas mesurer l'effet, la demande n'est pas encore mûre.
5. **Petit lot, testable.** Une fiche = un changement vérifiable en A/B, pas un refactor.

## D. Boucle de feedback fermée

Chaque correctif livré est ré-instrumenté : on rebranche les sources de l'étape 1 (votes, CCU, rétention Open Cloud, verbatims) pour vérifier que le score du problème **baisse réellement**. Une correction qui ne déplace pas la métrique est rouverte — on n'archive jamais sur la base de l'intention, seulement sur la preuve.
