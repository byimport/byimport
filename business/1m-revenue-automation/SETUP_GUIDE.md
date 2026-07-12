# Guide d'implémentation — Ce que tu dois faire toi-même

> Les outils automatisés (Apollo, HubSpot, Make) nécessitent des confirmations ou des upgrades.
> Ce guide liste ce qui est bloqué et comment le débloquer.

---

## ACTIONS IMMÉDIATES (aujourd'hui, avant 17h)

### 1. Apollo — Upgrade plan requis
**Bloqué :** Apollo plan gratuit ne permet pas la recherche de prospects dans la base mondiale.  
**Solution :** Upgrade vers Basic (~49$/mois) sur https://app.apollo.io/settings/plans  
**Débloque :** Recherche de 1000+ boulangeries, PMEs, cabinets médicaux en France pour By Solar

### 2. HubSpot — Créer 6 tâches urgentes By Solar
**Confirmer dans HubSpot pour créer les tâches de suivi pour les 6 prospects :**

Pour chaque contact, créer une tâche "Appel préparation RDV solaire" due aujourd'hui.
Contacts HubSpot IDs :
- Dr Jean Fournier : 769700664541
- Pierre Martin : 769711670501  
- Sophie Bernard : 769780577490
- Marie Dubois : 769733271740
- Laurent Petit : 769684489425
- Isabelle Moreau : 769740450025

**Email à envoyer à chacun (copier-coller) :**
```
Objet : Votre rendez-vous solaire — je prépare votre simulation de ROI

Bonjour [Prénom],

Je prépare votre simulation personnalisée.
Pour vous arriver avec des chiffres précis, j'ai besoin de :

1. Votre surface de toit approximative (en m²)
2. Votre facture électrique mensuelle moyenne
3. Vos horaires d'ouverture (7j/7 ? 5j/7 ?)

Ces 3 infos me permettent de calculer exactement vos économies annuelles
et votre retour sur investissement.

[CALENDLY_LINK]

À bientôt,
```

### 3. Make — Créer compte et 3 workflows
**URL :** https://www.make.com

**Workflow 1 (prioritaire) :** Meta Lead → Slack Alert
- Connecter : Meta Ads + Slack + HubSpot
- Déclencheur : Nouveau lead depuis lead form Meta
- Action : Créer contact HubSpot + Alerter Slack + Envoyer email de booking Calendly

**Workflow 2 :** HubSpot Deal Fermé → Actions post-closing
- Déclencheur : Deal stade = "Closed Won"
- Actions : Créer note HubSpot + Alert Slack + Email de bienvenue

**Workflow 3 :** Daily Digest
- Déclencheur : 18h00 chaque jour
- Actions : Pull données HubSpot → Post Slack avec revenus du jour

### 4. Apollo — Créer 3 séquences (faire depuis l'interface)
**URL :** https://app.apollo.io/sequences

**Séquence A : "By Solar — Relance prospects chauds"**
- Étape 1 (J0) : Email préparation RDV (voir APOLLO_SEQUENCES.md)
- Étape 2 (J3) : Email simulation ROI chiffré
- Étape 3 (J7) : Email last call + offre démo gratuite

**Séquence B : "Pilier Genève — Partenaires fiduciaires"**
- Étape 1 (J0) : Introduction partenariat
- Étape 2 (J4) : Cas concret (45k CHF récupérés)
- Étape 3 (J8) : Last call

**Séquence C : "Agences digitales — Managed Service"**
- Étape 1 (J0) : Question directe SEO/Ads
- Étape 2 (J4) : Exemple résultat concret
- Étape 3 (J8) : Dernière tentative

### 5. Pub Meta Ads — Lancer campagnes (budget requis)
**Nécessite :** Budget pub minimum 2,000€/semaine  
**À lancer dans :** https://business.facebook.com/adsmanager

Campagnes à créer (détails dans ADS_STRATEGY.md) :
1. "By Solar PME France" — conversion leads, audience artisans/gérants PME
2. "Leads Pilier Genève" — lead gen, audience 35-55 ans zone GE/Lausanne
3. "Yacht Été 2026" — trafic réservation, audience touristes Med

### 6. Calendly — Créer lien de booking
**URL :** https://calendly.com  
**Créer :** Event type "Simulation gratuite 20 min — Installation solaire"  
**Inclure dans :** Tous les emails By Solar

---

## OUTILS CONFIGURÉS (disponibles maintenant)

| Outil | État | Ce qui est possible |
|-------|------|---------------------|
| HubSpot | ✅ Connecté | Créer tâches, notes, deals, contacts |
| Apollo | ⚠️ Plan gratuit | Chercher dans ses propres contacts seulement |
| Meta Ads | 🔧 À connecter | Lancer campagnes si budget dispo |
| Google Ads | 🔧 À connecter | Lancer campagnes si budget dispo |
| Make | 🔧 À créer | Workflows d'automatisation |
| DocuSign | 🔧 À créer | Contrats automatisés |
| Calendly | 🔧 À créer | Booking RDV |

---

## TABLEAU DE BORD QUOTIDIEN

Bookmarker ces URLs :
- HubSpot pipeline : https://app.hubspot.com/contacts/148301705/deals
- HubSpot contacts : https://app.hubspot.com/contacts/148301705/contacts
- Apollo séquences : https://app.apollo.io/sequences
- Make workflows : https://www.make.com

---

## Estimation revenus si tu exécutes tout aujourd'hui

| Action | Revenus potentiels | Délai |
|--------|-------------------|-------|
| Envoyer les 6 emails By Solar | Pipeline 97k€ → probabilité +20% | Aujourd'hui |
| Fermer 2 deals By Solar (calls cette semaine) | 30–40k€ | J3–J7 |
| Lancer séquences Apollo (après upgrade) | 5–15 new leads By Solar | J7–J14 |
| Lancer Meta Ads pilier (si budget) | 20–50 leads | J3–J14 |
| Fermer 5/6 deals By Solar | 80–97k€ | J14–J21 |
| 10 nouveaux deals By Solar (pipeline mois 1) | 160k€ | J30 |
| **Total réaliste mois 1** | **~250k€** | J30 |
