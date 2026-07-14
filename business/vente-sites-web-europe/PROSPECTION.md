# Prospection — trouver les entreprises sans site web

## Principe

Il n'existe **aucun registre** des entreprises « sans site web ». On construit la liste en croisant deux sources :
1. Un **annuaire d'entreprises** (registre officiel ou plateforme locale) → l'univers complet de la niche dans la zone.
2. Une **vérification de présence web** par entreprise → filtre « pas de site ».

Le tri se fait niche par niche. Une passe sur « toute la France » n'a aucun sens : la liste serait inexploitable et invérifiable.

## Sources par pays

### France
- **API Recherche d'entreprises** (recherche-entreprises.api.gouv.fr) — gratuite, sans clé : raison sociale, SIREN, code NAF, adresse, effectif (tranche), date de création. Filtrable par NAF + département/commune.
- **Données financières** : les comptes déposés sont sur data.inpi.fr (gratuit) — beaucoup de TPE déposent en confidentialité, donc utiliser plutôt la **tranche d'effectif** comme proxy du CA (voir `TARIFICATION.md`).
- **Pages Jaunes / Google Maps** : fiches sans champ « site web » = premier signal.
- **Annuaires métiers** : CMA (artisans), ordres professionnels, fédérations (CAPEB, UMIH…).

### Suisse
- **Zefix** (zefix.ch) — registre du commerce central, gratuit : raison sociale, forme juridique, siège, but social. Pas de CA (jamais public en Suisse pour les PME non cotées) → proxy par forme juridique et effectif estimé.
- **local.ch / search.ch** — les fiches sans site web sont le meilleur signal.
- ⚠️ La prospection email froide est **interdite sans opt-in** (voir `CADRE_LEGAL.md`) : en Suisse, la liste sert au **téléphone et au courrier**, pas à l'email.

### Autres pays (quand le pilote FR/CH est rentable, pas avant)
- **Belgique** : Banque-Carrefour des Entreprises (KBO/BCE), données ouvertes.
- **Italie** : Registro Imprese (payant à l'acte) ; Pagine Gialle pour le signal « pas de site ».
- **Allemagne** : Handelsregister + Gelbe Seiten — mais opt-in strict, même canal que la Suisse.
- **Espagne** : Páginas Amarillas + BORME.
- Outils SaaS multi-pays si budget : Apollo.io / Vibe Prospecting / Clay (filtre « no website » approximatif — toujours revérifier à la main).

## Méthode de vérification « pas de site »

Pour chaque entreprise de la liste brute, dans l'ordre (s'arrêter au premier site trouvé) :

1. Recherche Google : `"<raison sociale>" <ville>` — regarder les 10 premiers résultats.
2. Fiche Google Business Profile : champ site web vide ?
3. Variantes de domaine évidentes : `<nom>.fr`, `<nom>.ch`, `<nom-ville>.fr`.
4. Page Facebook/Instagram utilisée **comme site** (menu, horaires, réservation) → compte comme présence partielle : prospect valable mais angle différent (« votre page Facebook ne vous appartient pas »).

**Classement :**
- **A — aucun site, fiche Google active avec avis** : cible prioritaire (se soucie déjà de son image).
- **B — aucun site, aucune présence** : cible secondaire (souvent pas demandeur).
- **C — page réseaux sociaux seule** : angle « site = actif que vous possédez ».
- **Exclu — site existant même moche** : c'est un autre marché (refonte), autre pitch, plus concurrentiel.

## Données à collecter par prospect (fiche type)

| Champ | Source | Usage |
|---|---|---|
| Raison sociale + nom commercial | Registre | Personnalisation |
| Dirigeant (nom, fonction) | Registre / LinkedIn | Contact nominatif — obligatoire en B2B FR |
| Adresse, ville | Registre | Démo (carte, zone d'intervention) |
| Téléphone | Fiche Google / annuaire | Relance + canal principal CH |
| Email | Site ? non — fiche annuaire, registre, ou formulaire de la fédération | Vérifier : email nominatif ≫ contact@ |
| Activité précise, spécialités | Fiche Google, avis clients | Contenu de la démo |
| Note Google + nb d'avis | Google Maps | Qualification (classe A) + contenu démo (afficher les avis) |
| Effectif (tranche) | Registre | Proxy prix (`TARIFICATION.md`) |
| Photos existantes | Fiche Google | Visuels de la démo |
| Ancienneté | Registre | Argument (« 20 ans de métier et invisible en ligne ») |

**Règle RGPD dès la collecte :** ne collecter que ce qui sert le contact professionnel, noter la source de chaque donnée, prévoir la suppression sur demande. Détail dans `CADRE_LEGAL.md`.

## Volume cible

- Liste brute par niche×zone : 100–200 entreprises.
- Après vérification « sans site » : typiquement 30–60 % restent.
- Après qualification (classe A + email/téléphone nominatif trouvé) : **30–50 prospects contactables** — c'est la bonne taille pour une vague. Au-delà, la personnalisation des démos ne suit plus.
