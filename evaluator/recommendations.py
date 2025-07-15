"""
Feedback generation for resume improvements.
"""
import re
from typing import Dict, List, Any

from evaluator.analyzer import ResumeAnalyzer


def extract_strengths_and_improvements(evaluation_data: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Extract strengths and areas for improvement from evaluation data.
    
    Args:
        evaluation_data: The evaluation data from the LLM as a dictionary
        
    Returns:
        Dictionary with strengths and improvements
    """
    # Default values
    default_strengths = [
        "Clear presentation of professional experience",
        "Relevant educational background",
        "Good organization of information"
    ]
    
    default_improvements = [
        "Add more quantifiable achievements",
        "Tailor skills section to match job requirements",
        "Enhance keywords related to the job description"
    ]
    
    # If we have structured data, use it directly
    strengths = evaluation_data.get("strengths", [])
    improvements = evaluation_data.get("improvements", [])
    
    # Ensure we have exactly 3 strengths and improvements
    if not strengths or len(strengths) < 3:
        # Add missing strengths
        while len(strengths) < 3:
            for default in default_strengths:
                if default not in strengths:
                    strengths.append(default)
                    break
    
    if not improvements or len(improvements) < 3:
        # Add missing improvements
        while len(improvements) < 3:
            for default in default_improvements:
                if default not in improvements:
                    improvements.append(default)
                    break
    
    return {
        "strengths": strengths[:3],  # Limit to top 3
        "improvements": improvements[:3]  # Limit to top 3
    }


def extract_missing_keywords(metrics: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Extract missing keywords from metrics.
    
    Args:
        metrics: Dictionary with keyword metrics
        
    Returns:
        Dictionary with missing keywords by category
    """
    missing_keywords = {}
    
    keyword_metrics = metrics.get("keyword_metrics", {})
    for category, data in keyword_metrics.items():
        if category != "overall" and "missing" in data:
            missing_keywords[category] = data["missing"]
    
    # Ensure we have at least some keywords in each category
    if not missing_keywords or all(not keywords for keywords in missing_keywords.values()):
        default_missing = {
            "technical_skills": ["Python", "SQL", "Data Analysis"],
            "soft_skills": ["Communication", "Leadership"],
            "industry_terms": ["Machine Learning"],
            "action_verbs": ["Implemented", "Developed"]
        }
        
        # Only use defaults if we have no data at all
        if not missing_keywords:
            missing_keywords = default_missing
    
    return missing_keywords


def generate_action_items(evaluation_data: Dict[str, Any], metrics: Dict[str, Any]) -> List[str]:
    """
    Generate prioritized action items based on evaluation data and metrics.
    
    Args:
        evaluation_data: The evaluation data from the LLM as a dictionary
        metrics: Dictionary with calculated metrics
        
    Returns:
        List of action items
    """
    # Default action items
    default_actions = [
        "Quantify achievements with specific metrics and results",
        "Tailor your resume to highlight skills relevant to the job description",
        "Use industry-specific keywords throughout your resume",
        "Improve formatting for better readability and visual appeal",
        "Add a strong professional summary highlighting your key qualifications"
    ]
    
    # If we have structured data, use it directly
    action_items = evaluation_data.get("action_items", [])
    
    # If no action items found or not enough, generate based on metrics
    if not action_items or len(action_items) < 3:
        # Get areas with lowest scores
        scores = metrics.get("scores", {})
        if scores:
            sorted_scores = sorted(scores.items(), key=lambda x: x[1])
            for criterion, score in sorted_scores[:2]:
                action = f"Improve {criterion.lower()} in your resume"
                if action not in action_items:
                    action_items.append(action)
        
        # Add keyword-related action items
        keyword_metrics = metrics.get("keyword_metrics", {})
        for category, data in keyword_metrics.items():
            if category != "overall" and data.get("percentage", 0) < 50:
                action = f"Add missing {category.replace('_', ' ')} to your resume"
                if action not in action_items:
                    action_items.append(action)
        
        # Add default action items if still not enough
        for default in default_actions:
            if default not in action_items:
                action_items.append(default)
            if len(action_items) >= 5:
                break
    
    return action_items[:5]  # Limit to top 5


def get_detailed_recommendations(
    resume_text: str,
    job_description: str,
    company_name: str,
    role_name: str,
    evaluation_results: Dict[str, Any],
    metrics: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Get detailed recommendations for improving the resume.
    
    Args:
        resume_text: The extracted text from the resume
        job_description: The job description text
        company_name: The name of the company
        role_name: The name of the role
        evaluation_results: Results from the LLM evaluation
        metrics: Dictionary with calculated metrics
        
    Returns:
        Dictionary with detailed recommendations
    """
    evaluation_data = evaluation_results.get("evaluation_data", {})
    
    # Extract strengths and improvements
    strengths_and_improvements = extract_strengths_and_improvements(evaluation_data)
    
    # Extract missing keywords
    missing_keywords = extract_missing_keywords(metrics)
    
    # Generate action items
    action_items = generate_action_items(evaluation_data, metrics)
    
    # Get detailed suggestions from LLM
    analyzer = ResumeAnalyzer()
    detailed_suggestions = analyzer.get_detailed_suggestions(
        resume_text=resume_text,
        job_description=job_description,
        evaluation_results=evaluation_results
    )
    
    # Extract the summary or create a formatted detailed suggestion
    if isinstance(detailed_suggestions, dict):
        detailed_text = detailed_suggestions.get("summary", "")
        if not detailed_text:
            # Format the structured data into text
            content_suggestions = detailed_suggestions.get("content_suggestions", [])
            structural_improvements = detailed_suggestions.get("structural_improvements", [])
            wording_changes = detailed_suggestions.get("wording_changes", [])
            
            sections = []
            
            if content_suggestions:
                content_section = "## Content Suggestions\n\n" + "\n".join([f"- {item}" for item in content_suggestions])
                sections.append(content_section)
            
            if structural_improvements:
                structure_section = "## Structural Improvements\n\n" + "\n".join([f"- {item}" for item in structural_improvements])
                sections.append(structure_section)
            
            if wording_changes:
                wording_section = "## Wording Changes\n\n" + "\n".join([f"- {item}" for item in wording_changes])
                sections.append(wording_section)
            
            before_after = detailed_suggestions.get("before_after_example", {})
            if before_after:
                section_name = before_after.get("section_name", "Section")
                before = before_after.get("before", "")
                after = before_after.get("after", "")
                
                if before and after:
                    example_section = f"## Example Improvement: {section_name}\n\n### Before:\n\n{before}\n\n### After:\n\n{after}"
                    sections.append(example_section)
            
            detailed_text = "\n\n".join(sections)
    else:
        detailed_text = str(detailed_suggestions)
    
    return {
        "strengths": strengths_and_improvements.get("strengths", []),
        "improvements": strengths_and_improvements.get("improvements", []),
        "missing_keywords": missing_keywords,
        "action_items": action_items,
        "detailed_suggestions": detailed_text
    } 