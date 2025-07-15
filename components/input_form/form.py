"""
Input form component for resume upload and job details.
"""
from typing import Tuple
import streamlit as st

import config
from utils.pdf_parser import extract_text_from_resume

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