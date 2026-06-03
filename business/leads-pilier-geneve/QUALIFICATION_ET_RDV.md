# Qualification & RDV qualifié — définition, scoring, handoff

> Ce document définit **ce qu'est un RDV qualifié** — le livrable facturable du call center /
> apporteur — et comment on le score, l'accepte ou le rejette, puis le transmet au
> conseiller/courtier. À **annexer au contrat** du prestataire ou à la convention apporteur.

## 1. Définition contractuelle — « RDV qualifié »

Un RDV est **qualifié** (donc facturable / commissionnable) si **tous** les critères sont réunis :

| # | Critère | Seuil |
|---|---------|-------|
| 1 | **Opt-in valide** | Preuve de consentement (horodatage + libellé) présente au dossier. |
| 2 | **Avoirs de prévoyance** | ≥ 50 000 CHF déclarés (2e pilier + libre passage + 3a cumulés). |
| 3 | **Situation pertinente** | Salarié, indépendant, frontalier, entre deux emplois (avec avoir de libre passage), ou projet EPL/société. |
| 4 | **Déclencheur identifié** | Un besoin concret (libre passage à consolider, rachat, 3a, achat logement, passage indépendant…). |
| 5 | **Créneau confirmé** | Date + format (cabinet GE / cabinet ou visio Lausanne) acceptés par le prospect, coordonnées vérifiées. |
| 6 | **Coordonnées valides** | Téléphone joignable + email corrects. |

Un RDV qui manque **un seul** de ces points **n'est pas** qualifié → non facturable (voir §4).

## 2. Scoring — priorisation de l'appel

Reprend et adapte le modèle de `BUDGET_ET_KPIS.md` (cohérence des deux documents) :

| Critère | Points |
|---------|--------|
| Avoirs ≥ 250k | +30 |
| Avoirs 100–250k | +20 |
| Avoirs 50–100k | +10 |
| Avoirs < 50k | −10 |
| Statut indépendant | +20 |
| Statut frontalier | +15 |
| Cadre salarié | +10 |
| Source partenaire/apporteur | +25 |
| Source Google Ads (intention forte) | +15 |
| Source Meta Ads | +5 |
| Source SEO organique | +20 |
| Rempli en heures ouvrées | +5 |
| Email professionnel (domaine propre) | +5 |

- **Score ≥ 50** → rappel < 5 min ouvré.
- **Score 30–49** → rappel < 4 h ouvré.
- **Score < 30** → email de qualification d'abord, appel si réponse.
- **Score < 10** → NPL (nurturing newsletter), pas d'appel humain/IA.

## 3. Fiche de handoff — prestataire/agent → conseiller

Remplie **pendant/juste après** l'appel, transmise avec le RDV. Sans elle, le conseiller
arrive à l'aveugle et le taux de signature chute.

```
FICHE RDV QUALIFIÉ
──────────────────
Prénom / Nom        :
Téléphone / Email   :
Ville / canton      : GE / VD          Format RDV : cabinet / visio
Date & heure RDV    :
Conseiller assigné  :

Source du lead      :                  Date opt-in :
Score               :   / 100

Situation           : salarié / indépendant / frontalier / sans emploi / proche retraite
Avoirs déclarés     :        CHF   (LPP courant / libre passage / 3a — préciser)
Déclencheur         :
Cas d'usage         : libre passage / rachat LPP / 3a / EPL logement / société
Notes de l'agent    : (verbatim utile, objections, urgence, sensibilités)

Consentement enreg. : oui / non        Doc envoyée au prospect : oui / non
```

## 4. Acceptation / rejet d'un RDV livré

Pour éviter les litiges de facturation **et** les RDV poubelles :

**RDV refusé (non facturable) si :**
- Avoirs réels < 50k constatés en RDV (déclaration gonflée).
- Opt-in absent ou invalide.
- Hors cible manifeste (anti-persona : < 30 ans avoirs < 30k, > 62 ans hors fenêtre, etc.,
  cf. `CIBLE_PERSONA.md`).
- Coordonnées erronées / prospect injoignable au moment du RDV.

**Politique no-show :**
- 1er no-show → le prestataire/apporteur **re-book une fois** (non refacturé).
- 2e no-show → RDV clos, **non facturable**.
- Payer uniquement les RDV **honorés** (voir `CALL_CENTER_PRESTATAIRE.md` §5 et
  `KPIS_CALL_CENTER.md`).

**Boucle de feedback :** chaque rejet est loggué avec motif et **remonté au marketing**
(un pic de rejets « avoirs gonflés » = un formulaire trop permissif à resserrer ; un pic
« hors cible » = un ciblage Meta/Google à corriger).

## 5. Frontière de responsabilité (rappel)

La qualification **n'est pas du conseil**. La fiche de handoff documente des **faits déclarés**
par le prospect, pas une recommandation. Le conseiller/courtier reste seul responsable du
conseil, de l'adéquation LSFin et de la signature. Voir `CONFORMITE_APPELS.md`.
