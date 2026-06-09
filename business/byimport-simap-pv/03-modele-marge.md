# Agent 3 — Modèle de marge à deux étages

En Voie C, deux marges s'empilent sous un seul prix : celle de **ByImport** (sur
le module) et celle du **partenaire installateur** (sur l'ensemble clé en main).
Le tout doit rester **sous le prix marché suisse** pour gagner. Ta part se
comprime mécaniquement — il faut la piloter au chiffre.

## Le flux de valeur

```
Coût rendu ByImport (module, CHF/Wc)
        │  + marge ByImport (%)
        ▼
Prix de vente ByImport → installateur (CHF/Wc)     ← TON chiffre d'affaires
        │  l'installateur ajoute onduleurs, structure, câblage,
        │  main-d'œuvre, ingénierie, sa propre marge
        ▼
Prix de l'offre clé en main → État (CHF/Wc installé)  ← doit battre le marché
```

ByImport ne gagne que sur **le poste module**. Le levier compétitif : ton prix au
partenaire doit être **inférieur à ce qu'il paie aujourd'hui** à son distributeur.

## Les 3 chiffres qui décident tout

1. **Coût rendu ByImport** (CHF/Wc) = prix usine + transport + douane + TVA import récupérable + assurance, ramené au Wc.
2. **Prix module marché installateur** (CHF/Wc) = ce que ton partenaire paie aujourd'hui. C'est ton **étalon de compétitivité**.
3. **Ta marge** (%) = entre ton coût rendu et ton prix de vente au partenaire.

**Règle d'or :** `Prix vente ByImport < Prix module marché installateur`.
Si ce n'est pas vrai, tu n'as pas d'offre — peu importe ta marge cible.

## Le calculateur

`modele_marge.py` (stdlib uniquement) chiffre tout instantanément :

```bash
python3 modele_marge.py \
  --puissance-wc 200000 \
  --cout-rendu 0.13 \
  --marge-pct 20 \
  --prix-marche 0.25
```

Sorties : CA ByImport, marge brute (CHF + %), prix/Wc au partenaire, **économie
offerte à l'installateur** vs marché, et **verdict de compétitivité**.

Lance `python3 modele_marge.py --aide-hypotheses` pour le détail des hypothèses
et des ordres de grandeur 2025-2026 (prix modules effondrés, à reconfirmer).

## Hypothèses illustratives (à REMPLACER par tes vrais chiffres)

| Poste | Valeur illustrative | Source à confirmer |
|---|---|---|
| Coût rendu module ByImport | ~0,13 CHF/Wc | Tes devis fournisseurs + transitaire (douane/TVA) |
| Prix module marché installateur CH | ~0,20–0,30 CHF/Wc | Demander à 2-3 installateurs / distributeurs |
| Marge ByImport cible | 15–25 % | Ton arbitrage volume/compétitivité |
| Part module dans le clé en main | ~25–40 % | Varie selon taille et complexité du toit |

> Ces chiffres ne sont **pas** des prix garantis. Le marché du module PV est
> volatil ; reconfirme chaque trimestre auprès de tes fournisseurs et du transitaire.

## Critères de viabilité

- ✅ Prix vente ByImport **nettement** < prix marché installateur (marge de manœuvre pour que l'installateur gagne ET partage).
- ✅ Marge ByImport ≥ seuil qui couvre ton risque appro + immobilisation.
- ✅ Volume du marché assez grand pour que l'économie absolue (CHF) motive le partenaire.
- ❌ Si ton coût rendu ≥ prix marché → renégocie l'usine, change de fournisseur, ou passe ce marché.
