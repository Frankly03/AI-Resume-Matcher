import re
import spacy

import spacy
from spacy.cli import download
import nltk
from nltk.corpus import stopwords

# Ensure stopwords are downloaded
try:
    stop_words = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))
    
# Try loading the model, and if it fails, download it
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    download('en_core_web_sm')
    nlp = spacy.load('en_core_web_sm')
        

def clean_job_description(text: str) -> str:
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', "", text)
    text = text.lower()
    tokens = [t for t in text.split() if t not in stop_words and len(t) > 2]
    return " ".join(tokens)

def extract_keywords(text: str, top_n=20) -> list:

    doc = nlp(text)
    keywords = [chunk.text.lower() for chunk in doc.noun_chunks if chunk.text.lower() not in stop_words]
    keyword_freq = {}
    for word in keywords:
        keyword_freq[word] = keyword_freq.get(word, 0) + 1
    sorted_keywords = sorted(keyword_freq.items(), key=lambda x: x[1], reverse=True)
    return [kw for kw, _ in sorted_keywords[:top_n]]