# Emails de prospection — séquence, personnalisation, urgence honnête

## Règles non négociables

1. **Un email = une personne = une démo.** Pas de publipostage générique. Les champs entre `{…}` sont remplis à la main ou vérifiés à la main.
2. **France uniquement par email** (voir `CADRE_LEGAL.md`). Suisse/Allemagne : téléphone + courrier (modèle courrier en bas).
3. **Jamais de fausse urgence.** La date de retrait de la démo est réelle, la capacité mensuelle annoncée est réelle.
4. **Pied d'email obligatoire** (identité, source de la donnée, désinscription) sur chaque message.
5. **Pas de prix dans les emails.** Le prix vient au téléphone, après la démo (voir `TARIFICATION.md`).

## Séquence France — 3 emails sur 10 jours

### Email 1 (J0) — la démo

**Objet :** `J'ai créé une maquette de site pour {nom commercial}`

> Bonjour {Prénom Nom},
>
> Je cherchais un {métier} du côté de {ville} et je suis tombé sur votre fiche Google — {détail vrai et précis : « 47 avis à 4,8, c'est rare dans le métier » / « vos photos du chantier de {X} sont impressionnantes »}. Par contre, pas de site web : quand on vous recommande, on ne trouve rien à montrer.
>
> Plutôt que de vous expliquer ce que ça pourrait donner, je l'ai fait. Voici une maquette de ce que serait votre site, construite à partir de votre fiche et de vos avis :
>
> 👉 {lien démo : demo.monagence.fr/{slug}}
>
> Elle vous appartient si elle vous plaît — on en parle 15 minutes au téléphone quand vous voulez : {lien calendrier ou téléphone}.
>
> Je la laisse en ligne jusqu'au **{date J+14, réelle}**, ensuite je la retire pour faire de la place aux maquettes suivantes.
>
> Bonne journée,
> {Prénom Nom}
> {Société} — {téléphone} — {adresse}
>
> ---
> _Vos coordonnées proviennent de {source : l'annuaire Sirene / votre fiche Pages Jaunes}. Pour ne plus recevoir de message de ma part : répondez STOP (effacement définitif sous 72 h)._

**Pourquoi ça marche :** le détail vrai prouve que ce n'est pas un robot ; la démo transforme une promesse en objet ; la date de retrait est une urgence honnête et vérifiable.

### Email 2 (J+4) — la relance utile

**Objet :** `Re: J'ai créé une maquette de site pour {nom commercial}`

> Bonjour {Prénom},
>
> Je me permets de revenir vers vous — la maquette de votre site est toujours en ligne ici : {lien}.
>
> Depuis mon premier message, j'ai ajouté {ajout réel : vos derniers avis Google / une page « zone d'intervention » avec {villes}}. Deux minutes sur votre téléphone suffisent pour vous faire une idée.
>
> Si ce n'est pas le moment, dites-le-moi simplement — je retire la maquette et je ne vous relance plus.
>
> {signature + pied légal identique}

**Pourquoi ça marche :** la relance apporte quelque chose de nouveau au lieu de répéter ; la porte de sortie explicite réduit les plaintes spam à presque zéro.

### Email 3 (J+9) — la clôture

**Objet :** `Je retire la maquette de {nom commercial} le {date}`

> Bonjour {Prénom},
>
> Dernier message de ma part : comme annoncé, je retire la maquette de votre site le {date}. Après cette date, la refaire repartirait de zéro.
>
> Si vous voulez la garder — telle quelle ou modifiée — un appel de 15 minutes suffit pour tout caler : {téléphone / lien calendrier}.
>
> Dans tous les cas, merci de votre attention, et bonne continuation avec {détail métier : les chantiers de la saison / la réouverture de la terrasse}.
>
> {signature + pied légal identique}

**Et on retire vraiment la démo à la date dite.** (Un prospect qui rappelle après : « je peux la remettre en ligne, le planning de {mois} a encore de la place » — vrai, donc utilisable.)

## Variante Suisse — courrier + téléphone

**Courrier A5/A4 imprimé, adressé au dirigeant** (légal partout, taux d'ouverture ~100 %) :

> Objet : Une maquette de site web pour {société} — en ligne 14 jours
>
> Madame, Monsieur {Nom},
>
> {Même corps que l'email 1, adapté} … Vous pouvez la voir ici : **{URL courte}** ou en scannant ce code : {QR code}.
>
> Je me permettrai de vous appeler la semaine du {date} pour recueillir votre avis. Si vous préférez ne pas être contacté, un message au {téléphone} ou à {email} suffit.

Puis **appel téléphonique** la semaine annoncée (le démarchage téléphonique B2B est licite en Suisse ; respecter l'astérisque ⭐ dans l'annuaire = refus de publicité, à vérifier sur local.ch avant chaque appel).

## Mesure

| Métrique | Seuil pilote sain | Si en dessous |
|---|---|---|
| Taux d'ouverture (E1) | > 50 % | Objet ou délivrabilité à revoir |
| Taux de clic démo | > 20 % | La promesse de l'objet ne se retrouve pas dans le corps |
| Taux de réponse (séquence) | > 10 % | Personnalisation insuffisante ou mauvaise niche |
| RDV / réponses | > 40 % | Revoir le CTA (trop d'engagement demandé) |
| Plaintes spam | 0 sur 50 | Si > 0 : stop, tout revoir |
