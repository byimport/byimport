# Vente de sites web aux entreprises sans présence en ligne — France, Suisse, Europe

> ⚠️ **Note** : Ce dossier contient des documents business sans rapport avec le plugin Toprank. Conservé en branche, ne touche ni `VERSION` ni `CHANGELOG.md`. Peut être exporté (PDF, Drive) sans impact sur le plugin.

## L'idée de départ, et pourquoi elle doit être recadrée

**Demande initiale :** trouver toutes les sociétés sans site web en France, en Suisse et en Europe, créer un site pour chacune, adapter le prix à leur chiffre d'affaires, et leur envoyer des emails en masse en créant l'urgence.

**Trois problèmes à corriger avant de lancer quoi que ce soit :**

1. **L'envoi en masse non sollicité est illégal dans la plupart des pays visés.** La Suisse (LCD art. 3 al. 1 let. o) et l'Allemagne (UWG §7) exigent un consentement préalable (opt-in) même en B2B. La France tolère l'opt-out B2B mais sous conditions strictes. Envoyer le même email à des milliers d'adresses fait blacklister le domaine expéditeur en quelques jours (Gmail/Outlook coupent à ~0,3 % de plaintes spam) et expose à des amendes. → Voir `CADRE_LEGAL.md` — **à lire avant tout envoi**.

2. **La fausse urgence est une pratique commerciale trompeuse** (directive 2005/29/CE, transposée partout en Europe) et elle détruit la confiance au premier appel. L'urgence honnête — capacité de production réellement limitée, démo réellement mise hors ligne à date fixe — convertit mieux et ne crée pas de risque. → Voir `EMAILS.md`.

3. **"Toutes les sociétés sans site web en Europe" n'est pas une base de données qui existe.** Elle se construit niche par niche, ville par ville. C'est un avantage : le business ne se gagne pas au volume mais au ciblage. 50 prospects hyper-qualifiés dans une niche avec un email réellement personnalisé battent 5 000 envois génériques — en taux de réponse ET en risque légal.

## Le modèle recadré (celui qui marche)

**Offre :** création de site vitrine pour TPE/PME locales sans présence web, avec **démo personnalisée construite AVANT le premier contact** — le prospect voit son propre site, pas une promesse.

**Mécanique de vente :**
1. Choisir UNE niche × UNE zone (ex. : artisans du bâtiment en Haute-Savoie, restaurants à Lausanne).
2. Constituer une liste de 30–50 entreprises vérifiées sans site (`PROSPECTION.md`).
3. Construire une maquette de démo par prospect à partir d'un template de niche (2–3 h/site une fois le template fait).
4. Contact individuel conforme au droit local, lien vers SA démo (`EMAILS.md`).
5. Prix annoncé selon la taille de l'entreprise (`TARIFICATION.md`).
6. Vente, mise en ligne, puis récurrent (hébergement + maintenance + SEO local — c'est là qu'est la vraie marge).

## 📂 Contenu du dossier

| Fichier | Usage |
|---------|-------|
| `PROSPECTION.md` | Où et comment trouver les entreprises sans site : sources par pays, méthode de vérification, données à collecter par prospect. |
| `CADRE_LEGAL.md` | Règles de prospection email pays par pays (FR, CH, DE, BE, IT, ES…), RGPD/nLPD, checklist avant envoi. **Bloquant.** |
| `TARIFICATION.md` | Grille de prix indexée sur la taille/CA de l'entreprise, offre récurrente, positionnement face à Wix/agences. |
| `EMAILS.md` | Séquence de 3 emails (FR + variante CH), personnalisation obligatoire, urgence honnête, règles de délivrabilité. |
| `PROCESSUS_VENTE.md` | Le workflow démo-avant-contact de bout en bout, de la liste au contrat signé, avec temps et outils par étape. |
| `STACK_TECHNIQUE.md` | Stack « nouvelle génération » : micro-animations, GSAP, 3D (Spline, Three.js, model-viewer), budget de performance, palier Signature 3D, et où la 3D vend vs dessert. |

## 🚀 Plan d'action 30 jours (pilote)

| Jour | Action | Livrable |
|------|--------|----------|
| J0–J3 | Choisir niche + zone. Lire `CADRE_LEGAL.md`. Préparer domaine d'envoi dédié + warm-up. | Niche validée, domaine prêt. |
| J3–J7 | Construire la liste : 30–50 entreprises vérifiées sans site, avec contact nominatif. | Fichier prospects complet. |
| J7–J14 | Créer le template de niche + 10 premières démos personnalisées. | 10 démos en ligne. |
| J14–J21 | Première vague : 10 contacts (email FR / courrier+téléphone CH), relances J+4 et J+9. | Premiers RDV. |
| J21–J30 | Vagues 2–3, premiers closings, mesurer : taux réponse, taux RDV, taux signature. | 1–3 ventes, chiffres réels. |

**Critère de scale :** si le pilote sort ≥ 10 % de réponses et ≥ 1 vente sur 30 contacts, on industrialise (autres zones, autres niches). Sinon on change de niche ou d'angle, pas de volume.

## 💡 Conseils business honnêtes

- **Le volume est un piège.** Le coût réel n'est pas l'envoi, c'est la démo personnalisée — et c'est précisément elle qui vend. Automatiser l'envoi sans automatiser la pertinence = spam.
- **Le récurrent vaut plus que la vente.** Un site à 1 500 € se vend une fois ; 79 €/mois de maintenance+hébergement+SEO local se vend 40 fois. Structurer l'offre autour du récurrent dès le premier contrat.
- **La Suisse se travaille au téléphone et par courrier**, pas par email froid (opt-in obligatoire). C'est plus lent mais les paniers y sont 1,5–2× plus élevés.
- **Beaucoup d'entreprises sans site n'en veulent pas** (bouche-à-oreille suffisant, artisan débordé qui refuse du travail). C'est un signal de qualification, pas un mur : cibler celles qui ont des avis Google actifs — elles se soucient déjà de leur image en ligne.
