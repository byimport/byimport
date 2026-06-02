# Briefing client — {id_lead}

> Fiche generee par `lead-pilier-qa-briefing` le {date_generation}. A ouvrir 10 min avant le RDV.
> Toute information `[MANQUANT]` est a clarifier en RDV. Toute `[ESTIMATION]` est extrapolee — verifier.

---

## 1. En-tete

| Champ | Valeur |
|---|---|
| ID lead | {id_lead} |
| Nom / Prenom | {nom} {prenom} |
| Date / heure RDV | {date_rdv} {heure_rdv} |
| Format | {cabinet / visio / domicile} |
| Lieu | {adresse_rdv} |
| Conseiller | {agent_attribue} |
| Score qualification | {score}/100 |
| Priorite | {A / B / C / D} |
| Persona | {persona_id} — {nom_persona} |
| LTV estimee | {ltv} CHF [ESTIMATION] |
| Probabilite conversion | {prob}% [ESTIMATION] |

## 2. Synthese en 3 phrases

> Qui c'est : {1 phrase profil}
> Pourquoi il vient : {1 phrase declencheur}
> Ce qu'on doit lui offrir : {1 phrase recommandation principale}

## 3. Contexte d'acquisition et conformite

- **Source :** {source} (canal + creative ou keyword si dispo)
- **Date entree :** {date_creation}
- **Nb tentatives de contact :** {nb_tentatives_contact}
- **Derniere action :** {derniere_action} ({prochaine_date})
- **Consentement LPD :** {oui/non} — date {date_consentement} — canal {canal_consentement}
- **Opt-in newsletter :** {oui/non}
- **Anciennete consentement :** {X mois} (limite 3 ans : OK / a renouveler avant {date_limite})

## 4. Situation actuelle

### Etat civil & famille
- {situation_familiale}
- Conjoint travaille en CH : {oui/non} ({salaire si Oui})
- Enfants a charge : {nb} ({age si dispo})
- Charges familiales mensuelles : {charges_chf} CHF

### Statut professionnel
- {statut_pro / statut_emploi_actuel}
- Employeur actuel : {employeur} ({secteur})
- Salaire brut annuel : {salaire_brut} CHF
- Si sans emploi : depuis {date_debut_chomage}, fin droit {date_fin_chomage}

### Statut fiscal
- Permis : {permis_sejour}
- Statut fiscal CH : {Resident / Quasi-resident / Frontalier}
- Canton de residence : {canton} ({pays si frontalier})
- AVS n° : {avs_numero} OU `[MANQUANT — requis pour Centrale 2e pilier]`

## 5. Investigation prevoyance

### 2e pilier (LPP) — historique CH
- Premier emploi CH : {date_debut}
- Dernier emploi CH : {date_fin}
- Nombre d'employeurs successifs : {nb_employeurs}
- Caisse pension derniere connue : {caisse}
- Avoirs derniers emploi : {avoirs_dernier} CHF [ESTIMATION si non confirme]
- **Avoirs totaux estimes : {avoirs_totaux} CHF**

### Centrale 2e pilier — statut investigation
- Demande envoyee : {oui/non} ({date_demande si Oui})
- Resultat : {resultat ou "en attente" ou "non demande"}
- Nb comptes libre passage identifies : {nb}
- Verification Fondation institution suppletive : {oui/non/NSP}
- **Action P0 si "non demande" : `[a faire avant RDV ou en RDV]`**

### 3e pilier (3a)
- Compte 3a existant : {oui/non}
- Institution : {banque ou compagnie d'assurance}
- Type produit : {compte epargne / ETF / titres geres / lie assurance}
- Solde : {solde} CHF
- Versement annee courante : {versement} CHF (plafond {plafond} → {atteint/partiel/non})

### Potentiel de rachat LPP
- {rachat_potentiel} CHF [ESTIMATION si non confirme par fiche LPP]
- Economie fiscale potentielle annuelle : `[a calculer avec barème fiscal client en RDV]`

## 6. Patrimoine consolide

| Categorie | Valeur (CHF) | Source |
|---|---|---|
| Immobilier CH | {immo_ch} | Declare client |
| Immobilier etranger | {immo_etranger} | Declare client |
| Liquidites | {liquidites} | Declare client |
| Avoirs LPP+LP | {avoirs_lpp} | Declare + estimation |
| 3a | {3a_solde} | Declare client |
| Autres avoirs | {autres} | Declare client |
| **TOTAL patrimoine estime** | **{total}** | — |

## 7. Diagnostic preliminaire (a presenter en RDV)

> **Rappel LSFin** : ce diagnostic n'est pas un avis financier engageant. Profil de risque et capacite a supporter les pertes a documenter via questionnaire approprié signé.

**Leviers prioritaires ordonnés par impact :**

1. **{Levier 1}** — gain estime {chiffre ou "a calculer"} — effort {faible/moyen/eleve}
   - Pourquoi maintenant : {raison}
   - Risques / contraintes : {liste}

2. **{Levier 2}** — ...

3. **{Levier 3}** — ...

## 8. Recommandation produit pressentie

| Produit | Pertinence | Justification | Concurrents a citer |
|---|---|---|---|
| {Produit 1} | ✓✓✓ | ... | ... |
| {Produit 2} | ✓✓ | ... | ... |
| {Produit 3} | ✗ | Non applicable car ... | — |

**A proposer en premier en RDV :** {Produit 1}

## 9. Questions ouvertes a clarifier en RDV

> Liste de ce qu'on ne sait pas encore et qu'il faut absolument demander.

- [ ] {Question 1}
- [ ] {Question 2}
- [ ] {Question 3}
- [ ] Confirmer le profil de risque (questionnaire LSFin)
- [ ] Confirmer la capacite mensuelle de versement
- [ ] Confirmer l'horizon de placement
- [ ] Demander beneficiaires souhaitees (3a, LPP)

## 10. Risques compliance — checklist a documenter

- [ ] FIB / KID a remettre pour chaque produit recommande
- [ ] Note d'information LSFin signee
- [ ] Questionnaire approprié signe et archive
- [ ] Divulgation des retrocessions (montants ou methode)
- [ ] Mention de l'organe de mediation
- [ ] Mise a jour `consentement_lpd` si necessaire (renouvellement)

## 11. Economie commerciale

| Indicateur | Valeur |
|---|---|
| Commission previsionnelle 1ere annee | {commission_y1} CHF [ESTIMATION] |
| Commission lifetime estimee | {commission_lifetime} CHF [ESTIMATION] |
| Effort estime (heures conseiller) | {h} h |
| Marge brute previsionnelle | {marge}% [ESTIMATION] |
| Probabilite conversion (basee score) | {prob}% |

## 12. Anti-fiche — ce qu'il ne faut PAS dire / faire

- ❌ Promettre un rendement chiffre sans conditionnel
- ❌ Garantir une economie d'impot precise sans calcul prealable avec sa fiche
- ❌ Vendre un produit hors universe documente dans la politique d'independance
- ❌ Forcer un mandat le jour meme — laisser 24-72h de reflexion (LSFin recommandation)
- ❌ {Anti-fiche specifique au lead ex : "Eviter de mentionner la concurrence VIAC vu sa preference assurance"}

---

**Genere par lead-pilier-qa-briefing — version {timestamp}**
