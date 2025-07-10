🚀 Resume Parser App | Pinnacle Labs Internship

A smart resume parsing web application developed as part of my internship at Pinnacle Labs. It extracts key candidate information from PDF/DOCX resumes using NLP and AI.

🛠 Technologies Used

- Python 3
- Streamlit (User Interface)
- spaCy (Natural Language Processing)
- pdfplumber / docx2txt (Text Extraction)
- Pandas (Data Processing)
- OpenPyXL (Excel Export)

💡 Features

- Upload resumes in PDF or DOCX format
- Extract:
  - Candidate Name
  - Email Address
  - Phone Number
  - Skills
  - Education
- Upload and parse multiple resumes
- Export parsed data to:
  - JSON
  - Excel
  - Local CSV file
- Clean UI with real-time parsing progress

⚙️ Installation

   📌 Clone the repository

   git clone https://github.com/YOUR_USERNAME/AI_Resume_Parser.git
   cd AI_Resume_Parser

   📌 Create and activate a virtual environment
   
   python -m venv venv
   venv\Scripts\activate  # On Windows

   📌 Install dependencies
   
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm

   📌 Run the app
   
   streamlit run app.py

💡 Future Improvements

- OCR Support for scanned/image-based resumes
- Experience Section Extraction (roles, companies, dates)
- Smart Skill Detection using AI models
- Resume Ranking System based on job criteria
- Database Integration for saving parsed results
