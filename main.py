import streamlit as st 
import os 
import tempfile
import pandas as pd 
import docx2txt

from app.resume_parser import extract_text_from_resume, extract_sections
from app.jd_parser import clean_job_description, extract_keywords
from app.embedder import TextEmbedder
from app.matcher import Matcher
from app.sample_jds import sample_jds

st.set_page_config(page_title="AI Resume Matcher", layout="wide")
st.title("AI-Powered Resumer Matcher")

#Upload Resumes
uploaded_files = st.file_uploader("Upload Resumes (.pdf or .docx)",  accept_multiple_files=True, type=["pdf", "docx"])

job_title_options = list(sample_jds.keys())
selected_job_title = st.selectbox("Choose a Job Role (Optional)", ["-- Select a Job Title --"] + job_title_options)

# Job Description Input
job_description = st.text_area("Paste Job Description Here", height=200)

if (not job_description) and (selected_job_title and selected_job_title != "-- Select a Job Title --"):
        job_description = sample_jds[selected_job_title]
        st.info(f'Using sample job description for **{selected_job_title}**')

if st.button("Match Resumes") and uploaded_files and job_description:

    with st.spinner("Processing resumes and matching..."):

        resume_texts = []
        resume_names = []
        resume_sections_list = []

        for file in uploaded_files:
            file_ext = os.path.splitext(file.name)[1].lower()

            # save to a temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
                tmp_file.write(file.read())
                tmp_path = tmp_file.name

            # extract text based on file type
            if file_ext == '.pdf':
                text = extract_text_from_resume(tmp_path)
            elif file_ext == '.docx':
                try:
                    text = docx2txt.process(tmp_path)
                except Exception as e:
                    st.error(f"Error reading DOCX file {file.name}: {e}")
                    continue
            else:
                text = ""


            os.remove(tmp_path)

            if text:
                resume_texts.append(text)
                resume_names.append(file.name)
                resume_sections_list.append(extract_sections(text))

        if not resume_texts:
            st.warning("No valid resumes processed.")
            st.stop()

        # Clean JD text & extract keywords
        cleaned_jd = clean_job_description(job_description)
        keywords = extract_keywords(cleaned_jd, top_n=10)


        # Embed
        embedder = TextEmbedder()
        resume_embeddings = embedder.embed(resume_texts)
        jd_embedding = embedder.embed([cleaned_jd])[0]

        # Match
        matcher = Matcher(embedder, cleaned_jd, resume_sections_list)
        scores, w_scores = matcher.match()
    

        # Results as DataFrame
        if scores:
            result_df = pd.DataFrame({
                "Resume Name": resume_names,
                "Match Scores(%)": scores
            }).sort_values(by="Match Scores(%)", ascending=False)
        else:
            st.warning(" No match scores computed. Please upload resumes and enter a valid job description.")

        with st.expander("View w_scores"):
            st.write(w_scores)

        # Show scores
        st.subheader("Matching Results")
        for idx, row in result_df.iterrows():
            st.write(f"**{row['Resume Name']}** — Match Score: `{row['Match Scores(%)']}%`")

        
        # Downloadable CSV
        csv = result_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Results as CSV", csv, "resume_match_score.csv", "text/csv")

        