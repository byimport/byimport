# Le site web — vitrine, réservation, et le « site vidéos carrées »

> Le site a **deux jobs** : (1) faire rêver (contenu, photos, vidéos carrées) et (2) **convertir sans friction** (dispo réelle → réservation → acompte payé). Un site magnifique qui ne prend pas d'acompte en ligne ne sert à rien.

## Choix de la stack — selon ton niveau

| Profil | Solution | Pourquoi |
|---|---|---|
| **Non-technique, vite** | **Webflow / WordPress + plugin booking**, ou un builder no-code (Framer) + Stripe Payment Links | En ligne en quelques jours, design correct, acompte possible. Idéal pour le test. |
| **Un peu technique** | **WordPress + WooCommerce Bookings** (ou plugin de location) | Calendrier de dispo, paiement, extras, le tout configurable sans coder. |
| **Technique / scale** | **Next.js + Stripe/Mangopay + CMS headless** (Sanity/Strapi) + calendrier custom | Contrôle total, perfs SEO, multi-zones plus tard. Plus long à construire. |

➡️ **Recommandation démarrage** : no-code/WordPress pour **valider en 2 semaines**. Tu re-platformes en Next.js seulement **après** avoir prouvé que ça vend. Ne sur-investis pas dans la techno avant le product-market fit.

## Architecture des pages

```
Accueil ──────────────► promesse + recherche (zone / date / nb pers.) + bateaux phares + preuves sociales
  │
  ├─ Catalogue ───────► filtres (type, capacité, prix, avec/sans skipper, sans permis) + cartes bateaux
  │     └─ Fiche bateau ─► galerie + vidéo carrée + specs + tarifs + calendrier dispo + CTA « Réserver »
  │
  ├─ Réservation ─────► date/créneau → extras → coordonnées → ACOMPTE en ligne → confirmation
  │
  ├─ Expériences ─────► bundles (coucher de soleil, EVJF/EVG, anniversaire, journée crique) → Modèle B
  ├─ Pages locales SEO ─► « Location bateau {ville/port} » (1 par zone) — capte l'intention de recherche
  ├─ À propos / Confiance ─► assurances, sécurité, avis, FAQ, conditions d'annulation
  └─ Contact / Conciergerie ─► WhatsApp + formulaire (beaucoup réservent par messagerie dans le nautisme)
```

## Le tunnel de réservation — règles non négociables

1. **Dispo en temps réel** : on ne propose que des créneaux réellement libres (cf. `OFFRE_ET_YACHTS.md`).
2. **Acompte en ligne (30 %)** dès la première réservation. Filtre les non-sérieux, sécurise ta marge, professionnalise. Solde réglé avant/au départ.
3. **Le moins de champs possible.** Date → bateau → extras → paiement. Chaque étape en trop fait chuter la conversion.
4. **Paiement** : Stripe (simple) ou **Mangopay/Stripe Connect** si tu veux **splitter automatiquement** la part propriétaire et ta commission (marketplace). Au début, encaisse tout toi-même et reverse manuellement — plus simple.
5. **Confirmation immédiate** (email + WhatsApp) avec lieu RDV, contact skipper, quoi apporter, conditions.
6. **Mobile-first** : 70–80 % du trafic loisir est mobile. Le tunnel doit être parfait sur téléphone.

## Le « site vidéos carrées » — ce que ça veut dire concrètement

La demande « un site avec des vidéos carrées (Canva) » se traduit ainsi côté site :

- **Format 1:1** intégré partout où c'est fort visuellement : hero d'accueil, vignette de chaque fiche bateau, page Expériences, témoignages.
- **Pourquoi le carré** : c'est le format **natif Reels/TikTok/feed Instagram** → la **même vidéo** sert sur le site ET en pub ET en organique social. Une production, trois usages (cf. `CONTENU_VIDEO_CANVA.md`).
- **Implémentation propre** :
  - vidéos **courtes (6–15 s), en autoplay muet + boucle** (sound-off par défaut, son au clic),
  - **compressées** (MP4 H.264, < 2–3 Mo) ou servies via un hébergeur vidéo (le poids tue le temps de chargement et le SEO),
  - **poster image** (1ʳᵉ frame) pour éviter le trou blanc au chargement,
  - `lazy-load` des vidéos hors écran.
- **Ne pas en abuser** : 1 vidéo hero + 1 par bateau suffit. Une page saturée de vidéos qui jouent toutes en même temps = lente et repoussante.

## SEO technique (capte la demande de `DEMANDE_MARCHE.md`)

- **Une page par intention/zone** : `/location-bateau-{ville}`, `/location-yacht-{ville}`, `/bateau-sans-permis-{ville}` — alignées sur les mots-clés à volume.
- **Données structurées** : `Product`/`Service` + `AggregateRating` (avis) + `LocalBusiness` → rich snippets.
- **Vitesse** : images en WebP, vidéos compressées, hébergement correct. Core Web Vitals = facteur de ranking ET de conversion.
- **Fiche Google Business Profile** par zone (énorme pour le local « location bateau près de moi »).

> 🔌 Les skills **Toprank** de ce repo (`seo:seo-page`, `seo:meta-tags-optimizer`, `seo:schema-markup-generator`, `seo:content-planner`) produisent exactement ces pages locales, métas et schémas. Réutilise-les.

## Tracking dès le jour 1
- **GA4 + conversions** (réservation, acompte payé, demande de devis, clic WhatsApp).
- **Pixel Meta + balise Google Ads** pour le retargeting et l'optimisation des campagnes.
- **Suivi des valeurs** : envoie la **valeur de la réservation** dans l'événement de conversion → tu optimises sur le CA, pas sur le volume.

## Honnêteté
- **Pas de site sans bateaux ni dispo réelle.** L'ordre est : demande → offre signée → site. Pas l'inverse.
- **Le no-code est un tremplin, pas une prison.** Assume de re-platformer plus tard ; ne perds pas 2 mois à coder un moteur custom avant la première vente.
- **WhatsApp convertit énormément dans le nautisme.** Beaucoup de clients veulent parler à un humain avant de payer 1 000 €. Un tunnel 100 % automatisé sans option humaine laisse de l'argent sur la table.
