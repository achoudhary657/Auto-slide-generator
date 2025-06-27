"""
Module for ingesting meeting transcripts from plain text and .docx files.
"""

import os
from typing import Optional

def read_txt(file_path: str) -> str:
    """Read plain text transcript from a .txt file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def read_docx(file_path: str) -> str:
    """Read transcript text from a .docx file."""
    from docx import Document
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def ingest_transcript(file_path: str) -> Optional[str]:
    """Ingest transcript from supported file types (.txt, .docx)."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Transcript file not found: {file_path}")
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.txt':
        return read_txt(file_path)
    elif ext == '.docx':
        return read_docx(file_path)
    else:
        raise ValueError(f"Unsupported transcript file type: {ext}")
