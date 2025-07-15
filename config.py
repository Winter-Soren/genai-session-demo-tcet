"""
Configuration settings for the Resume Evaluator application.
"""
import os
from typing import Dict
import dotenv

dotenv.load_dotenv()

# LLM Configuration
LLM_MODEL = "llama3-70b-8192"  # Groq's LLama 3 model
TEMPERATURE = 0.2  # Lower temperature for more deterministic outputs

# Resume Evaluation Settings
EVALUATION_CRITERIA = [
    "Relevance to Job Description",
    "Skills Match",
    "Experience Match",
    "Education Match",
    "Overall Format and Structure",
    "Action Verbs and Impact",
    "Keyword Optimization"
]

# Scoring weights for different criteria (must sum to 1.0)
CRITERIA_WEIGHTS: Dict[str, float] = {
    "Relevance to Job Description": 0.25,
    "Skills Match": 0.20,
    "Experience Match": 0.20,
    "Education Match": 0.10,
    "Overall Format and Structure": 0.10,
    "Action Verbs and Impact": 0.10,
    "Keyword Optimization": 0.05
}

# UI Configuration
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB max file size
ALLOWED_FILE_TYPES = ["pdf", "docx"]

# API Keys
def get_groq_api_key() -> str:
    """Get Groq API key from environment variable."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY environment variable not set. "
            "Please set it with your Groq API key."
        )
    return api_key 