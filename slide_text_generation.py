"""
Module for generating slide text content following the specified slide structure and formatting.
"""

from typing import List, Dict

def generate_cover_slide(client_name: str, project_name: str = "Proposal") -> Dict[str, str]:
    title = f"{client_name}"
    subtitle = f"Proposal for {project_name}"
    return {"title": title, "subtitle": subtitle, "bullets": []}

def generate_objectives_slide(objectives: str) -> Dict[str, List[str]]:
    bullets = [obj.strip() for obj in objectives.split('.') if obj.strip()]
    return {"title": "Client Objectives", "bullets": bullets}

def generate_pain_points_slide(pain_points: List[str]) -> Dict[str, List[str]]:
    return {"title": "Pain Points / Challenges", "bullets": pain_points}

def generate_phases_overview_slide(phases: List[Dict[str, str]]) -> Dict[str, List[str]]:
    bullets = [f"{phase['title']}: {phase['description']}" if phase['description'] else phase['title'] for phase in phases]
    return {"title": "Proposed Solution (Phases Overview)", "bullets": bullets}

def generate_phase_slide(phase: Dict[str, str], timeframe: str = "") -> Dict[str, List[str]]:
    title = phase.get("title", "Phase")
    subtitle = timeframe
    bullets = phase.get("activities", [])
    return {"title": title, "subtitle": subtitle, "bullets": bullets}

def generate_expected_outcomes_slide(expected_outcomes: str) -> Dict[str, List[str]]:
    bullets = [outcome.strip() for outcome in expected_outcomes.split('.') if outcome.strip()]
    return {"title": "Expected Outcomes", "bullets": bullets}

def generate_next_steps_slide(next_steps: List[str]) -> Dict[str, List[str]]:
    return {"title": "Next Steps / CTA", "bullets": next_steps}
