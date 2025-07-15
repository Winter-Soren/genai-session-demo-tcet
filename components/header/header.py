"""
Header component for displaying the application title and description.
"""
import streamlit as st

def display_header():
    """Display the application header."""
    st.title("Resume Evaluator")
    st.markdown(
        "Upload your resume and a job description to get AI-powered feedback and suggestions."
    ) 