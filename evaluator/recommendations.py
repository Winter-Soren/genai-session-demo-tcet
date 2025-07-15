"""
Feedback generation for resume improvements.
"""
import re
from typing import Dict, List, Any

from evaluator.analyzer import ResumeAnalyzer


def extract_strengths_and_improvements(evaluation_text: str) -> Dict[str, List[str]]:
    """
    Extract strengths and areas for improvement from evaluation text.
    
    Args:
        evaluation_text: The evaluation text from the LLM
        
    Returns:
        Dictionary with strengths and improvements
    """
    strengths = []
    improvements = []
    
    # Look for strengths section
    strength_patterns = [
        r"strengths:(.*?)(?=areas for improvement|improvements|weaknesses|$)",
        r"top\s*\d+\s*strengths:(.*?)(?=areas for improvement|improvements|weaknesses|$)",
        r"strengths of the resume:(.*?)(?=areas for improvement|improvements|weaknesses|$)"
    ]
    
    for pattern in strength_patterns:
        matches = re.search(pattern, evaluation_text, re.IGNORECASE | re.DOTALL)
        if matches:
            strength_text = matches.group(1).strip()
            # Extract bullet points or numbered items
            items = re.findall(r"(?:^|\n)(?:\d+\.|\*|\-)\s*(.*?)(?=$|\n)", strength_text)
            if items:
                strengths.extend([item.strip() for item in items])
            else:
                # If no bullet points, split by newlines
                lines = [line.strip() for line in strength_text.split("\n") if line.strip()]
                strengths.extend(lines)
            break
    
    # Look for improvements section
    improvement_patterns = [
        r"(?:areas for improvement|improvements|weaknesses):(.*?)(?=\n\n|$)",
        r"top\s*\d+\s*(?:areas for improvement|improvements|weaknesses):(.*?)(?=\n\n|$)",
        r"(?:areas for improvement|improvements|weaknesses).*?:(.*?)(?=\n\n|$)"
    ]
    
    for pattern in improvement_patterns:
        matches = re.search(pattern, evaluation_text, re.IGNORECASE | re.DOTALL)
        if matches:
            improvement_text = matches.group(1).strip()
            # Extract bullet points or numbered items
            items = re.findall(r"(?:^|\n)(?:\d+\.|\*|\-)\s*(.*?)(?=$|\n)", improvement_text)
            if items:
                improvements.extend([item.strip() for item in items])
            else:
                # If no bullet points, split by newlines
                lines = [line.strip() for line in improvement_text.split("\n") if line.strip()]
                improvements.extend(lines)
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
    
    return missing_keywords


def generate_action_items(
    evaluation_text: str,
    metrics: Dict[str, Any]
) -> List[str]:
    """
    Generate prioritized action items based on evaluation and metrics.
    
    Args:
        evaluation_text: The evaluation text from the LLM
        metrics: Dictionary with calculated metrics
        
    Returns:
        List of action items
    """
    action_items = []
    
    # Look for action items or suggestions in the evaluation text
    action_patterns = [
        r"(?:action items|suggested actions|recommendations):(.*?)(?=\n\n|$)",
        r"(?:action items|suggested actions|recommendations).*?:(.*?)(?=\n\n|$)"
    ]
    
    for pattern in action_patterns:
        matches = re.search(pattern, evaluation_text, re.IGNORECASE | re.DOTALL)
        if matches:
            action_text = matches.group(1).strip()
            # Extract bullet points or numbered items
            items = re.findall(r"(?:^|\n)(?:\d+\.|\*|\-)\s*(.*?)(?=$|\n)", action_text)
            if items:
                action_items.extend([item.strip() for item in items])
            break
    
    # If no action items found, generate based on metrics
    if not action_items:
        # Get areas with lowest scores
        scores = metrics.get("scores", {})
        if scores:
            sorted_scores = sorted(scores.items(), key=lambda x: x[1])
            for criterion, score in sorted_scores[:2]:
                action_items.append(f"Improve {criterion.lower()} in your resume")
        
        # Add keyword-related action items
        keyword_metrics = metrics.get("keyword_metrics", {})
        for category, data in keyword_metrics.items():
            if category != "overall" and data.get("percentage", 0) < 50:
                action_items.append(f"Add missing {category.replace('_', ' ')} to your resume")
    
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
    evaluation_text = evaluation_results.get("evaluation", "")
    
    # Extract strengths and improvements
    strengths_and_improvements = extract_strengths_and_improvements(evaluation_text)
    
    # Extract missing keywords
    missing_keywords = extract_missing_keywords(metrics)
    
    # Generate action items
    action_items = generate_action_items(evaluation_text, metrics)
    
    # Get detailed suggestions from LLM
    analyzer = ResumeAnalyzer()
    detailed_suggestions = analyzer.get_detailed_suggestions(
        resume_text=resume_text,
        job_description=job_description,
        evaluation_results=evaluation_results
    )
    
    return {
        "strengths": strengths_and_improvements.get("strengths", []),
        "improvements": strengths_and_improvements.get("improvements", []),
        "missing_keywords": missing_keywords,
        "action_items": action_items,
        "detailed_suggestions": detailed_suggestions
    } 