# Booking & paiement carte — code de référence (NON-LIVE)

> ⚠️ **Aucun paiement réel ici.** Ce dossier est une **implémentation de référence**
> du flux « paiement carte sur le site → réservation envoyée au propriétaire →
> tu gardes la marge ». Déplacer de l'argent réel exige : compte Stripe, entité
> juridique + KYC, et tests. Tant que ce n'est pas en place, le site reste en
> **preview `noindex`** et le bouton « Book & pay » ne fait rien de réel.

## Le flux

```
Client (site)                Serverless (Stripe)                 Propriétaire
─────────────                ───────────────────                 ────────────
1. "Book & pay by card"  ──► create_checkout_session.py
                              · recalcule le prix côté serveur (jamais le client)
                              · Checkout Session (destination charge) :
                                  application_fee = 40% (ta marge)
                                  destination     = compte Connect du proprio
2. paie sur Stripe (carte) ─► Stripe encaisse le TOTAL
                              · ta marge (40%) reste sur ton compte
                              · 60% routés vers le proprio (automatique)
3. paiement validé        ──► stripe_webhook.py (checkout.session.completed)
                              · vérifie la signature
                              · notify_owner() ───────────────────► email/SMS/WhatsApp
                              · enregistre la réservation                 "Nouvelle résa"
```

**« Garder la marge » = `application_fee_amount`** sur une *destination charge*
Stripe Connect : tu n'as jamais à reverser à la main, et tu ne détiens pas
indûment l'argent du propriétaire.

## Marge & affichage prix

- `pseo/pricing.py` : `SITE_MARGIN_PCT` (défaut **0.40**), `SITE_GROUP_SIZE` (défaut **10**).
- Public price (CSV) = ce que paie le client. Proprio = `total × (1 − 0.40)`, toi = `total × 0.40`.
- Affichage « **à partir de €X / personne** » = `total ÷ 10`, **avec** le total et la
  base « 10 personnes » affichés à côté (obligation légale FR : pas de prix/pers
  qui masque le total).

## Pour passer en LIVE (ordre)

1. **Entité juridique + assurance** opérateur/intermédiaire (cf. `../../CADRE_LEGAL.md`).
2. **Stripe** : compte plateforme + **Stripe Connect**, onboarder chaque propriétaire
   comme *connected account* (`acct_…`). Renseigner `owners.json`
   (copie de `owners.example.json`, **gitignoré**).
3. **Variables d'env** (dans le host serverless, jamais sur le site statique) :
   `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `SITE_BASE_URL`, et SMTP/Twilio
   pour `notify_owner`.
4. **Déployer** `create_checkout_session.py` et `stripe_webhook.py` comme
   fonctions serverless ; enregistrer l'URL du webhook dans le dashboard Stripe.
5. **Tester** en mode test Stripe (cartes 4242…) de bout en bout avant prod.
6. `pip install stripe` (dépendance de référence, hors cœur stdlib).

## Sécurité / conformité
- **Jamais** de clé secrète dans le site statique ni dans le repo. `owners.json`,
  `.env` sont gitignorés.
- Recalcule **toujours** le prix côté serveur depuis le `ref` (ne fais pas confiance
  au montant envoyé par le navigateur).
- Vérifie **toujours** la signature du webhook.
- RGPD : minimise les données client (tel/date), base légale, conservation limitée.
