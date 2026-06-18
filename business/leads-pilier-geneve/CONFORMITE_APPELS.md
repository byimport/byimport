# Conformité des appels — call center / apporteur (Genève + Lausanne)

> Complète `CADRE_LEGAL_LPD.md` (cadre de fond nLPD / LSFin / FINMA) **sans le dupliquer**.
> Ici : ce qui est spécifique au fait de **téléphoner** à des leads et de **prendre des RDV**,
> que ce soit via un prestataire humain ou des **agents IA**.
>
> ⚠️ **Ce n'est pas un avis juridique.** Faire valider par un avocat spécialisé avant lancement.

## 1. Démarchage à froid B2C — INTERDIT (LCD art. 3 al. 1 let. u)

- **Interdit** d'appeler un particulier avec qui on n'a **aucune relation préalable** et qui
  n'a **pas consenti**. Sanction : amende administrative + risque réputation.
- **Acheter une liste et l'appeler (humain ou IA) = illégal.** Aucun contournement.
- **Seul modèle autorisé ici** : rappeler un lead qui a **rempli un formulaire avec opt-in
  clair**. Le formulaire vaut consentement préalable au rappel **par téléphone ou email**.
- **Mention obligatoire** sur le formulaire : « En soumettant ce formulaire, j'accepte d'être
  recontacté(e) par [Cabinet/Marque] par téléphone ou email au sujet de ma prévoyance. »
- **Preuve d'opt-in** à conserver : horodatage + IP + libellé exact du consentement coché,
  pendant toute la durée du traitement **et 3 ans après**. Cette preuve doit **suivre le lead**
  jusqu'au prestataire/agent qui appelle.

> ⚠️ **Agents IA vocaux** : une voix IA ne change **rien** à la règle. Un appel IA vers un
> contact non opt-in reste du démarchage à froid illégal. L'IA n'appelle que des leads
> opt-in, exactement comme un humain.

## 2. Enregistrement des appels — consentement

- Informer **en début d'appel** que la conversation est enregistrée (« cet appel est
  enregistré pour la qualité ») et obtenir l'accord. C'est dans l'ouverture du script
  (`SCRIPTS_APPELS.md` §1).
- Conserver les enregistrements de façon sécurisée, durée limitée et justifiée (QA, preuve),
  inscrits au **registre des traitements** (RAT).
- **Agents IA** : si un agent vocal IA mène l'appel, l'information « enregistrement + agent
  automatisé » doit être donnée de façon transparente. Ne pas faire passer une IA pour un
  humain de façon trompeuse.

## 3. Frontière qualification ≠ conseil (LSFin)

- Le call center / l'apporteur **qualifie et prend RDV**. Il **ne fournit pas de conseil en
  placement** au sens de la LSFin (pas de recommandation personnalisée de produit, pas de
  chiffrage d'économie ferme, pas de « cette fondation est la meilleure »).
- Les **devoirs d'information LSFin** (feuille d'information, profil de risque, adéquation,
  confirmation écrite — cf. `CADRE_LEGAL_LPD.md` §2) incombent au **conseiller/courtier** qui
  reçoit le RDV, **avant** toute signature.
- Si l'apporteur/agent franchit la ligne (conseille, oriente vers un produit nommé contre
  commission), il peut devenir lui-même **intermédiaire financier/assurance** soumis à
  enregistrement — voir §5.

## 4. Sous-traitance & protection des données (nLPD)

- Le prestataire call-center (ou le fournisseur d'agents IA, ou le fournisseur de téléphonie)
  est un **sous-traitant** → **DPA (contrat de sous-traitance) signé avant le 1er appel**.
- Vérifier : **localisation des données** (Suisse/UE de préférence), durée de conservation,
  sous-traitance ultérieure soumise à accord, sécurité.
- **Transferts hors Suisse/UE** (ex. fournisseur IA US) → base légale requise (clauses types)
  + mention dans la politique de confidentialité. Beaucoup d'outils IA vocaux/CRM sont
  hébergés aux US : à **vérifier au cas par cas**, privilégier les options UE/CH ou avec
  garanties contractuelles.
- **Registre des traitements (RAT)** tenu (les avoirs financiers sont des données sensibles).
- **Notification PFPDT** sous 72 h en cas de fuite.
- Vous restez **responsable du traitement** : déléguer l'exécution ne délègue pas la
  responsabilité légale.

## 5. Statut de l'apporteur / commission (point sensible)

- Toucher une **commission** pour avoir amené un client à un courtier (modèle apporteur)
  a des implications : selon la nature des produits (assurance 3a, placements/titres), le
  régime **LSFin / LSA / LIA** peut imposer un **enregistrement** (registre des conseillers,
  registre des intermédiaires d'assurance) et des **obligations de transparence** sur la
  rétribution.
- La **commission doit être déclarée/transparente** vis-à-vis du client final et entre
  parties (convention apporteur écrite).
- **Action :** faire qualifier votre statut exact par un avocat **avant** d'encaisser des
  commissions — « simple apporteur de RDV » vs « intermédiaire » n'a pas le même régime, et
  la frontière dépend de ce que vous faites réellement (si vous ne faites que livrer un RDV
  qualifié sans conseiller, le régime est plus léger ; si vous orientez vers un produit, il
  s'alourdit). Voir `CADRE_LEGAL_LPD.md` §1.

## 6. Email / SMS de relance (LCD + nLPD)

- Pas de SMS/email **sans opt-in**. Le même consentement formulaire couvre le rappel et la
  relance liée à la demande.
- **Lien/mot de désinscription** fonctionnel ; honorer les oppositions **immédiatement**.

## 7. Publicité & propos financiers

- Pas de « rendement garanti », « sans risque », montant d'économie ferme. Voir l'encadré
  interdits de `SCRIPTS_APPELS.md` §9 et `CADRE_LEGAL_LPD.md` §6.

## 8. Checklist conformité — avant le 1er appel

| # | Action | Statut |
|---|--------|--------|
| 1 | Opt-in clair sur tous les formulaires + mention rappel téléphone/email | ☐ |
| 2 | Preuve d'opt-in capturée et transmise au prestataire/agent | ☐ |
| 3 | Script d'ouverture avec annonce d'enregistrement | ☐ |
| 4 | DPA signé avec prestataire / fournisseur IA / téléphonie | ☐ |
| 5 | Localisation des données vérifiée (+ clauses si hors UE/CH) | ☐ |
| 6 | Registre des traitements (RAT) à jour (appels, enregistrements) | ☐ |
| 7 | Frontière qualification/conseil écrite et comprise par les agents | ☐ |
| 8 | Statut apporteur/commission validé par avocat | ☐ |
| 9 | Convention apporteur écrite avec le(s) courtier(s) | ☐ |
| 10 | Process de notification PFPDT (responsable + modèle prêt) | ☐ |

**Tant que ces points ne sont pas cochés, ne lancer aucun appel.**

## Ressources
- **SECO (LCD démarchage)** : https://www.seco.admin.ch
- **PFPDT (protection données)** : https://www.edoeb.admin.ch
- **FINMA (registres, intermédiaires)** : https://www.finma.ch
- Voir aussi les ressources de `CADRE_LEGAL_LPD.md`.
