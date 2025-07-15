# Resume Evaluator

A GenAI-powered resume evaluation tool that helps students improve their resumes based on job descriptions.

## Overview

This application allows users to:
- Upload their resume (PDF format)
- Enter a job description, company name, and role
- Get an AI-powered analysis of how well their resume matches the job requirements
- Receive actionable feedback and suggestions for improvement
- See key metrics and scores for their resume

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python with LangChain
- **LLM**: Groq
- **Libraries**: PyPDF2, pandas, matplotlib

## Setup Instructions

1. Clone this repository
```bash
git clone <repository-url>
cd resume-evaluator
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up your Groq API key
```bash
export GROQ_API_KEY=your_api_key_here  # On Windows: set GROQ_API_KEY=your_api_key_here
```

5. Run the application
```bash
streamlit run app.py
```

## Project Structure

```
resume-evaluator/
├── README.md           # Project documentation
├── app.py              # Main Streamlit application
├── requirements.txt    # Dependencies
├── config.py           # Configuration settings
├── utils/
│   ├── __init__.py
│   ├── pdf_parser.py   # Resume parsing utilities
│   └── text_processor.py # Text cleaning and preprocessing
└── evaluator/
    ├── __init__.py
    ├── analyzer.py     # Core resume analysis logic
    ├── metrics.py      # Scoring system
    ├── prompts.py      # LLM prompts
    └── recommendations.py # Feedback generation
```

## Workshop Steps

1. Set up the environment and install dependencies
2. Create the basic Streamlit interface
3. Implement PDF parsing functionality
4. Connect to Groq API and set up LangChain
5. Create evaluation prompts and logic
6. Implement scoring and feedback generation
7. Add visualizations and final touches
8. Deploy the application

## Deployment Options

- **Streamlit Community Cloud**: Free hosting with GitHub integration
- **Hugging Face Spaces**: ML-friendly hosting platform
- **Local deployment**: Run locally for development and testing

## Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [Groq API Documentation](https://console.groq.com/docs/quickstart) 