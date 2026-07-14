# Processus de vente — de la liste au contrat, démo d'abord

## Vue d'ensemble

```
Niche×Zone → Liste vérifiée → Démos personnalisées → Contact → RDV 15 min → Contrat → Mise en ligne → Récurrent
   (J0-3)       (J3-7)            (J7-14)           (J14+)      (48h après     (sous 7j)   (sous 14j)     (mois 2+)
                                                                  réponse)
```

Le principe qui porte tout : **le prospect voit son site avant d'avoir parlé à qui que ce soit.** On ne vend pas une prestation, on montre un résultat.

## Étape 1 — Le template de niche (une fois par niche, ~2 jours)

Construire UN template de qualité par niche (ex. « artisan bâtiment ») :
- One-page + variante 5 pages, mobile d'abord (les artisans regardent leur téléphone, pas un écran 27").
- Blocs standard : héros avec métier+ville, services, réalisations/galerie, avis Google, zone d'intervention avec carte, formulaire de contact + téléphone cliquable.
- Emplacements variables clairement identifiés : nom, couleurs, photos, textes, avis.
- Stack au choix (statique + formulaire tiers, CMS léger…) — le critère est le coût marginal par démo, pas la techno.

## Étape 2 — La démo personnalisée (~2–3 h par prospect)

À partir de la fiche prospect (`PROSPECTION.md`) :
1. Injecter nom, ville, métier, spécialités relevées dans les avis.
2. Intégrer 3–5 **vrais avis Google** du prospect (publics, avec prénom de l'auteur).
3. Photos : celles de la fiche Google si exploitables, sinon banque d'images du métier avec mention « photos d'illustration — remplacées par les vôtres ».
4. Rédiger 3–4 paragraphes réellement spécifiques (années d'activité, zone, spécialités). C'est ici que les outils IA font gagner du temps — **sur le contenu, pas sur l'envoi**.
5. Déployer sur `demo.{agence}.fr/{slug}` avec :
   - bandeau « Maquette proposée à {société} — en ligne jusqu'au {date} »,
   - `noindex` (la démo ne doit pas se positionner sur le nom du prospect),
   - analytics simple : savoir si le lien a été ouvert, combien de temps, sur quelles pages.

**La date de retrait est notée dans le CRM et honorée.** C'est le socle de l'urgence honnête.

## Étape 3 — Le contact

Selon le pays : séquence email (France, `EMAILS.md`) ou courrier+appel (Suisse). Signal d'or : **le prospect a ouvert sa démo mais n'a pas répondu** → appel téléphonique dans les 48 h (« je voulais votre avis sur la maquette ») — c'est le meilleur moment de tout le processus.

## Étape 4 — Le RDV de 15 minutes (téléphone, pas de visio imposée)

Trame :
1. **Faire parler** (5 min) : « Vous avez vu la maquette — qu'est-ce qui vous a plu, qu'est-ce qui manque ? » Noter les modifications demandées : chaque demande de modification est un signal d'achat.
2. **Cadrer la valeur** (3 min) : ce que le site fait pour lui — être trouvé quand on le recommande, capter les demandes de devis la nuit et le week-end, afficher les avis.
3. **Annoncer le prix** (2 min) : le palier adapté (`TARIFICATION.md`), setup + mensuel, en une phrase, puis **se taire**.
4. **Traiter l'objection** (3 min) : réponses dans `TARIFICATION.md`.
5. **Conclure** (2 min) : « Si on part là-dessus, votre site est en ligne le {date sous 14 j}. Je vous envoie le devis dans l'heure. »

## Étape 5 — Contrat et encaissement

- Devis + contrat le jour même (l'élan retombe en 48 h). Signature électronique.
- **Acompte 40–50 % à la signature**, solde à la mise en ligne. Jamais de mise en ligne sans encaissement du solde.
- Le contrat inclut le récurrent (12 mois, puis tacite reconduction mensuelle) et précise ce qu'il couvre.
- Prévoir la propriété : le client possède son domaine et son contenu. C'est un argument de vente (« contrairement à une page Facebook, ce site vous appartient ») et un gage de confiance.

## Étape 6 — Livraison et récurrent

- Mise en ligne sous 14 jours max — la démo étant déjà à 80 %, tenir ce délai est facile et il impressionne.
- Onboarding : fiche Google reliée au site, domaine au nom du client, email pro si palier le prévoit.
- Mois 2+ : rapport trimestriel simple (visites, appels depuis le site, position Google locale). Ce rapport justifie le mensuel et prépare l'upsell (page supplémentaire, campagne locale).

## Outils minimum

| Besoin | Outil (au choix) |
|---|---|
| CRM / suivi des vagues | Tableur au début ; CRM léger dès 100 prospects |
| Envoi email (FR) | Boîte pro sur domaine dédié + suivi manuel — PAS d'outil de mass-mailing au pilote |
| Calendrier RDV | Calendly ou équivalent |
| Signature + devis | Outil de signature électronique |
| Démos | Hébergement wildcard `demo.*` + analytics léger |

## Ce que l'on n'automatise PAS (au pilote)

- L'envoi des emails (50 emails/vague s'envoient à la main en 2 h — et c'est ce qui garantit la personnalisation).
- La qualification téléphonique.
- La décision de prix.

Ce que l'on automatise volontiers : la constitution de la liste brute, la vérification « pas de site », la génération du premier jet de contenu de démo, le suivi d'ouverture des démos.
