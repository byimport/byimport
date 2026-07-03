# Location à la couchette (cabin charter) — tous les ports d'Europe

> ⚠️ Document business hors périmètre plugin. Module exécutable associé : `cabin-charter/`.

## L'idée : diviser le bateau par couchette pour augmenter le chiffre d'affaires

Au lieu de louer le bateau entier à un seul client, on vend **chaque couchette
individuellement**, avec un sur-prix unitaire. Le même bateau rapporte 25–35 % de
plus quand il part complet, et surtout il part **plus souvent** : le marché des
solos / couples sans groupe est massif et mal servi (c'est le modèle des
croisières-cabine, éprouvé en Grèce et en Croatie).

### La math (moteur : `cabin-charter/pricing.py`)

Exemple réel du moteur — voilier 8 couchettes, tarif net propriétaire 850 €/jour :

| Étape | Formule | Valeur |
|---|---|---|
| Prix public bateau entier | net × (1 + marge 25 %) | **1 060 €/jour** |
| Prix d'une couchette | (entier ÷ 8) × uplift 1,30 | **175 €/pers/jour** |
| CA si complet | 175 × 8 | **1 400 €/jour → +32 % vs entier** |
| Seuil de rentabilité | couvre le net 850 € | **5 couchettes** |
| Seuil de départ | max(rentabilité, 50 % remplissage) | **5 couchettes** |

Règles de calibration encodées dans le moteur :

- **Uplift ≤ 1,4** : au-delà, un groupe de 8 compare avec la location entière et
  l'écart se voit. 1,25–1,35 est la zone sûre.
- **Seuil de départ obligatoire** : en dessous, on rembourse ou on reporte —
  jamais de sortie à perte. Le seuil couvre toujours au minimum le tarif net dû
  au propriétaire.
- **Double affichage** : on publie les DEUX prix (couchette + bateau entier). Le
  client groupe prend l'entier, le client solo prend la couchette — deux
  segments, un seul bateau.

## « Tous les ports d'Europe » : couverture digitale ≠ couverture opérationnelle

Être honnête là-dessus, sinon le plan échoue :

- **Digital (fait)** : `cabin-charter/data/ports_europe.json` couvre **49 grands
  ports** de plaisance (Côte d'Azur, Baléares, Corse, Sardaigne, Sicile, Adriatique,
  Grèce, Atlantique, Canaries, Baltique — extensible en ajoutant une entrée). Le
  générateur produit une page par port : localisation exacte du bateau (carte),
  tarifs à la couchette et bateau entier, seuils de départ.
- **Anti-doorway** : un port **sans bateau sous mandat n'a pas de page** — il
  apparaît dans l'annuaire en « ouverture prochaine ». Publier 49 pages dont 37
  vides ferait classer le site comme spam par Google et tromperait le client.
  La couverture s'étend automatiquement à mesure que des mandats sont signés.
- **Opérationnel (à faire)** : chaque port actif exige des mandats à tarif net,
  un skipper fiable et une capacité de réponse locale. On active port par port —
  la version allégée été 2026 du plan maître (1 port, 3–5 mandats) reste la
  première étape ; ce module rend chaque nouveau port marginal quasi gratuit.

## Garde-fous légaux et opérationnels — à lire avant de vendre une couchette

1. **Vendre à la place ≠ louer un bateau.** Embarquer des passagers individuels
   payants relève du **transport de passagers** (armement/pavillon, brevet du
   skipper, nombre de passagers autorisé) et, combiné à d'autres prestations, de
   la **directive (UE) 2015/2302 voyages à forfait** (garantie insolvabilité,
   responsabilité de plein droit). Le mandat de courtage de `CADRE_LEGAL.md` ne
   couvre PAS ce cas — valider le montage par pays avant la première vente.
2. **Assurance** : la RC plaisance standard du propriétaire exclut souvent
   l'exploitation commerciale à la place. Exiger une extension charter/passagers.
3. **Cohabitation d'inconnus à bord** : cabines vendues par groupe de 2, jamais
   de couchette partagée entre inconnus dans la même cabine ; règles de bord
   écrites ; le skipper a autorité de débarquement.
4. **Remplissage** : le risque du modèle est un départ à 3 couchettes vendues.
   D'où le seuil de départ encodé + politique claire annoncée à la réservation
   (report ou remboursement intégral si seuil non atteint à J-7).

## Quickstart

```bash
cd cabin-charter
python3 -m unittest discover -s tests -p 'test_*.py'   # 7 tests
python3 generate.py --out ./dist                        # 49 ports, pages + sitemap
```

Remplacer `data/flotte_fixture.json` par les bateaux réellement sous mandat
(mêmes champs, `tarif_net_jour_eur` = tarif net signé) — le site se régénère.
