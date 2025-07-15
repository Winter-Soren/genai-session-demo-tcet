"""
Scoring system for resume evaluation.
"""
import re
from typing import Dict, List, Tuple, Any

import config


def extract_scores_from_evaluation(evaluation_text: str) -> Dict[str, int]:
    """
    Extract numerical scores from the LLM evaluation text.
    
    Args:
        evaluation_text: The evaluation text from the LLM
        
    Returns:
        Dictionary mapping criteria to scores (1-10)
    """
    scores = {}
    
    # Look for patterns like "Relevance to Job Description: 7/10" or similar
    for criterion in config.EVALUATION_CRITERIA:
        # Try different patterns to find scores
        patterns = [
            rf"{criterion}:?\s*(\d+)(?:/10|\s*out of\s*10)",
            rf"{criterion}.*?(\d+)(?:/10|\s*out of\s*10)",
            rf"{criterion}.*?score:?\s*(\d+)"
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, evaluation_text, re.IGNORECASE)
            if matches:
                try:
                    score = int(matches[0])
                    # Ensure score is in range 1-10
                    score = max(1, min(score, 10))
                    scores[criterion] = score
                    break
                except (ValueError, IndexError):
                    continue
    
    return scores


def extract_overall_match(evaluation_text: str) -> int:
    """
    Extract the overall match percentage from the evaluation text.
    
    Args:
        evaluation_text: The evaluation text from the LLM
        
    Returns:
        Overall match percentage (0-100)
    """
    # Look for patterns like "Overall match: 75%" or "75% match"
    patterns = [
        r"overall match:?\s*(\d+)%",
        r"match percentage:?\s*(\d+)%",
        r"(\d+)%\s*match",
        r"(\d+)%\s*overall"
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, evaluation_text, re.IGNORECASE)
        if matches:
            try:
                match_percentage = int(matches[0])
                # Ensure percentage is in range 0-100
                match_percentage = max(0, min(match_percentage, 100))
                return match_percentage
            except (ValueError, IndexError):
                continue
    
    # If no match found, calculate from individual scores
    scores = extract_scores_from_evaluation(evaluation_text)
    if scores:
        # Calculate weighted average
        weighted_sum = 0
        total_weight = 0
        
        for criterion, score in scores.items():
            weight = config.CRITERIA_WEIGHTS.get(criterion, 0)
            weighted_sum += score * weight
            total_weight += weight
        
        if total_weight > 0:
            # Convert from 1-10 scale to 0-100 percentage
            return int((weighted_sum / total_weight) * 10)
    
    # Default if no scores found
    return 50


def calculate_metrics(
    evaluation_results: Dict[str, Any],
    resume_text: str,
    job_description: str
) -> Dict[str, Any]:
    """
    Calculate metrics based on evaluation results.
    
    Args:
        evaluation_results: Results from the LLM evaluation
        resume_text: The extracted text from the resume
        job_description: The job description text
        
    Returns:
        Dictionary with calculated metrics
    """
    evaluation_text = evaluation_results.get("evaluation", "")
    keywords = evaluation_results.get("keywords", {})
    
    # Extract scores and match percentage
    scores = extract_scores_from_evaluation(evaluation_text)
    match_percentage = extract_overall_match(evaluation_text)
    
    # Calculate keyword metrics
    keyword_metrics = calculate_keyword_metrics(resume_text, keywords)
    
    return {
        "scores": scores,
        "match_percentage": match_percentage,
        "keyword_metrics": keyword_metrics
    }


def calculate_keyword_metrics(
    resume_text: str, 
    keywords: Dict[str, List[str]]
) -> Dict[str, Any]:
    """
    Calculate metrics related to keywords.
    
    Args:
        resume_text: The extracted text from the resume
        keywords: Dictionary of keywords by category
        
    Returns:
        Dictionary with keyword metrics
    """
    resume_lower = resume_text.lower()
    
    # Calculate presence of each keyword category
    metrics = {}
    for category, keyword_list in keywords.items():
        if not keyword_list:
            metrics[category] = {
                "present": [],
                "missing": [],
                "percentage": 0
            }
            continue
            
        present = []
        missing = []
        
        for keyword in keyword_list:
            if keyword.lower() in resume_lower:
                present.append(keyword)
            else:
                missing.append(keyword)
        
        total = len(keyword_list)
        percentage = (len(present) / total * 100) if total > 0 else 0
        
        metrics[category] = {
            "present": present,
            "missing": missing,
            "percentage": percentage
        }
    
    # Calculate overall keyword presence
    all_keywords = []
    for keyword_list in keywords.values():
        all_keywords.extend(keyword_list)
    
    present_count = 0
    for keyword in all_keywords:
        if keyword.lower() in resume_lower:
            present_count += 1
    
    overall_percentage = (present_count / len(all_keywords) * 100) if all_keywords else 0
    
    metrics["overall"] = {
        "total_keywords": len(all_keywords),
        "present_count": present_count,
        "percentage": overall_percentage
    }
    
    return metrics 