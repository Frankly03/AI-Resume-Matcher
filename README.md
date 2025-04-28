# AI Resume Matcher

**AI Resume Matcher** is a machine learning-powered tool that helps job seekers and recruiters match resumes with job descriptions based on relevance. This tool processes resumes and job descriptions, calculates a match score, and ranks resumes according to how well they fit the job description.

## Features

- Upload multiple resumes in PDF or DOCX format.
- Paste or select a job description from a list of sample jobs.
- AI-powered resume matching using advanced NLP techniques.
- Rank resumes by relevance to job description.
- Download the matching results as a CSV file.
- View detailed matching scores for each resume.

## Tech Stack

- Python
- Streamlit (for the web interface)
- PDFMiner (for PDF text extraction)
- Spacy (for NLP and NER)
- Sentence Transformers (for embedding text)
- scikit-learn (for cosine similarity calculation)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/ai-resume-matcher.git
   cd ai-resume-matcher

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   
4. Download the required Spacy language model:
   ```bash
   python -m spacy download en_core_web_sm

Usage
1. Download the required Spacy language model:
     After setting up the project and installing dependencies, you can start the app by running the following command:
     ```bash
        streamlit run main.py

2. Upload Resumes:
     You can upload multiple resumes in either PDF or DOCX format.
     The tool will process each resume and extract the relevant sections (such as skills, experience, education, etc.).


3. Enter or Select a Job Description:
     If you already have a Job Description (JD):
       You can simply paste your job description into the text box provided.
       This is the preferred method, as the system will match your resumes to the specific JD you provide.
   
     If you don't have a Job Description:
       Don't worry! We have preloaded a list of sample job descriptions for various roles.
       Just select a job role (e.g., Data Scientist, Machine Learning Engineer, etc.) from the dropdown list, and we’ll use the sample JD for matching your resumes.
   
5. Click "Match Resumes":
     Once your resumes are uploaded and the job description is provided, click the Match Resumes button.
     The tool will calculate a match score for each resume based on how well it matches the provided job description (or the selected sample JD).

6. Review the Results:
     After the processing is complete, the results will be displayed in a ranked list of resumes, showing their match score in percentage.
     The higher the match score, the more relevant the resume is to the job description.

5. Download the Results:
     You can download the matching results as a CSV file for further analysis and sharing.
     Click the "Download Results as CSV" button to save the results to your local system.
