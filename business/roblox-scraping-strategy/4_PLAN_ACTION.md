# Étape 4 — Plan d'action actionnable

> Restitution finale : un tableau de priorisation décidable, puis la spécification de la boucle de rétention à modifier. Les exemples de problèmes ci-dessous sont des **archétypes** issus des patterns récurrents sur les expériences Roblox ; ils s'instancient avec les données réelles collectées à l'étape 1.

## A. Tableau de priorisation

| Problème détecté | Source de la donnée | Solution technique (Luau) | Impact business (monétisation / rétention) | Priorité |
|---|---|---|---|---|
| Exploit de duplication d'items / Robux | DevForum + Discord `#bug-report` + chute anormale du ratio de votes (API) | Déplacer toute attribution de valeur côté **serveur** ; valider chaque RemoteEvent (type, bornes, anti-spam) ; idempotence DataStore | **Défensif critique** : stoppe l'hémorragie économique + risque modération Roblox ; protège tout le revenu | **P0** |
| Achat (gamepass/booster) non délivré | Verbatims « j'ai payé et rien » + remboursements | Fiabiliser le callback de réception (`ProcessReceipt` idempotent) ; rejouer la livraison au prochain login si échec | **Défensif** : protège le revenu déjà encaissé + la confiance (NPS) | **P0** |
| Crash récurrent (map/appareil mobile) | r/Roblox + Discord + baisse de CCU sur segment mobile | Repro + correctif ciblé ; télémétrie d'erreur ; dégrader proprement plutôt que crasher | **Défensif** : le mobile = majorité de l'audience Roblox → rétention directe | **P0/P1** |
| Pay-to-win ressenti (« impossible sans payer ») | r/Roblox + Discord `#general` + ratio de votes < 80 % | Rééquilibrer pour que le skill prime ; basculer la monétisation vers le **cosmétique** et le confort | **Rétention + Engagement Payouts** : remonte votes → rétention → Robux passif Premium | **P1** |
| Décrochage onboarding (~20 min, 1re récompense trop tardive) | Verbatims « je me suis lassé » + rétention D1 faible (Open Cloud) | Avancer la 1re récompense forte à < 5 min ; palier court terme visible en HUD (calcul serveur) | **Rétention (cœur)** : D1 ↑ alimente toute la suite du funnel et les Payouts | **P1** |
| Lassitude / fin de contenu (« rien à faire au max ») | Reddit + Discord `#suggestions` + plateau de la courbe CCU | Nouvelle boucle de contenu : base **gratuite** + extension premium optionnelle (Gamepass) | **Rétention + Gamepass** : prolonge le cycle de vie ; vend du « plus », pas du « nécessaire » | **P2** |
| Demande d'un style cosmétique précis | Ventes UGC (catalogue API) + Rolimon's + verbatims | Concevoir les items boutique d'après les styles à fort volume de ventes | **UGC (sain)** : revenu pur désirabilité, zéro impact équilibrage | **P2** |
| Friction de confort (slots d'inventaire, skips, file) | Discord `#suggestions` (QoL récurrent) | Option payante de confort (DevProduct/Gamepass) **sans** dégrader le joueur gratuit | **Monétisation confort** : ARPU ↑ en gardant l'équité | **P3** |

**Lecture :** P0 = court-circuite la file (défensif, < 24–72 h). P1 = chantiers rétention à fort ROI. P2/P3 = expansion de revenu une fois la base saine. On ne lance jamais un P2 de monétisation tant qu'un P0 économique est ouvert — vendre sur une base qui fuit gaspille le trafic.

## B. Spécification de la boucle de rétention à modifier

La cible prioritaire (P1) est la **boucle d'engagement précoce** : c'est elle qui décide si un joueur reste assez longtemps pour, ensuite, s'attacher, dépenser, et générer du payout Premium. Tant qu'elle fuit, tout investissement en aval (contenu, cosmétiques) est dilué.

### Diagnostic
Pic de churn autour de la 1re session : la première récompense significative arrive après le seuil de décrochage. Le joueur n'a pas eu de **preuve de progression** avant de partir.

### Mécanique cible (la boucle « Hook → Progress → Reward → Anticipate »)

```
   ┌──────────────────────────────────────────────────────────┐
   │                                                          │
   ▼                                                          │
[1] HOOK (< 90 s)           [2] PROGRESS (visible en continu) │
  action gratifiante         barre « prochain palier » en HUD │
  immédiate, 0 friction      mise à jour côté serveur         │
   │                                                          │
   ▼                                                          │
[3] REWARD (< 5 min)        [4] ANTICIPATE                    │
  1re récompense forte        teaser du palier suivant +      │
  (cosmétique/soft currency)  rendez-vous quotidien ───────────┘
```

1. **Hook (< 90 s)** — une action gratifiante immédiate, sans achat, sans tutoriel bloquant. Objectif : la première « bonne sensation » avant tout risque de décrochage.
2. **Progress (continu)** — un objectif court terme **toujours visible** (barre HUD). La progression est calculée et bornée **côté serveur** ; le client ne fait qu'afficher. Le joueur voit qu'il avance même quand il n'a pas encore gagné.
3. **Reward (< 5 min)** — la première récompense forte arrive **avant** le seuil de décrochage observé. De préférence un **cosmétique** ou de la **soft currency** (sans casser l'équilibrage), attribution idempotente via DataStore (`firstRewardClaimed`).
4. **Anticipate** — au moment de la récompense, on **montre le palier suivant** et on amorce un **rendez-vous quotidien** (récompense de connexion à valeur croissante) qui crée la raison de revenir demain.

### Rattachement business
- **Engagement Payouts** : ↑ durée de session et ↑ rétention D1/D7 → revenu passif Premium directement augmenté.
- **Gamepass/DevProduct** : un joueur retenu est un joueur *monétisable* ; les offres premium n'arrivent qu'**après** la preuve de valeur (jamais dans les 5 premières minutes).
- **UGC** : la 1re récompense cosmétique introduit l'univers visuel de la boutique → amorce le désir d'items payants ultérieurs.

### KPI de validation (A/B obligatoire)
| KPI | Source | Cible |
|---|---|---|
| Rétention D1 | Open Cloud Analytics | ↑ vs. cohorte témoin |
| Durée 1re session | Open Cloud Analytics | ↑ (dépasser le seuil de décrochage) |
| Ratio d'approbation (votes) | API votes Roblox | stable ou ↑ |
| Conversion payante J3–J7 | Analytics achats | ↑ **sans** baisse du ratio de votes |

> Règle de décision : on ne généralise la nouvelle boucle que si la rétention D1 monte **sans** dégrader le ratio de votes ni la conversion. Si l'un des deux se dégrade, on rouvre la fiche (boucle de feedback fermée, étape 2 §D). Aucune généralisation sur l'intention — uniquement sur la preuve mesurée.

## C. Séquencement recommandé (90 jours, indicatif)
1. **Semaines 1–2 (P0)** : colmater les failles économiques et les achats non délivrés. Rien d'autre ne compte tant que la base fuit.
2. **Semaines 3–6 (P1)** : refonte de la boucle d'engagement précoce + rééquilibrage anti-pay-to-win. A/B systématique.
3. **Semaines 7–10 (P2)** : nouvelle boucle de contenu (base gratuite + extension) et premiers items UGC pilotés par la demande.
4. **Semaines 11–12 (P3)** : monétisation de confort, mesurée à ARPU constant sur l'équité.

À chaque étape, on rebranche les sources de l'étape 1 et on vérifie que le **score** des problèmes traités (étape 2) baisse réellement.
