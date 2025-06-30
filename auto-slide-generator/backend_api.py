from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from auto_slide_generator import transcript_ingestion, slide_text_generation

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SlideContent(BaseModel):
    title: str
    subtitle: Optional[str] = None
    bullets: List[str]

class SlideDeck(BaseModel):
    slides: List[SlideContent]

@app.post("/upload/")
async def upload_transcript(file: UploadFile = File(None), text: Optional[str] = Form(None)):
    """
    Accept transcript file (.txt or .docx) or raw text input.
    Returns extracted transcript text.
    """
    transcript_text = ""
    if file:
        contents = await file.read()
        if file.filename.endswith(".txt"):
            transcript_text = contents.decode("utf-8")
        elif file.filename.endswith(".docx"):
            transcript_text = transcript_ingestion.parse_docx(contents)
        else:
            return {"error": "Unsupported file type. Please upload .txt or .docx files."}
    elif text:
        transcript_text = text
    else:
        return {"error": "No transcript file or text provided."}
    return {"transcript": transcript_text}

@app.post("/process/")
async def process_transcript(transcript: str = Form(...)):
    """
    Process transcript text: summarize and segment into structured slide content.
    """
    # Placeholder segmentation logic; replace with real NLP segmentation
    client_name = "Client Name"
    project_name = "Project Proposal"
    objectives = transcript[:min(len(transcript), 500)]
    pain_points = [transcript[500:1000]] if len(transcript) > 500 else []
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

    return {"slides": slides}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
