# Cadre légal — prospection email B2B en Europe

> **À lire avant tout envoi.** Ce document est un cadrage opérationnel, pas un avis juridique. Pour un lancement multi-pays sérieux, faire valider par un avocat.

## Vue d'ensemble par pays

| Pays | Email froid B2B | Base légale | Conséquence pratique |
|---|---|---|---|
| **France** | ✅ Opt-out toléré | ePrivacy transposée + doctrine CNIL | Email OK **si** nominatif, lié à la fonction du destinataire, avec désinscription |
| **Suisse** | ❌ Opt-in requis | LCD art. 3 al. 1 let. o + nLPD | Pas d'email froid. Téléphone et courrier OK |
| **Allemagne** | ❌ Opt-in requis | UWG §7 | Pas d'email froid. Amendes réelles, avocats spécialisés en Abmahnung |
| **Autriche** | ❌ Opt-in requis | TKG §174 | Comme l'Allemagne |
| **Belgique** | ⚠️ Opt-out limité | CDE — exception « personnes morales » | Email à adresse **générique** de l'entreprise (info@) OK ; adresse nominative = consentement |
| **Italie** | ❌ Opt-in de fait | Codice Privacy, Garante strict | Traiter comme opt-in |
| **Espagne** | ⚠️ Opt-out étroit | LSSI art. 21 | Intérêt légitime B2B admis si lien direct produit↔fonction |
| **Pays-Bas** | ⚠️ Opt-out B2B | Telecommunicatiewet | Similaire France |
| **Royaume-Uni** | ✅ Opt-out corporate | PECR | Sociétés (Ltd) OK ; sole traders = opt-in |

**Décision opérationnelle :** le pilote email se fait en **France** (et NL/UK si extension). La **Suisse, l'Allemagne, l'Autriche et l'Italie se travaillent par téléphone et courrier postal** — le courrier adressé à l'entreprise est légal partout et, avec un lien/QR vers la démo personnalisée, convertit très bien sur les artisans.

## Règles France (le canal principal du pilote)

Conditions cumulatives pour l'email B2B sans consentement (doctrine CNIL) :

1. **Pertinence professionnelle** : l'objet de la sollicitation est en rapport avec la fonction du destinataire. Vendre un site web au gérant d'une TPE : ✅.
2. **Identification claire de l'expéditeur** : nom, société, coordonnées complètes dans chaque email. Pas de domaine jetable anonyme.
3. **Moyen de s'opposer simple et gratuit** dans chaque message : lien de désinscription OU « répondez STOP » — traité sous 72 h, définitivement.
4. **Information RGPD** : d'où vient la donnée (art. 14 RGPD — « source : registre Sirene / annuaire X »), droit d'accès et de suppression. Une ligne en pied d'email suffit.
5. **Adresse nominative professionnelle** (`p.durand@entreprise.fr`) : OK si fonction pertinente. Adresse générique (`contact@`) : OK aussi en B2B.

## Registre des traitements (RGPD art. 30) — minimum vital

Tenir un fichier (tableur suffit au début) :
- Finalité : prospection commerciale B2B.
- Base légale : intérêt légitime (art. 6.1.f).
- Données : identité, fonction, coordonnées pro, données publiques d'activité. **Rien d'autre.**
- Source de chaque donnée (traçabilité art. 14).
- Durée de conservation : 3 ans après dernier contact sans réponse, puis suppression.
- Liste d'opposition : toute demande STOP y entre à vie et est vérifiée avant chaque vague.

## Fausse urgence = pratique commerciale trompeuse

La directive 2005/29/CE (transposée dans toute l'UE, art. L121-2 s. code de la consommation en France ; LCD en Suisse) interdit de **déclarer faussement qu'une offre n'est disponible que pendant une période limitée**. Concrètement :

- ❌ « Plus que 2 places ce mois-ci » si c'est faux.
- ❌ Compte à rebours artificiel, « offre expire ce soir » renouvelée chaque jour.
- ✅ « Votre démo reste en ligne jusqu'au [date], ensuite je la retire » — **si on la retire vraiment**.
- ✅ « Je lance 5 sites par mois, le planning de [mois] a encore 2 créneaux » — **si c'est la vraie capacité**.

L'urgence honnête est plus efficace : elle est vérifiable, donc crédible.

## Délivrabilité (l'autre police, privée celle-là)

Gmail et Outlook appliquent leurs propres règles, plus dures que la loi :

- **Domaine d'envoi dédié** (ex. `hello@monagence-web.fr`), jamais le domaine principal — un blacklistage ne doit pas tuer la boîte pro.
- **SPF + DKIM + DMARC** configurés avant le premier envoi (exigé par Gmail/Yahoo depuis 2024).
- **Warm-up 2–3 semaines** : commencer à 5–10 emails/jour, monter progressivement.
- **< 0,3 % de taux de plainte spam** sinon coupure Gmail. À 30–50 emails ultra-personnalisés par vague, ce seuil ne sera jamais un problème ; à 5 000 envois génériques, il l'est immédiatement — c'est la raison technique (en plus de la légale) pour laquelle le volume est une impasse.
- Un lien de désinscription fonctionnel réduit les plaintes : les gens se désinscrivent au lieu de signaler.
