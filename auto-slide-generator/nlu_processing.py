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
        segments = [seg.strip() for seg in transcript.split("\\n\\n") if seg.strip()]
        categorized_segments = {cat: [] for cat in CATEGORIES}

        if not segments:
            return categorized_segments

        # Batch classify all segments at once
        results = self.classifier(segments, candidate_labels=CATEGORIES)

        # results is a list of dicts, one per segment
        for segment, result in zip(segments, results):
            top_label = result['labels'][0]
            categorized_segments[top_label].append(segment)

        return categorized_segments
