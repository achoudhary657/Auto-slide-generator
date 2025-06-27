"""
Module for Natural Language Understanding (NLU) to parse and segment meeting transcripts.
Uses Hugging Face transformers for semantic segmentation and classification.
"""

from typing import Dict, List
from transformers import pipeline
import torch

# Define categories for segmentation
CATEGORIES = [
    "Introductions",
    "Client Goals",
    "Pain Points",
    "Technical Constraints",
    "Suggested Next Steps"
]

class TranscriptNLU:
    def __init__(self):
        # Use zero-shot-classification pipeline for flexible category assignment
        self.classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

    def segment_transcript(self, transcript: str) -> Dict[str, List[str]]:
        """
        Segment the transcript into logical categories.
        Returns a dictionary mapping category to list of text segments.
        """
        segments = transcript.split("\\n\\n")  # naive paragraph split
        categorized_segments = {cat: [] for cat in CATEGORIES}

        for segment in segments:
            if not segment.strip():
                continue
            result = self.classifier(segment, candidate_labels=CATEGORIES)
            top_label = result['labels'][0]
            categorized_segments[top_label].append(segment.strip())

        return categorized_segments
