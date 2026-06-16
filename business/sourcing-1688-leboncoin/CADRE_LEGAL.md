# Cadre légal — vendre sur Leboncoin des produits importés de Chine

Ce document n'est pas un conseil juridique ; c'est la check-list opérationnelle des obligations
connues. En cas de doute sur un produit précis, vérifier auprès des sources citées.

## 1. Statut : acheter pour revendre = activité commerciale, point final

Revendre **avec marge** des biens **achetés pour être revendus** est une activité commerciale
par nature (art. L110-1 du Code de commerce). Ce n'est pas de la vente d'occasion entre
particuliers. Sans statut :

- travail dissimulé (URSSAF) + redressement fiscal sur les ventes constatées ;
- Leboncoin transmet automatiquement les données de ventes à l'administration fiscale
  (directive **DAC7**) au-delà de 30 ventes ou ~2 000 €/an — l'activité est donc visible ;
- pratique commerciale trompeuse au sens DGCCRF si on se présente comme particulier
  (le "faux particulier" est explicitement sanctionné).

**Solution simple : micro-entreprise** (autoentrepreneur.urssaf.fr, gratuit, ~30 min) :
- Activité "achat-revente de marchandises" (BIC). Cotisations ~12,3 % du CA encaissé,
  versement libératoire possible.
- Plafond micro : 188 700 € de CA pour l'achat-revente ; franchise de TVA jusqu'au seuil en
  vigueur (~85 000 € pour les biens — vérifier l'année en cours).
- Numéro SIREN exigé par Leboncoin pour un compte PRO — c'est aussi la clé de l'automatisation
  de la publication (voir `AUTOMATISATION.md`).

## 2. Côté Leboncoin

- **Compte PRO obligatoire** dès que l'activité est habituelle et lucrative. Vendre en volume
  sur un compte particulier = suppression d'annonces puis bannissement, en plus du risque DGCCRF.
- Le compte PRO impose les obligations du vendeur professionnel envers des consommateurs :
  **garantie légale de conformité 2 ans**, droit de rétractation **14 jours** pour les ventes à
  distance (livraison), mentions légales (SIREN) sur le profil.
- Interdictions Leboncoin à respecter (liste non exhaustive) : contrefaçons, armes y compris
  certains couteaux, produits rappelés, e-cigarettes/liquides, médicaments, compléments.

## 3. Douane et TVA à l'import

- **TVA 20 % dès le premier euro** sur les imports hors UE (depuis juillet 2021). Assiette :
  valeur produit + transport + assurance + droits.
- **Droits de douane** : 0 à 12 % selon le code SH (nomenclature TARIC). En dessous de 150 € de
  valeur intrinsèque, exonération de droits (pas de TVA-exonération) — mais **fractionner les
  envois pour rester sous 150 € est de la fausse déclaration**, et les agents déclarent des
  valeurs minorées par défaut : exiger une déclaration à la valeur réelle, c'est l'importateur
  (vous) qui porte le risque en cas de contrôle.
- Conserver factures 1688/agent + preuves de paiement : c'est la justification de valeur en cas
  de contrôle, et la base de la comptabilité d'achat.
- En micro-entreprise en franchise de TVA, la TVA d'import n'est **pas récupérable** — elle est
  intégrée au coût de revient (cf. `MARGES_ET_COUTS.md`).

## 4. Conformité produit : l'importateur EST le responsable

En important de Chine pour revendre, vous endossez juridiquement le rôle de l'importateur /
metteur sur le marché (règlement UE 2019/1020 sur la surveillance du marché) :

- **Marquage CE** réel pour les catégories couvertes (électrique, jouets, EPI, radio/BT…).
  Les "certificats CE" fournis par les vendeurs 1688 sont fréquemment des faux ou des rapports
  de test sans valeur — un vrai dossier comporte déclaration UE de conformité + rapports de test
  d'un laboratoire identifiable, à votre nom de produit.
- **REACH** (substances chimiques) s'applique aux textiles, plastiques, bijoux.
- **RED/CEM** pour tout ce qui émet (Bluetooth, WiFi, 433 MHz).
- Étiquetage français : identification du responsable, instructions en français quand la
  sécurité l'exige.
- Sanction : retrait/rappel à vos frais, amendes DGCCRF, responsabilité civile et pénale en cas
  d'accident.

**Stratégie pragmatique du dossier :** se cantonner aux catégories listées dans
`DEMANDE_FRANCE.md` §3 (rangement, textile simple, accessoires mécaniques, basse tension USB)
où l'exposition réglementaire est faible, et exclure d'office jouets, puériculture, 230 V,
cosmétique, contact alimentaire. Le score de risque conformité du CSV
(`risque_conformite` 1-5) pénalise automatiquement ces produits dans le classement.

## 5. Récapitulatif des obligations dans l'ordre chronologique

1. Créer la micro-entreprise (avant la première vente, pas après).
2. Passer le compte Leboncoin en PRO avec le SIREN.
3. Vérifier le code TARIC + exigences CE du premier produit AVANT de payer le lot test.
4. Importer avec déclaration à valeur réelle, archiver factures et preuves.
5. Vendre avec les mentions pro (garantie 2 ans, rétractation 14 j sur les envois).
6. Déclarer le CA à l'URSSAF (mensuel ou trimestriel), tenir le registre des achats.
