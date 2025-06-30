"""
Module for generating slide text content following the specified slide structure and formatting.
"""

from typing import List, Dict
from ai_integration import generate_slide_content_summary

def generate_cover_slide(client_name: str, project_name: str = "Proposal") -> Dict[str, str]:
    title = f"{client_name}"
    subtitle = f"Proposal for {project_name}"
    return {"title": title, "subtitle": subtitle, "bullets": []}

def generate_objectives_slide(objectives: str) -> Dict[str, List[str]]:
    # Use AI to generate detailed bullet points from objectives text
    detailed_content = generate_slide_content_summary(objectives)
    if detailed_content:
        bullets = [sentence.strip() for sentence in detailed_content.replace('\n', '. ').split('.') if sentence.strip()]
        if not bullets:
            bullets = [detailed_content.strip()]
    else:
        bullets = []
    return {"title": "Client Objectives", "bullets": bullets}

def generate_pain_points_slide(pain_points: List[str]) -> Dict[str, List[str]]:
    # Combine pain points into a single string and generate detailed content
    combined_text = " ".join(pain_points)
    detailed_content = generate_slide_content_summary(combined_text)
    if detailed_content:
        bullets = [sentence.strip() for sentence in detailed_content.replace('\n', '. ').split('.') if sentence.strip()]
        if not bullets:
            bullets = [detailed_content.strip()]
    else:
        bullets = []
    return {"title": "Pain Points / Challenges", "bullets": bullets}

def generate_phases_overview_slide(phases: List[Dict[str, str]]) -> Dict[str, List[str]]:
    combined_text = " ".join([f"{phase['title']}: {phase['description']}" if phase['description'] else phase['title'] for phase in phases])
    detailed_content = generate_slide_content_summary(combined_text)
    if detailed_content:
        bullets = [sentence.strip() for sentence in detailed_content.replace('\n', '. ').split('.') if sentence.strip()]
        if not bullets:
            bullets = [detailed_content.strip()]
    else:
        bullets = []
    return {"title": "Proposed Solution (Phases Overview)", "bullets": bullets}

def generate_phase_slide(phase: Dict[str, str], timeframe: str = "") -> Dict[str, List[str]]:
    title = phase.get("title", "Phase")
    subtitle = timeframe
    activities_text = " ".join(phase.get("activities", []))
    detailed_content = generate_slide_content_summary(activities_text)
    bullets = [line.strip() for line in detailed_content.split('\n') if line.strip()]
    return {"title": title, "subtitle": subtitle, "bullets": bullets}

def generate_expected_outcomes_slide(expected_outcomes: str) -> Dict[str, List[str]]:
    detailed_content = generate_slide_content_summary(expected_outcomes)
    bullets = [line.strip() for line in detailed_content.split('\n') if line.strip()]
    return {"title": "Expected Outcomes", "bullets": bullets}

def generate_next_steps_slide(next_steps: List[str]) -> Dict[str, List[str]]:
    combined_text = " ".join(next_steps)
    detailed_content = generate_slide_content_summary(combined_text)
    bullets = [line.strip() for line in detailed_content.split('\n') if line.strip()]
    return {"title": "Next Steps / CTA", "bullets": bullets}
