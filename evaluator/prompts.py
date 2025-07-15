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

Evaluate the resume and return ONLY a JSON object with the following structure:
{{
    "criteria_scores": {{
        "Relevance to Job Description": {{
            "score": 7,
            "explanation": "Brief explanation for the score",
            "suggestion": "Specific suggestion for improvement"
        }},
        // Include all criteria with their scores (1-10), explanations, and suggestions
    }},
    "overall_match_percentage": 75,
    "strengths": [
        "Strength 1",
        "Strength 2",
        "Strength 3"
    ],
    "improvements": [
        "Area for improvement 1",
        "Area for improvement 2",
        "Area for improvement 3"
    ],
    "missing_keywords": [
        "keyword1",
        "keyword2",
        "keyword3"
    ],
    "action_items": [
        "Action item 1",
        "Action item 2",
        "Action item 3",
        "Action item 4",
        "Action item 5"
    ],
    "evaluation_summary": "A brief overall evaluation summary of the resume"
}}

IMPORTANT REQUIREMENTS:
1. You MUST provide EXACTLY 3 strengths and 3 areas for improvement
2. You MUST provide at least 5 action items prioritized by impact
3. Return ONLY valid JSON with no additional text, markdown formatting, or code blocks
4. Ensure all scores are integers between 1 and 10
5. Overall match percentage must be an integer between 0 and 100
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

Return ONLY a JSON object with the following structure:
{{
    "technical_skills": ["skill1", "skill2", ...],
    "soft_skills": ["skill1", "skill2", ...],
    "industry_terms": ["term1", "term2", ...],
    "action_verbs": ["verb1", "verb2", ...]
}}

IMPORTANT REQUIREMENTS:
1. You MUST provide EXACTLY 15 technical skills
2. You MUST provide EXACTLY 10 soft skills
3. You MUST provide EXACTLY 5 industry-specific terms
4. You MUST provide EXACTLY 5 action verbs
5. Return ONLY valid JSON with no additional text, markdown formatting, or code blocks
6. If the job description doesn't explicitly mention enough items, infer relevant ones based on the industry and role
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

Return ONLY a JSON object with the following structure:
{{
    "content_suggestions": [
        "Specific content suggestion 1",
        "Specific content suggestion 2",
        "Specific content suggestion 3",
        "Specific content suggestion 4",
        "Specific content suggestion 5"
    ],
    "structural_improvements": [
        "Structural improvement 1",
        "Structural improvement 2",
        "Structural improvement 3"
    ],
    "wording_changes": [
        "Wording change 1",
        "Wording change 2",
        "Wording change 3"
    ],
    "before_after_example": {{
        "section_name": "Experience",
        "before": "Original text from the resume",
        "after": "Improved version of the text"
    }},
    "summary": "A brief summary of the key improvements recommended"
}}

IMPORTANT REQUIREMENTS:
1. You MUST provide EXACTLY 5 content suggestions
2. You MUST provide EXACTLY 3 structural improvements
3. You MUST provide EXACTLY 3 wording changes
4. Return ONLY valid JSON with no additional text, markdown formatting, or code blocks
5. Make all suggestions specific and actionable
"""
    return prompt 