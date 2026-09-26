import streamlit as st
from pypdf import PdfReader
from docx import Document
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

    text = ""

    if uploaded_file.name.endswith(".pdf"):

        reader = PdfReader(uploaded_file)

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"


    elif uploaded_file.name.endswith(".docx"):

        doc = Document(uploaded_file)

        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"

    text = re.sub(r"\s+", " ", text)

    return text
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

You are a professional ATS resume reviewer.

Target Position:
{job_title}

Analyze the resume against the job requirements.

Important:
- Never invent candidate information.
- Do not create fake achievements, numbers, certifications, or experience.
- Separate existing information from suggestions.
- Any example improvement must be labelled as "Example only".

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

job_title = st.text_input(
    "Target Job Title"
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
            st.subheader("Resume Analysis Report")

st.info(
"""
⚠️ AI-generated suggestions should be verified by the candidate.

Please add only information that accurately represents your actual
experience, skills, achievements, and qualifications.
"""
)

st.markdown(result)

st.download_button(
    label="Download ATS Report",
    data=result,
    file_name="ATS_Resume_Report.txt",
    mime="text/plain"
)
            st.markdown(result)
            st.download_button(
    label="Download ATS Report",
    data=result,
    file_name="ATS_Resume_Report.txt",
    mime="text/plain"
)

    else:
        st.warning("Please upload resume and enter job description.")
