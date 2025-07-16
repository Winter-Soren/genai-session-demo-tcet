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
    

       
        


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nApplication terminated by user.")
        sys.exit(0)
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        sys.exit(1) 