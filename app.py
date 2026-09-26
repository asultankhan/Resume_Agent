import streamlit as st
from pypdf import PdfReader
from groq import Groq
import re

st.set_page_config(
    page_title="AI Resume Reviewer",
    page_icon="📄"
)

st.title("📄 AI Resume Reviewer")
st.write("Upload your resume and compare it with a target job description.")

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

def extract_resume_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    text = re.sub(r"\s+", " ", text)
    return text


def analyze_resume(resume_text, job_description):

    prompt = f"""
You are a senior ATS resume reviewer.

Analyze the resume against the job description.

Rules:
- Do not invent information.
- Do not create fake achievements.
- Do not add unsupported numbers.
- Clearly mention missing information.

Resume:
{resume_text}

Job Description:
{job_description}

Provide:

1. Resume Strengths
2. Matching Qualifications
3. Missing Skills
4. ATS Keyword Analysis
5. Formatting Issues
6. Improvement Suggestions
7. Fact Verification Checklist
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content


uploaded_resume = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste Job Description"
)

if st.button("Analyze Resume"):

    if uploaded_resume and job_description:

        with st.spinner("Analyzing resume..."):

            resume_text = extract_resume_text(uploaded_resume)

            result = analyze_resume(
                resume_text,
                job_description
            )

            st.subheader("Resume Analysis Report")
            st.markdown(result)

    else:
        st.warning("Please upload resume and enter job description.")
