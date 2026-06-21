# Automation Stack — Workflows Make + Zapier

## Architecture globale

```
                    ┌─────────────────────────────────────────┐
                    │           SOURCES DE LEADS              │
                    │  Apollo → Clay → HubSpot                │
                    │  Meta Ads → Lead Form → HubSpot         │
                    │  Google Ads → Landing Page → HubSpot    │
                    │  Yacht Site → Réservation → HubSpot     │
                    └──────────────┬──────────────────────────┘
                                   │
                    ┌──────────────▼──────────────────────────┐
                    │         MAKE (CERVEAU CENTRAL)          │
                    │  • Routing par flux (A/B/C)             │
                    │  • Scoring automatique                  │
                    │  • Assignment aux séquences             │
                    │  • Alertes Slack temps réel             │
                    └──────────────┬──────────────────────────┘
                                   │
          ┌────────────────────────┼────────────────────────┐
          │                        │                        │
┌─────────▼────────┐   ┌──────────▼────────┐   ┌──────────▼────────┐
│  NURTURING AUTO  │   │  BOOKING AUTO     │   │  CLOSING AUTO     │
│  HubSpot email   │   │  Calendly RDV     │   │  DocuSign contrat │
│  sequences       │   │  + Slack alert    │   │  + Gmail confirm  │
└─────────┬────────┘   └──────────┬────────┘   └──────────┬────────┘
          │                        │                        │
          └────────────────────────┼────────────────────────┘
                                   │
                    ┌──────────────▼──────────────────────────┐
                    │         REPORTING QUOTIDIEN             │
                    │  Coupler.io → Google Sheets             │
                    │  Supermetrics → Ads performance         │
                    │  Slack #revenue → digest 9h + 18h       │
                    └─────────────────────────────────────────┘
```

---

## Workflow 1 : Apollo → HubSpot (déclencheur principal)

**Outil : Make**  
**Déclencheur :** Nouveau contact exporté depuis Apollo (webhook ou polling CSV)

```
[Apollo export CSV/webhook]
      ↓
[Make: Parse contact data]
      ↓
[Make: Check if email exists in HubSpot]
      ├── Oui → Update propriétés + log
      └── Non → Create contact HubSpot
                      ↓
              [Assign à séquence selon flux]
              ├── fiduciaire/patrimoine → Séquence A (Pilier)
              ├── agence/marketing → Séquence B (Managed Service)
              └── food/import → Séquence C (Olive oil)
                      ↓
              [Start HubSpot sequence automatiquement]
                      ↓
              [Slack: notify #outbound "Nouveau contact: [Prénom] [Société]"]
```

**Fréquence :** Immédiat (webhook) ou toutes les heures (polling)

---

## Workflow 2 : Lead Meta Ads → CRM → Alerte immédiate

**Outil : Make**  
**Déclencheur :** Nouveau lead sur Meta Ads Lead Form

```
[Meta Ads Lead Form submitted]
      ↓
[Make: Receive webhook]
      ↓
[Make: Create/update HubSpot contact]
      │   Properties: prénom, email, téléphone, flux=B2C_Pilier
      ↓
[Make: Send Calendly booking link via Gmail]
      │   Template: "Bonjour [Prénom], voici le lien pour notre appel de 15 min..."
      ↓
[Make: Create HubSpot deal "Lead Pilier - [Prénom]" au stade "Contacté"]
      ↓
[Make: Post Slack #leads "🔥 Nouveau lead Meta: [Prénom] | [Téléphone] | [Email]"]
      ↓
[Make: Créer tâche HubSpot "Appeler [Prénom] dans 5 minutes"]
```

**SLA critique :** Rappel sous 5 minutes en heures ouvrées → conversion +40%

---

## Workflow 3 : Réservation Yacht → Confirmation automatique

**Outil : Make**  
**Déclencheur :** Nouveau booking sur le site yacht

```
[Réservation confirmée (Stripe/paiement reçu)]
      ↓
[Make: Receive webhook]
      ↓
[Make: Create HubSpot deal "Yacht - [Date] - [Prénom]"]
      │   Montant : prix public
      │   Stade : "Gagné"
      ↓
[Make: Send Gmail confirmation client]
      │   Template: infos pratiques, lieu, heure, numéro skipper
      ↓
[Make: Send Gmail notification propriétaire bateau]
      │   Template: "Réservation confirmée pour le [Date], client: [Prénom]"
      ↓
[Make: Update Google Calendar propriétaire]
      ↓
[Make: Slack #revenue "⛵ Réservation yacht: [Prénom] | [Date] | [Montant]€"]
      ↓
[Make: Si 7 jours avant → Email rappel automatique client]
      ↓
[Make: Si 48h avant → SMS client (via Twilio ou autre)]
```

---

## Workflow 4 : Deal fermé → Actions post-closing

**Outil : Make**  
**Déclencheur :** Deal HubSpot passe au stade "Gagné"

```
[HubSpot Deal: Stade = "Gagné"]
      ↓
[Make: Receive webhook HubSpot]
      ↓
[Make: DocuSign → Créer enveloppe contrat depuis template]
      │   Préremplir: nom client, montant, durée
      ↓
[Make: Send DocuSign à l'email client]
      ↓
[Make: Gmail → Email de bienvenue + prochaines étapes]
      ↓
[Make: HubSpot → Créer ticket onboarding "Onboarding [Prénom]"]
      ↓
[Make: Slack #revenue "🎉 DEAL FERMÉ: [Prénom] | [Montant]€ | [Flux]"]
      ↓
[Make: Mettre à jour spreadsheet Google "Revenue Tracker"]
      │   Colonnes: Date, Client, Flux, Montant, Cumul
      ↓
[Make: Si cumul > 100k€ → Notification spéciale Slack 🏆]
```

---

## Workflow 5 : Daily Revenue Digest

**Outil : Make**  
**Déclencheur :** Schedule 9h00 et 18h00 chaque jour

```
[Make: Schedule 9h00 + 18h00]
      ↓
[Make: Query HubSpot → Deals fermés aujourd'hui]
      ↓
[Make: Query HubSpot → Deals fermés cette semaine]
      ↓
[Make: Query HubSpot → Pipeline total (deals ouverts)]
      ↓
[Make: Coupler.io → Revenus pub Meta + Google du jour]
      ↓
[Make: Construire message Slack]
      │   📊 DIGEST [DATE] [9h/18h]
      │   ✅ Revenus aujourd'hui: X€
      │   📈 Revenus semaine: X€
      │   🎯 Objectif mois: 1,000,000€
      │   🔢 Restant: X€
      │   📅 Jours restants: X
      │   💰 Pipeline ouvert: X€
      │   ---
      │   🔥 Leads chauds: X
      │   📞 RDV aujourd'hui: X
      │   ✉️ Emails envoyés: X
      ↓
[Make: Post Slack #revenue]
```

---

## Workflow 6 : Relance automatique leads froids

**Outil : Make + HubSpot**  
**Déclencheur :** Lead HubSpot sans activité depuis 3 jours et stade "Contacté"

```
[HubSpot: Lead inactif 3j + stade "Contacté"]
      ↓
[Make: Trigger workflow]
      ↓
[Make: Check nombre de relances déjà envoyées]
      ├── < 3 relances → Envoyer prochain email de séquence
      └── ≥ 3 relances → Marquer "Froid" + créer tâche appel manuel
              ↓
      [Make: Slack #outbound "⚠️ Lead froid à appeler manuellement: [Prénom]"]
```

---

## Setup prioritaire (Semaine 1 uniquement)

**Ordre d'implémentation :**

1. **Make compte + connexions** (30 min) : HubSpot, Gmail, Slack, Calendly, Meta Ads, DocuSign
2. **Workflow 2** (Meta Lead → Alerte immédiate) — Impact le plus rapide
3. **Workflow 5** (Daily Digest) — Visibilité immédiate sur les chiffres
4. **Workflow 1** (Apollo → HubSpot) — Outbound en place
5. **Workflow 3** (Yacht booking) — Réservations été
6. **Workflow 4** (Deal fermé) — Post-closing automatisé
7. **Workflow 6** (Relance froids) — Récupère les leads perdus

---

## Credentials à préparer

| Outil | Action requise |
|-------|----------------|
| Apollo | API key dans compte + export webhook activé |
| HubSpot | Access token (private app) avec scopes: contacts, deals, tasks |
| Make | Compte créé, connexions autorisées |
| Calendly | OAuth app + webhook "invitee.created" |
| DocuSign | Developer account → template contrat type |
| Meta Ads | Lead Ads → CRM Integration → Make webhook |
| Google Ads | Connecter compte → NotFair MCP |
| Slack | Workspace channel #revenue + #leads + #outbound |
| Coupler.io | Connexion HubSpot + Meta Ads + Google Ads → Google Sheets |
