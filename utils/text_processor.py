"""
Text processing utilities for resume and job description analysis.
"""
import re
from typing import List, Set


def clean_text(text: str) -> str:
    """
    Clean and normalize text by removing extra whitespace and special characters.
    
    Args:
        text: Input text to clean
        
    Returns:
        Cleaned text
    """
    # Replace multiple whitespace with single space
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters that aren't relevant
    text = re.sub(r'[^\w\s.,;:!?()-]', '', text)
    
    return text.strip()


def extract_skills(text: str) -> Set[str]:
    """
    Extract potential skills from text using common patterns.
    This is a simple implementation and not as accurate as LLM-based extraction.
    
    Args:
        text: Input text to extract skills from
        
    Returns:
        Set of extracted skills
    """
    # Common technical skills (simplified list)
    common_skills = {
        'python', 'java', 'javascript', 'typescript', 'html', 'css', 'react', 
        'angular', 'vue', 'node', 'express', 'django', 'flask', 'spring', 
        'sql', 'nosql', 'mongodb', 'postgresql', 'mysql', 'oracle', 'aws', 
        'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'ci/cd',
        'machine learning', 'deep learning', 'ai', 'data science', 'nlp',
        'computer vision', 'tensorflow', 'pytorch', 'keras', 'pandas', 
        'numpy', 'scikit-learn', 'tableau', 'power bi', 'excel', 'word',
        'powerpoint', 'photoshop', 'illustrator', 'figma', 'sketch',
        'leadership', 'communication', 'teamwork', 'problem solving',
        'critical thinking', 'time management', 'project management',
        'agile', 'scrum', 'kanban', 'jira', 'confluence', 'slack'
    }
    
    # Convert text to lowercase for case-insensitive matching
    text_lower = text.lower()
    
    # Find all skills in the text
    found_skills = {skill for skill in common_skills if skill in text_lower}
    
    return found_skills


def calculate_keyword_density(text: str, keywords: List[str]) -> float:
    """
    Calculate the density of keywords in the text.
    
    Args:
        text: Input text
        keywords: List of keywords to check
        
    Returns:
        Keyword density as a percentage
    """
    if not text or not keywords:
        return 0.0
    
    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)
    total_words = len(words)
    
    if total_words == 0:
        return 0.0
    
    keyword_count = 0
    for keyword in keywords:
        keyword_lower = keyword.lower()
        keyword_count += sum(1 for word in words if word == keyword_lower)
    
    return (keyword_count / total_words) * 100.0 