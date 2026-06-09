# Agent 1 — Veille simap.ch (Photovoltaïque)

Objectif : recevoir automatiquement les avis PV pertinents, filtrés sur le
segment où ByImport + un partenaire peuvent réellement gagner.

## Codes CPV à charger dans tes alertes

| CPV | Intitulé | Usage |
|---|---|---|
| `09331200` | Modules solaires photovoltaïques | **Cœur de cible** — fourniture de modules |
| `09331000` | Panneaux solaires | Large, capte les variantes de libellé |
| `09332000` | Installation solaire | Marchés d'installation (travaux) → repérer les installateurs |
| `09330000` | Énergie solaire | Filet large |
| `31712331` | Cellules photovoltaïques | Composants |
| `45261215` | Travaux de couverture par panneaux solaires | Marchés travaux → **liste des installateurs gagnants = partenaires cibles** |

> Affine l'arborescence (jusqu'à 8 chiffres) dans le gestionnaire CPV de simap :
> https://www.simap.ch/shabforms/servlet/CpvManagerDispatcher?REDIRECT=CPV&LANGUAGE=FR&MODE=CPV

## Configuration des alertes (à faire une fois)

1. Crée un **compte utilisateur** simap (gratuit). Pas besoin de « profil
   soumissionnaire » juste pour la veille et les alertes.
2. Crée un **abonnement / alerte par code CPV** ci-dessus → e-mail à chaque
   nouvel avis, toute la Suisse.
3. **Filtres prioritaires** : type = *Fournitures* **et** *Travaux* (le PV
   apparaît dans les deux) ; procédure = *gré à gré* + *sur invitation* en
   priorité (voir seuils ci-dessous).
4. Surveille séparément les **avis d'adjudication** sur `09332000` / `45261215`
   → ils révèlent les installateurs qui gagnent les marchés PV publics
   (cf. `02-recherche-partenaire.md`).

## L'échelle des seuils (cantonal AIMP/IVöB, HT, inchangés 2024/2025)

| Procédure | Fournitures | Travaux (gros œuvre) | Lecture stratégique |
|---|---|---|---|
| **Gré à gré** | < 150 000 | < 300 000 | Choix libre, références quasi inutiles — porte d'entrée |
| **Sur invitation** | 150 000 – 250 000 | 300 000 – 500 000 | Min. 3 offres invitées — se faire connaître = être invité |
| **Ouverte / sélective** | ≥ 250 000 | ≥ 500 000 | Concurrence pleine, aptitude lourde — éviter au début |

> Confirme les valeurs exactes (et les seuils internationaux AMP/OMC) sur la
> page officielle : https://www.vd.ch/etat-droit-finances/marches-publics/valeurs-seuils
> Note : sous les seuils internationaux, l'accès des entreprises **étrangères**
> n'est pas garanti → c'est pourquoi ByImport passe par un **partenaire suisse**.

## Critères de filtrage d'un bon avis pour ByImport

Retenir un avis si :
- ✅ Objet = installation/fourniture PV avec une **part module significative**.
- ✅ Variantes **autorisées** (sinon le module imposé doit matcher ton sourcing).
- ✅ Critères d'attribution avec **poids prix réel** (≥ 30-40 %) — sinon ton avantage coût ne pèse pas.
- ✅ Délai de dépôt **réaliste** vu ton délai d'approvisionnement modules.

Écarter si :
- ❌ Marque/module unique imposé sans variante possible et hors de ton catalogue.
- ❌ Exigence de production locale / origine suisse du module.
- ❌ Délai trop court pour sécuriser l'appro.

## Pourquoi pas les voitures (rappel)

Véhicules écartés au démarrage : **homologation OFROU/UE + réseau SAV + garantie
constructeur** exigés par les acheteurs publics, valeur unitaire qui pousse vite
en procédure ouverte, et marge écrasée par les importateurs officiels. À
reconsidérer seulement avec un garage/concessionnaire partenaire et un canal EV
spécifique.
