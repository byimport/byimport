# By Solar — Kit campagne email (acquisition conforme RGPD)

> **Hors périmètre plugin.** Ce dossier est un artefact business spécifique à By Solar (installation de panneaux solaires photovoltaïques). Il **ne fait pas partie** du plugin Toprank : ne pas le référencer depuis un skill, le manifeste, `AGENTS.md` ou le `README` du plugin, et ne pas toucher `VERSION` / `CHANGELOG.md` à cause de lui. Voir la note `business/` du `CLAUDE.md`.

## Ce que ce kit fait — et ne fait pas

| Fait | Ne fait pas |
|---|---|
| Définit **comment segmenter** des contacts **déjà opt-in** via les skills `crm-query` / `crm-reports` | N'envoie **aucun** email |
| Fournit des **modèles d'emails conformes** (FR) : objet, corps, mentions légales, désinscription, identité expéditeur | Ne fait **pas** de prospection à froid vers des particuliers non consentants |
| Décrit la **remise à un ESP** (Brevo, Mailchimp, HubSpot Marketing…) pour l'envoi | Ne contourne **pas** le consentement ni la traçabilité |

L'envoi d'emails ne passe **jamais** par le connecteur CRM (il n'a pas d'outil d'envoi) ni par un script maison : il passe par un **ESP** qui gère consentement, désinscription en 1 clic, authentification du domaine (SPF/DKIM/DMARC) et journalisation.

## Le cadre légal, en clair (France / UE)

- **B2C (particuliers)** : prospection commerciale par email = **consentement préalable (opt-in) obligatoire** (RGPD art. 6 + directive ePrivacy, doctrine CNIL). Pas d'opt-in → pas d'email. Le cold-emailing B2C est **illégal** et détruit la délivrabilité.
- **B2B (adresses professionnelles)** : toléré si le message est **en rapport avec la fonction** du destinataire **et** propose une désinscription claire. Reste recommandé de privilégier l'opt-in.
- **Tout email** doit comporter : identité de l'expéditeur, objet non trompeur, lien de **désinscription** fonctionnel, et le traitement effectif des désinscriptions (< 72 h en pratique).
- **Registre** : conserver la **preuve du consentement** (source, date, périmètre) pour chaque contact — c'est une obligation, pas une option.

Si la base By Solar ne contient pas de contacts opt-in, la bonne réponse n'est pas d'emailer quand même : c'est de **générer des leads opt-in** (landing + formulaire de consentement, Google/Meta Ads, SEO local) — ce que les skills existants du plugin savent faire.

## Le pipeline conforme (vue d'ensemble)

```
1. SEGMENTER   crm-query  → liste des contacts opt-in qui matchent la cible
   (+ crm-reports pour dimensionner / profiler le segment)
        │
        ▼
2. RÉDIGER     email-templates.md → contenu conforme (objet, corps, mentions, désinscription)
        │
        ▼
3. ENVOYER     esp-handoff.md → import du segment dans l'ESP, campagne, envoi consenti
        │
        ▼
4. MESURER     ouvertures / clics / désinscriptions dans l'ESP → réinjection des intéressés en CRM
```

## Fichiers de ce kit

- `segmentation.md` — comment construire le segment opt-in avec `crm-query` / `crm-reports`.
- `email-templates.md` — modèles d'emails FR conformes pour By Solar.
- `esp-handoff.md` — procédure de remise à un ESP (sans envoi via le CRM).
