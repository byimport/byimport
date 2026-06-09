# Déploiement du site — mise en ligne (preview noindex puis production)

> Le générateur produit un **site statique** dans `dist/` : il s'héberge partout (Vercel, Netlify, GitHub Pages, n'importe quel CDN/bucket). Build en **stdlib pure, zéro `pip install`**.

## ⚠️ Avant toute mise en ligne PUBLIQUE (lire)

Le site contient des **données placeholder** : `{{BRAND}}`, téléphone fictif, `example.com`, et des **prix indicatifs**. Tant que ce n'est pas remplacé par du réel :

- **Reste en PREVIEW (`noindex`)** — c'est le build par défaut (`bash build_site.sh`). Chaque page porte `<meta name="robots" content="noindex,follow">` et `robots.txt` interdit toute indexation.
- **Ne passe en PRODUCTION (indexable)** qu'avec : marque réelle, **opérateur/entité juridique réel**, **prix réels**, mentions légales/CGV (cf. `../CADRE_LEGAL.md`). Annoncer des charters à des prix inventés sans opérateur = trompeur + risque juridique.

Renseigne tes vraies valeurs **sans toucher au code** dans `branding.json` (marque, **domaine réel**, téléphone, WhatsApp) — ou exporte `SITE_BRAND`/`SITE_DOMAIN`/`SITE_PHONE`/`SITE_WHATSAPP`. Mets tes **prix réels** dans `pseo/data/*.csv`. `branding.json` est committé (identité publique du site) ; les **secrets** (`.env`, `api/owners.json`, clés Stripe) sont gitignorés. Marge & affichage par personne : `pseo/pricing.py` (`SITE_MARGIN_PCT`, `SITE_GROUP_SIZE`). Paiement carte : voir `api/README.md`.

```bash
cp branding.example.json branding.json   # puis édite tes vraies valeurs
bash build_site.sh prod                   # build indexable avec ta marque
```

## Build local

```bash
cd luxe-pipeline
bash build_site.sh           # PREVIEW (noindex) — défaut
bash build_site.sh prod      # PRODUCTION (indexable) — uniquement quand prêt
python3 -m http.server -d dist 8080   # prévisualiser sur http://localhost:8080
```

## Option A — Vercel (recommandé pour du statique)

`vercel.json` est déjà fourni (build preview + `outputDirectory: dist`).

```bash
npm i -g vercel
cd luxe-pipeline
vercel            # preview deploy → URL *.vercel.app (noindex)
vercel --prod     # quand tu es prêt (pense à build_site.sh prod dans vercel.json)
```

Pour la prod indexable : passe `buildCommand` à `bash build_site.sh prod` dans `vercel.json`.

## Option B — Netlify

`netlify.toml` fourni (publish `dist`, header `X-Robots-Tag: noindex` en preview).

```bash
npm i -g netlify-cli
cd luxe-pipeline
netlify deploy            # preview
netlify deploy --prod     # production (retire le header noindex quand prêt)
```

## Option C — GitHub Pages (sans compte tiers)

Build en CI puis publication. Exemple de job (à adapter, **dans un repo dédié au site**, pas le repo plugin) :

```yaml
- run: cd luxe-pipeline && bash build_site.sh preview   # ou prod
- uses: actions/upload-pages-artifact@v3
  with: { path: luxe-pipeline/dist }
- uses: actions/deploy-pages@v4
```

> Ne pas activer Pages sur le repo du plugin Toprank — héberge le site dans un repo/projet séparé pour ne pas mélanger les domaines.

## Domaine
- **Preview** : sous-domaine gratuit du host (`*.vercel.app` / `*.netlify.app`) suffit.
- **Production** : un domaine de marque (ex. `charter.tamarque.com`). Configure le DNS chez le host, force HTTPS.

## Checklist passage PREVIEW → PRODUCTION
- [ ] `branding.json` créé avec marque / domaine / téléphone / WhatsApp réels
- [ ] Prix réels dans `pseo/data/*.csv` (ou alimentés par le connector + tes tarifs)
- [ ] Opérateur/entité juridique réel + assurances (`../CADRE_LEGAL.md`)
- [ ] Mentions légales, CGV, politique de confidentialité ajoutées
- [ ] `build_site.sh prod` (retire le noindex) + retrait du header noindex côté host
- [ ] `robots.txt` en mode Allow + `sitemap.xml` soumis à Search Console
- [ ] Tracking (GA4, conversions, pixel) branché sur le form de devis
