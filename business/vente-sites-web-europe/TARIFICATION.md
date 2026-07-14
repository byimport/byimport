# Tarification — indexer le prix sur la taille de l'entreprise

## Le problème avec « le prix selon le chiffre d'affaires »

Le CA exact d'une TPE est rarement public (dépôts confidentiels en France, jamais publiés en Suisse). Et annoncer un prix ouvertement indexé sur le CA du client (« je vous ai vu faire 800 k€, donc c'est plus cher ») est perçu comme opportuniste et fait fuir.

**La bonne pratique :** des **paliers d'offre** dont la valeur croît avec la taille du client, et un ciblage du palier via des **proxys observables** :

| Proxy | Où le trouver | Ce qu'il indique |
|---|---|---|
| Tranche d'effectif | Registre (Sirene, Zefix) | Taille générale |
| Forme juridique | Registre | EI/auto-entrepreneur ≪ SARL/Sàrl ≪ SAS/SA |
| Nb d'avis Google + note | Google Maps | Volume d'activité + sensibilité image |
| Véhicules flottés, locaux | Street View, photos | Niveau d'investissement |
| Secteur | Code NAF/NOGA | Panier moyen du métier (un couvreur ≫ un cordonnier) |

## Grille France (€ HT)

| Palier | Cible (proxys) | Setup | Récurrent /mois | Contenu |
|---|---|---|---|---|
| **Essentiel** | Solo, 0–2 salariés, < 20 avis | 890–1 200 € | 59 € | One-page : présentation, services, avis Google intégrés, formulaire, carte, mobile, SEO local de base |
| **Artisan Pro** | 3–9 salariés, activité visible | 1 800–2 500 € | 89 € | 5–7 pages, page par service, galerie chantiers/réalisations, demande de devis, GBP optimisé |
| **PME Locale** | 10–49 salariés, multi-services ou multi-sites | 3 500–6 000 € | 149–249 € | Multi-pages, rédaction complète, photos pro (partenaire), SEO local avancé, suivi mensuel, éventuel multilingue |
| **Signature 3D** | Niches visuelles (architectes, agenceurs, horlogerie, luxe) | 6 000–12 000 € | 249–399 € | Site Signature avec scènes 3D interactives, direction artistique, animations GSAP — détail, cibles et grille CH dans `STACK_TECHNIQUE.md` |

## Grille Suisse (CHF HT) — mêmes paliers, ×1,6–1,8

| Palier | Setup | Récurrent /mois |
|---|---|---|
| Essentiel | 1 500–2 000 CHF | 90 CHF |
| Artisan Pro | 3 000–4 500 CHF | 150 CHF |
| PME Locale | 6 000–10 000 CHF | 250–400 CHF |

Les prix suisses ne sont pas de l'opportunisme : coûts d'acquisition plus élevés (téléphone/courrier, pas d'email froid), attentes de qualité locales, et concurrence des agences suisses à 8–15 k CHF le site vitrine.

## Le récurrent est le vrai produit

Marge d'un setup à 1 800 € après démo, production, vente : correcte une fois.
Marge de 89 €/mois × 36 mois de durée de vie moyenne : **3 200 € par client, quasi sans coût marginal**.

Le récurrent couvre : hébergement, domaine, sauvegardes, mises à jour, 2 modifications de contenu/mois, rapport SEO local trimestriel. Le vendre **dans le même contrat** que le setup (pas en option) : « votre site, hébergé, maintenu et visible, pour X € puis Y €/mois ».

## Positionnement face aux objections prix

- **« Wix/Jimdo c'est 15 €/mois »** → « Et c'est vous qui faites tout : le design, les textes, le référencement, la maintenance. Combien vaut une journée de votre temps sur un chantier ? Moi je vous livre un site fini qui vous ramène des appels, vous ne touchez à rien. »
- **« Mon neveu peut le faire »** → ne pas se battre ; proposer de garder la démo sous le coude. Une partie revient 6 mois plus tard.
- **« Trop cher »** → descendre d'un palier, jamais de remise sur le même palier (la remise dévalorise la démo qu'ils ont déjà vue).
- **« Pas besoin, le bouche-à-oreille suffit »** → « Vos clients satisfaits parlent de vous — et la première chose que fait la personne qui reçoit la recommandation, c'est vous chercher sur Google. Aujourd'hui elle trouve [rien / vos concurrents]. »

## Règle d'or

Le prix s'annonce **après** que le prospect a vu sa démo, jamais dans le premier email. La démo crée la valeur perçue ; le prix sans démo n'est qu'un chiffre comparable à Wix.
