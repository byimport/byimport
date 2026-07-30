# 00 — Démarrage débutant (commence ICI)

> Tu débutes, aucune vente encore, pas de partenaire, pas de société suisse.
> C'est normal. Voici l'ordre exact des premiers pas. **Ne dépense rien** tant
> que les phases 0 et 1 ne sont pas validées.

## La règle d'or du débutant

> Ton premier objectif n'est **pas une vente**. C'est **une conversation avec un
> installateur PV suisse intéressé**. Tant que tu n'as pas ça, tu n'investis ni
> dans une société suisse, ni dans du stock, ni dans quoi que ce soit.

## Phase 0 — Reconnaissance (cette semaine · 100 % gratuit)

1. **Crée ton compte simap** (gratuit) et charge les alertes CPV solaire
   → voir `01-veille-simap.md`.
2. **Observe le marché** : lis 5 à 10 avis PV récents + leurs **avis
   d'adjudication**. Objectif : comprendre comment c'est formulé, quelles
   puissances, quels prix, et **qui gagne**.
3. **Dresse une liste de 10 installateurs cibles** (les adjudicataires récurrents)
   → méthode dans `02-recherche-partenaire.md`.

✅ Fin de phase 0 : tu as un compte, des alertes actives, et une liste de 10 noms.

## Phase 1 — Validation des chiffres (semaines 2-4 · gratuit/faible coût)

4. **Obtiens ton coût rendu réel** : demande à tes fournisseurs un **prix module
   CHF/Wc rendu en Suisse** (devis écrit, incluant transport/douane).
5. **Obtiens l'étalon marché** : demande à 2-3 installateurs (ou distributeurs)
   ce qu'ils paient aujourd'hui le module au Wc.
6. **Fais tourner le calculateur** avec tes vrais chiffres :
   ```bash
   python3 modele_marge.py --puissance-wc 200000 --cout-rendu <TON_COUT> \
       --marge-pct 20 --prix-marche <PRIX_MARCHE>
   ```
   → S'il dit **❌ NON COMPÉTITIF**, inutile de prospecter : renégocie l'usine ou
   change de fournisseur d'abord. S'il dit **✅ COMPÉTITIF**, tu as une vraie offre.

✅ Fin de phase 1 : tu **sais** si ton prix bat le marché. C'est le go/no-go.

## Phase 2 — Premier contact partenaire (mois 1-2)

7. **Envoie l'email type** à 5-10 installateurs de ta liste
   (`02-recherche-partenaire.md`).
8. **Décroche une conversation**, compare tes prix aux leurs sur une référence.
9. **Sécurise un accord d'approvisionnement** (clauses : exclusivité,
   anti-contournement, garantie — voir `02`).

✅ Fin de phase 2 : un installateur dit « OK, envoie-moi tes prix sur le prochain
marché ». **C'est ta vraie première victoire.**

## Phase 3 — Premier marché réel (quand un avis adapté tombe)

10. Une alerte simap matche → tu m'envoies l'avis (lien ou PDF).
11. On déroule le cycle 4 agents en réel : fiche marché → sourcing → marge →
    offre + annexe technique pour ton partenaire.

## Phase 4 — Structurer (seulement après 1-2 marchés gagnés)

12. Évaluer la bascule en **filiale suisse (Voie A)** + **TVA CH**, pour capter
    les références à ton nom. Avec une fiduciaire/avocat suisse.

---

## Attentes réalistes (sois patient)

- Les marchés publics sont un **cycle lent** : des semaines entre la publication
  d'un avis et l'adjudication.
- Une **première vente** réaliste se compte en **plusieurs mois**, pas en jours.
  C'est le rythme normal de ce business — ce n'est pas un échec.
- Le travail des premières semaines (veille + chiffres + contacts) ne rapporte
  rien immédiatement mais **construit la machine**. C'est l'investissement qui
  paie ensuite.

## Ce que tu ne fais PAS encore

- ❌ Créer une société suisse (tant qu'aucun partenaire n'est intéressé).
- ❌ Acheter du stock (tant qu'aucun marché n'est gagné).
- ❌ Viser les voitures (terrain trop dur pour débuter — voir `01`).
- ❌ Viser les gros marchés ouverts (aptitude trop lourde pour l'instant).
