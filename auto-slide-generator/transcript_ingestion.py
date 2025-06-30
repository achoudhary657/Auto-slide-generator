import io
from typing import Union
from docx import Document

def parse_txt(file_content: bytes) -> str:
    return file_content.decode('utf-8')

def parse_docx(file_content: bytes) -> str:
    """
    Parse .docx file content bytes and extract full text.
    """
    file_stream = io.BytesIO(file_content)
    document = Document(file_stream)
    full_text = []
    for para in document.paragraphs:
        full_text.append(para.text)
    return '\\n'.join(full_text)
