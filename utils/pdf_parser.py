"""
Utilities for parsing resume files (PDF and DOCX).
"""
import io
from typing import Optional, BinaryIO

from pypdf import PdfReader
import docx


def extract_text_from_pdf(file_content: BinaryIO) -> str:
    """
    Extract text from a PDF file.
    
    Args:
        file_content: File-like object containing PDF data
        
    Returns:
        Extracted text as a string
    """
    pdf_reader = PdfReader(file_content)
    text = ""
    
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n\n"
    
    return text.strip()


def extract_text_from_docx(file_content: BinaryIO) -> str:
    """
    Extract text from a DOCX file.
    
    Args:
        file_content: File-like object containing DOCX data
        
    Returns:
        Extracted text as a string
    """
    doc = docx.Document(file_content)
    text = ""
    
    for paragraph in doc.paragraphs:
        if paragraph.text:
            text += paragraph.text + "\n"
    
    return text.strip()


def extract_text_from_resume(file_content: BinaryIO, file_type: str) -> str:
    """
    Extract text from a resume file based on its type.
    
    Args:
        file_content: File-like object containing the resume
        file_type: Type of file ('pdf' or 'docx')
        
    Returns:
        Extracted text as a string
        
    Raises:
        ValueError: If file_type is not supported
    """
    if file_type.lower() == "pdf":
        return extract_text_from_pdf(file_content)
    elif file_type.lower() == "docx":
        return extract_text_from_docx(file_content)
    else:
        raise ValueError(f"Unsupported file type: {file_type}") 