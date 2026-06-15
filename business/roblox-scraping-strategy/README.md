# Roblox — Stratégie de scraping ciblé, analyse de feedback & alignement business

> **Nature du document.** Artefact business autonome, **sans lien avec le plugin Toprank**. Conformément à `CLAUDE.md`, ce dossier vit dans `business/` et n'est référencé par aucune skill, aucun manifeste ni le README racine. Pas de bump de `VERSION`, pas de `CHANGELOG`.

Ce dossier décrit, du point de vue d'un ingénieur data + analyste business spécialisé Roblox, comment passer de **données brutes scrapées** à un **plan d'action monétisable** pour une expérience (jeu) Roblox.

## Chaîne de valeur (vue d'ensemble)

```
  Sources de données            Traitement              Décision business
 ┌──────────────────┐     ┌──────────────────┐     ┌──────────────────────┐
 │ API Roblox        │     │ Classification    │     │ Levier de monétisation│
 │ Sites analytics   │ ──▶ │ sévérité +        │ ──▶ │ (Gamepass / DevProduct│
 │ Feedback externe  │     │ demande latente   │     │  / Premium Payouts /  │
 │ (Discord/Reddit)  │     │ → specs Luau      │     │  UGC)                 │
 └──────────────────┘     └──────────────────┘     └──────────────────────┘
```

## Plan du dossier

| Fichier | Contenu | Étape de la mission |
|---|---|---|
| [`1_STRATEGIE_SCRAPING.md`](./1_STRATEGIE_SCRAPING.md) | Sources critiques, endpoints API, métriques clés, cadence, garde-fous légaux | Étape 1 |
| [`2_PROTOCOLE_ANALYSE.md`](./2_PROTOCOLE_ANALYSE.md) | Classification par sévérité + traduction plaintes → specs Luau | Étape 2 |
| [`3_ALIGNEMENT_MONETISATION.md`](./3_ALIGNEMENT_MONETISATION.md) | Rattachement de chaque correctif à un levier rentable et éthique | Étape 3 |
| [`4_PLAN_ACTION.md`](./4_PLAN_ACTION.md) | Tableau de priorisation + spécification de la boucle de rétention | Étape 4 |

## Principes directeurs

1. **Donnée fiable avant action.** Une métrique seule ment (un pic de CCU sans rétention = trafic acheté qui churn). On croise toujours ≥ 2 sources.
2. **Monétisation éthique uniquement.** On optimise la *valeur perçue* (contenu, équilibrage, cosmétiques), jamais les mécaniques prédatrices (pay-to-win agressif, loot boxes opaques visant les mineurs). Roblox sanctionne ces pratiques et elles détruisent la rétention long terme.
3. **Respect des conditions d'utilisation.** Le scraping se limite aux API publiques documentées, dans les limites de débit, et aux sites qui l'autorisent. Voir les garde-fous en fin de `1_STRATEGIE_SCRAPING.md`.
