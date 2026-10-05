# Diagnostic du moteur de revenus — 5 octobre 2026

Audit des automatisations réellement en service sur le compte, à partir de leurs
données d'exécution, de Gmail et de l'endpoint de tracking de BY Group. Aucun
chiffre ici n'est estimé : chacun est lu dans le système.

## La conclusion, avant les détails

**Le goulot d'étranglement n'est pas le manque d'automatisation — il y en a déjà.
C'est que le moteur existant ne produit aucun résultat mesurable, et que trois
défauts concrets le vident en silence.**

Ajouter des agents par-dessus un tunnel non mesuré, c'est exactement le mode de
défaillance de monkeyspunk (voir [`../monkeyspunk/AUDIT.md`](../monkeyspunk/AUDIT.md)) :
cinq semaines de silence pendant que rien ne se vendait. L'ordre correct est
**rendre mesurable → réparer les fuites → puis seulement démultiplier**.

## Ce qui tourne réellement

| Routine | Fréquence | Durée du dernier run | Verdict |
|---|---|---|---|
| Prospection IT BY Group | lun. + jeu. 07:55 Paris | **41 min 31 s** | le vrai moteur, il travaille |
| solution (BY Solar) | lun. 07:00 | 4 min 44 s | tourne depuis mai, aucune vente constatée |
| Veille jeux concours | quotidien 06:30 | 39 s | sans rapport avec le CA |
| Project planning and design review | **toutes les heures** | **20 s** | ne produit rien (voir défaut n°4) |

## Les quatre défauts, par impact sur le CA

### 1. Une réponse automatique d'absence est active pendant la prospection

Message `1a10b7c3b6f0c3cb`, envoyé le 5 oct. à 09:54:13, deux secondes après un
e-mail entrant, à `postmaster@cio56699.info.n8n.io` :

> « Actuellement en rendez-vous, je vous répondrais dans les plus brefs délais. Cordialement »

Conséquences, par ordre de gravité :

- **Tout prospect qui répond reçoit un vent automatique** au lieu d'une réponse.
  C'est la conversion elle-même qui est tuée, sur le seul événement qui compte.
- Elle répond aussi aux `no-reply` et aux adresses de rebond, ce qui a produit au
  moins **3 rebonds `mailer-daemon` en 30 jours** (n8n ×2, tryhackme, aliexpress ×3).
  Pour un compte Gmail qui fait du démarchage, c'est de la réputation d'expéditeur
  détruite gratuitement.
- Elle annonce à chaque newsletter que la personne est « en rendez-vous ».

**Correctif : désactiver le répondeur automatique dans Gmail → Paramètres →
Général → Réponse automatique.** Dix secondes, et c'est le point le plus rentable
de tout ce document.

### 2. La mesure est aveugle

L'endpoint de tracking que la routine utilise déjà
(`bygroup-tech-talent.netlify.app/p/stats`) renvoie :

```
entreprises suivies : 1
ouvertures : 0   visites de page : 1   clics : 0
```

Alors que **14 e-mails de prospection ont été envoyés le 1er octobre à 15:24**
(mozilla, ptc, hinted.me, andre-chevalley, ensolum, table.media, cascination,
laelaps, securecell, superchat, glassdollar, wattfox, predium, live-eo) et
qu'environ 13 brouillons ont été produits le 5 octobre.

Une seule entreprise sur ~25 touchées apparaît dans le tracking, et elle
(`The Garage of Nyon`) ne fait pas partie des 14 destinataires. **Le pixel ou la
clé de rapprochement par nom d'entreprise ne fonctionne pas.**

Tant que ce n'est pas réparé, il est impossible de distinguer un problème de
délivrabilité d'un problème de ciblage — donc impossible d'améliorer quoi que ce soit.

### 3. 46 % du travail produit des brouillons inenvoyables

Sur les 13 brouillons créés le 5 octobre entre 06:27 et 06:36 :

- **7 avec destinataire** (wandelbots, legartis, speedgoat, scholarshipowl, infisical, clarity.ca, imprint.co)
- **6 sans aucun destinataire** → ils ne pourront jamais être envoyés

C'est conforme à la consigne actuelle de la routine (« laisse le destinataire vide »),
mais ça veut dire que près de la moitié d'un run de 41 minutes part à la poubelle,
budget Clay inclus.

**Correctif de consigne :** ne pas créer de brouillon quand aucun e-mail n'est trouvé.
Enregistrer la fiche en `status: "sans_contact"` et réinvestir le budget
d'enrichissement sur des entreprises où un décideur est joignable. Le prompt le dit
déjà : « une entreprise sans décideur joignable par e-mail vaut moins qu'une PME
avec un CTO identifié » — il faut en tirer la conséquence.

### 4. Environ 2 900 exécutions à vide

La routine « Project planning and design review » tourne **toutes les heures**
(`59 * * * *`) depuis le 2 juin 2026, soit ~24 fois par jour pendant 4 mois.
Chaque run dure **20 secondes** et son prompt est « Review and plan improvements
across all active projects » — sans projet désigné, sans dépôt, sans sortie définie.

Elle ne produit rien et n'a jamais rien produit. **Correctif : la désactiver.**

## Ce qu'il reste du tunnel, en chiffres

```
41 min de travail × 2 fois/semaine
   -> ~13 brouillons par run
      -> 7 envoyables  (6 sans destinataire)
         -> 14 envoyés le 1er oct.
            -> 0 ouverture mesurée
               -> 0 réponse de prospect
                  -> 0 rendez-vous
```

Avec, au bout de la chaîne, un répondeur automatique prêt à éconduire la première
personne qui répond.

## Ordre d'intervention

| # | Action | Coût | Effet |
|---|---|---|---|
| 1 | Désactiver la réponse automatique Gmail | 10 s | débloque la conversion |
| 2 | Désactiver la routine horaire | 1 min | supprime ~24 runs/jour à vide |
| 3 | Réparer le pixel / le rapprochement par nom d'entreprise | 1 h | rend le tunnel observable |
| 4 | Ne plus créer de brouillon sans destinataire | modif. de prompt | récupère ~46 % du run |
| 5 | Installer une revue de tunnel hebdomadaire (voir ci-dessous) | 1 routine | la boucle d'auto-amélioration |
| 6 | Alors seulement : augmenter le volume ou ajouter des canaux | — | sur des données fiables |

## La seule automatisation qu'il vaut la peine d'ajouter maintenant

Pas un agent de plus qui produit : **un agent qui mesure**. C'est ça,
l'auto-amélioration — une boucle fermée sur des chiffres, pas un prompt qui dit
« améliore-toi ».

Spécification d'une routine hebdomadaire (lundi, après le run de prospection) :

1. Compter les brouillons créés depuis 7 jours, avec et sans destinataire.
2. Compter les envois réels (`in:sent`) vers des domaines de prospects.
3. Lire `/p/stats` : ouvertures, visites, clics, et les signaux chauds.
4. Compter les réponses entrantes de prospects (hors rebonds et newsletters).
5. Comparer à la semaine précédente et **ne remonter que les écarts** : taux de
   destinataire trouvé, taux d'ouverture, taux de réponse, rendez-vous pris.
6. Si le taux d'ouverture reste à 0 avec des envois > 10, le signaler comme une
   panne de délivrabilité ou de mesure, pas comme une mauvaise performance.

C'est le chaînon manquant : aujourd'hui personne ne saurait dire si la semaine a
été bonne ou mauvaise.

## Reproduire

Les chiffres viennent de : `list_triggers` (durées de run), `list_drafts` et
`search_threads in:sent newer_than:30d` (Gmail), `get_message 1a10b7c3b6f0c3cb`
(le répondeur automatique), et `curl` sur l'endpoint `/p/stats` de BY Group.
