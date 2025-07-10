import streamlit as st
import pdfplumber
import docx2txt
import re
import spacy
import pandas as pd
import json
from io import BytesIO
from time import sleep

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# =========================
# FUNCTION DEFINITIONS
# =========================
def extract_text_from_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

def extract_text_from_docx(uploaded_file):
    return docx2txt.process(uploaded_file)

def extract_email(text):
    match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return match.group() if match else "Not found"

def extract_phone(text):
    match = re.search(r"\+?\d[\d\s\-()]{8,14}\d", text)
    return match.group() if match else "Not found"

def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return "Not found"

def extract_skills(text):
    skill_set = [
        "python", "java", "sql", "html", "css", "javascript", "c++", "c#", "excel",
        "project management", "time management", "public speaking", "conflict management",
        "data analytics", "communication", "team player", "leadership", "negotiation",
        "recruitment", "hr policies", "benefits", "payroll", "compliance", "training",
        "organizational skills", "analytical skills", "problem solving", "decision making",
        "microsoft office", "presentation", "employee engagement", "talent acquisition"
    ]

    found = []
    resume_text = text.lower()

    for skill in skill_set:
        if skill.lower() in resume_text:
            found.append(skill.title())

    return list(set(found))


def extract_education(text):
    education_keywords = [
        "bachelor", "master", "ph.d", "mba", "b.a", "m.a", "bsc", "msc", "bca", "mca"
    ]
    institute_keywords = ["university", "college", "institute", "school"]
    
    lines = text.lower().split("\n")
    results = []

    for i, line in enumerate(lines):
        if any(degree in line for degree in education_keywords):
            if any(inst in line for inst in institute_keywords):
                results.append(line.strip().title())
            elif i+1 < len(lines) and any(inst in lines[i+1] for inst in institute_keywords):
                results.append((line + " " + lines[i+1]).strip().title())

    return list(set(results))




# =========================
# STREAMLIT UI
# =========================

st.set_page_config(page_title="AI Resume Parser", layout="wide")

st.markdown("""
    <h1 style='text-align: center; color: #003366;'>📄 AI Resume Parser</h1>
    <p style='text-align: center; font-size: 18px;'>Upload resumes (PDF/DOCX) and extract candidate info using AI</p>
    <hr>
""", unsafe_allow_html=True)

uploaded_files = st.file_uploader("Upload One or More Resumes (PDF or DOCX)", type=["pdf", "docx"], accept_multiple_files=True)

if uploaded_files:
    all_parsed_data = []
    progress = st.progress(0)

    for i, file in enumerate(uploaded_files):
        st.markdown(f"### 📄 {file.name}")

        # Extract text
        file_type = file.name.split('.')[-1].lower()
        if file_type == "pdf":
            resume_text = extract_text_from_pdf(file)
        else:
            resume_text = extract_text_from_docx(file)

        # Extract fields
        name = extract_name(resume_text)
        email = extract_email(resume_text)
        phone = extract_phone(resume_text)
        skills = extract_skills(resume_text)
        education = extract_education(resume_text)

        # Show info
        st.info(f"👤 **Name:** {name}")
        st.info(f"📧 **Email:** {email}")
        st.info(f"📞 **Phone:** {phone}")
        st.info(f"💼 **Skills:** {', '.join(skills) if skills else 'Not found'}")
        st.info(f"🎓 **Education:** {', '.join(education) if education else 'Not found'}")

        # Store for export
        parsed_data = {
            "Name": name,
            "Email": email,
            "Phone": phone,
            "Skills": ', '.join(skills),
            "Education": ', '.join(education)
        }
        all_parsed_data.append(parsed_data)
        progress.progress((i + 1) / len(uploaded_files))
        sleep(0.1)

    st.success(f"✅ Parsed {len(all_parsed_data)} resume(s) successfully.")

    # Create export buttons after all files are processed
    st.markdown("## 💾 Download All Parsed Data")
    all_df = pd.DataFrame(all_parsed_data)

    all_df.to_csv("parsed_resumes.csv", index=False)
    st.success("📁 All parsed data also saved as 'parsed_resumes.csv' in your project folder.")


    # Download JSON
    json_data = json.dumps(all_parsed_data, indent=2)
    st.download_button("📥 Download All as JSON", data=json_data, file_name="all_resumes.json", mime="application/json")

    # Download Excel
    excel_buffer = BytesIO()
    all_df.to_excel(excel_buffer, index=False, engine='openpyxl')
    excel_buffer.seek(0)
    st.download_button("📥 Download All as Excel", data=excel_buffer, file_name="all_resumes.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

else:
    st.warning("📁 Please upload one or more resumes to begin.")

st.divider()
st.markdown("<small style='text-align: center; display: block;'>Built with 💙 using Python & Streamlit</small>", unsafe_allow_html=True)
