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
    
    def __init__(self):
        """Initialize the resume analyzer with Groq LLM."""
        self.llm = ChatGroq(
            api_key=config.get_groq_api_key(),
            model=config.LLM_MODEL, 
            temperature=config.TEMPERATURE
        )
        self.output_parser = StrOutputParser()
    
    def _parse_json_response(self, response: str) -> Dict:
        """
        Parse JSON response from LLM and handle common formatting issues.
        
        Args:
            response: String response from LLM
            
        Returns:
            Parsed JSON as dictionary
        """
        # Clean up the response to extract just the JSON part
        if "```json" in response:
            response = response.split("```json")[1].split("```")[0].strip()
        elif "```" in response:
            response = response.split("```")[1].split("```")[0].strip()
        
        # Remove any trailing or leading non-JSON text
        try:
            # Find the first opening brace
            start_idx = response.find('{')
            if start_idx == -1:
                raise ValueError("No JSON object found in response")
            
            # Find the last closing brace
            end_idx = response.rindex('}')
            if end_idx == -1:
                raise ValueError("No closing brace found in response")
            
            # Extract just the JSON part
            json_str = response[start_idx:end_idx+1]
            
            # Parse the JSON
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            print(f"Raw response: {response}")
            # Return empty dict as fallback
            return {}
    
    def extract_keywords_from_job(self, job_description: str) -> Dict[str, List[str]]:
        """
        Extract important keywords from a job description.
        
        Args:
            job_description: The job description text
            
        Returns:
            Dictionary with extracted keywords by category
        """
        prompt = get_keyword_extraction_prompt(job_description)
        
        # Create a runnable sequence
        chain = (
            PromptTemplate.from_template("{prompt}")
            | self.llm
            | self.output_parser
        )
        
        # Run the chain
        result = chain.invoke({"prompt": prompt})
        
        # Parse the JSON response
        try:
            keywords = self._parse_json_response(result)
            return keywords
        except Exception as e:
            print(f"Error extracting keywords: {e}")
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
        
        # Create a runnable sequence
        chain = (
            PromptTemplate.from_template("{prompt}")
            | self.llm
            | self.output_parser
        )
        
        # Run the chain
        evaluation_result = chain.invoke({"prompt": prompt})
        
        # Parse the JSON response
        try:
            evaluation_data = self._parse_json_response(evaluation_result)
            # Return combined results
            return {
                "evaluation": evaluation_result,  # Keep the raw result for reference
                "evaluation_data": evaluation_data,  # Add the structured data
                "keywords": keywords
            }
        except Exception as e:
            print(f"Error parsing evaluation result: {e}")
            # Return raw result if parsing fails
            return {
                "evaluation": evaluation_result,
                "keywords": keywords
            }
    
    def get_detailed_suggestions(
        self,
        resume_text: str,
        job_description: str,
        evaluation_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Get detailed suggestions for improving the resume.
        
        Args:
            resume_text: The extracted text from the resume
            job_description: The job description text
            evaluation_results: Results from the initial evaluation
            
        Returns:
            Detailed suggestions as a dictionary
        """
        # Create suggestions prompt
        prompt = get_improvement_suggestions_prompt(
            resume_text=resume_text,
            job_description=job_description,
            evaluation_results=evaluation_results
        )
        
        # Create a runnable sequence
        chain = (
            PromptTemplate.from_template("{prompt}")
            | self.llm
            | self.output_parser
        )
        
        # Run the chain
        suggestions_result = chain.invoke({"prompt": prompt})
        
        # Parse the JSON response
        try:
            suggestions_data = self._parse_json_response(suggestions_result)
            return suggestions_data
        except Exception as e:
            print(f"Error parsing suggestions: {e}")
            # Return raw result if parsing fails
            return {"summary": suggestions_result} 