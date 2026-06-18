# By Solar — Remise à un ESP (l'envoi ne passe jamais par le CRM)

Le connecteur CRM **n'envoie pas d'emails** — il sert à *segmenter* (voir `segmentation.md`). L'envoi se fait dans un **ESP** (Email Service Provider) qui gère consentement, désinscription, authentification du domaine et statistiques. Exemples : Brevo (ex-Sendinblue, FR), Mailchimp, HubSpot Marketing Email, Mailjet.

## Pourquoi un ESP, pas un script

Un envoi conforme et délivrable exige :

- **Authentification du domaine** : SPF, DKIM, DMARC configurés sur le domaine d'envoi By Solar.
- **Désinscription en 1 clic** + liste de suppression respectée automatiquement.
- **Gestion du consentement et de la preuve** (date, source, périmètre) par contact.
- **Réputation IP/domaine**, throttling, boucles de rétroaction (FBL), gestion des bounces.

Un script `sendmail` maison ne fournit rien de tout cela : il finit en spam et expose juridiquement. On ne fait donc **aucun** envoi côté CRM ni côté code.

## Procédure

1. **Choisir l'ESP** et authentifier le domaine d'envoi (SPF/DKIM/DMARC). Vérifier le domaine avant tout envoi.
2. **Importer l'audience consentante** produite à `segmentation.md` :
   - **Préférer une synchro native CRM ↔ ESP** (ex. intégration HubSpot↔ESP, ou la liste marketing native de HubSpot) plutôt qu'un export CSV manuel : la synchro propage les désinscriptions dans les deux sens.
   - Si export CSV : n'exporter **que** le segment opt-in, ne pas laisser traîner le fichier de PII, le supprimer après import.
3. **Mapper les champs de fusion** attendus par les modèles (`email-templates.md`) : `prenom`, `region`, `date_consentement`, `lien_landing`, `lien_desinscription`, `lien_politique_confidentialite`, `adresse_postale_entreprise`, `email_contact`.
4. **Configurer la campagne** : expéditeur « By Solar », objet du modèle, pied de page légal complet, lien de désinscription injecté par l'ESP.
5. **Tester** : envoi de test, passage anti-spam (ex. score de l'ESP), vérif rendu mobile, vérif que la désinscription fonctionne réellement.
6. **Envoyer** (ou planifier), puis **mesurer** dans l'ESP : ouvertures, clics, désinscriptions, plaintes spam.

## Boucle de retour vers le CRM

- Les contacts qui **cliquent / demandent l'étude** repassent en CRM comme leads chauds (via `crm-query`/le CRM) pour le suivi commercial.
- Les **désinscriptions** doivent être reflétées dans le CRM (propriété de consentement mise à `false`) pour que les futurs segments les excluent automatiquement. Si la synchro native ne le fait pas, planifier une mise à jour — opération d'**écriture**, donc via la surface d'écriture du CRM (hors skills `crm-*`, qui sont en lecture seule), avec confirmation.

## Garde-fous

- Jamais d'envoi à un contact dont le consentement n'est pas explicitement vrai.
- Jamais d'achat/import de listes externes.
- Respect des désinscriptions sous 72 h max.
- Conserver la preuve de consentement : en cas de réclamation CNIL, c'est ce qui protège By Solar.
