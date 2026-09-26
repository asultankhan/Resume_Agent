import streamlit as st
from pypdf import PdfReader
from docx import Document
from groq import Groq
import re


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="AI Resume Reviewer",
    page_icon="📄"
)


st.title("📄 AI Resume Reviewer")

st.write(
    "Upload your resume and compare it with a target job description."
)


# -----------------------------
# Groq API Setup
# -----------------------------

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)


# -----------------------------
# Resume Extraction Function
# -----------------------------

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



# -----------------------------
# AI Resume Analysis Function
# -----------------------------

def analyze_resume(resume_text, job_title, job_description):


    prompt = f"""

You are a professional ATS Resume Reviewer and Career Advisor.

Target Job Title:
{job_title}


Analyze the candidate resume against the job description.


IMPORTANT RULES:

- Do not invent any information.
- Do not create fake achievements.
- Do not add unsupported numbers or percentages.
- Do not assume certifications or skills.
- Separate existing information from suggestions.
- Any example improvement must be labelled "Example Only".


Candidate Resume:

{resume_text}


Job Description:

{job_description}


Generate report using this structure:


# Resume Alignment Report


## 1. Professional Summary Assessment


## 2. Strong Matches


## 3. Missing or Weakly Demonstrated Skills


## 4. ATS Keyword Analysis

Present Keywords:

Missing Keywords:


## 5. ATS Formatting Issues


## 6. Recommended Improvements


## 7. Suggested Resume Enhancements


## 8. Fact Verification Checklist

Classify suggestions as:

[Existing Information]

[Needs Candidate Confirmation]

[Example Only]

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



# -----------------------------
# User Interface
# -----------------------------


job_title = st.text_input(
    "Target Job Title"
)


uploaded_resume = st.file_uploader(

    "Upload Resume (PDF/DOCX)",

    type=["pdf", "docx"]

)


job_description = st.text_area(

    "Paste Job Description"

)



# -----------------------------
# Analyze Button
# -----------------------------


if st.button("Analyze Resume"):


    if uploaded_resume and job_description and job_title:


        with st.spinner("Analyzing resume..."):


            resume_text = extract_resume_text(
                uploaded_resume
            )


            result = analyze_resume(

                resume_text,

                job_title,

                job_description

            )


            st.subheader(
                "Resume Analysis Report"
            )


            st.info(
            """
            ⚠️ AI-generated suggestions should be verified by the candidate.

            Please add only information that accurately represents your actual
            experience, skills, achievements, and qualifications.
            """
            )


            st.markdown(result)


            st.download_button(

                label="⬇️ Download ATS Report",

                data=result,

                file_name="ATS_Resume_Report.txt",

                mime="text/plain"

            )


    else:


        st.warning(
            "Please upload resume, enter job title, and provide job description."
        )
