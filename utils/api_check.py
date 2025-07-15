"""
Utility for checking API key configuration.
"""
import streamlit as st
import config

def check_api_key() -> bool:
    """
    Check if the Groq API key is set.
    
    Returns:
        bool: True if API key is set, False otherwise
    """
    try:
        config.get_groq_api_key()
        return True
    except ValueError:
        return False

def display_api_key_error():
    """Display error message when API key is not set."""
    st.error(
        "Groq API key not found. Please set the GROQ_API_KEY environment variable."
    )
    st.info(
        "You can get a Groq API key from [console.groq.com](https://console.groq.com/)"
    ) 