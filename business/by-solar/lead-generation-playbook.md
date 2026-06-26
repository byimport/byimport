# By Solar — Playbook d'acquisition (modélisé sur les meilleurs, adapté)

> Hors périmètre plugin (artefact `business/`). Objectif : générer des **leads opt-in** qualifiés pour la pose de panneaux photovoltaïques, en copiant ce qui marche chez les meilleurs installateurs et en l'adaptant à By Solar. Aucun envoi à froid : on **fait venir** des prospects qui consentent, on ne spamme pas.

## Ce que font les meilleurs (Otovo, Svea Solar, EDF ENR, top installateurs locaux)

| Levier gagnant | Pourquoi ça marche | Adaptation By Solar |
|---|---|---|
| **Devis/simulation en ligne instantané** | Le prospect obtient une valeur immédiate (économies estimées) en échange de ses coordonnées → opt-in naturel | Simulateur « économies + éligibilité aux aides » sur la landing, formulaire de **consentement explicite** (case non pré-cochée) |
| **Aides prises en charge pour vous** | Le frein n°1 est la complexité administrative | Hook « On s'occupe de vos aides 2026 (prime autoconsommation, TVA réduite) » |
| **Prix/financement transparents** | Réduit l'anxiété, qualifie le budget | Afficher fourchettes + financement / paiement échelonné |
| **Rappel ultra-rapide** | Le premier qui rappelle gagne le RDV | SLA de rappel < 1 h en heures ouvrées |
| **Preuve sociale locale** | Confiance = nerf de la guerre sur un achat à plusieurs k€ | Avis Google, photos de chantiers **dans la zone**, nb d'installations |
| **Qualification dès le formulaire** | N'envoie au commercial que des leads exploitables | Mini-quiz : propriétaire ? maison ? facture mensuelle ? code postal ? |

## Le funnel (et le skill du plugin qui l'outille)

```
CANAUX (haut de funnel)                         SKILL
  Google Search "devis panneaux solaires {ville}" → google-ads/manage + google-ads/copy
  Meta/Insta lead ads (quiz éligibilité)          → meta-ads/manage
  SEO local + "aides solaires 2026"               → seo/seo-analysis, seo/content-writer, seo/keyword-research
  Réponses IA (ChatGPT/Perplexity) "installateur" → seo/geo-optimizer
        │
        ▼
LANDING + SIMULATEUR (consentement explicite)     → seo/seo-page, seo/content-writer
        │  (double opt-in : email de confirmation)
        ▼
QUALIFICATION (quiz) → lead scoré dans le CRM      → crm-query (lecture/segmentation)
        │
        ▼
RAPPEL < 1h + RDV → suivi nurture (opt-in only)    → business/by-solar/hubspot-outreach.md
        │
        ▼
DEVIS / POSE / AVIS → réinjection avis & parrainage → boucle
```

## Ciblage : à qui s'adresse l'offre (critères de qualification)

Un lead solaire exploitable est en général :

- **Propriétaire** (pas locataire) — discriminant n°1 ;
- **Maison individuelle** (ou copro/local pro pour le B2B) avec toiture exploitable ;
- **Facture d'électricité** au-dessus d'un seuil (ex. > 100 €/mois) → ROI crédible ;
- dans la **zone d'intervention** de By Solar (codes postaux desservis) ;
- avec une **intention** (a demandé une simulation / un devis).

Ces critères deviennent : (a) les questions du quiz de la landing, (b) les filtres de segment dans `crm-query`, (c) les critères de ciblage Ads.

## Campagnes à lancer (modèle → adaptation)

### 1. Google Search — intention chaude
- Mots-clés (via `seo/keyword-research` puis `google-ads/manage`) : `devis panneaux solaires {ville}`, `prix installation photovoltaïque {région}`, `installateur panneaux solaires {ville}`, `aides panneaux solaires 2026`.
- Négatifs : `gratuit arnaque`, `emploi`, `formation`, `bricolage`, `prix de rachat edf` (curieux non acheteurs).
- Annonce (via `google-ads/copy`) : USP = devis gratuit + aides prises en charge + rappel rapide. Extension lieu + avis.

### 2. Meta/Instagram — lead ads avec quiz
- Format lead ad natif avec le quiz d'éligibilité (propriétaire/maison/facture/CP).
- Accroche créative : avant/après facture, « combien votre toit peut vous faire économiser ? ».
- `meta-ads/manage` pour la structure ; respecter le learning phase, fréquence < 3.

### 3. SEO + GEO — captation longue traîne et IA
- Pages locales « Panneaux solaires à {ville} : prix, aides, installateur » (`seo/content-writer`, `seo/seo-page`).
- Contenu « aides solaires 2026 » optimisé pour les moteurs **et** pour les réponses IA (`seo/geo-optimizer`).

## KPIs à suivre (comme les meilleurs)
- **CPL** (coût par lead opt-in), **taux de qualification** (leads exploitables / leads), **taux de prise de RDV**, **délai de rappel**, **taux de transformation devis→pose**, **CAC** vs **panier moyen** d'une installation.
- Dimensionner et profiler les segments via `crm-reports` (leads opt-in par région, par mois, par source).

## Règle d'or
On **attire** des prospects qui laissent leur consentement, on ne **démarche pas** à froid. Si le volume opt-in est insuffisant, on augmente le haut de funnel (Ads/SEO) — jamais on n'élargit vers des contacts non consentants.
