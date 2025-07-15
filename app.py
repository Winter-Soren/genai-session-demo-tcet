"""
Resume Evaluator - A GenAI-powered resume evaluation tool.
"""
import io
import os
from typing import Dict, Any, List, Tuple

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import config
from utils.pdf_parser import extract_text_from_resume
from evaluator.analyzer import ResumeAnalyzer
from evaluator.metrics import calculate_metrics
from evaluator.recommendations import get_detailed_recommendations


# Page configuration
st.set_page_config(
    page_title="Resume Evaluator",
    page_icon="📝",
    layout="wide"
)


def check_api_key() -> bool:
    """Check if the Groq API key is set."""
    try:
        config.get_groq_api_key()
        return True
    except ValueError:
        return False


def display_header():
    """Display the application header."""
    st.title("Resume Evaluator")
    st.markdown(
        "Upload your resume and a job description to get AI-powered feedback and suggestions."
    )


def display_input_form() -> Tuple[str, str, str, str]:
    """
    Display the input form for resume and job details.
    
    Returns:
        Tuple containing (resume_text, job_description, company_name, role_name)
    """
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Upload Resume")
        uploaded_file = st.file_uploader(
            "Upload your resume (PDF or DOCX)",
            type=config.ALLOWED_FILE_TYPES
        )
        
        resume_text = ""
        if uploaded_file is not None:
            try:
                file_type = uploaded_file.name.split(".")[-1]
                resume_text = extract_text_from_resume(uploaded_file, file_type)
                st.success("Resume uploaded successfully!")
                with st.expander("Preview Extracted Text"):
                    st.text(resume_text[:500] + "..." if len(resume_text) > 500 else resume_text)
            except Exception as e:
                st.error(f"Error extracting text from resume: {str(e)}")
    
    with col2:
        st.subheader("Job Details")
        company_name = st.text_input("Company Name")
        role_name = st.text_input("Role/Position")
        job_description = st.text_area("Job Description", height=300)
    
    return resume_text, job_description, company_name, role_name


def create_radar_chart(scores: Dict[str, int]) -> go.Figure:
    """
    Create a radar chart for the evaluation scores.
    
    Args:
        scores: Dictionary mapping criteria to scores (1-10)
        
    Returns:
        Plotly figure object
    """
    categories = list(scores.keys())
    values = list(scores.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Your Resume',
        line_color='rgba(31, 119, 180, 0.8)',
        fillcolor='rgba(31, 119, 180, 0.3)'
    ))
    
    # Add a "perfect score" reference
    fig.add_trace(go.Scatterpolar(
        r=[10] * len(categories),
        theta=categories,
        fill='toself',
        name='Perfect Score',
        line_color='rgba(44, 160, 44, 0.5)',
        fillcolor='rgba(44, 160, 44, 0.1)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )
        ),
        showlegend=True,
        title="Resume Evaluation Scores"
    )
    
    return fig


def create_keyword_chart(keyword_metrics: Dict[str, Any]) -> go.Figure:
    """
    Create a bar chart for keyword metrics.
    
    Args:
        keyword_metrics: Dictionary with keyword metrics
        
    Returns:
        Plotly figure object
    """
    categories = []
    percentages = []
    
    for category, data in keyword_metrics.items():
        if category != "overall":
            categories.append(category.replace("_", " ").title())
            percentages.append(data["percentage"])
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=percentages,
            marker_color='rgba(31, 119, 180, 0.8)'
        )
    ])
    
    fig.update_layout(
        title="Keyword Coverage by Category (%)",
        xaxis_title="Category",
        yaxis_title="Coverage (%)",
        yaxis=dict(range=[0, 100])
    )
    
    return fig


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
        if scores:
            radar_chart = create_radar_chart(scores)
            st.plotly_chart(radar_chart, use_container_width=True)
    
    with col2:
        if keyword_metrics:
            keyword_chart = create_keyword_chart(keyword_metrics)
            st.plotly_chart(keyword_chart, use_container_width=True)
    
    # Display strengths and improvements
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Strengths")
        strengths = recommendations.get("strengths", [])
        if strengths:
            for strength in strengths:
                st.markdown(f"✅ {strength}")
        else:
            st.info("No specific strengths identified.")
    
    with col2:
        st.subheader("Areas for Improvement")
        improvements = recommendations.get("improvements", [])
        if improvements:
            for improvement in improvements:
                st.markdown(f"🔍 {improvement}")
        else:
            st.info("No specific areas for improvement identified.")
    
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
        st.info("No missing keywords identified.")
    
    # Display action items
    st.subheader("Recommended Actions")
    action_items = recommendations.get("action_items", [])
    if action_items:
        for i, action in enumerate(action_items, 1):
            st.markdown(f"{i}. {action}")
    else:
        st.info("No specific action items identified.")
    
    # Display detailed suggestions
    with st.expander("Detailed Improvement Suggestions", expanded=False):
        detailed_suggestions = recommendations.get("detailed_suggestions", "")
        if detailed_suggestions:
            st.markdown(detailed_suggestions)
        else:
            st.info("No detailed suggestions available.")
    
    # Display raw evaluation
    with st.expander("Raw Evaluation", expanded=False):
        evaluation_text = evaluation_results.get("evaluation", "")
        if evaluation_text:
            st.markdown(evaluation_text)
        else:
            st.info("No raw evaluation available.")


def main():
    """Main application function."""
    display_header()
    
    # Check for API key
    if not check_api_key():
        st.error(
            "Groq API key not found. Please set the GROQ_API_KEY environment variable."
        )
        st.info(
            "You can get a Groq API key from [console.groq.com](https://console.groq.com/)"
        )
        return
    
    # Display input form
    resume_text, job_description, company_name, role_name = display_input_form()
    
    # Evaluate button
    if st.button("Evaluate Resume"):
        if not resume_text:
            st.error("Please upload a resume.")
            return
        
        if not job_description:
            st.error("Please enter a job description.")
            return
        
        if not company_name:
            st.warning("Company name not provided. Using 'Unknown Company'.")
            company_name = "Unknown Company"
        
        if not role_name:
            st.warning("Role name not provided. Using 'Unspecified Role'.")
            role_name = "Unspecified Role"
        
        # Show progress
        with st.spinner("Analyzing your resume..."):
            # Initialize analyzer
            analyzer = ResumeAnalyzer()
            
            # Evaluate resume
            evaluation_results = analyzer.evaluate_resume(
                resume_text=resume_text,
                job_description=job_description,
                company_name=company_name,
                role_name=role_name
            )
            
            # Calculate metrics
            metrics = calculate_metrics(
                evaluation_results=evaluation_results,
                resume_text=resume_text,
                job_description=job_description
            )
            
            # Get recommendations
            recommendations = get_detailed_recommendations(
                resume_text=resume_text,
                job_description=job_description,
                company_name=company_name,
                role_name=role_name,
                evaluation_results=evaluation_results,
                metrics=metrics
            )
        
        # Display results
        display_evaluation_results(
            evaluation_results=evaluation_results,
            metrics=metrics,
            recommendations=recommendations
        )


if __name__ == "__main__":
    main() 