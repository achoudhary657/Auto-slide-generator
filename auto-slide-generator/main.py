"""
Main script to run the automated slide deck generator.
"""

import os
import sys
from auto_slide_generator import transcript_ingestion, slide_text_generation, ai_integration
from slide_generation import create_presentation, add_title_slide, add_content_slide, save_presentation

def generate_slide_deck_from_transcript(file_path: str, output_path: str):
    # Determine file type and parse transcript
    if file_path.endswith(".txt"):
        with open(file_path, "rb") as f:
            transcript_text = transcript_ingestion.parse_txt(f.read())
    elif file_path.endswith(".docx"):
        with open(file_path, "rb") as f:
            transcript_text = transcript_ingestion.parse_docx(f.read())
    else:
        print("Unsupported file type. Please provide a .txt or .docx file.")
        return

    # Segment transcript and generate slide content
    client_name = "Client Name"
    project_name = "Project Proposal"
    objectives = transcript_text[:min(len(transcript_text), 500)]
    pain_points = [transcript_text[500:1000]] if len(transcript_text) > 500 else []
    phases = [{"title": "Phase 1", "description": "Initial phase", "activities": ["Activity 1", "Activity 2"]}]
    expected_outcomes = "Expected outcomes based on the transcript."
    next_steps = ["Next step 1", "Next step 2"]

    slides = []
    slides.append(slide_text_generation.generate_cover_slide(client_name, project_name))
    slides.append(slide_text_generation.generate_objectives_slide(objectives))
    slides.append(slide_text_generation.generate_pain_points_slide(pain_points))
    slides.append(slide_text_generation.generate_phases_overview_slide(phases))
    for phase in phases:
        slides.append(slide_text_generation.generate_phase_slide(phase))
    slides.append(slide_text_generation.generate_expected_outcomes_slide(expected_outcomes))
    slides.append(slide_text_generation.generate_next_steps_slide(next_steps))

    # Create presentation
    prs = create_presentation()
    add_title_slide(prs, slides[0]["title"], slides[0]["subtitle"])
    for slide in slides[1:]:
        add_content_slide(prs, slide["title"], slide.get("bullets", []))
    save_presentation(prs, output_path)
    print(f"Presentation saved to {output_path}")

def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py <transcript_file> <output_pptx>")
        return
    transcript_file = sys.argv[1]
    output_file = sys.argv[2]
    generate_slide_deck_from_transcript(transcript_file, output_file)

if __name__ == "__main__":
    main()
