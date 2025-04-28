from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import spacy

class Matcher:
    def __init__(self, embedder, jd_text, resume_sections_list):
        self.embedder = embedder
        self.nlp = spacy.load('en_core_web_sm')
        self.resume_sections_list = resume_sections_list
        self.jd_text = jd_text

    def extract_ner_keywords(self, text):
        doc = self.nlp(text)
        keywords = [ent.text.lower() for ent in doc.ents if ent.label_ in ['ORG', "SKILL", "TECH", "WORK_OF_ART"]]
        return keywords
    
    def section_similarity(self, resume_sections):
        scores = {}
        for section in ["skills", "experience", "projects", 'certificates', 'education', 'achievements', 'profile']:
            section_text = resume_sections.get(section, "")
            if section_text.strip():
                section_embedding = self.embedder.embed([section_text])[0]
                jd_embedding = self.embedder.embed([self.jd_text])[0]
                score = cosine_similarity([section_embedding], [jd_embedding])[0][0]
                scores[section] = score
            else:
                scores[section] = 0
        return scores

    def match(self):
        match_scores = []
        jd_keywords = self.extract_ner_keywords(self.jd_text)
        
        resume_section = []
        wt_scores = []
        wtg_scores = []
        ner_keywords = []

        for resume_sections in self.resume_sections_list:
            section_scores = self.section_similarity(resume_sections)
            resume_section.append(resume_sections)
            wt_scores.append(section_scores)

            # weighted sum
            weighted_score = (
                0.55 * section_scores['skills'] + 
                0.45 * section_scores['experience'] + 
                0.35 * section_scores['projects'] + 
                0.15 * section_scores['certificates'] +
                0.30 * section_scores['education'] +
                0.10 * section_scores['achievements'] +
                0.10 * section_scores['profile']
            )
            wtg_scores.append(weighted_score)

            # Bonus for NER keyword overlap
            # resume_text = " ".join(resume_sections.values()).lower()
            # ner_hits = sum(1 for kw in jd_keywords if kw in resume_text)
            # bonus = min(ner_hits * 0.01, 0.1) # up to 10% boost

            final_score = round(weighted_score * 100, 2)
            match_scores.append(min(final_score, 100.0))

        ner_keywords.append(jd_keywords)

        return match_scores, section_scores