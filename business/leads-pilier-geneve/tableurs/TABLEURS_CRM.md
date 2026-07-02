# Tableurs CRM — Documentation des fichiers

> Deux tableurs CSV (`prospects_orphan_lpp.csv` et `prospects_3a.csv`) servent de **gabarits de tracking** prospects pour les deux segments prioritaires identifiés dans le dossier. Chaque ligne = un prospect. Chaque colonne = une donnée actionnable.

## Pourquoi pas du .xlsx natif ?

Le format CSV est universel : Excel (Mac/Win), Google Sheets, LibreOffice, Numbers, et tout CRM (HubSpot, Pipedrive, Notion, Airtable) l'importent en un clic. Pour avoir un .xlsx avec formatage (couleurs conditionnelles, listes déroulantes, totaux), voir [Conversion en .xlsx formaté](#conversion-en-xlsx-formaté) en bas.

## Ouvrir dans Excel

- **Excel Suisse / France :** le séparateur par défaut est le **point-virgule (`;`)**. Double-cliquer sur le fichier devrait suffire. Encodage UTF-8.
- **Excel US :** si les colonnes ne se séparent pas, faire `Data > From Text/CSV > Delimiter: Semicolon`.
- **Google Sheets :** `Fichier > Importer > Type de séparateur: Point-virgule`.

---

## 1. `prospects_orphan_lpp.csv` — Prospects "LPP perdu / sans libre passage tracé"

### Cible

Personnes qui ont travaillé en Suisse (passé ou présent) **mais qui ne savent pas où sont leurs avoirs LPP** ou n'ont pas de compte de libre passage actif identifié. Cas typiques :

1. **Cadre ayant changé plusieurs fois d'employeur** et perdu la trace d'un ancien LPP (cas le plus fréquent).
2. **Expatrié(e) parti(e) puis revenu(e) en Suisse**, avec LPP de la première période chez la Fondation institution supplétive par défaut.
3. **Frontalier(e) licencié(e)** ne sachant pas si ses avoirs sont automatiquement transférés.
4. **Personne ayant rompu son contrat et reçu un courrier qu'elle n'a jamais traité** — les avoirs sont à la Fondation institution supplétive LPP au bout de 6 mois sans choix.

### Note légale importante

En Suisse, dès qu'on a cotisé au LPP (salaire annuel >22 050 CHF en 2026), des avoirs **existent forcément quelque part**. La Centrale du 2e pilier (https://www.zentralstelle.ch) permet de rechercher gratuitement où ils dorment. **Première action systématique pour tout lead "orphan LPP" : initier la demande Centrale 2e pilier dès la qualification.**

### Dictionnaire des colonnes

| Catégorie | Colonne | Description | Format / Valeurs |
|---|---|---|---|
| **Tracking** | `id_lead` | Identifiant unique | `LP-AAAA-NNNN` |
| | `date_creation` | Date d'entrée du lead | YYYY-MM-DD |
| | `source` | Canal d'acquisition | ex: "Google Ads - keyword X", "Meta Ads - angle Y", "Recommandation fiduciaire" |
| | `agent_attribue` | Conseiller responsable | Prénom + initiale nom |
| **Identité** | `civilite` | M., Mme, Dr, etc. | Texte court |
| | `nom`, `prenom` | | |
| | `date_naissance` | | YYYY-MM-DD |
| | `age` | Calculé | Entier |
| | `sexe` | | M / F / X |
| | `nationalite` | Code ISO 2 | CH, FR, IT, PT, ES, DE, etc. |
| | `langue` | Langue de contact | FR / DE / IT / EN (mix séparé par /) |
| **Contact** | `email` | | Email valide, vérifié |
| | `telephone` | Format E.164 | +41 79 ... ou +33 6 ... |
| | `adresse`, `npa`, `localite` | | |
| | `canton_residence` | | GE, VD, ZH, ... ou pays si frontalier |
| | `pays_residence` | | CH, France, ... |
| **Statut admin** | `permis_sejour` | | Suisse, C, B, L, G frontalier, Sans |
| | `avs_numero` | 13 chiffres | `756.XXXX.XXXX.XX` (optionnel mais utile pour Centrale) |
| | `statut_fiscal` | | Resident, Quasi-resident, Frontalier, Non-resident |
| **Emploi actuel** | `statut_emploi_actuel` | | Sans emploi, Indemnites chomage, Reconversion, Sabbatique, Au foyer, Retraite anticipee, En formation |
| | `sans_emploi_depuis` | Date début | YYYY-MM-DD |
| | `indemnites_chomage` | Touche ALV/Pole Emploi | Oui / Non / Fin de droit |
| | `fin_droit_chomage` | | YYYY-MM-DD |
| | `projet_professionnel` | | Reprise emploi salarie, Independance, Depart Suisse, Retraite, Sans projet |
| **Historique CH** | `hist_emploi_ch_debut` | Premier emploi CH | YYYY-MM-DD |
| | `hist_emploi_ch_fin` | Dernier jour | YYYY-MM-DD |
| | `nb_employeurs_ch` | Total carriere CH | Entier (info critique = nombre de comptes LP potentiels) |
| | `dernier_employeur`, `avant_dernier_employeur` | Nom raison sociale | Texte |
| | `salaire_dernier_brut_annuel` | CHF | Entier |
| **LPP investigation** | `lpp_caisse_derniere_connue` | Caisse pension dernier employeur | Texte |
| | `lpp_avoirs_estimes_dernier_chf` | Avoirs du dernier emploi | Entier CHF |
| | `lpp_avoirs_totaux_estimes_chf` | Estimation tous comptes | Entier CHF |
| | `centrale_2e_pilier_interrogee` | Demande envoyée | Oui / Non |
| | `centrale_date_demande` | | YYYY-MM-DD |
| | `centrale_resultat` | Texte libre | ex: "3 comptes identifies dont 1 institution suppletive" |
| | `nb_comptes_lp_identifies` | | Entier |
| | `institution_suppletive_verifiee` | Vérif Fondation suppletive | Oui / Non / NSP |
| **Autres avoirs prévoyance** | `a_3a_oui_non` | Compte 3a existant | Oui / Non |
| | `3a_institution` | | Banque ou compagnie d'assurance |
| | `3a_solde_chf` | | Entier |
| **Famille** | `situation_familiale` | | Celibataire, Marie, Pacse, Divorce, Veuf |
| | `conjoint_travaille_ch` | | Oui / Non + salaire si Oui |
| | `enfants_a_charge` | | Entier |
| | `charges_famille_mensuelles_chf` | | Entier |
| **Patrimoine** | `patrimoine_immo_ch_chf` | Valeur estimée | Entier |
| | `patrimoine_immo_etranger_chf` | | Entier |
| | `liquidites_chf` | Compte courant + epargne | Entier |
| | `autres_avoirs_chf` | Bourse, crypto, etc. | Entier |
| **Intention** | `declencheur_demande` | Raison du contact | Texte court |
| | `urgence` | | Immediat / 3 mois / 6 mois / Long terme |
| **Scoring** | `score_qualification` | Calculé (voir formule) | 0–100 |
| | `ltv_estimee_chf` | Commissions lifetime potentielles | Entier |
| | `priorite_rappel` | A=immediat / B=24h / C=72h / D=NPL | A / B / C / D |
| **Conformité** | `consentement_lpd` | | Oui / Non |
| | `date_consentement` | | YYYY-MM-DD |
| | `canal_consentement` | | Formulaire web, Lead form Meta, Telephone, Email |
| | `opt_in_newsletter` | | Oui / Non |
| **Pipeline** | `statut_commercial` | | Nouveau, Contacte, Qualifie, RDV pris, Mandat signe, Perdu, NPL |
| | `prochaine_action` | | Texte |
| | `prochaine_date` | | YYYY-MM-DD |
| | `nb_tentatives_contact` | | Entier |
| **Recommandation** | `produits_recommandes` | | Texte |
| | `mandat_signe` | | Oui / Non |
| | `date_mandat` | | YYYY-MM-DD |
| | `commission_previsionnelle_chf` | | Entier |
| **Notes** | `notes_qualification` | Visible équipe commerciale | Texte long |
| | `notes_internes` | Strictement internes (jamais partagé client) | Texte long |

---

## 2. `prospects_3a.csv` — Prospects "Ouverture / optimisation 3e pilier"

### Cible

Personnes voulant **ouvrir, comparer, ou consolider un 3a** (pilier 3a, prévoyance liée). Couvre :

1. **Salariés résidents** sans 3a ou avec 3a sous-optimisé (souvent banque traditionnelle 1990s).
2. **Indépendants** voulant exploiter le plafond élevé (~36 288 CHF/an en 2026).
3. **Frontaliers quasi-résidents** (>90% revenus en CH) éligibles depuis 2020 — segment niche.
4. **Couples** voulant optimiser à deux.

### Dictionnaire des colonnes (différences vs orphan LPP)

Les colonnes communes (`id_lead`, identité, contact, conformité, scoring, pipeline) suivent la même logique. Colonnes spécifiques :

| Catégorie | Colonne | Description | Format |
|---|---|---|---|
| **Statut pro** | `statut_pro` | | Salarie CDI, Salarie CDD, Independant, Frontalier, Sans emploi, Etudiant, Retraite |
| | `type_contrat` | | CDI temps plein, CDI temps partiel, CDD, Apprentissage |
| | `employeur_actuel`, `secteur_activite` | | Texte |
| | `date_debut_activite_ch` | | YYYY-MM-DD |
| **Revenus** | `salaire_brut_annuel_chf`, `salaire_net_annuel_chf` | | Entier |
| | `revenus_complementaires_chf` | Vacations, location, etc. | Entier |
| | `avs_cotise_oui_non` | Indispensable pour eligibilite 3a | Oui / Non |
| **3a existant** | `3a_existant` | | Aucun / Banque / Assurance / Mixte |
| | `3a_institution` | Banque ou compagnie | Texte |
| | `3a_type_produit` | | Compte epargne classique / ETF / Titres geres / Lié assurance / NSP |
| | `3a_solde_chf` | | Entier |
| | `3a_versement_annee_courante_chf` | | Entier (verif si plafond atteint) |
| | `3a_plafond_atteint` | | Oui / Non / Partiel |
| **2e pilier (contexte)** | `2e_pilier_caisse` | | Texte |
| | `2e_pilier_salaire_assure` | Salaire LPP coordonne | Entier CHF |
| | `2e_pilier_avoirs_chf` | Avoirs LPP courant | Entier |
| | `potentiel_rachat_lpp_chf` | Lacune rachetable | Entier |
| | `libre_passage_existant_chf` | Si applicable | Entier |
| **Objectifs** | `objectif_principal` | | Optimisation fiscale / Capital retraite / Achat immobilier / Couverture invalidite-deces / Mixte |
| | `objectifs_secondaires` | | Texte multi-valeurs séparé par virgule |
| | `profil_risque` | | Conservateur / Equilibre / Croissance / Action |
| | `budget_mensuel_3a_chf` | Capacite de versement | Entier |
| | `preference_produit` | | Banque ETF / Banque classique / Assurance liee / Mixte / NSP |
| **Concurrence** | `banque_actuelle` | Banque principale | Texte |
| | `a_compare_concurrents` | | Oui / Non |
| | `concurrents_cites` | | VIAC, Frankly, Finpension, Yallo, Lloyd 1825, true wealth, Selma, etc. |
| | `recommande_par` | Apporteur | Texte |
| | `echeance_decision` | | Immediat / Avant fin annee / Q1 / Pas presse |
| | `deja_client_courtier` | Risque d'opposition | Oui / Non |
| **Famille / Patrimoine** | Idem `orphan_lpp` plus `conjoint_3a` | Conjoint a-t-il un 3a ? | Oui / Non / NSP |

### Notes par segment

- **Salarié résident :** plafond 7 258 CHF/an en 2026. LTV typique 800–2 500 CHF.
- **Indépendant sans 2e pilier :** plafond 20% du revenu net, max 36 288 CHF/an en 2026. LTV typique 4 000–12 000 CHF.
- **Frontalier quasi-résident :** plafond aligné salarié résident **si** opte pour TOU (taxation ordinaire ultérieure) — vérifier conditions. Niche peu compétitive.
- **Conjoint :** vendre une stratégie couple double le LTV pour zero CAC supplémentaire. Toujours demander à la qualification.

---

## Formule de scoring (commune aux 2 fichiers)

À implémenter dans une colonne `score_qualification` Excel via formule (voir `formula_scoring_excel.txt` ci-dessous), ou côté CRM si tu utilises HubSpot/Pipedrive.

### Pour `prospects_orphan_lpp.csv`

```
SCORE = base 0
  + 30 si lpp_avoirs_totaux_estimes_chf >= 250000
  + 20 si lpp_avoirs_totaux_estimes_chf entre 100k et 250k
  + 10 si lpp_avoirs_totaux_estimes_chf entre 50k et 100k
  -  5 si lpp_avoirs_totaux_estimes_chf < 50k

  + 25 si projet_professionnel = "Independance" ou "Depart Suisse"
  + 15 si urgence = "Immediat"
  + 10 si urgence = "3 mois"

  + 15 si nb_employeurs_ch >= 3 (forte probabilite plusieurs comptes a consolider)
  + 10 si centrale_2e_pilier_interrogee = "Oui"

  + 15 si source contient "Partenaire" ou "Recommandation"
  + 10 si source contient "SEO"
  +  5 si source contient "Google Ads"
  +  3 si source contient "Meta"

PRIORITE_RAPPEL :
  A (rappel < 1h ouvree) si SCORE >= 70
  B (rappel < 4h ouvrees) si SCORE 50-69
  C (rappel < 24h ouvrees) si SCORE 30-49
  D (NPL email seulement) si SCORE < 30
```

### Pour `prospects_3a.csv`

```
SCORE = base 0
  + 30 si statut_pro = "Independant" ET salaire_brut_annuel >= 120000
  + 20 si salaire_brut_annuel >= 100000
  + 10 si salaire_brut_annuel entre 70k et 100k
  -  5 si salaire_brut_annuel < 60000 (plafond 3a = 7258 = economie impot marginale)

  + 20 si budget_mensuel_3a_chf >= 500
  + 10 si budget_mensuel_3a_chf entre 200 et 499

  + 15 si echeance_decision = "Immediat" OU "Avant fin annee"
  + 10 si echeance_decision = "Q1"

  + 15 si potentiel_rachat_lpp_chf >= 30000 (cross-sell LPP)
  + 10 si conjoint sans 3a (deal couple potentiel)

  + 15 si source contient "Partenaire"
  + 10 si source contient "SEO"
  +  5 si source contient "Google Ads"
```

---

## Conversion en .xlsx formaté

Si tu veux des classeurs `.xlsx` avec listes déroulantes, mise en forme conditionnelle (rouge si CPL > seuil, vert si mandat signé), et formules calculées, **script Python one-shot** :

```python
# Pré-requis : pip install openpyxl pandas
import pandas as pd
from openpyxl.formatting.rule import ColorScaleRule
from openpyxl.styles import PatternFill, Font

for stem in ["prospects_orphan_lpp", "prospects_3a"]:
    df = pd.read_csv(f"{stem}.csv", sep=";", encoding="utf-8")
    out = f"{stem}.xlsx"
    df.to_excel(out, index=False, sheet_name="Prospects")

    from openpyxl import load_workbook
    wb = load_workbook(out)
    ws = wb["Prospects"]

    # En-tete en gras + couleur
    header_fill = PatternFill("solid", fgColor="1F4E78")
    for cell in ws[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = header_fill

    # Gradient sur score_qualification (colonne a localiser dynamiquement)
    score_col_letter = None
    for cell in ws[1]:
        if cell.value == "score_qualification":
            score_col_letter = cell.column_letter
            break
    if score_col_letter:
        col_range = f"{score_col_letter}2:{score_col_letter}{ws.max_row}"
        ws.conditional_formatting.add(col_range, ColorScaleRule(
            start_type="num", start_value=0, start_color="F8696B",
            mid_type="num", mid_value=50, mid_color="FFEB84",
            end_type="num", end_value=100, end_color="63BE7B"))

    # Geler la 1ere ligne
    ws.freeze_panes = "A2"
    # Filtre automatique
    ws.auto_filter.ref = ws.dimensions

    wb.save(out)
    print(f"OK -> {out}")
```

Sauvegarder ce snippet sous `convert_to_xlsx.py` à côté des CSV, puis :

```bash
pip install openpyxl pandas
python convert_to_xlsx.py
```

Génère `prospects_orphan_lpp.xlsx` et `prospects_3a.xlsx` avec en-tête stylé, gradient couleur sur le score, panneaux figés et filtres automatiques.

Pour les **listes déroulantes** (statut, canton, priorité), ajouter avant `wb.save()` :

```python
from openpyxl.worksheet.datavalidation import DataValidation
dv_priorite = DataValidation(type="list", formula1='"A,B,C,D"', allow_blank=True)
ws.add_data_validation(dv_priorite)
# Localiser la colonne priorite_rappel et appliquer
for cell in ws[1]:
    if cell.value == "priorite_rappel":
        dv_priorite.add(f"{cell.column_letter}2:{cell.column_letter}{ws.max_row}")
```

---

## Conformité (rappel)

Ces tableurs contiennent des **données personnelles sensibles** (situation financière, état civil, AVS). Implications nLPD :

1. **Stockage** : poste de travail chiffré (FileVault / BitLocker), ou cloud avec hébergement Suisse/UE chiffré (Infomaniak kDrive, Tresorit, OneDrive avec chiffrement côté client).
2. **Accès** : restreint au conseiller attribué + supervision. **Pas de partage par email non chiffré.**
3. **Conservation** : 3 ans après dernier contact pour les leads non convertis, 10 ans pour les clients sous mandat (LBA).
4. **Droits** : tout prospect peut demander accès, rectification, suppression. Process documenté requis.
5. **AVS** : ne pas demander/stocker tant que pas strictement nécessaire (uniquement pour interroger la Centrale 2e pilier ou monter un dossier rachat). Minimisation des données = règle nLPD.

Voir `CADRE_LEGAL_LPD.md` pour le détail.

---

## Évolution recommandée

À 100+ leads, **migrer vers un vrai CRM** (HubSpot Starter gratuit jusqu'à 1 000 contacts, Pipedrive ~15 CHF/mois) :
- Workflow automatiques (relance J+2, J+7, J+30 si pas de réponse).
- Intégration formulaires web → CRM (Webhook).
- Conformité LPD intégrée (consentement timestamped, droit d'accès UI).
- Reporting commercial.

Garder le CSV comme **export de sauvegarde mensuel**.
