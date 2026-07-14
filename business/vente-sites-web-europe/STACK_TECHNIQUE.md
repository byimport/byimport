# Stack technique — sites « nouvelle génération » avec animations 3D

## D'abord, l'avertissement honnête

La 3D sur un site vitrine est un **outil de différenciation, pas un standard à appliquer partout**. Deux réalités à garder en tête :

1. **Le prospect type du playbook consulte sur mobile, souvent en 4G.** Une scène 3D mal budgétée ajoute 2–5 s de chargement ; au-delà de 3 s, ~50 % des visiteurs mobiles partent. Un site qui rame fait perdre les appels qu'il devait générer — et le client le mesurera.
2. **Google mesure les Core Web Vitals** (LCP, INP, CLS) pour le classement local. Un site 3D non optimisé se fait battre par le site une-page basique du concurrent. Vendre du « nouvelle génération » qui dégrade le référencement local serait contraire à la promesse du récurrent (« visible sur Google »).

Donc : **la 3D se vend là où l'image prime sur l'appel immédiat**, et elle s'implémente avec un budget de performance strict.

## Où la 3D vend / où elle dessert

| Niche | 3D pertinente ? | Pourquoi |
|---|---|---|
| Architectes, maîtres d'œuvre | ✅ Fort | Visualisation de volumes = cœur du métier |
| Menuisiers/agenceurs haut de gamme, cuisinistes | ✅ Fort | Configurateur ou vue 3D d'une réalisation = effet démo maximal |
| Horlogerie, joaillerie, artisanat d'art (marché CH !) | ✅ Fort | Produit rotatif 360° = standard du luxe |
| Hôtels, spas, domaines viticoles | ✅ Moyen | Visite immersive, mais la photo/vidéo pro fait souvent mieux |
| Restaurants | ⚠️ Faible | Le visiteur veut le menu, les horaires, réserver — en 5 s |
| Plombiers, électriciens, dépannage | ❌ Contre-productif | Visiteur en situation d'urgence : téléphone cliquable > tout |
| Commerces de proximité | ❌ Contre-productif | Horaires, adresse, avis. Point. |

**Règle :** la 3D s'aligne sur le palier **Signature** (voir plus bas), proposé aux niches ✅ — pas ajoutée d'office aux démos Essentiel/Artisan Pro.

## Stack recommandée

### Socle (tous paliers)
- **Site statique généré** (Astro ou équivalent) : HTML/CSS servi tel quel, scores Lighthouse 95+ sans effort, hébergement à coût quasi nul, rien à maintenir côté sécurité. C'est ce qui rend le récurrent rentable.
- **Micro-animations CSS + `IntersectionObserver`** : apparitions au scroll, compteurs, hover soignés. 80 % de l'effet « site moderne » pour 0 coût de performance. **C'est le vrai « nouvelle génération » pour les paliers Essentiel et Artisan Pro.**

### Couche animation (Artisan Pro et +)
- **GSAP + ScrollTrigger** : animations au scroll fluides (parallaxe, pin de sections, timelines). ~60 ko, impact perf maîtrisé.
- **Lottie** pour les animations vectorielles (icônes animées, illustrations) : léger, net sur tous les écrans.

### Couche 3D (palier Signature uniquement)
- **Spline** (spline.design) : éditeur 3D no-code, export web interactif. Idéal pour produire vite un héros 3D ou un objet manipulable par démo. Limite : watermark/coûts selon plan, moins de contrôle perf.
- **Three.js** (ou React Three Fiber si stack React) : contrôle total, gratuit, mais 1–3 jours de dev par scène. À réserver aux scènes réutilisables entre clients d'une même niche (ex. : un configurateur de dressing paramétrable = un développement, N clients menuisiers).
- **`<model-viewer>`** (Google, web component) : LA solution 80/20 pour montrer un objet en 3D — un fichier `.glb` + une balise HTML, rotation/zoom tactiles natifs, AR sur mobile inclus. Parfait pour produit d'artisanat, meuble, pièce d'horlogerie.
- **Scan photogrammétrie** (Polycam ou équivalent, depuis un smartphone) pour produire les modèles 3D des réalisations du client sans modeleur 3D.

### Budget de performance non négociable (palier Signature)
- Scène 3D **lazy-loadée** : le héros affiche d'abord une image (le LCP), la 3D se charge après interaction ou en idle.
- Modèles compressés (Draco/meshopt), textures ≤ 1024 px, **< 1,5 Mo par scène**.
- Fallback statique si `prefers-reduced-motion` ou GPU faible (mobiles d'entrée de gamme).
- Test systématique en 4G throttlée avant livraison : **LCP < 2,5 s mobile**, sinon on allège.

## Le palier « Signature 3D » (extension de `TARIFICATION.md`)

| | France | Suisse |
|---|---|---|
| Setup | 6 000–12 000 € | 10 000–20 000 CHF |
| Récurrent /mois | 249–399 € | 400–600 CHF |
| Contenu | Site multi-pages Signature + 1–2 scènes 3D (produit 360°, configurateur simple ou héros immersif), direction artistique, photos/scans des réalisations, GSAP sur l'ensemble | idem |

- **Cible** : les niches ✅ du tableau — en Suisse romande, l'horlogerie/joaillerie et l'architecture d'intérieur sont le sweet spot (paniers élevés, culture du beau, concurrence d'agences à 20–40 k CHF).
- **Effet démo** : pour ces prospects, la démo Signature inclut **un de leurs produits/réalisations scanné en 3D** (photogrammétrie depuis leurs photos publiques si suffisantes, sinon proposé au RDV). Voir sa propre création tourner en 360° dans sa future page d'accueil est l'argument de vente le plus fort de tout le playbook.
- **Coût de production démo** : 1–2 jours (vs 2–3 h pour une démo standard) → réserver aux prospects classe A de ces niches, 5–10 démos Signature par vague maximum.

## Et Wix / Webflow / Framer ?

- **Wix** : incompatible avec le positionnement. Pas de vraie 3D custom performante, le client peut l'acheter lui-même, et la promesse du playbook est précisément « l'inverse de Wix ». Ne pas l'utiliser, même en dépannage.
- **Webflow / Framer** : défendables pour accélérer la production visuelle (Framer a des intégrations Spline natives), mais abonnement par site qui ronge le récurrent, et dépendance à la plateforme — contraire à l'argument « ce site vous appartient ». Acceptable pour prototyper une DA, pas pour livrer.
- **Verdict** : statique + GSAP + (`model-viewer` | Spline | Three.js) reste la stack qui maximise à la fois l'effet démo, la performance, la marge sur le récurrent et l'argument de propriété.
