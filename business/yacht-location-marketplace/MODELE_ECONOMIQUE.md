# Modèle économique — comment la marge se fait vraiment

> Rappel du README : le courtage pur plafonne à ~15 %. Les 20–50 % demandés exigent un des 3 modèles ci-dessous. On les détaille, avec leurs risques.

## Vocabulaire

- **Tarif net (ou tarif propriétaire)** : ce que tu reverses au propriétaire du bateau. Négocié à l'avance.
- **Prix public** : ce que paie le client final.
- **Marge brute** : `(Prix public − Tarif net − coûts variables directs) / Prix public`.
- **Coûts variables directs** : carburant si inclus, commission de paiement (~1,5–3 %), skipper si externe, commission marketplace si tu passes par Click&Boat, etc.

## Modèle A — Achat-gros / revente-détail (le plus simple pour viser 30–50 %)

Tu négocies un **tarif net ferme** avec le propriétaire, tu fixes **librement** le prix public.

```
Exemple journée semi-rigide 8 pers. avec skipper, zone Méditerranée
  Prix public                         1 200 €
  − Tarif net propriétaire (avec skipper)  -800 €
  − Carburant (si à ta charge)            -90 €
  − Frais paiement (2 %)                  -24 €
  = Marge brute                          286 €  → 24 %
```

Pour monter à 35–50 %, deux leviers :
1. **Tarif net plus bas** via **exclusivité / volume** (le propriétaire accepte 650 € net contre la garantie de X jours/mois). Voir `OFFRE_ET_YACHTS.md`.
2. **Prix public plus haut** justifié par le **service** (réservation instantanée, conciergerie, skipper pro, photos pro). Le client ne compare pas un bateau, il compare une **expérience sans friction**.

- **Risque** : invendu = manque à gagner, **pas une perte sèche** (tu ne paies que si tu vends — sauf si tu signes des minima garantis). Le vrai risque est de **bloquer des créneaux** que tu ne remplis pas et d'agacer le propriétaire.

## Modèle B — Packaging d'expérience (la marge se fait sur les à-côtés)

Tu ne vends pas « un bateau à 1 000 € », tu vends « **Journée privée coucher de soleil, 10 pers., apéritif & photos incluses — 1 690 €** ».

```
  Bateau + skipper (net)              900 €  (marge ~15 % seulement ici)
  Apéritif / traiteur               +180 €  (coût 70 € → marge 110 €)
  Photographe 1h                    +250 €  (coût 120 € → marge 130 €)
  Transferts / champagne / déco     +120 €  (coût 40 € → marge 80 €)
  ----------------------------------------
  Prix public bundle               1 690 €
  Coût total                       1 130 €
  Marge brute bundle                 560 €  → 33 %
```

- La **coque** se marge mal (15 %), mais **apéro / photo / déco / transferts se margent 40–60 %**. Plus le panier d'extras est gros, plus la marge globale monte vers 40–50 %.
- **Bonus** : ces bundles sont **moins comparables** → tu sors de la guerre des prix des marketplaces.
- **Risque** : complexité opérationnelle (coordonner traiteur, photographe, skipper). Commence avec 1–2 extras, pas 6.

## Modèle C — Day-charter haute rotation (volume sur petites unités)

Petites unités (6–12 pers.), **demi-journées**, zone très touristique, **prix dynamique** (plus cher juillet-août, week-ends, coucher de soleil).

- Marge cible **25–40 %** via **mandats d'exclusivité locale** sur quelques bateaux que tu fais **tourner 2 créneaux/jour** en haute saison.
- L'enjeu = **taux de remplissage**. Un bateau à 35 % de marge mais rempli 15 jours/mois bat un bateau à 50 % rempli 4 jours/mois.
- **Risque** : usure du bateau, dépendance à la météo, gestion des annulations.

## Tableau de décision

| Critère | Modèle A (revente) | Modèle B (bundle) | Modèle C (rotation) |
|---|---|---|---|
| Marge atteignable | 25–45 % | 33–50 % | 25–40 % |
| Complexité opé | Faible | Élevée | Moyenne |
| Capital de départ | Faible | Moyen | Moyen |
| Dépendance saison | Forte | Forte | Très forte |
| Différenciation | Moyenne | **Forte** | Moyenne |
| Recommandé pour démarrer | ✅ Oui | Plus tard | Si forte demande day-charter |

➡️ **Recommandation : démarre en Modèle A**, ajoute 1–2 extras (glisse vers B) une fois que le tunnel tourne. Réserve C aux zones où `DEMANDE_MARCHE.md` montre une demande day-charter massive.

## Unit economics — la réservation moyenne (à recalibrer)

| Hypothèse | Valeur de départ |
|---|---|
| Panier moyen (prix public) | 1 200 € |
| Marge brute moyenne | 28 % → **336 €** |
| Coût d'acquisition (pub) par réservation (CAC) | 80–140 € |
| **Marge nette par réservation** | **~200–250 €** |
| Réservations nécessaires / mois pour 5 000 € de marge nette | **20–25** |

> Si ton CAC dépasse ta marge brute, tu paies pour vendre à perte. Surveille `CAC < 0,5 × marge brute` comme garde-fou (voir `BUDGET_KPIS.md`).

## Sources de revenu additionnelles (margées fort)

- **Extras** (apéro, photo, déco, paddle, jet) — 40–60 % de marge.
- **Assurance annulation / dépôt sans franchise** — commission 20–30 %.
- **Frais de service** affiché (3–8 % du panier) — assumé, transparent.
- **Vente de bateaux** (courtage classique 8–10 %) — peu de volume mais tickets élevés ; à activer une fois la marque crédible.
- **Affiliation** vers Click&Boat/SamBoat pour les demandes que tu ne peux pas servir — récupère une commission au lieu de perdre le lead.

## Le piège à éviter
**Ne jamais vendre un créneau que tu n'es pas sûr de pouvoir honorer.** Une double-réservation ou un bateau indisponible = remboursement + avis catastrophe + propriétaire qui te lâche. La marge ne vaut rien si l'opérationnel ne suit pas. Le calendrier de dispo **temps réel** (voir `SITE_WEB.md`) n'est pas un luxe, c'est vital.
