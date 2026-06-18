# Call center externalisé — modèle opérationnel (Genève + Lausanne)

> Couche **opérationnelle** en aval du marketing : ce dossier génère des leads opt-in
> (Google Ads, Meta, SEO, partenaires) ; ce document décrit comment un **prestataire
> call-center externalisé** les rappelle, les qualifie et fixe des **RDV qualifiés** avec
> le conseiller, sur Genève **et** Lausanne.
>
> ⚠️ **Modèle légal unique** : on ne rappelle **que des leads entrants ayant donné leur
> consentement** (formulaire opt-in). Le démarchage à froid B2C est interdit en Suisse
> (LCD art. 3 al. 1 let. u). Voir `CONFORMITE_APPELS.md`. Acheter une liste et la faire
> appeler par le prestataire = illégal, non négociable, hors de ce dossier.

## 1. Pourquoi externaliser (et les limites)

**Ce que l'externalisation achète :**
- Démarrage rapide (équipe formée, téléphonie, plages horaires couvertes sans recruter).
- Capacité élastique (gérer un pic Q4 sur le 3a sans embaucher).
- Coût variable plutôt que charge fixe d'un SDR interne.

**Ce que l'externalisation coûte :**
- **Moins de contrôle qualité et de conformité** — c'est *votre* responsabilité légale qui
  est engagée (sous-traitant nLPD, devoirs LSFin), pas la leur. Vous restez responsable du
  traitement.
- **Marge plus faible** qu'une équipe interne à volume élevé.
- **Risque de dérive** : un prestataire payé au RDV brut a une incitation à booker des RDV
  non qualifiés. Tout le contrat doit neutraliser cette incitation (voir §5).

**Règle d'or :** le prestataire **qualifie et prend RDV**. Il ne **conseille jamais** sur un
produit, ne cite jamais de rendement, ne signe rien. Le conseil et la signature du mandat
restent côté cabinet. Cette frontière est à la fois commerciale, qualité **et** légale
(LSFin) — voir `CONFORMITE_APPELS.md` §3.

## 2. Flux de bout en bout

```
Lead opt-in (Meta/Google/SEO/partenaire)
   │  (preuve d'opt-in : horodatage + IP + libellé du consentement)
   ▼
CRM (HubSpot / Pipedrive)  ──  scoring auto (voir QUALIFICATION_ET_RDV.md)
   │  routage temps réel (webhook) vers le prestataire
   ▼
Prestataire — RAPPEL « speed-to-lead »
   │  Score ≥50 : < 5 min ouvré   │  Score 30–49 : < 4 h ouvré   │  Score <30 : email d'abord
   ▼
Appel de qualification (script, 3–5 min) ──► qualifié ?
   │  NON → disqualification polie + log motif (pas de RDV forcé)
   │  OUI ▼
Prise de RDV qualifié
   │  GE : cabinet rue X ou visio   │  Lausanne : cabinet/espace VD ou visio
   ▼
Confirmation immédiate (SMS + email) + rappel J-1 (anti-no-show)
   ▼
Fiche de handoff → conseiller (voir QUALIFICATION_ET_RDV.md)
   ▼
RDV honoré → conseil (cabinet) → mandat signé
```

Le prestataire travaille dans **votre** CRM (accès délégué) ou dans le sien avec
synchronisation. Préférer **votre CRM** : vous gardez la donnée, la preuve d'opt-in et
l'historique d'appel — critique pour la conformité et pour ne pas être prisonnier du
prestataire.

## 3. Sélection d'un prestataire romand

### Critères éliminatoires (pas de compromis)
- **Français natif**, accent et registre adaptés à une clientèle suisse romande aisée
  (35–55 ans, avoirs ≥100k). Un plateau offshore générique détruit la crédibilité sur ce
  vertical — la cible raccroche.
- **Couverture horaire GE + Lausanne** : 8h–19h en semaine + samedi matin (les cadres
  rappellent hors bureau).
- **Conformité nLPD** : prêt à signer un **DPA** (contrat de sous-traitance), données
  hébergées en Suisse/UE, registre des traitements. Voir `CONFORMITE_APPELS.md` §4.
- **Enregistrement des appels** avec gestion du consentement (pour la QA et la preuve).
- **Secteur financier/assurance** déjà pratiqué — un prestataire qui connaît le 2e/3e pilier
  monte en compétence en jours, pas en mois.

### Due diligence — questions à poser
1. Pouvez-vous travailler **dans notre CRM** (HubSpot/Pipedrive) ?
2. Quel **délai de rappel garanti** (speed-to-lead) en heures ouvrées ?
3. Combien de **tentatives** par lead, sur quelle fenêtre, avant abandon ?
4. Signez-vous un **DPA nLPD** ? Où sont hébergées les données ? Sous-traitez-vous vous-même ?
5. Enregistrez-vous les appels ? Comment gérez-vous le **consentement** en début d'appel ?
6. Acceptez-vous une **facturation au RDV honoré** (pas au RDV brut) ?
7. Pouvez-vous fournir des **échantillons d'appels** pour notre QA hebdomadaire ?
8. Référence client sur un vertical financier régulé en Suisse ?

### Red flags (fuir)
- « On a déjà une base de prospects prévoyance à appeler. » → **cold calling illégal**. Stop.
- Refus de signer un DPA ou de localiser les données.
- Facturation **au RDV brut** sans clause de remplacement des no-shows / hors-cible.
- Plateau offshore non francophone natif « mais ça passe ».
- Promesse de volumes de RDV déconnectée de votre volume de leads (ils inventeront des RDV).

## 4. Contrat & SLA

| Clause | Niveau attendu |
|--------|----------------|
| **Speed-to-lead** | < 5 min ouvré pour score ≥50 ; < 4 h ouvré sinon. Pénalité si délai moyen dépasse le seuil 2 semaines de suite. |
| **Tentatives par lead** | ≥ 5 sur 7 jours (mix appel + SMS + email), à des heures variées, avant statut « injoignable ». |
| **Plages horaires** | Lun–ven 8h–19h, sam 9h–12h. |
| **Définition du RDV qualifié** | Annexée au contrat = `QUALIFICATION_ET_RDV.md`. Pas d'ambiguïté : c'est le livrable facturable. |
| **Propriété des données & scripts** | Vous. Le prestataire ne réutilise ni ne revend les leads. Restitution à la fin du contrat. |
| **DPA nLPD** | Signé avant le 1er appel. Sous-traitance ultérieure soumise à accord écrit. |
| **Enregistrement & QA** | Accès à un échantillon d'appels chaque semaine pour scoring qualité. |
| **Réversibilité** | Préavis court (30 j), restitution des données, pas de lock-in CRM. |

## 5. Modèles de tarification

| Modèle | Comment ça marche | Pour / Contre |
|--------|-------------------|---------------|
| **Au RDV qualifié honoré** | X CHF par RDV qui (a) respecte la définition `QUALIFICATION_ET_RDV.md` **et** (b) est **honoré** (le prospect se présente). | ✅ aligne le prestataire sur la qualité. ❌ le prestataire porte le risque no-show → tarif unitaire plus élevé. |
| **À l'heure / à l'ETP** | Facturation du temps agent. | ✅ simple, bon si volume de leads régulier. ❌ aucune incitation à la qualité ; à éviter seul. |
| **Hybride (recommandé)** | Petit fixe (base horaire couvrant le temps de traitement) **+ bonus par RDV honoré**. | ✅ couvre le prestataire sur le temps, le motive sur le résultat, sans l'inciter au RDV poubelle. |

**Ordres de grandeur indicatifs** (Suisse romande, vertical financier — à négocier, *pas*
des prix fermes) : **60–120 CHF par RDV qualifié honoré**, ou **base horaire + 30–60 CHF de
bonus/RDV** en hybride. À mettre en regard de la valeur d'un lead qualifié (~225 CHF en 1ère
année, voir `BUDGET_ET_KPIS.md`) : un coût par RDV honoré sous ~100 CHF reste rentable si le
taux RDV → mandat tient (~30%).

**Garde-fou anti-RDV-poubelle (impératif) :**
- Payer le RDV **accepté/honoré**, jamais le RDV brut.
- **Non-facturation** des RDV hors-cible (sous les critères) ou no-show non re-bookés.
- Plafonner le bonus si le **taux RDV → présence** chute sous un seuil (ex. < 60 %) : signe
  que le prestataire sur-book des prospects mous. Voir `KPIS_CALL_CENTER.md`.

## 6. Périmètre interne vs délégué

| Tâche | Prestataire | Cabinet (interne) |
|-------|:---:|:---:|
| Rappel speed-to-lead | ✅ | |
| Qualification (script) | ✅ | |
| Prise de RDV + confirmation + rappel J-1 | ✅ | |
| Fiche de handoff | ✅ (remplie) | ✅ (relue) |
| **Conseil produit / recommandation** | ❌ **interdit** | ✅ |
| **Signature du mandat** | ❌ | ✅ |
| Preuve d'opt-in / conformité du traitement | (applique) | ✅ **responsable** |
| Scripts, définition RDV qualifié, QA | (exécute) | ✅ **possède** |

## 7. Calcul de capacité (dimensionner la commande)

Méthode simple pour estimer le besoin et challenger le devis du prestataire :

```
Leads bruts/mois               = L
Leads à appeler (score ≥30)    ≈ 70 % × L
Tentatives/lead                ≈ 4         → appels à passer ≈ 2.8 × L
Temps moyen par tentative      ≈ 6 min (incl. compose, voicemail, notes)
Heures agent/mois              ≈ (2.8 × L × 6) / 60
RDV qualifiés attendus         ≈ 30–40 % des leads joignables qualifiables
```

**Exemple Romandie, régime de croisière (GE + Lausanne) :** L ≈ 200 leads/mois
→ ~560 tentatives → ~56 h agent/mois (≈ 0.35 ETP) → ~45–70 RDV qualifiés/mois.
En **pic Q4 (3a)**, L peut doubler : prévoir la clause d'élasticité dans le contrat pour ne
pas exploser le speed-to-lead quand le volume monte.

**Genève vs Lausanne :** un seul pool d'agents bilingues suffit (même langue, mêmes produits).
La seule différence opérationnelle est la **logistique du RDV** (cabinet GE / cabinet ou
visio VD) et la **nuance fiscale cantonale** que l'agent n'a *pas* à expliquer — il qualifie
et book, le conseiller traite le détail fiscal (voir frontière LSFin, `CONFORMITE_APPELS.md`).

## 8. Pièges fréquents

- **Déléguer la responsabilité légale** : non. Vous restez responsable du traitement nLPD et
  des devoirs LSFin. Le prestataire est sous-traitant, pas bouclier.
- **Ne pas annexer la définition du RDV qualifié** au contrat → litiges de facturation garantis.
- **Payer au RDV brut** → flot de RDV mous, conseiller qui perd son temps, économie détruite.
- **Laisser le prestataire dans son propre CRM** → vous perdez la donnée et la preuve d'opt-in.
- **Sous-dimensionner pour Q4** → speed-to-lead qui explose au pire moment (saison 3a).
- **Laisser l'agent conseiller** → violation LSFin + RDV « pré-vendus » qui déçoivent.
