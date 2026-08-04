# Placement de freelances FR/UE chez clients suisses — dossier commercial

> ⚠️ **Note** : ce dossier contient des documents business sans rapport avec le plugin Toprank. Conservé en branche, ne touche ni `VERSION` ni `CHANGELOG.md`. Peut être exporté (PDF, Drive) sans impact sur le plugin.
>
> ⚠️ **Ce repo est public.** Ne commite ici aucun nom de client, nom de freelance, TJM nominatif signé, marge réelle par compte, ni clé d'API. Les fourchettes présentes sont des repères de marché, pas tes chiffres.

## Modèle

Sourcer des freelances tech en France / UE, les placer chez des PME et scale-ups suisses (Genève, Lausanne, Vaud, Zurich) à **20–25 % sous le prix d'une ESN genevoise**, en marge brute de 38–42 %.

L'arbitrage est réel mais il n'est pas gratuit : il est contraint par le droit suisse de la location de services, et il consomme de la trésorerie. Les deux points sont traités dans `GRILLE_TARIFAIRE.md`, sections 6 et 4 — **à lire avant de signer quoi que ce soit.**

## 📂 Contenu

| Fichier | Usage |
|---|---|
| `GRILLE_TARIFAIRE.md` | Grille achat / vente / marge par profil, règles de négociation, structure de coûts, besoin en trésorerie, contrainte LSE, procédure de recalibration. |
| `scripts/grille.json` | Source de vérité des prix. Le tableau markdown est généré depuis ce fichier. |
| `scripts/chiffrage.py` | Calculateur de mission : coût, marge, verdict vs plancher, trésorerie à avancer. |

## 🚀 Démarrage

```bash
cd business/freelances-suisse

# Voir la grille
python3 scripts/chiffrage.py --liste

# Chiffrer une mission au prix catalogue
python3 scripts/chiffrage.py --profil fullstack-confirme --jours 60

# Le client négocie
python3 scripts/chiffrage.py --profil fullstack-confirme --vente 950 --jours 60

# Sortie JSON (pour brancher dans n8n)
python3 scripts/chiffrage.py --profil devops --vente 1150 --jours 90 --json
```

Python 3.8+, stdlib uniquement, aucune dépendance.

## Les trois nombres à retenir

| | |
|---|---|
| **38 %** | Marge brute cible. En-dessous, tu justifies. |
| **28 %** | Plancher absolu. En-dessous, tu refuses. |
| **~13 000 CHF** | Trésorerie immobilisée par mission active (décalage de paiement de 30 jours). Multiplie par ton nombre de missions simultanées — c'est ce chiffre-là qui plafonne ta croissance, pas la demande. |

## À faire avant la première mission

- [ ] Faire valider le montage contractuel par un avocat suisse (section 6 — l'interdiction de la location de services transfrontalière n'est pas contournable).
- [ ] Faire rédiger les deux contrats-cadres (client / freelance) avec clause de non-sollicitation symétrique.
- [ ] Souscrire une RC professionnelle.
- [ ] Confirmer le traitement TVA (autoliquidation côté suisse) avec ton comptable.
- [ ] Recalibrer `scripts/grille.json` après les trois premiers deals réels.
