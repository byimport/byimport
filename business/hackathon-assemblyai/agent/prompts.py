"""Prompts LeMUR pour CallSense. Séparés du code pour être itérés facilement.

LeMUR applique un LLM sur la transcription. On demande une sortie JSON stricte pour pouvoir la
parser et générer un rapport structuré (pas du texte libre non exploitable).
"""

ANALYSIS_PROMPT = """Tu es un analyste commercial expert. À partir de la transcription d'un appel
(commercial ou support) ci-dessus, produis UNIQUEMENT un objet JSON valide, sans texte autour,
avec exactement ces clés :

{
  "summary": "résumé de l'appel en 3 phrases maximum",
  "customer_intent": "ce que le client veut vraiment, en une phrase",
  "objections": ["liste des objections/freins exprimés par le client"],
  "action_items": [
    {"owner": "commercial|client", "task": "action concrète à faire", "priority": "haute|moyenne|basse"}
  ],
  "sentiment": "positif|neutre|négatif — ressenti global du client",
  "risk_of_loss": "faible|moyen|élevé — risque de perdre ce client/deal",
  "followup_email": "brouillon d'e-mail de relance prêt à envoyer, ton professionnel, en français",
  "rep_coaching": {
    "score": 0,
    "strengths": ["ce que le commercial a bien fait"],
    "improvements": ["ce que le commercial doit améliorer"]
  }
}

Le score de coaching est un entier de 0 à 100. N'invente aucun fait absent de la transcription."""
