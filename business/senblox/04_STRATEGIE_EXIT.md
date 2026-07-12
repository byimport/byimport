# 04 — Stratégie d'exit : construire la brique manquante évidente

Rappel du principe posé en [00](00_REALITE_CHECK.md) §5 : on ne « construit pas pour vendre », on construit une entreprise autonome dont les métriques et les actifs correspondent exactement à ce que les équipes corp-dev des quatre acquéreurs cibles savent déjà qu'il leur manque. L'exit se prépare en rendant l'acquisition *évidente et compétitive*, pas en la mendiant.

## 1. Les KPIs que les acquéreurs screènent réellement

Un acquéreur stratégique paie pour trois choses : une courbe (croissance + rétention), un fossé (technologie + écosystème créateurs), et l'absence de squelettes (modération, conformité, dette). Grille cible pour ouvrir un process sérieux (mois 24–30) :

### Courbe (la demande)

| KPI | Seuil « conversation » | Seuil « bidding war » |
|---|---|---|
| DAU | 300 k | 1 M+ |
| Rétention D30 | ≥ 10 % | ≥ 13 % |
| Croissance MoM (organique) | +10 % | +15 % soutenus 6 mois |
| Temps de session moyen | 25 min | 40 min |
| Part des 13–24 ans | > 60 % | > 70 % (la démo que tous les acquéreurs perdent) |

### Fossé (l'offre et la tech)

| KPI | Seuil « conversation » | Seuil « bidding war » |
|---|---|---|
| Créateurs actifs monétisés (> 100 $/mois) | 500 | 3 000+ |
| Créateurs vivant de la plateforme (> 2 000 $/mois) | 30 | 200+ (chacun est un ambassadeur verrouillé) |
| Payouts créateurs annualisés | 2 M$ | 20 M$+ |
| Mondes publiés / mois | 5 000 | 50 000 (dont % assisté IA — la métrique Studio) |
| Ratio joueurs→créateurs 30 j | 3 % | 5 % |

### Efficience (la preuve d'ingénierie)

| KPI | Cible | Pourquoi ça compte en due diligence |
|---|---|---|
| Coût infra / heure-joueur | < 0,01 $ blended | Prouve que la marge à 70 % créateurs tient à l'échelle de l'acquéreur |
| Coût infra / DAU / mois | < 0,15 $ | Comparable direct avec les internes de l'acquéreur (qui font pire) |
| Marge brute plateforme | > 55 % du take rate | Démontre un modèle, pas une subvention |
| Incidents modération médiatisés | 0 | La question n°1 du board acquéreur (voir Guardian) |
| Uptime plan de jeu | 99,9 % | Hygiène de base |

**Règle de pilotage : ces KPIs sont le tableau de bord de board dès le mois 6.** Chaque trimestre est raconté dans un « acquirer narrative memo » interne d'une page — l'histoire qu'on pourra montrer telle quelle en data room.

## 2. Packaging par acquéreur : quatre briques, quatre discours

Le même actif se raconte différemment. Dès la série A, chaque sous-système est architecturé pour être **démontrable isolément** (voir §3).

### Microsoft — « le pipeline UGC-IA et le cloud gaming web »

- **La brique manquante** : Minecraft vieillit, Xbox n'a pas de plateforme UGC jeune, et Azure cherche des workloads gaming de référence. Senblox = la démographie 10–20 ans + un Studio IA qui est une vitrine parfaite pour l'IA Microsoft + une infra multi-joueurs cloud-native migrant naturellement sur Azure/PlayFab.
- **Ce qu'on démontre** : coût/heure-joueur, l'agent Forge (création par prompt), le runtime navigateur (= « du gaming dans Edge/Teams/Discord sans console »).
- **Angle d'approche** : partenariat Azure crédits dès la série A (programme startups) → visibilité interne ; ID@Xbox et l'équipe Minecraft comme sponsors internes.

### Epic Games — « la distribution instantanée qui manque à UEFN »

- **La brique manquante** : Epic a le moteur et l'économie créateurs (40 %), mais **aucune distribution web** — Fortnite reste un client de 100 Go hors iOS. Senblox = le runtime « clic → jeu » et le funnel mobile web qu'UEFN ne peut pas offrir, plus une population de créateurs low-code qu'UEFN (trop complexe) exclut.
- **Ce qu'on démontre** : le funnel lien→jeu (60–70 % de conversion), l'escalier no-code→code du Studio, l'interop avatars.
- **Risque à gérer** : Epic est le plus susceptible de « construire plutôt qu'acheter ». Contre-mesure : vitesse et brevets/avance sur le runtime WASM.

### Meta — « le metaverse web qui remplace Horizon »

- **La brique manquante** : Horizon Worlds échoue sur le contenu ET la démographie ; Meta a acheté puis fermé Crayta faute de distribution. Senblox = des mondes UGC avec de la traction réelle chez les jeunes, jouables en lien dans Instagram/WhatsApp/Messenger, plus WebXR prêt pour Quest ([01](01_POSITIONNEMENT_STRATEGIQUE.md) §1).
- **Ce qu'on démontre** : la démo Quest WebXR, la boucle sociale (invitation → session en cours), Guardian (Meta est le plus sensible au risque réputationnel mineurs).
- **Réalisme** : Meta paie bien mais son historique d'intégration (Crayta) est un argument *contre* — utile surtout comme enchérisseur pour créer la compétition.

### Sony — « la couche sociale jeune et le UGC PlayStation »

- **La brique manquante** : PlayStation n'a ni plateforme UGC (Dreams a été abandonné), ni présence forte chez les 10–16 ans, ni stratégie mobile/web convaincante. Senblox = le pipeline de la prochaine génération de joueurs PlayStation + un runtime portable sur PS5/mobile.
- **Ce qu'on démontre** : la rétention 10–16 ans, la portabilité du runtime (le serveur Rust tourne où on veut ; un client natif est dérivable du code WASM).

### Acquéreurs de second cercle (à cultiver pour la tension compétitive)

Tencent (thèse Roblox Chine), Netflix Games (distribution web instantanée), Google (YouTube Playables cherche exactement ce runtime), Discord (les Activities sont notre canal n°2 — un rachat défensif est plausible).

## 3. Architecture d'acquérabilité (décisions techniques prises POUR la due diligence)

1. **Modularité démontrable** : trois actifs à interfaces propres, chacun démontrable seul en data room — (a) le runtime client WASM/WebGPU, (b) Guardian (modération multimodale as-a-service), (c) le Studio IA + agent Forge. Un acquéreur qui ne veut que deux des trois briques est quand même un acquéreur.
2. **Hygiène IP dès le jour 1** : CLA pour toute contribution, inventaire SBOM des licences (pas de GPL contaminante dans le runtime), chaîne de cession IP fondateurs/employés propre, marque déposée (UE/US) — et vigilance particulière sur le choix Luau (licence MIT, OK) et sur toute API « inspirée » de Roblox (on documente l'indépendance de conception, cf. précédents jurisprudentiels API).
3. **Conformité en avance de phase** : dossiers COPPA/DSA/OSA tenus à jour, DPO tôt, audits de sécurité annuels (rapports en data room). Le coût est faible en continu, prohibitif en rattrapage — et une non-conformité découverte en due diligence coûte 20–30 % du prix ou tue le deal.
4. **Portabilité cloud** : GKE/Agones et Postgres sont standards ; l'abstraction des providers IA ([02](02_ARCHITECTURE_TECHNIQUE_MVP.md) §3.2) évite qu'un acquéreur voie un mariage forcé avec le cloud d'un concurrent.
5. **Data room permanente** : métriques (définitions écrites : un « DAU » est défini une fois pour toutes), contrats créateurs standardisés, ledger auditable. Objectif : due diligence en 6 semaines, pas 6 mois — la vitesse protège le prix.

## 4. Déroulé du process (mois 24–36)

1. **Mois 12+** : partenariats d'infrastructure et de distribution avec 2–3 acquéreurs potentiels (crédits Azure, Discord Activities, dev kit Quest). Chaque partenariat = un sponsor interne qui connaît nos chiffres.
2. **Mois 18–24** : série A/B avec un fonds ayant un track record d'exits gaming (Index, a16z Games, Bitkraft, Makers Fund) — leur réseau corp-dev vaut autant que leur argent. Les inbound « soft » d'acquéreurs commencent ici ; on les documente, on ne les poursuit pas.
3. **Mois 24–30** : atteinte de la grille §1, mandat à une banque M&A tech (Aream, LionTree, Qatalyst selon taille). Process structuré : teaser → management presentations → LOI. **Règle d'or : ne jamais négocier avec un seul acheteur.** La compétition Microsoft/Epic/Meta/Sony est le seul levier de prix d'une startup face à un géant.
4. **Fourchette de valorisation réaliste** : à 1 M DAU, ~40–60 M$ de run-rate GMV et la démographie 13–24, les comparables (acquisitions de plateformes sociales/UGC jeunes en croissance) placent la fourchette **300 M$–1 Md$+** selon la tension compétitive et le multiple stratégique — le haut de fourchette exige la bidding war, donc la préparation des §2 et §3.
5. **Plan B assumé** : si aucun process ne converge, l'entreprise vit sur son take rate (marge brute > 55 %, voir §1) et vise la rentabilité à 2–3 M DAU. Une entreprise qui n'a pas besoin de vendre se vend plus cher.

## 5. Synthèse : les 5 décisions irréversibles à prendre maintenant

1. **Web-first, runtime propriétaire WASM/WebGPU** — c'est le fossé technique et l'argument de chaque pitch acquéreur.
2. **70 % créateurs, transparent** — c'est le mécanisme d'acquisition de l'offre ; il n'est crédible que s'il est gravé publiquement dès le jour 1.
3. **Guardian comme produit cœur budgété** — c'est l'assurance-vie réglementaire et un actif cessible.
4. **Pas de crypto, pas de marketplace spéculative au MVP** — chaque acquéreur coté l'exigera ; autant ne jamais créer le passif.
5. **Le tableau de bord growth = la grille d'exit**, tenu dès le mois 6 — pour que le jour où Microsoft appelle, la data room soit déjà écrite.
