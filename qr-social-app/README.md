# MonQR

Un **QR code imprimable** qui regroupe **tous les réseaux sociaux** d'une personne sur
une seule page, et où les visiteurs peuvent **laisser un avis** et **liker** avec un
pouce bleu 👍.

> ⚠️ Projet **autonome**, sans rapport avec le plugin Toprank du reste de ce dépôt.
> Il vit isolé dans le dossier `qr-social-app/`, sur une branche secondaire — il n'est
> référencé par aucun manifeste, skill, `AGENTS.md` ou `README` du plugin.

## Ce que ça fait

1. **Créer sa carte** : nom, présentation, photo/logo, couleur, et tous les réseaux
   (Instagram, Facebook, TikTok, X, YouTube, LinkedIn, Snapchat, WhatsApp, Telegram,
   Twitch, Pinterest, site web, e-mail, téléphone).
2. **QR code** : généré automatiquement, **téléchargeable en PNG** et **imprimable**
   (mise en page dédiée à l'impression) — à coller où vous voulez.
3. **Page publique** : la personne qui scanne arrive sur une jolie page avec tous les
   liens cliquables.
4. **Avis + likes** : les visiteurs laissent un commentaire et likent ceux des autres
   (pouce bleu, un like par visiteur).

## Lancer en local

Aucune dépendance à installer — uniquement Node.js (≥ 18) :

```bash
cd qr-social-app
npm start
# ou : node server.js
```

Puis ouvrez http://localhost:3000

Pour changer le port : `PORT=8080 node server.js`

## Architecture

- **`server.js`** — serveur HTTP en Node.js pur (aucune dépendance npm). Sert les
  fichiers statiques et expose une petite API JSON.
- **Stockage** — deux fichiers JSON dans `data/` (`profiles.json`, `comments.json`),
  créés au premier lancement. Pas de base de données.
- **`public/`** — le front-end (HTML/CSS/JS sans framework), en français.
- **QR code** — rendu côté navigateur via la librairie `qrcodejs` (CDN). Si le réseau
  est indisponible, le lien du profil reste affiché et copiable.

### API

| Méthode | Route                                            | Rôle                         |
|---------|--------------------------------------------------|------------------------------|
| GET     | `/api/profiles`                                  | 50 dernières cartes (public) |
| POST    | `/api/profiles`                                  | Créer une carte              |
| GET     | `/api/profiles/:id`                              | Carte + commentaires         |
| POST    | `/api/profiles/:id/comments`                     | Ajouter un commentaire       |
| POST    | `/api/profiles/:id/comments/:cid/like`           | Liker un commentaire         |

## Limites connues (MVP)

- **Pas d'authentification** : n'importe qui peut créer une carte. Un `editToken` est
  généré côté serveur mais l'édition/suppression n'est pas encore exposée.
- **Modération** : les commentaires sont publiés directement (le texte est échappé à
  l'affichage pour éviter toute injection, mais il n'y a pas d'anti-spam).
- **Anti double-like** côté navigateur uniquement (localStorage).
- Pensez à sauvegarder/sécuriser le dossier `data/` en production.

## Tests

```bash
node test/api.test.js
```
