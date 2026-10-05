# Correctif du prompt « Prospection IT BY Group »

**Routine** `trig_01U2HDPfZis52gNxZdoLYNnG` — à éditer sur
<https://claude.ai/code/routines/trig_01U2HDPfZis52gNxZdoLYNnG>

Un agent ne peut modifier que les routines qu'il a lui-même créées : celle-ci a été
créée depuis l'interface, donc le changement doit être appliqué à la main. Deux
remplacements exacts, rien d'autre.

## Pourquoi

Sur les 13 brouillons produits le 5 octobre, **6 n'avaient aucun destinataire** —
soit 46 % d'un run de 41 minutes, budget d'enrichissement Clay inclus, en
brouillons qui ne pourront jamais être envoyés.

Le prompt pose déjà le bon principe : « une entreprise sans décideur joignable par
e-mail vaut moins qu'une PME avec un CTO identifié ». Il n'en tire simplement pas
la conséquence.

## Remplacement 1 — étape 4 : ne plus produire de brouillon sans destinataire

**Chercher :**

```
N'invente JAMAIS d'adresse ni de nom ; si rien n'est trouvé, laisse le destinataire vide et écris dans notes « Pas d'e-mail : postuler via l'annonce ».
```

**Remplacer par :**

```
N'invente JAMAIS d'adresse ni de nom. Si aucun e-mail n'est trouvé, NE CRÉE AUCUN BROUILLON pour cette entreprise : mets son status à « sans_contact », écris dans notes « Pas d'e-mail trouvé le [date] : aucun brouillon créé », et passe à l'entreprise suivante sans dépenser de budget d'enrichissement supplémentaire sur elle. Un brouillon sans destinataire ne peut pas être envoyé : le produire est du temps de run perdu.
```

## Remplacement 2 — étape 3 : déclarer le nouveau status

**Chercher :**

```
status "a_contacter", contact "", email ""
```

**Remplacer par :**

```
status "a_contacter" (ou "sans_contact" si aucun e-mail n'a pu être trouvé), contact "", email ""
```

## Remplacement 3 (optionnel mais recommandé) — rendre le gaspillage visible

Dans le dernier paragraphe (format du message final), **chercher :**

```
Rappelle en une ligne le nombre de brouillons qui attendent d'être envoyés.
```

**Remplacer par :**

```
Rappelle en une ligne le nombre de brouillons qui attendent d'être envoyés, et le taux de destinataire trouvé (entreprises de priorité 1 et 2 traitées avec un e-mail / total traité). Si ce taux est inférieur à 70 %, dis-le explicitement : c'est du temps de run et du budget d'enrichissement perdus.
```

## Effet attendu

- Fin des brouillons inenvoyables : le volume de brouillons baisse, la part
  envoyable monte vers 100 %.
- Le budget d'enrichissement se concentre sur les entreprises réellement joignables.
- Les entreprises `sans_contact` restent dans le tableau de suivi : elles ne sont
  pas perdues, elles sont simplement sorties de la file d'e-mailing (on peut les
  travailler autrement — LinkedIn, téléphone, candidature via l'annonce).
- Le taux de destinataire trouvé devient une métrique visible à chaque run, et la
  routine « Revue de tunnel » le suit d'une semaine sur l'autre.

## Ce que ce correctif ne répare pas

Rien, côté conversion. Tant que la réponse automatique d'absence de Gmail est
active et que le tracking ne remonte que 1 entreprise sur ~25, envoyer plus de
brouillons propres ne produira pas plus de rendez-vous. Voir l'ordre
d'intervention dans [`README.md`](README.md) : ce correctif est le point 4, pas le
point 1.
