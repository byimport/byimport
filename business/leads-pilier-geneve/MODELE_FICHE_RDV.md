# Modèle — Dossier de RDV qualifié (fiche prospect → SwissKap)

> Fiche **prête à remplir**, une par prospect. Remplie par vous ou par l'**agent IA** pendant
> la qualification, puis transmise au **conseiller SwissKap** qui mène le RDV visio et signe.
> C'est le livrable qui conditionne votre commission : **un dossier complet = un RDV qui signe**.
>
> Voir la logique dans `QUALIFICATION_ET_RDV.md` (définition du RDV qualifié + scoring) et
> les formulations autorisées dans `SCRIPTS_APPELS.md` (§9) / `CONFORMITE_APPELS.md`.

## 1. Modèle vierge (à copier pour chaque prospect)

```
══════════════════════════════════════════════
DOSSIER RDV QUALIFIÉ — réf. : __________  Date : ____/____/____
══════════════════════════════════════════════

IDENTITÉ & CONTACT
  Prénom / Nom        : ______________________________
  Téléphone           : ______________________________
  Email               : ______________________________
  Langue              : FR / autre : ____________
  Canton              : GE / VD / VS / FR / NE / JU / autre

SITUATION
  Statut              : salarié / indépendant / frontalier / sans emploi / proche retraite
  Âge (tranche)       : <35 / 35–45 / 45–55 / 55–62 / >62
  Employeur / secteur : ______________________________

AVOIRS DE PRÉVOYANCE (déclarés)
  2e pilier (LPP actuel)        : ____________ CHF
  Compte de libre passage       : ____________ CHF   (où ? __________________)
  3e pilier 3a                  : ____________ CHF   (banque / assurance)
  TOTAL estimé                  : ____________ CHF

BESOIN / CAS D'USAGE  (cocher)
  ☐ Libre passage (sans emploi / changement) — transfert vers fondation au nom du client
  ☐ Rachat LPP (déduction fiscale)
  ☐ 3e pilier 3a (ouverture / optimisation)
  ☐ EPL — achat résidence principale (retrait / nantissement LPP)
  ☐ Indépendant / création de société
  Déclencheur (verbatim)        : ______________________________________________

QUALIFICATION
  Score (/100)        : ______   (voir grille QUALIFICATION_ET_RDV.md §2)
  Qualifié ?          : OUI / NON      Si NON, motif : ________________________

RENDEZ-VOUS
  Format              : visio (Google Meet / Teams / Calendly) / cabinet
  Date & heure        : ____/____/____  à ____:____  (Europe/Zurich)
  Conseiller SwissKap : ______________________________
  Lien visio          : ______________________________

CONFORMITÉ
  Opt-in              : ☐ oui  — date/heure : __________  source : __________
  Preuve d'opt-in     : ☐ jointe (horodatage / libellé du consentement)
  Consent. enregistr. : ☐ annoncé en début d'appel
  Doc envoyée prospect: ☐ oui

NOTES POUR LE CONSEILLER
  (objections, urgence, sensibilités, ce qu'il faut savoir avant le RDV)
  ______________________________________________________________________
  ______________________________________________________________________

PROCHAINE ACTION
  ☐ Confirmation SMS+email envoyée   ☐ Rappel J-1 programmé   ☐ Fiche transmise SwissKap
══════════════════════════════════════════════
```

## 2. Exemple rempli

```
DOSSIER RDV QUALIFIÉ — réf. : 2026-0042   Date : 11/06/2026

IDENTITÉ & CONTACT
  Prénom / Nom : Marc D.        Tél : +41 7X XXX XX XX     Email : marc.d@exemple.ch
  Langue : FR                   Canton : GE

SITUATION
  Statut : salarié (cadre)      Âge : 35–45      Secteur : PME tech

AVOIRS (déclarés)
  2e pilier : 180'000   Libre passage : 85'000 (Inst. supplétive)   3a : 35'000 (banque)
  TOTAL : ~300'000 CHF

BESOIN / CAS D'USAGE
  ☑ Libre passage dormant à consolider   ☑ Rachat LPP
  Déclencheur : « j'ai changé d'employeur il y a 3 ans, je crois que j'ai un ancien 2e pilier
  qui dort »

QUALIFICATION
  Score : 70/100      Qualifié : OUI

RENDEZ-VOUS
  Format : visio (Google Meet)   Date : 13/06/2026 à 17:30 (Europe/Zurich)
  Conseiller SwissKap : __________   Lien : (généré par Calendly)

CONFORMITÉ
  Opt-in : oui — 10/06 14:22, source Meta lead form   Preuve : ☑
  Consent. enregistrement : ☑ annoncé      Doc envoyée : ☑

NOTES
  Très réceptif, veut surtout comprendre le libre passage dormant. Ne pas survendre le rachat
  au 1er RDV. Disponible le soir uniquement.

PROCHAINE ACTION
  ☑ Confirmation envoyée   ☑ Rappel J-1   ☐ Fiche transmise SwissKap
```

## 3. Les mêmes champs en **questions de formulaire** (Calendly / CRM / Google Form)

À mettre comme **questions d'intake** sur la page de réservation Calendly (ou dans le chat de
l'agent IA) pour que le dossier se pré-remplisse tout seul :

1. Nom complet *(texte)*
2. Email *(email)*
3. Téléphone *(téléphone)*
4. Canton de résidence *(liste : GE / VD / VS / FR / NE / JU / autre)*
5. Votre situation *(liste : salarié / indépendant / frontalier / entre deux emplois / proche retraite)*
6. Montant approximatif de vos avoirs de prévoyance cumulés *(liste : <50k / 50–100k / 100–250k / 250–500k / >500k)*
7. Ce qui vous amène *(texte court — le déclencheur)*
8. Case opt-in *(obligatoire)* : « J'accepte d'être recontacté(e) par téléphone/email et de
   participer à un rendez-vous conseil. » + lien politique de confidentialité.

> ⚠️ La **question 6** est le filtre clé : auto-rejet si `<50k` (sauf cas départ Suisse /
> EPL). Voir les filtres de `META_ADS_PLAN.md` et le scoring de `QUALIFICATION_ET_RDV.md`.

## 4. Checklist avant d'envoyer le dossier à SwissKap

- ☐ Les 6 critères du **RDV qualifié** sont remplis (`QUALIFICATION_ET_RDV.md` §1).
- ☐ **Opt-in prouvé** (horodatage + libellé) joint au dossier.
- ☐ Créneau visio **confirmé** + lien généré + rappel J-1 programmé.
- ☐ Notes utiles pour le conseiller renseignées (pas de blabla, du concret).
- ☐ **Aucune** promesse interdite n'a été faite au prospect (rendement, nom de banque,
  déblocage de 2e pilier) — cf. `SCRIPTS_APPELS.md` §9.
- ☐ Dossier horodaté et archivé dans le CRM (traçabilité commission + conformité nLPD).

> 💡 **Astuce data** : ce modèle est volontairement « plat » (un champ = une donnée) pour
> être directement transformé en **colonnes CRM** ou en **schéma JSON** si vous automatisez la
> transmission à SwissKap via Make/n8n. Dites-le-moi si vous voulez la version JSON/CSV.
