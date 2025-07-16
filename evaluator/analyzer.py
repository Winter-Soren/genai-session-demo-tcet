"""
Core resume analysis logic using LangChain and Groq LLM.
"""
import json
from typing import Dict, Any, List

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

import config
from evaluator.prompts import (
    get_resume_evaluation_prompt,
    get_keyword_extraction_prompt,
    get_improvement_suggestions_prompt
)


class ResumeAnalyzer:
    """
    Analyzes resumes against job descriptions using LLMs.
    """
    
    # TODO: Add the methods to analyze the resume
   
    pass