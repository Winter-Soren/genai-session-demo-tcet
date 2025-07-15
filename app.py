"""
Resume Evaluator - A GenAI-powered resume evaluation tool.
"""
import sys
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Resume Evaluator",
    page_icon="📝",
    layout="wide"
)

from components.header.header import display_header
from components.input_form.form import display_input_form
from components.results.evaluation_results import display_evaluation_results
from utils.api_check import check_api_key, display_api_key_error

from evaluator.analyzer import ResumeAnalyzer
from evaluator.metrics import calculate_metrics
from evaluator.recommendations import get_detailed_recommendations


def main():
    """Main application function."""
    display_header()
    
    # Check for API key
    if not check_api_key():
        display_api_key_error()
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
        
        try:
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
        except KeyboardInterrupt:
            st.error("Operation cancelled by user.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nApplication terminated by user.")
        sys.exit(0)
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        sys.exit(1) 