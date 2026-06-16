# Connecteurs d'automatisation — état des lieux vérifié (juin 2026)

Recherche effectuée en direct sur les catalogues Zapier (9 000+ apps), IFTTT et Make.
Verdict d'ensemble : **tout le pipeline est connectable sauf les deux extrémités**
(achat 1688 et publication Leboncoin), qui n'ont de connecteur nulle part — et c'est
structurel, pas un oubli (pas d'API publique côté Leboncoin particulier, plateforme
domestique chinoise côté 1688).

## Ce qui existe, étape par étape

| Étape du pipeline | Connecteur vérifié | Plateforme | Usage |
|---|---|---|---|
| Tableur central (shortlist, stock, ventes) | **Google Sheets** | Zapier (34 actions), IFTTT (17), Make | Remplace le CSV local : une feuille `candidats`, une feuille `stock_ventes` |
| Génération des annonces | **Anthropic (Claude)** | Zapier (6 actions), Make (`anthropic-claude`) | Nouvelle ligne dans la feuille candidats → annonce générée (titre + corps via le gabarit d'AUTOMATISATION.md §2.4) → écrite dans la colonne `annonce` |
| Veille prix Alibaba/Amazon | **ScrapingBee / Oxylabs / Airtop** | Make | Scraping managé de pages produits (Amazon direct chez Oxylabs/ScrapingBee) pour surveiller les prix de marché et détecter les hausses/baisses |
| Alertes (repricing, annonce > 10 j, réassort) | **Telegram / Gmail / e-mail** | Zapier, IFTTT, Make | Règle de suivi d'AUTOMATISATION.md §2.5 : cellule mise à jour → notification |
| Planification | Scheduler natif | Make / Zapier / IFTTT (+ cron local) | Déclenchement hebdo du scoring et des vérifications |
| Multi-canal plus tard | **Etsy, Facebook Catalogs, Shopify, PrestaShop** | Make, Zapier | Quand le volume justifie un 2e canal en plus de Leboncoin PRO |

## Ce qui N'existe PAS (vérifié, pas supposé)

- **Leboncoin** : zéro résultat sur Zapier, IFTTT et Make. Aucune API publique pour
  particuliers. La seule intégration officielle reste **Leboncoin PRO + import de
  catalogue / agrégateurs partenaires** (cf. AUTOMATISATION.md §1). Tout connecteur ou
  bot "Leboncoin" non officiel = scraping déguisé = bannissement.
- **Google Trends** : aucun connecteur Zapier/IFTTT (pas d'API officielle Google).
  Solution : script local `pytrends` en cron, qui écrit dans la Google Sheet.
- **1688 / agents d'achat (CSSBuy, Superbuy…)** : pas d'API publique, pas de connecteur.
  L'achat reste manuel — et c'est voulu (contrôle qualité, SOURCING_1688.md §3).

## Architecture recommandée (sobre, 0-20 €/mois)

```
                       ┌──────────────────────────────┐
  cron local (hebdo)   │       GOOGLE SHEETS          │   Zapier/Make
  pytrends + scripts ─→│  candidats | stock_ventes    │←─ Claude : génère l'annonce
  score_produits.py    │  (le hub unique du système)  │   à chaque nouveau candidat GO
                       └──────────────┬───────────────┘
                                      │ cellule modifiée / seuil franchi
                                      ▼
                       Telegram : "annonce X sans contact depuis 10 j → -10 %"
                                      │
                                      ▼
                       PUBLICATION : manuelle assistée (copier-coller)
                       puis import catalogue Leboncoin PRO à ≥ 15 références
```

Mise en place dans l'ordre :
1. Migrer `scripts/produits_candidats.csv` vers une Google Sheet (le script lit un export
   CSV de la feuille — rien à changer au code).
2. Zap n°1 : nouvelle ligne `verdict=GO` → Claude rédige l'annonce → colonne `annonce`.
3. Zap n°2 : date de mise en ligne > 10 jours ET contacts = 0 → alerte Telegram repricing.
4. Cron local hebdo : `score_produits.py` sur l'export de la feuille + pytrends.
5. (Plus tard) Make + ScrapingBee pour surveiller les prix Amazon des références actives.

## Ce qu'on refuse de brancher

Un "connecteur" qui publierait automatiquement sur Leboncoin côté particulier
(Selenium, extensions navigateur, services tiers non agréés). Détection DataDome,
bannissement du compte et du SIREN associé — le coût d'un ban dépasse des années
d'économie de copier-coller. La publication s'automatise par la voie PRO, pas autrement.
