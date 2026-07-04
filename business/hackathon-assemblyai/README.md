# CallSense — agent IA d'analyse d'appels

Candidature au **$50k AI Hackathon (AssemblyAI)** sur Devpost. Dossier sous `business/`, sans lien
avec le plugin Toprank.

## Le produit en une phrase

Vous déposez l'enregistrement d'un appel commercial ou support → CallSense le transcrit, l'analyse,
et renvoie un **plan d'action prêt à l'emploi** : résumé, objections du client, tâches à faire,
brouillon d'e-mail de relance, et une note de coaching pour le commercial.

## Pourquoi ce concept peut gagner

Le jury note sur trois axes — CallSense vise les trois :

- **Viabilité business** : les équipes de vente/support paient déjà pour l'analyse d'appels
  (marché « conversation intelligence » réel). Cible claire : TPE/PME sans outil coûteux.
- **IA-native** : le produit *n'existe pas* sans IA. Transcription (AssemblyAI) + raisonnement LLM
  sur le contenu réel de l'appel (LeMUR) = cœur du produit, pas un gadget greffé.
- **Impact** : gain de temps concret par appel (relance rédigée, actions priorisées, coaching).

Et il utilise AssemblyAI **en profondeur** (diarisation, sentiment, LeMUR), pas juste en surface —
ce que les juges d'un hackathon sponsorisé regardent.

## Comment ça marche (déjà codé, `agent/`)

```
export ASSEMBLYAI_API_KEY=...        # clé gratuite sur assemblyai.com
pip install -r requirements.txt
python -m agent.callsense mon_appel.mp3 --out outputs/rapport
# → outputs/rapport.json (structuré)  +  outputs/rapport.md (lisible)
```

- `agent/callsense.py` — pipeline transcription → analyse LeMUR → rapport.
- `agent/prompts.py` — le prompt d'analyse (sortie JSON stricte), isolé pour itérer vite.

Le code compile et suit l'API réelle du SDK AssemblyAI. Il n'a pas encore tourné en vrai : il faut
**une clé API** (votre compte) et un fichier audio de test — voir checklist.

## Faits du concours

- **Prix** : jusqu'à 50 000 $.
- **Deadline** : 11 décembre 2026, 12:30 PT — large marge, on a le temps de bien faire.
- **Règles** : projet **nouveau** (ce dépôt en est un), **un** projet par équipe, historique de
  commits Git visible sur GitHub, **vidéo démo de 2 min max** obligatoire.
- **À vérifier dans le règlement officiel** : éligibilité par pays (les hackathons Devpost excluent
  les pays sous sanctions ; la France n'en fait pas partie, mais confirmez sur la page des règles).

## Checklist de soumission — ce que VOUS devez faire

Je code et rédige tout ; ces gestes exigent votre identité :

1. [ ] Créer un compte **AssemblyAI** (gratuit) → récupérer la clé API.
2. [ ] Créer un compte **Devpost** et s'inscrire au hackathon.
3. [ ] Créer un **compte GitHub** public pour le projet (l'historique de commits est exigé — on ne
   peut pas soumettre un dépôt vide de dernière minute).
4. [ ] Lancer l'agent sur **1–2 vrais enregistrements** d'appels (ou des exemples audio) pour
   produire des rapports de démonstration.
5. [ ] Enregistrer une **vidéo démo de 2 min** (je vous écris le script).
6. [ ] Remplir et **soumettre** le formulaire Devpost avant le 11 décembre.

Je peux faire : le code, le prompt, le README, le script vidéo, le texte de la page Devpost.
Vous faites : les comptes, l'exécution avec votre clé, l'enregistrement de la vidéo, la soumission.

## Statut

MVP codé et compilable. **Prochaine étape** : dès que vous avez une clé AssemblyAI, on lance sur un
audio de test, on vérifie la sortie, et j'ajuste le prompt jusqu'à un rapport nickel.

## Honnêteté

Gagner reste incertain — des centaines d'équipes participeront. Mais contrairement à tout le reste
de cette série de projets, **celui-ci est réellement à votre portée** : pas de labo, pas de machine,
pas de matériel, pas de clients payants exigés. Du temps, un compte, et un bon produit. C'est le
pari le plus sain.

## Sources

- [Page du hackathon (Devpost)](https://assemblyai-hackathon.devpost.com/)
- [Docs AssemblyAI — transcription](https://www.assemblyai.com/docs/getting-started/transcribe-an-audio-file)
