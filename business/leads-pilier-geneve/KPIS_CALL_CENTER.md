# KPIs call center & scorecard prestataire/apporteur

> KPIs **opérationnels** du centre d'appels, en complément des KPIs marketing/économiques de
> `BUDGET_ET_KPIS.md`. Objectif : piloter la vitesse, la qualité des RDV, et éviter le
> RDV poubelle — que l'exécutant soit un prestataire humain ou des agents IA.

## 1. Les KPIs qui comptent

| KPI | Définition | Cible | Pourquoi |
|-----|------------|-------|----------|
| **Speed-to-lead** | Délai lead reçu → 1ère tentative | < 5 min (score ≥50, h. ouvrées) | Sous 5 min : ~35% de prise de RDV ; au-delà de 24h : ~8%. Le KPI n°1. |
| **Taux de contact** | Leads joints / leads appelés | 55–75% | Sous 55% : tentatives trop peu nombreuses ou mauvaises heures. |
| **Connect → RDV** | RDV pris / leads joints qualifiables | 30–40% | Mesure la qualité du script et de la qualification. |
| **RDV → présence** | RDV honorés / RDV pris | ≥ 60–70% | Anti-no-show. **Sous 60% = sur-booking de prospects mous.** |
| **RDV → mandat** | Mandats signés / RDV honorés | ~30% | Mesure la qualité réelle du RDV (côté conseiller). |
| **Coût par RDV qualifié honoré** | Coût total / RDV honorés | < ~100 CHF | À comparer à la valeur lead (~225 CHF 1ère année, `BUDGET_ET_KPIS.md`). |
| **Taux de rejet RDV** | RDV refusés (hors-cible/opt-in/no-show) / RDV livrés | < 15% | Au-delà : définition mal appliquée ou ciblage à revoir. |
| **Productivité agent** | Tentatives, talk time, RDV/jour | suivi tendanciel | Dimensionnement et détection de dérive. |

## 2. Scorecard prestataire (revue hebdomadaire)

```
SEMAINE DU ___                         Cible      Réel    Statut
Leads routés                            —          ___
Speed-to-lead moyen (score ≥50)        < 5 min    ___     🟢/🟡/🔴
Taux de contact                         55–75%     ___     🟢/🟡/🔴
Connect → RDV                           30–40%     ___     🟢/🟡/🔴
RDV pris                                —          ___
RDV → présence                          ≥ 60%      ___     🟢/🟡/🔴
Taux de rejet RDV                       < 15%      ___     🟢/🟡/🔴
Coût / RDV honoré                       < 100 CHF  ___     🟢/🟡/🔴
Écoutes QA réalisées (échantillon)     ≥ 5 appels ___
```

## 3. Monitoring qualité (call scoring)

Écouter un **échantillon d'appels chaque semaine** (≥ 5) et noter :
- Ouverture conforme (rappel opt-in + annonce enregistrement) — voir `SCRIPTS_APPELS.md`.
- Qualification des 3 pivots (déclencheur, situation, avoirs) réellement posés.
- **Aucune** parole interdite (rendement, montant ferme, « titre de propriété », conseil
  produit) — tolérance **zéro** (`SCRIPTS_APPELS.md` §9, `CONFORMITE_APPELS.md`).
- Disqualification polie quand non pertinent (pas de RDV forcé).
- Fiche de handoff complète et exacte.

Un appel non conforme côté **conformité** (parole interdite, pas d'annonce d'enregistrement)
= 🔴 critique, correction immédiate, pas un simple point qualité.

## 4. Rémunération & garde-fous anti-RDV-poubelle

- Payer le **RDV qualifié honoré**, pas le RDV brut (`CALL_CENTER_PRESTATAIRE.md` §5).
- **Non-facturation** des RDV hors-cible, opt-in manquant, no-show non re-bookés.
- **Plafonner le bonus** si `RDV → présence` < 60% sur 2 semaines : signal de sur-booking.
- Si `RDV → mandat` chute alors que `connect → RDV` monte → le prestataire « pousse » des RDV
  faibles : resserrer la définition et écouter plus d'appels.

## 5. Seuils d'alerte (cohérents avec `BUDGET_ET_KPIS.md`)

| Métrique | Seuil rouge | Action |
|----------|-------------|--------|
| Speed-to-lead moyen > 1 h | Critique | Revoir routage / capacité / élasticité Q4. |
| Taux de contact < 45% | Critique | Plus de tentatives, meilleures plages horaires. |
| RDV → présence < 50% | Critique | Anti-no-show + suspicion sur-booking → audit. |
| Taux de rejet RDV > 25% | Critique | Définition RDV mal appliquée ou ciblage à corriger. |
| Parole interdite en QA | Très critique | Reformation immédiate ; risque légal (`CONFORMITE_APPELS.md`). |
| Coût/RDV honoré > valeur lead | Critique | Renégocier tarif ou améliorer le taux de conversion. |

## 6. Cadence de revue

- **Quotidien** : speed-to-lead, volume de RDV pris (dashboard auto).
- **Hebdomadaire** : scorecard §2 + écoutes QA §3 (30 min).
- **Mensuel** : RDV → mandat, coût/RDV honoré, taux de rejet, bilan vs valeur lead.
- **Trimestriel** : renégociation tarif, ajustement de la définition RDV, bilan global.
