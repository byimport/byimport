# Canal de veille exploitable — Feuilles d'avis officiels (FAO)

> Le nouveau simap.ch (depuis le 01.07.2024) est une appli JavaScript **sans API
> publique** : ses listes ne sont pas lisibles par un outil automatique. **Mais**
> les **Feuilles d'Avis Officiels cantonales** republient les avis simap et sont,
> elles, **lisibles** (pages rendues côté serveur). C'est notre canal de veille
> de secours, en complément des alertes e-mail simap.

## Vaud — faovd.ch (vérifié, fonctionne)

Pages lisibles, contenu réel et daté, mises à jour à chaque édition FAO :

| Section | URL | Contient |
|---|---|---|
| État de Vaud | `https://www.faovd.ch/marches-publics/canton` | CHUV, DGIP, DAB, DGNSI… |
| Communes | `https://www.faovd.ch/marches-publics/communes` | Marchés communaux |
| Autres adjudicateurs | `https://www.faovd.ch/marches-publics/autres` | Fondations, Romande Energie, services industriels — **PV fréquent ici** |

- **Pagination** : `?page=2`, `?page=3`… (jusqu'à ~40+ pages selon la section).
- **Visible sans abonnement** : objet, adjudicateur, date, n° de publication simap.
- **Réservé aux abonnés / sur simap** : cahier des charges complet, délai de
  dépôt, critères. → Ouvre la publication sur ton compte simap (gratuit) avec le
  **n° de publication** pour le détail.

### Méthode de scan PV (Vaud)

1. Parcourir `/autres`, `/canton`, `/communes`, page par page.
2. Repérer les mots-clés : *photovoltaïque, solaire, panneaux, CFC 231.5*
   (231.5 = code CFC suisse des installations PV).
3. Pour un **appel d'offres** PV → noter le n° simap, ouvrir sur simap, récupérer
   délai + specs → lancer le cycle 4 agents.
4. Pour un **avis d'adjudication** PV → noter l'**adjudicataire** = installateur
   actif → cible pour l'e-mail partenaire (`02-recherche-partenaire.md`).

### Exemples réels trouvés (édition FAO n°45-46, juin 2026)

> Datés — à reconfirmer sur simap, donnés comme preuve que le canal fonctionne.

- **simap 37587-01** — « ESE Yverdon-les-Bains, K2, CFC 231.5 INSTALLATIONS
  PHOTOVOLTAÏQUES » — Fondation St-George — *appel d'offres* → cible marché.
- **simap 26566-03** — « Autonomie électrique – Lot 1 Extension photovoltaïque »
  — Betelec SA — *adjudication* → lead partenaire installateur.

## Genève & Valais — à brancher de la même façon

Pour couvrir tout le bassin proche de Saint-Julien :
- **Genève** : Feuille d'avis officielle (fao.ge.ch) — vérifier la section marchés
  publics et sa lisibilité par fetch.
- **Valais** : Bulletin officiel (bulletinofficiel.vs.ch) — idem.
- Sinon, les **alertes e-mail simap** par CPV (cf. `01-veille-simap.md`) couvrent
  tous les cantons sans scan manuel — c'est le canal principal ; la FAO est le
  complément consultable à la demande.

> ⚠️ Ce canal donne des **pistes**, pas le dossier complet. La source officielle
> et le dépôt d'offre restent **simap.ch**.
