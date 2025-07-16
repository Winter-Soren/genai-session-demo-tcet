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

1. Create a virtual environment

If you do not have virtualenv installed, run the following command:

```bash
pip install virtualenv
```

Then, create and activate a virtual environment:

```bash
python -m virtualenv venv
source venv/bin/activate  
```

On Windows:
```bash
venv\Scripts\activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Set up your Groq API key

Create a `.env` file and add the following:

```bash
GROQ_API_KEY=your_api_key_here  
```

4. Run the application

```bash
streamlit run app.py
```

## Steps to Begin

Download the boilerplate to get started.

Create a file named `pdf_parser.py` in the `utils` directory:

```python
from typing import Optional, BinaryIO

from pypdf import PdfReader
import docx


def extract_text_from_pdf(file_content: BinaryIO) -> str:
    pdf_reader = PdfReader(file_content)
    text = ""
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n\n"
    return text.strip()

def extract_text_from_docx(file_content: BinaryIO) -> str:
    doc = docx.Document(file_content)
    text = ""
    for paragraph in doc.paragraphs:
        if paragraph.text:
            text += paragraph.text + "\n"
    return text.strip()

def extract_text_from_resume(file_content: BinaryIO, file_type: str) -> str:
    if file_type.lower() == "pdf":
        return extract_text_from_pdf(file_content)
    elif file_type.lower() == "docx":
        return extract_text_from_docx(file_content)
    else:
        raise ValueError(f"Unsupported file type: {file_type}") 
```

Now, open `app.py` and add the input form:

```python
resume_text, job_description, company_name, role_name = display_input_form()
```

Next, go inside this method, i.e., inside `components/input_form/form.py`, and call the method to extract the text from your resume:

```python
resume_text = extract_text_from_resume(uploaded_file, file_type)
```

Now, let's create a button to submit and add form field validation:

```python
if st.button("Evaluate Resume"):
    if not resume_text:
        st.error("Please upload a resume.")
        return
    # Add more form field validation here
```

When the button is clicked, we need to perform some actions. While the action is not yet completed, show a loader to the user:

```python
with st.spinner("Analyzing your resume..."):
```

Now, go inside the file `analyzer.py` in the `evaluator` directory. There you will find the `ResumeAnalyzer` class.

Create its constructor:

```python
def __init__(self):
    """Initialize the resume analyzer with Groq LLM."""

    self.llm = ChatGroq(
        api_key=config.get_groq_api_key(),
        model=config.LLM_MODEL, 
        temperature=config.TEMPERATURE
    )
    self.output_parser = StrOutputParser()
```

Create a method named:

``` python
def evaluate_resume(
        self,
        resume_text: str,
        job_description: str,
        company_name: str,
        role_name: str
    ) -> Dict[str, Any]:
```

Get the keywords:

```python
keywords = ""
```

Let's create the `extract_keywords_from_job` method:

```python
def extract_keywords_from_job(self, job_description: str) -> Dict[str, List[str]]:
    """
    Extract important keywords from a job description.
    
    Args:
        job_description: The job description text
    
    Returns:
        Dictionary with extracted keywords by category
    """
    prompt = get_keyword_extraction_prompt(job_description)
    
    # Create a runnable sequence
    chain = (
        PromptTemplate.from_template("{prompt}")
        | self.llm
        | self.output_parser
    )
    
    # Run the chain
    result = chain.invoke({"prompt": prompt})
    
    # Parse the JSON response
    try:
        keywords = self._parse_json_response(result)
        return keywords
    except Exception as e:
        print(f"Error extracting keywords: {e}")
        # Fallback if JSON parsing fails
        return {
            "technical_skills": [],
            "soft_skills": [],
            "industry_terms": [],
            "action_verbs": []
        }
```

Now, call the method:

```python
keywords = self.extract_keywords_from_job(job_description)
```

Let's get our prompt template:

```python
prompt = get_resume_evaluation_prompt(
    resume_text=resume_text,
    job_description=job_description,
    company_name=company_name,
    role_name=role_name,
    evaluation_criteria=config.EVALUATION_CRITERIA
)
```

```python
# Create a runnable sequence
chain = (
    PromptTemplate.from_template("{prompt}")
    | self.llm
    | self.output_parser
)

evaluation_result = chain.invoke({"prompt": prompt})

# Parse the JSON response
try:
    evaluation_data = self._parse_json_response(evaluation_result)
    # Return combined results
    return {
        "evaluation": evaluation_result,  # Keep the raw result for reference
        "evaluation_data": evaluation_data,  # Add the structured data
        "keywords": keywords
    }
except Exception as e:
    print(f"Error parsing evaluation result: {e}")
    # Return raw result if parsing fails
    return {
        "evaluation": evaluation_result,
        "keywords": keywords
    }
```

Since the JSON parsing method is not created, copy and paste it:

```python
def _parse_json_response(self, response: str) -> Dict:
    """
    Parse JSON response from LLM and handle common formatting issues.
    
    Args:
        response: String response from LLM
    
    Returns:
        Parsed JSON as dictionary
    """
    # Clean up the response to extract just the JSON part
    if "```json" in response:
        response = response.split("```json")[1].split("```")[0].strip()
    elif "```" in response:
        response = response.split("```")[1].split("```")[0].strip()
    
    # Remove any trailing or leading non-JSON text
    try:
        # Find the first opening brace
        start_idx = response.find('{')
        if start_idx == -1:
            raise ValueError("No JSON object found in response")
        # Find the last closing brace
        end_idx = response.rindex('}')
        if end_idx == -1:
            raise ValueError("No closing brace found in response")
        # Extract just the JSON part
        json_str = response[start_idx:end_idx+1]
        # Parse the JSON
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        print(f"Raw response: {response}")
        # Return empty dict as fallback
        return {}
```

Now that our main `ResumeAnalyzer` is ready, let's go back to the `app.py` file.

Let's create an instance of our class and invoke it:

```python
analyzer = ResumeAnalyzer()
```

Let's evaluate our resume:

```python
evaluation_results = analyzer.evaluate_resume(
    resume_text=resume_text,
    job_description=job_description,
    company_name=company_name,
    role_name=role_name
)
```

Calculate the metrics for the graph and overall analysis of your evaluation results:

```python
metrics = calculate_metrics(
    evaluation_results=evaluation_results,
    resume_text=resume_text,
    job_description=job_description
)
```

Now that we have completed our main resume evaluation, let's get the recommendations for improvements.

Go to the `ResumeAnalyzer` class again and write another method to get detailed recommendations:

```python
def get_detailed_suggestions(
    self,
    resume_text: str,
    job_description: str,
    evaluation_results: Dict[str, Any]
) -> Dict[str, Any]:
```

Call our improvement suggestions prompt:

```python
prompt = get_improvement_suggestions_prompt(
    resume_text=resume_text,
    job_description=job_description,
    evaluation_results=evaluation_results
)
```

Now, let's create a runnable sequence:

```python
chain = (
    PromptTemplate.from_template("{prompt}")
    | self.llm
    | self.output_parser
)

# Run the chain
suggestions_result = chain.invoke({"prompt": prompt})

# Parse the JSON response
try:
    suggestions_data = self._parse_json_response(suggestions_result)
    return suggestions_data
except Exception as e:
    print(f"Error parsing suggestions: {e}")
    # Return raw result if parsing fails
    return {"summary": suggestions_result} 
```

Now, invoke this class and call the `get_detailed_suggestions` method in `recommendations.py` in the `evaluator` directory:

```python
detailed_suggestions = analyzer.get_detailed_suggestions(
    resume_text=resume_text,
    job_description=job_description,
    evaluation_results=evaluation_results
)
```

Now, let's call our method `get_detailed_recommendations` in `app.py`:

```python
recommendations = get_detailed_recommendations(
    resume_text=resume_text,
    job_description=job_description,
    company_name=company_name,
    role_name=role_name,
    evaluation_results=evaluation_results,
    metrics=metrics
)
```

When the process is completed, we want to show the output:

```python
display_evaluation_results(
    evaluation_results=evaluation_results,
    metrics=metrics,
    recommendations=recommendations
)
```






