# Plan : tes 1 000 premiers euros en 21 jours

> Rédigé le 13/10/2026. Dossier autonome, sans rapport avec le plugin Toprank (voir `CLAUDE.md`, section « About `business/` »).

## 1. Ce que je sais de toi (et ce que je ne sais pas)

**Sources : uniquement ce dépôt, tes skills Claude et tes connecteurs. Rien d'autre.**

| Constat | Source |
|---|---|
| Tu travailles en français et tu as 5 projets en parallèle : export d'huile d'olive Tunisie→Chine, marketplace de yachts (+ pipeline luxe/jets), Senblox (« concurrent de Roblox »), MonQR (QR code social avec avis/likes), Toprank (skills Google Ads / Meta Ads / SEO) | `business/`, `qr-social-app/`, racine du dépôt |
| Tu as déjà un vrai outil de travail en publicité et SEO : audit Google Ads, audit Meta Ads, SEO, rédaction de contenu | `google-ads/`, `meta-ads/`, `seo/` |
| Tu as commencé à monter une offre « portail de vente de talents », test à **250 €** via un lien Stripe, avec n8n/Make + Apollo + Vercel | skill `toutfaire` |
| Tu as accès à Stripe, Gmail, Vercel, Canva, Calendly, Shopify, Make, Zapier. Google Ads, Meta Ads et Apollo sont à autoriser | connecteurs |
| Tu as passé beaucoup de temps à charger des skills et des plugins (`evolu`, `ruflo`, `graphify`, etc.) | liste des skills |

**Je ne sais pas** : ton pays, ton statut juridique, ton budget, ton temps disponible, ton niveau de pub, si tu as déjà un client, ni ce que couvre exactement l'offre « talents » à 250 €. **Corrige-moi si une hypothèse ci-dessous est fausse, le plan change.**

## 2. Verdict franc : aucun de tes 5 projets ne te fait gagner 1 000 € vite

| Projet | Pourquoi pas pour les 1 000 premiers € |
|---|---|
| **Senblox** | Ton propre `00_REALITE_CHECK.md` chiffre 12 à 20 M€ avant l'exit. |
| **Huile d'olive → Chine** | Un conteneur coûte ~67 000 $. Il faut l'enregistrement GACC et 3 à 6 mois avant la première expédition. Ta propre doc le dit. |
| **Yachts** | Budget de lancement 3 000 à 8 000 €, avocat maritime inclus. Nous sommes mi-octobre, donc hors saison en Méditerranée. À reprendre pour mars-avril. |
| **MonQR** | Produit fini, mais commodité : Linktree, Google Business et les QR gratuits existent déjà. Tu devrais en vendre des dizaines à bas prix. |
| **Portail talents 250 €** | Peut marcher, mais je ne vois ni le produit ni les clients. 4 ventes suffisent, à condition d'avoir un acheteur identifié. |

**Ce qui est vendable en 3 semaines avec ce que tu as déjà : un service d'audit publicitaire (Google Ads / Meta Ads / SEO local) pour petites entreprises locales.** Tu as les outils d'audit, tu n'as besoin ni de stock, ni de capital, ni de site compliqué. L'inconvénient est que tu vends ton temps, pas un actif. Pour un premier 1 000 €, c'est le bon compromis.

## 3. L'offre

| Offre | Prix | Contenu |
|---|---|---|
| **Audit Flash** | **250 €** (**150 €** pour les 2 premiers clients, en échange d'un témoignage) | Audit du compte Google Ads **ou** Meta Ads **ou** du SEO local. PDF de 5 pages : gaspillage chiffré, 5 corrections prioritaires, estimation du gain. Appel de restitution de 20 min. |
| **Suite (upsell)** | 300 à 500 €/mois | Mise en œuvre des corrections + suivi mensuel. |

**Maths pour 1 000 €** (hypothèses prudentes, à remplacer par tes vrais taux) :

- 4 audits à 250 € = 1 000 €
- ou 2 audits à 150 € + 1 audit à 250 € + 1 mois de suite à 450 € ≈ 1 000 €
- Entonnoir : ~200 contacts qualifiés → ~20 réponses → ~8 appels → 3 à 4 ventes. **Ces taux sont une estimation, pas une mesure.** Si tu es à moitié, il te faut 3 semaines de plus.

## 4. Plan jour par jour

### Jours 1-3 : mise en place (0 €)
- [ ] Statut légal : si tu es en France, micro-entreprise (gratuit, 1 jour). Sinon, l'équivalent chez toi. **Sans statut, pas de facture, donc pas de vrai revenu.**
- [ ] Un compte Stripe actif pour encaisser. Le lien de paiement existe déjà dans ton skill `toutfaire` ; vérifie qu'il correspond bien à cette offre avant de l'utiliser.
- [ ] Autoriser **NotFair-GoogleAds** et **NotFair-MetaAds** dans tes réglages de connecteurs (je ne peux pas le faire à ta place).
- [ ] Choisir **UNE** niche locale et **UNE** ville. Ex. : artisans (plombiers, électriciens), cliniques dentaires, restaurants, garages. Critère : ils paient déjà de la pub et chaque client leur rapporte 200 € ou plus.
- [ ] Gèle les 4 autres projets jusqu'au jour 21.

### Jours 4-7 : liste de prospects (≈ 2 h/jour)
- [ ] Rechercher « {métier} {ville} » sur Google. Les entreprises dans les résultats **sponsorisés** paient déjà de la pub : ce sont tes cibles.
- [ ] Remplir une feuille : nom, site, téléphone, 1 défaut visible (page lente, pas de numéro cliquable, pas de suivi d'appels, etc.).
- [ ] Objectif : **60 prospects** avec un défaut précis noté pour chacun.

### Jours 8-14 : prospection (≈ 3 h/jour)
- [ ] 30 contacts/jour sur 5 jours = 150 contacts. Par téléphone, Instagram/LinkedIn ou passage en boutique. Privilégie le téléphone et le message direct à l'e-mail de masse (RGPD/ePrivacy : l'e-mail à froid est encadré).
- [ ] Message type (à adapter à chaque prospect) :
  > Bonjour {prénom}, j'ai regardé votre annonce Google pour « {mot-clé} » : {défaut précis}. Ça vous fait probablement perdre {estimation} par mois. Je peux vous envoyer un mini-audit gratuit de 3 points. Intéressé ?
- [ ] Les 3 points gratuits sont ton **teaser**. Le PDF complet (5 pages) est la prestation payante.
- [ ] Cadence : relance 1 à J+2, relance 2 à J+5, puis stop.
- [ ] Prends les appels via Calendly (déjà connecté).

### Jours 15-21 : vente et livraison
- [ ] Vendre l'audit à 150 € (2 premiers), puis 250 €. Paiement avant livraison, via Stripe.
- [ ] Livrer en 48 h avec les skills `google-ads/audit` ou `meta-ads/audit` ou `seo/seo-analysis`. **Relis et corrige à la main avant d'envoyer : c'est ta réputation, pas celle de l'outil.**
- [ ] À chaque livraison : demander un témoignage + proposer la suite (300 à 500 €/mois) + demander 2 recommandations.

## 5. Suivi (mets-le dans une feuille de calcul)

| Indicateur | Cible |
|---|---|
| Prospects contactés | 150 à 200 |
| Taux de réponse | ≥ 10 % |
| Appels réalisés | ≥ 6 |
| Audits vendus | ≥ 3 |
| CA cumulé | 1 000 € à J21 |

**Règle de décision à J10 :** si tu as contacté 80 personnes et obtenu 0 appel, le problème est le message ou la niche, pas le volume. Change de niche avant d'envoyer plus.

## 6. Risques

1. **Pas de niche précise, donc pas de preuve** : c'est la cause n°1 d'échec. Une seule niche, une seule ville.
2. **Tu prospectes mal ou pas assez** : 3 h/jour sont nécessaires. Si ton temps disponible est de 1 h/jour, compte 6 à 8 semaines.
3. **Livrable mal relu** : l'audit automatique peut se tromper. Chaque chiffre que tu affirmes doit être vérifié dans le compte du client.
4. **Tu rouvres les autres projets** : c'est le risque que j'estime le plus probable, vu ton historique de 5 projets en parallèle.
5. **Accès aux comptes clients** : n'utilise que des accès en lecture, donnés explicitement par écrit.

## 7. Après les 1 000 €

- Réinvestir dans **un seul** projet. Mon ordre de préférence : (1) transformer l'audit en abonnement mensuel, (2) yachts en mars, quand la saison reprend, avec les 3 000 à 8 000 € du budget de lancement, (3) MonQR en bonus pour tes clients locaux (QR « laissez un avis Google »).
- Huile d'olive et Senblox : seulement quand tu auras du capital et une équipe. Pas avant.

## 8. Ce dont j'ai besoin de toi

1. Ton **pays** et ton **statut** (micro-entreprise ou autre).
2. Ton **temps réel** par jour pendant 3 semaines.
3. Ce que contient exactement l'offre « talents » à 250 € : si elle a déjà un acheteur, c'est peut-être plus rapide que l'audit.
4. Ta **niche préférée** (ou je t'en propose trois avec une estimation de volume de recherche).
