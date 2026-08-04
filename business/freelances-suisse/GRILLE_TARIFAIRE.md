# Grille tarifaire interne — placement de freelances FR/UE chez clients suisses

> ⚠️ **Note** : dossier business sans rapport avec le plugin Toprank. Ne touche ni `VERSION` ni `CHANGELOG.md`.
>
> ⚠️ **Ce repo est public.** Les chiffres ci-dessous sont des **fourchettes de marché** et des **règles de calcul**, pas tes taux réels négociés. Ne commite jamais ici : nom de client, nom de freelance, TJM nominatif effectivement signé, marge réelle par compte. Ces données-là restent dans ton tableur privé.

**Objet :** chiffrer une mission en 2 minutes. Trois questions, une réponse : *combien ça me coûte, combien je marge, suis-je au-dessus de mon plancher.*

---

## 1. Le modèle économique en une ligne

```
Prix de vente CH  =  TJM marché FR  ×  1.20 (prime mission suisse)  ×  FX  ÷  (1 − marge cible)
```

L'arbitrage que tu vends est réel : un dev fullstack confirmé coûte ~525 €/j en France et se facture ~1 400 CHF/j par une ESN genevoise. **Mais ne prends pas tout l'écart.** Le prix d'achat est fixé à **TJM marché français × 1.20**, pas au TJM français. Trois raisons, dans cet ordre d'importance :

1. **Rétention.** Le freelance qui découvre qu'il est acheté 630 € et revendu 1 050 CHF part au premier renouvellement — ou se fait embaucher en direct. S'il gagne déjà +20 % vs son marché habituel, l'écart devient supportable.
2. **Qualité de sourcing.** À prix marché tu prends ce qui reste. À +20 % tu prends ceux qui refusent les ESN.
3. **Durabilité de la marge.** Une marge de 50 % sur un freelance sous-payé est une marge qui a une date d'expiration. À 38–42 % avec un freelance content, elle tient.

---

## 2. La grille

**Taux de planification : 1 EUR = 0.98 CHF.** Volontairement au-dessus du marché (~0.93–0.94 à la dernière calibration) : ce coussin de ~5 % fait qu'une variation défavorable de l'euro mange le coussin, pas ta marge. Une variation favorable, c'est du bonus. **Ne chiffre jamais au taux spot.**

Tous les prix sont **HT / hors TVA**, par jour ouvré, hors frais de déplacement.

<!-- TABLEAU GÉNÉRÉ — ne pas éditer à la main.
     Modifie scripts/grille.json puis : python3 scripts/chiffrage.py --table -->

| Profil | Marché FR (€/j) | Achat (€/j) | Coût (CHF/j) | **Vente (CHF/j)** | Plancher (CHF/j) | Marge (CHF/j) | Marge % | Réf. ESN GE (CHF/j) | Écart |
|---|---|---|---|---|---|---|---|---|---|
| Dev fullstack junior (0–3 ans) | 300–400 | 420 | 412 | **750** | 575 | 338 | 45% | 950–1150 | -29% |
| QA / automatisation de tests | 400–550 | 570 | 559 | **950** | 800 | 391 | 41% | 1050–1250 | -17% |
| UX / UI designer | 400–550 | 570 | 559 | **975** | 800 | 416 | 43% | 1100–1300 | -19% |
| Dev frontend confirmé (React / Vue) | 420–560 | 590 | 578 | **1000** | 825 | 422 | 42% | 1200–1400 | -23% |
| Dev fullstack confirmé (3–7 ans) | 450–600 | 630 | 617 | **1050** | 875 | 433 | 41% | 1300–1550 | -26% |
| Dev mobile (iOS / Android / RN) | 450–650 | 660 | 647 | **1100** | 925 | 453 | 41% | 1350–1600 | -25% |
| Dev backend spécialisé (Java / .NET / Go) | 500–700 | 720 | 706 | **1150** | 1000 | 444 | 39% | 1400–1650 | -25% |
| Data engineer | 500–700 | 720 | 706 | **1175** | 1000 | 469 | 40% | 1450–1700 | -25% |
| Product Manager / Product Owner | 500–700 | 720 | 706 | **1175** | 1000 | 469 | 40% | 1400–1650 | -23% |
| DevOps / SRE / Cloud (K8s, AWS, Azure) | 550–750 | 780 | 764 | **1275** | 1075 | 511 | 40% | 1550–1850 | -25% |
| Dev fullstack senior / tech lead (7+ ans) | 600–750 | 810 | 794 | **1275** | 1125 | 481 | 38% | 1550–1850 | -25% |
| Data scientist / ML engineer | 550–780 | 800 | 784 | **1300** | 1100 | 516 | 40% | 1600–1900 | -26% |
| Cybersécurité (pentest / GRC) | 600–850 | 870 | 853 | **1450** | 1200 | 597 | 41% | 1700–2100 | -24% |
| Architecte solution / cloud | 700–900 | 960 | 941 | **1550** | 1325 | 609 | 39% | 1800–2200 | -22% |
| Consultant SAP / ERP | 700–1000 | 1020 | 1000 | **1700** | 1400 | 700 | 41% | 1900–2400 | -21% |

**Lecture :** la colonne *Vente* est ton prix catalogue — celui que tu annonces. La colonne *Plancher* est le prix sous lequel tu ne descends **jamais** (calé sur 28 % de marge brute). L'écart entre les deux, ~15–20 %, c'est ta marge de négociation, et rien de plus.

**Ton argumentaire tient dans la dernière colonne :** *« -20 à -25 % sous une ESN genevoise, même profil, même séniorité »*. C'est vrai, c'est vérifiable, et c'est assez pour ouvrir une porte sans passer pour du low-cost. Ne descends pas à -40 % : à ce niveau l'acheteur suisse ne se dit pas « bonne affaire », il se dit « où est le problème ».

---

## 3. Chiffrer un deal en 2 minutes

```bash
# Prix catalogue, mission de 60 jours
python3 scripts/chiffrage.py --profil fullstack-confirme --jours 60

# Le client négocie à 950 CHF/j — est-ce que ça passe ?
python3 scripts/chiffrage.py --profil fullstack-confirme --vente 950 --jours 60

# Profil hors grille : achat négocié 700 €/j, vendu 1 200 CHF/j
python3 scripts/chiffrage.py --achat-eur 700 --vente 1200 --jours 40

# Tous les IDs de profil
python3 scripts/chiffrage.py --liste
```

Le script sort trois verdicts, et le code de retour suit :

| Verdict | Condition | Ce que tu fais | Exit code |
|---|---|---|---|
| **OK** | marge ≥ 38 % | Tu envoies le devis. | 0 |
| **ATTENTION** | 28 % ≤ marge < 38 % | Acceptable si mission longue, client récurrent, ou compte stratégique à ouvrir. Jamais en one-shot. | 0 |
| **REFUS** | marge < 28 % ou sous le plancher | Tu remontes le prix ou tu passes. | 1 |

Le code de retour permet de brancher le chiffrage dans un workflow n8n : `exit 1` = ne génère pas le devis.

---

## 4. Ce que la marge brute doit encore payer

**La marge brute n'est pas ton revenu.** Sur 100 CHF de marge brute, compte 30 à 40 CHF qui partent avant toi :

| Poste | Ordre de grandeur | Base |
|---|---|---|
| Provision impayés | 1,5 % du CA | À provisionner dès la première facture, pas après le premier défaut. |
| RC professionnelle + protection juridique | 2 000–3 000 CHF/an | Non négociable : tu réponds du travail d'un tiers. |
| Comptabilité + juridique (contrats-cadres, CGV) | 3 000–5 000 CHF/an | Plus cher la première année (rédaction des modèles). |
| Outils (CRM, Apollo, e-signature, hébergement n8n) | ~250 CHF/mois | ~3 000 CHF/an. |
| Acquisition commerciale | 8–15 % de la marge brute | Temps + outils par client signé. |
| **Coût de structure annuel hors acquisition** | **~10 000–13 000 CHF** | |

**Le seuil de rentabilité :** à ~450 CHF de marge brute/jour et ~205 jours facturés par slot et par an (congés, inter-contrats, ramp-up inclus — ne compte jamais 220), **un slot actif dégage ~92 000 CHF de marge brute/an**. Un seul slot couvre la structure et te paie. Le deuxième est celui qui construit l'entreprise.

### Le vrai mur : la trésorerie

C'est la contrainte qui tue ce modèle, pas la marge.

Tu paies le freelance à 30 jours. Le client suisse paie à 45–60 jours, parfois plus dans les grands comptes. **Tu avances donc en permanence 15 à 30 jours de coût d'achat par mission active.**

| Missions actives simultanées | Trésorerie à immobiliser (décalage 30 j) |
|---|---|
| 1 | ~13 000 CHF |
| 3 | ~40 000 CHF |
| 5 | ~66 000 CHF |
| 10 | ~132 000 CHF |

Le script calcule ce besoin (`Trésorerie à avancer`) sur chaque chiffrage. **Trois leviers, par ordre d'efficacité :**

1. **Acompte de 30 % à la commande** sur toute mission > 20 jours avec un nouveau client. C'est le seul levier gratuit.
2. **Escompte paiement 15 jours : -2 % sur la facture.** Tu perds 2 points de marge, tu récupères 30 jours de trésorerie. Sur un modèle qui croît, c'est un excellent échange — l'affacturage coûte plus cher.
3. **Négocier 45 jours de délai de paiement freelance** — à ne faire qu'en dernier recours. Payer ses freelances en retard est le moyen le plus rapide de perdre les bons.

**Règle absolue : tu paies le freelance à l'échéance, même si le client est en retard.** C'est la seule chose qui te différencie durablement d'une ESN, et c'est ce qui te vaut d'être recommandé. Le coût de cette règle, c'est exactement le tableau ci-dessus — provisionne-le, ne le découvre pas.

---

## 5. Règles de négociation

### Remises autorisées (cumulables, plafond global -12 %)

| Levier | Remise | Contrepartie exigée — non négociable |
|---|---|---|
| Volume : 2–3 profils simultanés | -3 % | Engagement simultané contractuel, pas une intention. |
| Volume : 4+ profils simultanés | -6 % | Idem + contrat-cadre signé. |
| Durée : 6 mois fermes | -3 % | Ferme = préavis de 30 jours, pas de résiliation libre. |
| Paiement à 15 jours | -2 % | Vérifié sur la première facture, sinon la remise saute. |

**Trois remises que tu n'accordes pas :**

- **Une remise « pour démarrer », sans contrepartie.** Elle devient le prix de référence du compte, définitivement. Le premier prix est le seul que tu fixes vraiment.
- **Une remise financée en baissant l'achat.** Si tu rognes sur le freelance pour tenir un prix client, tu perds le freelance dans les trois mois et tu as vendu ta marge deux fois.
- **Une remise sous le plancher.** Le plancher n'est pas un objectif de négociation, c'est la limite en-dessous de laquelle le deal te coûte de l'argent une fois la structure absorbée.

### Indexation et renouvellement

- Clause d'indexation annuelle **+2 à +4 %** dans tout contrat-cadre. Sans clause, l'inflation te mange en silence sur les missions longues.
- **Au renouvellement, augmente le prix d'achat avant que le freelance ne le demande.** +3 à +5 %. Le coût est marginal, l'effet sur la rétention est disproportionné.
- Clause de révision si l'EUR/CHF bouge de plus de 5 % sur la durée d'un contrat > 6 mois. Ça marche dans les deux sens et c'est défendable comme tel.

### Clause de non-sollicitation (la plus importante du contrat)

Le risque structurel du modèle : le client embauche ton freelance en direct au bout de six mois et tu perds l'annuité.

- **Durée :** 12 mois après la fin de la mission.
- **Indemnité :** 6 mois de marge brute de la mission, **ou** 20 % du salaire annuel brut proposé — le montant le plus élevé des deux.
- **Symétrie :** la clause vise le client *et* le freelance. Elle doit être dans les deux contrats, sinon elle est contournable en une signature.
- **Ne la cache pas.** Annonce-la à la signature comme une clause standard. Une clause découverte au moment du litige ne se plaide pas bien.

---

## 6. Contrainte juridique qui conditionne toute la grille

**À faire valider par un avocat suisse avant la première mission. Ce n'est pas un avis juridique — c'est la raison pour laquelle la grille est construite comme elle l'est.**

Le droit suisse distingue deux choses que le langage commercial confond :

| | **Contrat d'entreprise / mandat** | **Location de services** |
|---|---|---|
| Qui dirige le travail | Le freelance (ou toi) | Le client |
| Ce que tu vends | Un résultat, un livrable | Des heures de travail |
| Cadre légal | Libre | **LSE — autorisation obligatoire** |

La **LSE** (loi fédérale sur le service de l'emploi et la location de services) pose un obstacle décisif : **la location de services depuis l'étranger vers la Suisse n'est pas autorisée.** Une société française ne peut pas mettre du personnel à disposition d'un client suisse sous la direction de ce client, avec ou sans licence. Ce n'est pas une formalité coûteuse — c'est une interdiction.

**Conséquence directe sur ton offre.** Trois montages seulement tiennent :

1. **Prestation de services à distance depuis la France, avec obligation de résultat.** Le freelance travaille sous ta responsabilité ou la sienne, livre un périmètre défini, n'est pas intégré à la hiérarchie du client. **C'est le montage que la grille suppose, et c'est aussi le plus rentable** — pas de déplacement, pas de détachement, pas de licence.
2. **Régie sur site en Suisse** → tu as besoin d'une **entité suisse titulaire d'une autorisation de location de services** (autorisation cantonale, ou fédérale si tu opères hors canton, avec caution). Coût, délai et capital immobilisé significatifs. À n'envisager qu'une fois le modèle 1 rentable.
3. **Mission ponctuelle sur site avec déplacement** → procédure d'annonce pour travailleurs détachés (annonce préalable en ligne, plafond de 90 jours/an pour les ressortissants UE/AELE), respect des conditions salariales suisses usuelles, et **preuve du statut d'indépendant** du freelance. Genève contrôle activement la pseudo-indépendance.

**Le piège opérationnel :** même sous contrat de prestation, si le freelance est de facto dirigé au quotidien par le client — daily du client, tickets assignés par le client, congés validés par le client — les autorités peuvent requalifier en location de services. Ce que tu écris dans le contrat ne suffit pas ; c'est la réalité de la relation qui compte.

**Trois règles à tenir dans la conduite des missions :**
- Le périmètre est défini par livrable ou par jalon, pas par « mise à disposition ».
- Le point d'entrée opérationnel, c'est toi, pas le manager du client.
- Le freelance facture toi, tu factures le client. Jamais de facturation directe, jamais de triangulaire.

### TVA

- **Prestation de services B2B à un client suisse :** le lieu de la prestation est chez le destinataire. Le client suisse déclare l'**impôt sur les acquisitions** (taux normal 8,1 %). Tu factures sans TVA suisse, avec la mention d'autoliquidation. Vérifie le traitement côté français avec ton comptable.
- **Si tu crées une entité suisse** : assujettissement obligatoire au-delà de 100 000 CHF de chiffre d'affaires annuel mondial.

---

## 7. Maintenir la grille

La grille est un fichier de données, pas un tableau à retoucher à la main.

```bash
# 1. Modifier scripts/grille.json (prix, profils, paramètres)
# 2. Régénérer le tableau de la section 2 :
python3 scripts/chiffrage.py --table
# 3. Coller la sortie à la place du tableau existant
```

**Rythme de recalibration :**

| Quoi | Fréquence | Signal de déclenchement |
|---|---|---|
| Taux FX de planification | Trimestriel | L'EUR/CHF sort de la bande 0.90–0.98. |
| TJM marché FR (colonne achat) | Semestriel | Deux refus consécutifs de bons profils sur le prix. |
| Prix de vente + réf. ESN | Semestriel | Trois deals perdus d'affilée sur le prix, ou trois gagnés sans aucune négociation (tu es trop bas). |
| Plancher | Annuel | Changement du coût de structure. |

**Le signal le plus utile est le taux d'acceptation sans négociation.** S'il dépasse ~40 %, ton prix catalogue est trop bas : monte-le de 5 % sur les nouveaux deals et observe. Un prix qui ne se négocie jamais est un prix mal placé.

---

## 8. Ce que cette grille ne couvre pas

Dit franchement, pour que tu ne construises pas dessus sans le savoir :

- **Les fourchettes de marché sont des ordres de grandeur de calibration, pas des données sourcées.** Confronte-les à tes trois premiers deals réels et corrige `grille.json` — c'est le seul jeu de données qui vaille.
- **Les références ESN genevoises sont des estimations de positionnement.** Elles servent l'argumentaire ; ne les cite pas comme des chiffres publiés dans un email client.
- **Le forfait n'est pas modélisé.** La grille est en régie / TJM. Ne vends au forfait qu'une fois le périmètre verrouillé par écrit : au forfait, le dépassement sort intégralement de ta marge, et un dépassement de 20 % sur une marge de 40 % t'en laisse 25.
- **Aucun coût de recrutement par freelance placé** n'est imputé au deal. Si tu paies pour sourcer (annonces, temps de qualification), impute-le au premier deal du freelance, pas à tous.
