# PATCH 04 — Nettoyage SEO et conformité

Aucun de ces points n'est bloquant, mais chacun coûte de la crédibilité ou crée une exposition.

## 4.1 Supprimer le paragraphe de pied de page bourré de mots-clés

Le footer contient aujourd'hui :

> Monkeys Punk (also known as Punk Monkeys) is a collection of 10,000 unique pixel art NFTs
> on Ethereum featuring the $PUNK cryptocurrency. […] The punk crypto ecosystem includes DAO
> governance and pixel art artist grants. Monkeys Punk — where punk meets crypto, NFTs meet
> pixel art on the blockchain.

C'est du bourrage de mots-clés caractérisé : répétition de « punk crypto », « pixel art NFTs »,
« blockchain » sans valeur informative pour un lecteur. Google traite ce motif comme un signal
de spam, et il n'apporte rien : le contenu éditorial de la page (2 838 mots, structure en
sections, FAQ balisée) est déjà largement suffisant pour se classer.

**Action :** supprimer le paragraphe. Garder la baseline courte juste au-dessus
(« Built on Ethereum. Stored on IPFS. Powered by $PUNK. Owned by you. »), qui est bonne.

## 4.2 Supprimer `<meta name="keywords">`

35 termes, ignorés par Google depuis 2009. Pire, la liste contient :

```
… testnet blockchain, Ethereum testnet, test network, …
```

La page vend un déploiement **mainnet** et se positionne involontairement sur « testnet ».
C'est aussi en contradiction directe avec le bloc « SMART CONTRACT DEPLOYED — live on
Ethereum Mainnet ». Un visiteur qui compare les deux se demande sur quel réseau il mint.

**Action :** supprimer la balise entière. Même remarque pour la mention « Tested on testnet
before Ethereum mainnet deployment » du footer : elle est vraie et rassurante, mais elle doit
être dans le bloc de preuve, pas dans un paragraphe SEO.

## 4.3 Auto-héberger les deux polices

La page charge `Press Start 2P` et `Space Grotesk` depuis `fonts.googleapis.com`.
Le bandeau cookies affirme :

> 🍪 This site sets no tracking cookies and collects no personal data.
> Only the fonts are loaded from Google Fonts. By continuing, you accept this.

Or charger une police depuis Google transmet l'adresse IP du visiteur à Google — c'est
exactement le point tranché par le tribunal régional de Munich en janvier 2022 (affaire
Google Fonts). Avec une version française et un ciblage européen, la phrase « collects no
personal data » est inexacte en l'état.

**Action :** télécharger les deux familles en `.woff2`, les servir depuis `/fonts/`, déclarer
les `@font-face` en CSS inline (déjà 25 Ko de `<style>`, donc pas de requête supplémentaire),
et supprimer les trois `<link>` vers Google. Le bandeau devient alors exact, et on gagne
deux connexions externes sur le chemin critique.

```css
@font-face {
  font-family: 'Space Grotesk';
  src: url('/fonts/space-grotesk-400.woff2') format('woff2');
  font-weight: 400; font-display: swap;
}
```

## 4.4 Créer les pages légales manquantes

Il n'y a aujourd'hui ni mentions légales, ni CGU, ni politique de confidentialité.
Pour un site qui vend des actifs numériques à une audience européenne, avec une version
française et du trafic publicitaire payant, c'est le minimum :

| Page | Contenu minimum |
|---|---|
| `/legal` | éditeur, contact, hébergeur, forme juridique |
| `/terms` | nature du produit, absence de garantie de valeur, frais réseau à la charge de l'acheteur, droits d'usage commercial accordés au holder |
| `/privacy` | données collectées (e-mail de la capture du patch 03), base légale, durée, droits RGPD, sous-traitants |

Les lier depuis le footer. Le disclaimer déjà présent (« No financial return is promised or
should be expected ») est bon et doit être reporté dans les CGU.

## 4.5 Ajouter le lien X/Twitter

Le `<head>` déclare `twitter:site = @MonkeysPunk` mais aucun lien vers X n'existe dans la page.
Seuls Discord, OpenSea et Instagram sont liés. Pour un lancement NFT, X reste le canal de
distribution principal : soit le compte existe et il faut le lier, soit il n'existe pas et il
faut retirer la balise `twitter:site` qui promet un compte introuvable.

## 4.6 Pointer OpenSea vers la collection, pas vers le profil

Le lien actuel va vers `opensea.io/monkeyspunkfounder`, c'est-à-dire le **profil du créateur**.
Comme preuve publique des mints #1 et #2, la page de la **collection** est plus convaincante
et ne dépend pas du contenu du portefeuille personnel du fondateur.

## 4.7 Rafraîchir `lastmod` dans le sitemap

`sitemap.xml` annonce `lastmod = 2026-07-27` et `changefreq = weekly` pour les deux URL.
Le HTML n'a pas changé d'un octet depuis au moins le 20 août. Soit le contenu bouge et
`lastmod` doit suivre, soit il ne bouge pas et `changefreq: weekly` est un signal faux.
À régler en même temps que la mise à jour de la copie du mint.
