"""
Component for displaying evaluation results and recommendations.
"""
from typing import Dict, Any
import json
import streamlit as st

from components.charts.radar_chart import create_radar_chart
from components.charts.keyword_chart import create_keyword_chart

def display_evaluation_results(
    evaluation_results: Dict[str, Any],
    metrics: Dict[str, Any],
    recommendations: Dict[str, Any]
):
    """
    Display the evaluation results and recommendations.
    
    Args:
        evaluation_results: Results from the LLM evaluation
        metrics: Dictionary with calculated metrics
        recommendations: Dictionary with recommendations
    """
    match_percentage = metrics.get("match_percentage", 0)
    scores = metrics.get("scores", {})
    keyword_metrics = metrics.get("keyword_metrics", {})
    
    # Display match percentage
    st.header("Resume Evaluation Results")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.metric("Overall Match", f"{match_percentage}%")
    
    with col2:
        overall_keywords = keyword_metrics.get("overall", {})
        present_count = overall_keywords.get("present_count", 0)
        total_keywords = overall_keywords.get("total_keywords", 0)
        st.metric("Keywords Present", f"{present_count}/{total_keywords}")
    
    with col3:
        keyword_percentage = overall_keywords.get("percentage", 0)
        st.metric("Keyword Coverage", f"{keyword_percentage:.1f}%")
    
    # Display charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Always create and display radar chart
        radar_chart = create_radar_chart(scores)
        st.plotly_chart(radar_chart, use_container_width=True)
    
    with col2:
        if keyword_metrics:
            keyword_chart = create_keyword_chart(keyword_metrics)
            st.plotly_chart(keyword_chart, use_container_width=True)
    
    # Display strengths and improvements
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Key Strengths")
        strengths = recommendations.get("strengths", [])
        if strengths:
            for strength in strengths:
                st.markdown(f"✅ {strength}")
        else:
            # Create default strengths if none are provided
            st.info("Analyzing resume strengths...")
    
    with col2:
        st.subheader("Areas for Improvement")
        improvements = recommendations.get("improvements", [])
        if improvements:
            for improvement in improvements:
                st.markdown(f"🔍 **{improvement}**")
        else:
            # Create default improvements if none are provided
            st.info("Analyzing areas for improvement...")
    
    # Display missing keywords
    st.subheader("Missing Keywords")
    missing_keywords = recommendations.get("missing_keywords", {})
    if missing_keywords:
        tabs = st.tabs([category.replace("_", " ").title() for category in missing_keywords.keys()])
        
        for i, (category, keywords) in enumerate(missing_keywords.items()):
            with tabs[i]:
                if keywords:
                    st.write(", ".join(keywords))
                else:
                    st.info(f"No missing {category.replace('_', ' ')} keywords identified.")
    else:
        st.info("Analyzing missing keywords...")
    
    # Display action items
    st.subheader("Recommended Actions")
    action_items = recommendations.get("action_items", [])
    if action_items:
        for i, action in enumerate(action_items, 1):
            st.markdown(f"**{i}.** {action}")
    else:
        st.info("Generating recommended actions...")
    
    # Display detailed suggestions
    with st.expander("Detailed Improvement Suggestions", expanded=False):
        detailed_suggestions = recommendations.get("detailed_suggestions", "")
        if detailed_suggestions:
            st.markdown(detailed_suggestions)
        else:
            st.info("Detailed suggestions will appear here after analysis.")
    
    # Display raw evaluation in a more readable format
    with st.expander("Raw Evaluation", expanded=False):
        evaluation_data = evaluation_results.get("evaluation_data", {})
        if evaluation_data:
            # Format the evaluation data into sections
            st.subheader("Criteria Scores")
            criteria_scores = evaluation_data.get("criteria_scores", {})
            for criterion, data in criteria_scores.items():
                score = data.get("score", 0)
                explanation = data.get("explanation", "")
                suggestion = data.get("suggestion", "")
                
                st.markdown(f"**{criterion}**: {score}/10")
                st.markdown(f"*{explanation}*")
                st.markdown(f"Suggestion: {suggestion}")
                st.markdown("---")
            
            # Overall match
            st.subheader("Overall Match")
            match_pct = evaluation_data.get("overall_match_percentage", 0)
            st.markdown(f"**Match Percentage**: {match_pct}%")
            
            # Strengths and improvements
            st.subheader("Strengths")
            for strength in evaluation_data.get("strengths", []):
                st.markdown(f"- {strength}")
                
            st.subheader("Areas for Improvement")
            for improvement in evaluation_data.get("improvements", []):
                st.markdown(f"- {improvement}")
            
            # Missing keywords
            st.subheader("Missing Keywords")
            for keyword in evaluation_data.get("missing_keywords", []):
                st.markdown(f"- {keyword}")
            
            # Action items
            st.subheader("Action Items")
            for i, action in enumerate(evaluation_data.get("action_items", []), 1):
                st.markdown(f"{i}. {action}")
            
            # Summary
            st.subheader("Summary")
            st.markdown(evaluation_data.get("evaluation_summary", ""))
        else:
            # If no structured data, display the raw text
            evaluation_text = evaluation_results.get("evaluation", "")
            if evaluation_text:
                try:
                    # Try to parse and pretty print the JSON if it's a string
                    if isinstance(evaluation_text, str) and evaluation_text.strip().startswith("{"):
                        parsed_json = json.loads(evaluation_text)
                        st.json(parsed_json)
                    else:
                        st.markdown(evaluation_text)
                except:
                    st.markdown(evaluation_text)
            else:
                st.info("Raw evaluation will appear here after analysis.") 