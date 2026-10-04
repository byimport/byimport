# PATCH 02 — Sécurité de la page de connexion wallet

Deux corrections rapides sur une page qui demande à l'utilisateur de connecter un wallet.

## 2.1 Intégrité du script ethers.js (SRI)

**Problème.** `ethers` est chargé dynamiquement depuis cdnjs sans attribut `integrity` :

```js
var s = document.createElement("script");
s.src = "https://cdnjs.cloudflare.com/ajax/libs/ethers/5.7.2/ethers.umd.min.js";
```

Sur une page qui manipule un wallet, c'est le vecteur classique d'injection de *drainer* :
un CDN compromis ou un intermédiaire réseau remplace le fichier et signe des transactions
à la place de l'utilisateur. Le navigateur n'a aucun moyen de s'en apercevoir.

**Correctif.** Ajouter le hash d'intégrité et le mode CORS :

```js
var s = document.createElement("script");
s.src = "https://cdnjs.cloudflare.com/ajax/libs/ethers/5.7.2/ethers.umd.min.js";
s.integrity = "sha384-Htz1SE4Sl5aitpvFgr2j0sfsGUIuSXI6t8hEyrlQ93zflEF3a29bH2AvkUROUw7J";
s.crossOrigin = "anonymous";
s.onerror = function () {
  alert("Le composant de connexion n'a pas pu être vérifié. Rechargez la page.");
};
s.onload = function () { _initStaking(); };
document.head.appendChild(s);
```

Hash vérifié le 4 octobre 2026 :

```
$ curl -sL https://cdnjs.cloudflare.com/ajax/libs/ethers/5.7.2/ethers.umd.min.js \
  | openssl dgst -sha384 -binary | openssl base64 -A
Htz1SE4Sl5aitpvFgr2j0sfsGUIuSXI6t8hEyrlQ93zflEF3a29bH2AvkUROUw7J
```

**Mieux encore :** auto-héberger `ethers.umd.min.js` (760 Ko) sur `monkeyspunk.io` et
supprimer la dépendance CDN. Le fichier est déjà chargé paresseusement, donc l'auto-hébergement
ne coûte rien sur le premier rendu.

## 2.2 Logos de wallet hotlinkés depuis des domaines tiers

**Problème.** La modale de connexion charge ses logos depuis :

| Source | Souci |
|---|---|
| `altcoinsbox.com/wp-content/uploads/.../coinbase-wallet-logo.png` | **blog tiers aléatoire** |
| `upload.wikimedia.org/.../MetaMask_Fox.svg` | dépendance externe |
| `trustwallet.com/assets/images/media/assets/TWT.png` | dépendance externe |

Trois conséquences : si l'un tombe, la modale de connexion s'affiche cassée au pire moment ;
ces hôtes reçoivent l'IP et le referer de chaque visiteur ; et un utilisateur crypto qui
inspecte la source d'une modale de wallet et y trouve un lien vers un blog inconnu a un
réflexe de méfiance immédiat et légitime.

**Correctif.** La page inline déjà 11 images en data-URI — appliquer le même traitement.
Télécharger les logos officiels une fois, les convertir, et remplacer les `src` :

```bash
# Récupérer les logos depuis leurs sources officielles, puis :
for f in metamask.svg coinbase.png trust.png; do
  echo "$f -> data:$(file -b --mime-type "$f");base64,$(base64 -w0 "$f")"
done
```

Puis dans le markup, remplacer chaque `<img src="https://…">` par le data-URI obtenu.
Le fallback `onerror` existant peut alors être supprimé : il ne sert plus à rien.

```html
<!-- avant -->
<img src="https://altcoinsbox.com/wp-content/uploads/2022/12/coinbase-wallet-logo.png"
     alt="Coinbase Wallet" onerror="this.outerHTML='…'">

<!-- après -->
<img src="data:image/png;base64,iVBORw0KGgo…" alt="Coinbase Wallet" width="36" height="36">
```

## 2.3 Durcissement complémentaire (optionnel, même journée)

Ajouter une CSP en en-tête HTTP (Apache est le serveur, donc `.htaccess`) :

```apache
Header always set Content-Security-Policy "default-src 'self'; \
  script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; \
  style-src 'self' 'unsafe-inline'; \
  img-src 'self' data:; \
  connect-src 'self' https://ethereum-rpc.publicnode.com https://eth.drpc.org; \
  frame-ancestors 'none'"
Header always set X-Content-Type-Options "nosniff"
Header always set Referrer-Policy "strict-origin-when-cross-origin"
```

`img-src 'self' data:` casse volontairement les trois logos hotlinkés — ce qui force la
correction 2.2 et empêche la régression. Si les polices restent chez Google, ajouter
`https://fonts.googleapis.com` à `style-src` et `https://fonts.gstatic.com` à `font-src`
(voir patch 04, qui recommande de les auto-héberger et de ne rien ajouter du tout).
