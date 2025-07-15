"""
LLM prompts for resume evaluation.
"""
from typing import Dict, List


def get_resume_evaluation_prompt(
    resume_text: str,
    job_description: str,
    company_name: str,
    role_name: str,
    evaluation_criteria: List[str]
) -> str:
    """
    Generate a prompt for evaluating a resume against a job description.
    
    Args:
        resume_text: The extracted text from the resume
        job_description: The job description text
        company_name: The name of the company
        role_name: The name of the role
        evaluation_criteria: List of criteria to evaluate
        
    Returns:
        Formatted prompt string
    """
    criteria_str = "\n".join([f"- {criterion}" for criterion in evaluation_criteria])
    
    prompt = f"""
You are an expert resume reviewer and career coach with extensive experience in technical hiring.

TASK: Evaluate the provided resume for the {role_name} position at {company_name} based on the job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

EVALUATION CRITERIA:
{criteria_str}

For each criterion, provide:
1. A score from 1-10 (where 10 is perfect)
2. A brief explanation for the score
3. Specific suggestions for improvement

Then, provide an overall assessment including:
1. Overall match percentage (0-100%)
2. Top 3 strengths of the resume
3. Top 3 areas for improvement
4. Key missing keywords or skills from the job description
5. Suggested action items prioritized by impact

Format your response as a structured evaluation with clear sections and bullet points.
"""
    return prompt


def get_keyword_extraction_prompt(job_description: str) -> str:
    """
    Generate a prompt for extracting important keywords from a job description.
    
    Args:
        job_description: The job description text
        
    Returns:
        Formatted prompt string
    """
    prompt = f"""
You are an expert in technical recruitment and keyword optimization for job applications.

TASK: Extract the most important keywords and skills from the following job description.

JOB DESCRIPTION:
{job_description}

Please provide:
1. A list of the top 15 technical skills mentioned or implied in the job description
2. A list of the top 10 soft skills mentioned or implied in the job description
3. A list of the top 5 industry-specific terms or knowledge areas
4. A list of 5 action verbs that would be effective on a resume for this role

Format your response as JSON with the following structure:
{{
    "technical_skills": ["skill1", "skill2", ...],
    "soft_skills": ["skill1", "skill2", ...],
    "industry_terms": ["term1", "term2", ...],
    "action_verbs": ["verb1", "verb2", ...]
}}
"""
    return prompt


def get_improvement_suggestions_prompt(
    resume_text: str,
    job_description: str,
    evaluation_results: Dict
) -> str:
    """
    Generate a prompt for detailed improvement suggestions based on evaluation.
    
    Args:
        resume_text: The extracted text from the resume
        job_description: The job description text
        evaluation_results: Results from the initial evaluation
        
    Returns:
        Formatted prompt string
    """
    prompt = f"""
You are an expert resume writer with extensive experience helping candidates optimize their resumes for specific job applications.

TASK: Provide detailed, actionable suggestions to improve the resume for the specific job.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

PREVIOUS EVALUATION RESULTS:
{evaluation_results}

Please provide:
1. 3-5 specific content suggestions (exact phrases or bullet points to add)
2. 2-3 structural improvements
3. Specific wording changes to better align with the job description
4. A before/after example of one section of the resume that could be improved

Format your response in clear sections with specific, actionable advice that the candidate can immediately implement.
"""
    return prompt 