"""
Module for AI model integration to generate slide content using free alternative APIs or local models.
Supports switching between models for performance optimization.
"""

import requests
import torch

# Import transformers for local model usage
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

# Define available AI models/APIs
AI_MODELS = {
    "huggingface_gpt2": {
        "url": "https://api-inference.huggingface.co/models/gpt2",
        "token": "",  # Add token if needed
    },
    "google_flan_t5_small": {
        "url": "https://api-inference.huggingface.co/models/google/flan-t5-small",
        "token": "",
    },
    # Add more models here as needed
}

# Remove deepseek model identifier and replace with CPU-compatible summarization models
LOCAL_MODELS = {
    "t5_small": "t5-small",
    "distilbart_cnn": "sshleifer/distilbart-cnn-12-6",
}

# Select model to use (default to CPU-compatible summarization model)
SELECTED_MODEL = "t5_small"

headers = {"Authorization": f"Bearer {AI_MODELS[SELECTED_MODEL]['token']}"} if SELECTED_MODEL in AI_MODELS and AI_MODELS[SELECTED_MODEL]['token'] else {}

def get_device():
    # Force CPU usage to avoid MPS instability on Mac Apple Silicon
    return "cpu"

def generate_slide_content_summary(data_summary):
    """Generate slide content summary using CPU-compatible transformers summarization pipeline."""
    import logging
    from transformers import pipeline

    logging.debug(f"Input data summary: {data_summary}")

    try:
        # Remove "summarize:" prefix to avoid confusion
        prompt = data_summary.strip()
        if len(prompt) < 20:
            # If input too short, return as is
            logging.debug("Input too short for summarization, returning original text")
            return prompt

        summarizer = pipeline("summarization", model=LOCAL_MODELS[SELECTED_MODEL], device=-1)
        summary = summarizer(prompt, max_length=150, min_length=20, do_sample=False)[0]['summary_text']
        logging.debug(f"Generated summary: {summary}")

        # Fallback for empty or low-quality output
        if not summary or len(summary.strip()) < 10:
            logging.warning("Summary too short or empty, retrying with default model")
            fallback_summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", device=-1)
            summary = fallback_summarizer(prompt, max_length=150, min_length=20, do_sample=False)[0]['summary_text']
            logging.debug(f"Fallback summary: {summary}")

        return summary
    except Exception as e:
        logging.error(f"Error during model summarization: {e}")
        return None  # Return None to indicate failure

# Removed old generate_slide_content_summary function as replaced by new CPU-compatible version above
