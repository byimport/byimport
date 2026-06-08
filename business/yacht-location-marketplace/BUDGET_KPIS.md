# Budget & KPIs

> Chiffres **illustratifs**, à recalibrer avec ta zone réelle (`DEMANDE_MARCHE.md`) et ton modèle de marge (`MODELE_ECONOMIQUE.md`). Hypothèse : 1 zone (Méditerranée), Modèle A (revente, marge brute ~28 %), lancement hors-saison pour être prêt avant le pic.

## Hypothèses économiques de base

| Hypothèse | Valeur de départ |
|---|---|
| Panier moyen (prix public) | 1 200 € |
| Marge brute moyenne | 28 % → **336 €** |
| CAC (coût pub par réservation) | 80–140 € |
| **Marge nette par réservation** | **~200–250 €** |
| Taux de conversion visiteur → réservation | 1,5–3 % |
| Acompte exigé | 30 % |

→ **Garde-fou** : `CAC < 0,5 × marge brute` (ici CAC < ~168 €). Au-delà, tu vends à perte.

## Budget de lancement — 90 jours

### Phase 0–1 (J0–J30) — Demande, offre, mise en place

| Poste | Coût | Notes |
|-------|------|-------|
| Avocat maritime (mandat-type + statut) | 1 500–2 500 € | One-shot, indispensable (`CADRE_LEGAL.md`) |
| Comptable (TVA, structure) | 500–1 000 € | One-shot |
| Étude de demande (outils SEO) | 0–200 € | Keyword Planner gratuit ; Ahrefs si budget |
| Site (no-code/WordPress + booking + paiement) | 0–2 000 € | DIY = quasi 0 ; sous-traité = 2 000 € |
| Production contenu (15 vidéos carrées Canva) | 0–800 € | Canva Pro + éventuel tournage/drone |
| Photos pro bateaux | 0–600 € | Souvent fournies par propriétaires |
| PSP / outils (Stripe/Mangopay, hébergement) | ~50 €/mois | |
| **Smoke test pub** (valider la zone) | 300 € | Avant d'investir plus |
| **Total Phase 0–1** | **~3 000–8 000 €** | Selon DIY vs sous-traitance |

### Phase 2 (J31–J60) — Lancement test

| Poste | Coût |
|-------|------|
| Google Ads — média | 2 000 € |
| Meta/TikTok — média | 1 200 € |
| Outils (CRM léger, tracking, hébergement) | 150 € |
| Production contenu continue | 300 € |
| **Total Phase 2** | **~3 650 €** |

**Réservations attendues M2** : 12–22 → **CA 14 000–26 000 € → marge brute 4 000–7 300 €.**

### Phase 3 (J61–J90) — Optimisation / scale

| Poste | Coût |
|-------|------|
| Google Ads | 3 000 € |
| Meta/TikTok | 2 000 € |
| SEO (contenu + tech) | 800 € |
| Partenariats (relationnel) | 300 € |
| Outils | 150 € |
| **Total Phase 3** | **~6 250 €** |

**Réservations attendues M3** : 20–35 → **CA 24 000–42 000 € → marge brute 6 700–11 800 €.**

### Récap 90 jours

| Métrique | Cumul |
|----------|-------|
| Budget total | ~13 000–18 000 € |
| Réservations | 35–60 |
| CA généré | 42 000–72 000 € |
| Marge brute générée | 12 000–20 000 € |
| **Seuil de rentabilité (budget pub couvert)** | dès M2 si CAC tenu |

> ⚠️ Ces chiffres supposent un lancement **en montée de saison**. Lancé en plein hiver méditerranéen, le même budget rapporte beaucoup moins — d'où l'importance de la saisonnalité (`DEMANDE_MARCHE.md`).

## KPIs à suivre — par fréquence

### Quotidien (dashboard)
- Dépense pub & CAC par campagne
- Réservations & valeur du jour
- Taux de réponse aux demandes WhatsApp/devis (< 1h)
- Taux de remplissage des bateaux (créneaux vendus / dispo)

### Hebdomadaire (revue 30 min)
- CAC hebdo par canal (alerte si > cible × 1,5)
- Taux de conversion tunnel (visiteur → acompte payé)
- Abandons de tunnel (à quelle étape)
- Hook rate / rétention des créatifs vidéo

### Mensuel (revue 2 h)
- CA, marge brute, marge nette
- ROAS par canal
- Taux de remplissage par bateau (couper les bateaux jamais réservés)
- Note moyenne avis & incidents opérationnels
- Mots-clés/créatifs gagnants vs perdants (réallouer)
- Mise à jour demande (`DEMANDE_MARCHE.md`)

## P&L mensuel — régime de croisière, haute saison (illustratif)

```
REVENUS
  35 réservations × 1 200 €                 42 000 €  (CA encaissé, dont reversement proprio)
  Extras (apéro, photo, déco)                3 500 €
  ----------------------------------------------------
MARGE BRUTE (≈28 % sur coque + extras margés) 13 800 €

COÛTS ACQUISITION
  Google Ads                                  3 000 €
  Meta/TikTok                                 2 000 €
  SEO + contenu                                 800 €
  Commissions partenaires                       600 €
  Outils (PSP, hébergement, CRM)                300 €
  TOTAL CAC                                    6 700 €
  → CAC / réservation : ~190 €

MARGE APRÈS ACQUISITION                        7 100 €

COÛTS FIXES
  Toi / opérations                          variable
  Assurances RC pro, compta                     500 €
  Divers                                        300 €
  ----------------------------------------------------
RÉSULTAT NET (avant rémunération)            ~6 300 €
```

→ En **basse saison**, ce P&L peut passer en négatif : réduis le média, vis sur la trésorerie accumulée l'été, pousse la vente/l'événementiel. **Budgète l'année, pas le mois.**

## Seuils d'alerte

| Métrique | Seuil rouge | Action |
|----------|-------------|--------|
| CAC > 50 % de la marge brute sur 14 j | Critique | Couper mots-clés/créatifs déficitaires, revoir LP |
| Taux conversion tunnel < 1 % | Critique | Diagnostic tunnel (dispo ? acompte ? mobile ?) |
| Taux de remplissage < 20 % sur un bateau | Élevé | Repricer ou retirer le bateau |
| 1 avis < 3★ ou incident sécurité | Très critique | Stop sur ce bateau/skipper, enquête |
| Trésorerie < 2 mois de charges | Critique | Réduire média, activer cash (acomptes, ventes) |

## Quand reconsidérer toute la stratégie
- **Fin de 1ʳᵉ saison, marge nette négative malgré du volume** → problème de **marge** (tarif net trop élevé) ou de **CAC** (mauvais canal/zone). Renégocie les tarifs nets ou change de modèle (B/C).
- **CAC > marge brute de façon persistante** → la zone est trop concurrentielle en pub. Bascule le poids vers SEO/partenariats/organique, ou change de zone.
- **Dépendance totale à juillet-août** → construis du contre-saisonnier (vente de bateaux, événementiel, 2e hémisphère) ou accepte un modèle 100 % saisonnier assumé.
