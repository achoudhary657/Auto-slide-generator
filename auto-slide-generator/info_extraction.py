"""
Module for extracting structured insights from segmented transcript text.
"""

from typing import Dict, List, Optional
import re

def extract_client_name(introductions: List[str]) -> Optional[str]:
    """
    Extract client name from introductions segment using simple heuristics.
    """
    for intro in introductions:
        match = re.search(r"my name is ([A-Za-z ]+)", intro, re.I)
        if match:
            return match.group(1).strip()
        match = re.search(r"this is ([A-Za-z ]+)", intro, re.I)
        if match:
            return match.group(1).strip()
    return None

def extract_objectives(client_goals: List[str]) -> str:
    """
    Combine client goals into a concise objective statement.
    """
    return " ".join(client_goals).strip()

def extract_pain_points(pain_points: List[str]) -> List[str]:
    """
    Extract key pain points as bullet points.
    """
    from transformers import pipeline
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    points = []
    for text in pain_points:
        # Summarize each pain point text to a concise bullet
        summary = summarizer(text, max_length=50, min_length=10, do_sample=False)[0]['summary_text']
        points.append(summary.strip())
    return points

def extract_phases(suggested_next_steps: List[str]) -> List[Dict[str, str]]:
    """
    Extract proposed solution phases with optional descriptions.
    Returns list of dicts with 'title' and 'description'.
    """
    phases = []
    for step in suggested_next_steps:
        # Improved heuristic: split by semicolon or newline, then by colon or dash for title and description
        phase_entries = re.split(r"[;\n]+", step)
        for entry in phase_entries:
            parts = re.split(r"[:\-]+", entry, maxsplit=1)
            title = parts[0].strip() if parts else ""
            description = parts[1].strip() if len(parts) > 1 else ""
            if title:
                phases.append({"title": title, "description": description})
    # Limit to 3-6 phases
    return phases[:6]

def extract_expected_outcomes(outcomes: List[str]) -> str:
    """
    Combine expected outcomes into a concise statement.
    """
    from transformers import pipeline
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    combined_text = " ".join(outcomes).strip()
    if not combined_text:
        return ""

    summary = summarizer(combined_text, max_length=100, min_length=20, do_sample=False)[0]['summary_text']
    return summary.strip()

def extract_structured_insights(segmented_text: Dict[str, List[str]]) -> Dict[str, object]:
    """
    Extract all structured insights from segmented transcript.
    """
    client_name = extract_client_name(segmented_text.get("Introductions", []))
    objectives = extract_objectives(segmented_text.get("Client Goals", []))
    pain_points = extract_pain_points(segmented_text.get("Pain Points", []))
    phases = extract_phases(segmented_text.get("Suggested Next Steps", []))
    outcomes = extract_expected_outcomes(segmented_text.get("Suggested Next Steps", []))

    return {
        "client_name": client_name or "Client",
        "objectives": objectives,
        "pain_points": pain_points,
        "phases": phases,
        "expected_outcomes": outcomes
    }
