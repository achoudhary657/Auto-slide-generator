"""
Module for AI model integration to generate slide content using a free alternative API.
"""

import requests
import torch

FREE_AI_API_URL = "https://api-inference.huggingface.co/models/gpt2"  # Example free model on Hugging Face
FREE_AI_API_TOKEN = ""  # If needed, user can add token here

headers = {"Authorization": f"Bearer {FREE_AI_API_TOKEN}"} if FREE_AI_API_TOKEN else {}

def get_device():
    if torch.backends.mps.is_available() and torch.backends.mps.is_built():
        return "mps"
    elif torch.cuda.is_available():
        return "cuda"
    else:
        return "cpu"

def generate_slide_content_summary(data_summary):
    """Generate slide content summary using a free AI API or fallback to local summarization."""
    import logging
    logging.basicConfig(level=logging.DEBUG)
    device = get_device()
    logging.debug(f"Device detected for AI generation: {device}")
    # If device is mps or cuda, fallback to API to avoid hangs
    if device in ["mps", "cuda"]:
        prompt = f"Generate a concise and clear slide content summary based on this data summary:\n{data_summary}"
        payload = {
            "inputs": prompt,
            "parameters": {"max_length": 150, "temperature": 0.7},
        }
        try:
            response = requests.post(FREE_AI_API_URL, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            logging.debug(f"AI API response: {result}")
            if isinstance(result, list) and "generated_text" in result[0]:
                generated_text = result[0]["generated_text"].strip()
                logging.debug(f"Generated text from AI API: {generated_text}")
                return generated_text
            else:
                logging.error("Unexpected response format from AI API.")
                return "Error: Unexpected response format from AI API."
        except Exception as e:
            logging.error(f"AI API call failed: {e}")
            # Fallback to local summarization on error
            from transformers import pipeline
            summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)
            summary = summarizer(data_summary, max_length=150, min_length=40, do_sample=False)[0]['summary_text']
            logging.debug(f"Generated summary from local summarizer (fallback): {summary}")
            return summary
    else:
        # Local summarization fallback (if CPU)
        from transformers import pipeline
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)
        summary = summarizer(data_summary, max_length=150, min_length=40, do_sample=False)[0]['summary_text']
        logging.debug(f"Generated summary from local summarizer: {summary}")
        return summary
