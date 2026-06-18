# By Solar — Modèles d'emails conformes (FR)

Modèles destinés à des contacts **ayant donné leur consentement**. À charger dans un ESP (voir `esp-handoff.md`), jamais à envoyer via le connecteur CRM ou un script maison.

## Éléments obligatoires sur chaque email

- **Identité expéditeur** claire : « By Solar » + adresse postale de l'entreprise + email de contact réel.
- **Objet non trompeur** : décrit honnêtement le contenu, pas de fausse urgence ni de « Re: » trompeur.
- **Lien de désinscription** fonctionnel et visible, traité effectivement (l'ESP gère la liste de suppression).
- **Mention RGPD** : finalité, base légale (consentement), droit d'accès/rectification/opposition, lien vers la politique de confidentialité.
- **Personnalisation** seulement à partir de champs réellement présents (prénom, région) — pas de variable vide affichée.

Les placeholders `{{...}}` correspondent à des champs de fusion à mapper dans l'ESP depuis le segment CRM.

---

## Modèle A — Premier contact (prospect opt-in, jamais sollicité)

**Objet :** `{{prenom}}, et si votre toit produisait votre électricité ?`
*(variante : `Réduire votre facture d'électricité avec le solaire — étude gratuite`)*

```
Bonjour {{prenom}},

Vous nous avez indiqué être intéressé(e) par l'énergie solaire — merci de votre confiance.

By Solar installe des panneaux photovoltaïques pour les particuliers
en {{region}}. En quelques minutes, nous estimons gratuitement :

  • le potentiel solaire de votre toiture,
  • l'économie annuelle réaliste sur votre facture,
  • les aides auxquelles vous êtes éligible.

Sans engagement. Vous décidez ensuite si vous souhaitez aller plus loin.

  → Demander mon étude gratuite : {{lien_landing}}

Une question ? Répondez simplement à cet email, un conseiller By Solar
vous recontacte.

Belle journée,
L'équipe By Solar
```

**Pied de page (obligatoire) :**
```
By Solar — {{adresse_postale_entreprise}}
Vous recevez cet email parce que vous avez consenti à être contacté(e)
par By Solar le {{date_consentement}}.
Se désinscrire : {{lien_desinscription}}   |   Confidentialité : {{lien_politique_confidentialite}}
Conformément au RGPD, vous disposez d'un droit d'accès, de rectification
et d'opposition : {{email_contact}}.
```

---

## Modèle B — Relance (a ouvert/cliqué mais n'a pas converti)

**Objet :** `{{prenom}}, votre estimation solaire vous attend`

```
Bonjour {{prenom}},

Vous aviez commencé à vous renseigner sur le solaire avec By Solar.
Votre toiture en {{region}} a peut-être un vrai potentiel — l'étude
reste gratuite et sans engagement.

  → Reprendre où vous en étiez : {{lien_landing}}

Si ce n'est plus d'actualité, pas de souci : vous pouvez vous
désinscrire en bas de cet email.

L'équipe By Solar
```

*(Même pied de page obligatoire que le Modèle A.)*

---

## Modèle C — Contact professionnel (B2B, adresse pro)

Pour des destinataires **professionnels** (toiture d'entreprise, copropriété, agriculteur), message en rapport avec leur fonction, opt-out clair.

**Objet :** `Autoconsommation solaire pour {{nom_entreprise}} — étude de rentabilité`

```
Bonjour {{prenom}},

By Solar accompagne les {{secteur}} de {{region}} dans l'installation
de panneaux photovoltaïques en autoconsommation : réduction des charges
d'électricité et valorisation du patrimoine bâti.

Nous proposons une étude de rentabilité gratuite adaptée à votre site.

  → Planifier un échange de 15 min : {{lien_rdv}}

Si vous ne souhaitez pas recevoir nos communications, désinscription
en un clic ci-dessous.

Cordialement,
L'équipe By Solar
```

*(Pied de page obligatoire ; en B2B la base peut être l'intérêt légitime, mais l'opt-out doit rester immédiat.)*

---

## À proscrire (raisons de conformité ET de délivrabilité)

- Objets mensongers, fausses urgences, « RE: »/« FWD: » trompeurs, MAJUSCULES, emojis en rafale.
- Email à une adresse **sans consentement** (B2C) — illégal et destructeur pour la réputation du domaine.
- Pièces jointes lourdes, images sans texte alternatif, lien de désinscription absent ou factice.
- Achat de listes d'emails : non conforme et toxique pour la délivrabilité.
