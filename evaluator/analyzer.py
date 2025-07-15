"""
Core resume analysis logic using LangChain and Groq LLM.
"""
import json
from typing import Dict, Any, List

from langchain.chains import LLMChain
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

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
    
    def __init__(self):
        """Initialize the resume analyzer with Groq LLM."""
        self.llm = ChatGroq(
            api_key=config.get_groq_api_key(),
            model=config.LLM_MODEL, 
            temperature=config.TEMPERATURE
        )
    
    def extract_keywords_from_job(self, job_description: str) -> Dict[str, List[str]]:
        """
        Extract important keywords from a job description.
        
        Args:
            job_description: The job description text
            
        Returns:
            Dictionary with extracted keywords by category
        """
        prompt = get_keyword_extraction_prompt(job_description)
        
        # Create a simple chain
        chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate.from_template("{prompt}"),
            verbose=False
        )
        
        # Run the chain
        result = chain.run(prompt=prompt)
        
        # Parse the JSON response
        try:
            # The LLM might include markdown code block markers, so we need to clean those
            if "```json" in result:
                result = result.split("```json")[1].split("```")[0].strip()
            elif "```" in result:
                result = result.split("```")[1].split("```")[0].strip()
            
            keywords = json.loads(result)
            return keywords
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return {
                "technical_skills": [],
                "soft_skills": [],
                "industry_terms": [],
                "action_verbs": []
            }
    
    def evaluate_resume(
        self,
        resume_text: str,
        job_description: str,
        company_name: str,
        role_name: str
    ) -> Dict[str, Any]:
        """
        Evaluate a resume against a job description.
        
        Args:
            resume_text: The extracted text from the resume
            job_description: The job description text
            company_name: The name of the company
            role_name: The name of the role
            
        Returns:
            Dictionary with evaluation results
        """
        # First, extract keywords from job description
        keywords = self.extract_keywords_from_job(job_description)
        
        # Create evaluation prompt
        prompt = get_resume_evaluation_prompt(
            resume_text=resume_text,
            job_description=job_description,
            company_name=company_name,
            role_name=role_name,
            evaluation_criteria=config.EVALUATION_CRITERIA
        )
        
        # Create a simple chain
        chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate.from_template("{prompt}"),
            verbose=False
        )
        
        # Run the chain
        evaluation_result = chain.run(prompt=prompt)
        
        # Return combined results
        return {
            "evaluation": evaluation_result,
            "keywords": keywords
        }
    
    def get_detailed_suggestions(
        self,
        resume_text: str,
        job_description: str,
        evaluation_results: Dict[str, Any]
    ) -> str:
        """
        Get detailed suggestions for improving the resume.
        
        Args:
            resume_text: The extracted text from the resume
            job_description: The job description text
            evaluation_results: Results from the initial evaluation
            
        Returns:
            Detailed suggestions as a string
        """
        # Create suggestions prompt
        prompt = get_improvement_suggestions_prompt(
            resume_text=resume_text,
            job_description=job_description,
            evaluation_results=evaluation_results
        )
        
        # Create a simple chain
        chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate.from_template("{prompt}"),
            verbose=False
        )
        
        # Run the chain
        suggestions = chain.run(prompt=prompt)
        
        return suggestions 