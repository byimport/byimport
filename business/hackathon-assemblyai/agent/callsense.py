"""CallSense — agent IA qui transforme un enregistrement d'appel en plan d'action.

Pipeline :
  1. Transcription de l'appel via AssemblyAI (avec identification des interlocuteurs + sentiment).
  2. Analyse LLM de la transcription via LeMUR → résumé, objections, actions, e-mail de relance,
     coaching du commercial (sortie JSON structurée).
  3. Génération d'un rapport lisible (Markdown) + du JSON brut.

Usage :
    export ASSEMBLYAI_API_KEY=...          # clé obtenue sur assemblyai.com (niveau gratuit)
    python -m agent.callsense chemin/vers/appel.mp3 --out rapport
    # ou une URL publique :
    python -m agent.callsense https://exemple.com/appel.mp3 --out rapport

Sortie : rapport.json + rapport.md
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys

import assemblyai as aai

from .prompts import ANALYSIS_PROMPT


def transcribe(source: str) -> aai.Transcript:
    """Transcrit un fichier local ou une URL, avec diarisation et détection de langue."""
    config = aai.TranscriptionConfig(
        speaker_labels=True,       # sépare les interlocuteurs (commercial / client)
        language_detection=True,   # gère les appels FR/EN sans config manuelle
        sentiment_analysis=True,   # sentiment par phrase, pour recouper l'analyse LLM
    )
    transcript = aai.Transcriber().transcribe(source, config=config)
    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(f"Échec de transcription : {transcript.error}")
    return transcript


def analyze(transcript: aai.Transcript) -> dict:
    """Applique le LLM (LeMUR) sur la transcription et renvoie l'analyse en dict.

    LeMUR est branché sur la transcription : il raisonne sur le texte réel de l'appel, pas sur un
    copier-coller. On force une sortie JSON et on la parse défensivement.
    """
    result = transcript.lemur.task(
        prompt=ANALYSIS_PROMPT,
        final_model=aai.LemurModel.claude3_5_sonnet,
    )
    raw = result.response.strip()
    # LeMUR renvoie parfois le JSON entouré de ```; on nettoie avant de parser.
    if raw.startswith("```"):
        raw = raw.split("```", 2)[1].removeprefix("json").strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # on ne perd pas le travail : on renvoie le texte brut sous une clé dédiée
        return {"_unparsed": raw}


def speaker_breakdown(transcript: aai.Transcript) -> list[dict]:
    """Renvoie la conversation tour par tour (qui a dit quoi)."""
    if not transcript.utterances:
        return [{"speaker": "?", "text": transcript.text or ""}]
    return [{"speaker": u.speaker, "text": u.text} for u in transcript.utterances]


def render_markdown(analysis: dict, turns: list[dict]) -> str:
    """Génère un rapport Markdown lisible pour un humain (le livrable montrable au jury/client)."""
    if "_unparsed" in analysis:
        return f"# Rapport CallSense\n\n> Analyse brute (JSON non parsé) :\n\n{analysis['_unparsed']}\n"

    coaching = analysis.get("rep_coaching", {})
    lines = [
        "# Rapport d'appel — CallSense",
        "",
        f"**Résumé :** {analysis.get('summary', '—')}",
        f"**Intention client :** {analysis.get('customer_intent', '—')}",
        f"**Sentiment :** {analysis.get('sentiment', '—')}  ·  "
        f"**Risque de perte :** {analysis.get('risk_of_loss', '—')}",
        "",
        "## Objections",
        *([f"- {o}" for o in analysis.get("objections", [])] or ["- (aucune détectée)"]),
        "",
        "## Actions à faire",
        *([
            f"- **[{a.get('priority', '?')}]** ({a.get('owner', '?')}) {a.get('task', '')}"
            for a in analysis.get("action_items", [])
        ] or ["- (aucune)"]),
        "",
        "## Coaching du commercial",
        f"**Score : {coaching.get('score', '—')}/100**",
        "",
        "*Points forts :*",
        *([f"- {s}" for s in coaching.get("strengths", [])] or ["- —"]),
        "",
        "*À améliorer :*",
        *([f"- {i}" for i in coaching.get("improvements", [])] or ["- —"]),
        "",
        "## E-mail de relance (prêt à envoyer)",
        "",
        "```",
        analysis.get("followup_email", "—"),
        "```",
        "",
        "## Transcription (tour par tour)",
        *[f"- **{t['speaker']}** : {t['text']}" for t in turns],
    ]
    return "\n".join(lines)


def run(source: str, out_stem: pathlib.Path) -> None:
    if not os.environ.get("ASSEMBLYAI_API_KEY"):
        sys.exit("Définissez ASSEMBLYAI_API_KEY (clé gratuite sur assemblyai.com).")
    aai.settings.api_key = os.environ["ASSEMBLYAI_API_KEY"]

    print("→ Transcription…", file=sys.stderr)
    transcript = transcribe(source)
    print("→ Analyse LLM (LeMUR)…", file=sys.stderr)
    analysis = analyze(transcript)
    turns = speaker_breakdown(transcript)

    out_stem.parent.mkdir(parents=True, exist_ok=True)
    out_stem.with_suffix(".json").write_text(
        json.dumps({"analysis": analysis, "turns": turns}, ensure_ascii=False, indent=2)
    )
    out_stem.with_suffix(".md").write_text(render_markdown(analysis, turns))
    print(f"✓ Écrit {out_stem.with_suffix('.json')} et {out_stem.with_suffix('.md')}", file=sys.stderr)


def main() -> None:
    p = argparse.ArgumentParser(description="CallSense — appel audio → plan d'action IA")
    p.add_argument("source", help="Chemin d'un fichier audio local ou URL publique")
    p.add_argument("--out", type=pathlib.Path, default=pathlib.Path("outputs/rapport"),
                   help="Préfixe des fichiers de sortie (déf. outputs/rapport)")
    args = p.parse_args()
    run(args.source, args.out)


if __name__ == "__main__":
    main()
