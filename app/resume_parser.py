import os
from pdfminer.high_level import extract_text
import re

SECTION_HEADERS = {
    "skills": ['skills', 'technical skills', 'technologies', 'hard skills'],
    "experience": ['experience', 'work experience', 'professional experience', 'internship', 'business experience'],
    'projects': ['projects', 'academic projects', 'personal projects', 'academic project' ],
    'profile': ['profile', "professional summary", "objective", 'career','summary',],
    'achievements': ['awards', 'achievements', 'accomplishments'],
    'certificates': ['certificates', 'certifications'],
    'education': ['education', 'education background']
}

all_possible_headers = [
    "skills", "experience", "professional experience", "work experience", 
    "projects", "certifications", "education", "summary", "professional summary",
    "objective", "languages", "achievements", "accomplishments", "hobbies",
    "interests", "awards", "internships", "technical skills", "technologies",
    "academic projects", "personal projects", "profile", "hard skills", 'career', 'academic project', 'education background', 'certificates', 'business experience'
]

def extract_text_from_resume(file_path: str) -> str:
    try:
        text = extract_text(file_path)
        return clean_resume_text(text)
    except Exception as e:
        print(f"!!! Failed to extract text from {file_path}: {e}")
        return ""
    
def clean_resume_text(text: str) -> str:
    lines = text.splitlines()
    cleaned_lines = [' '.join(line.strip().split()) for line in lines if line.strip()]
    return '\n'.join(cleaned_lines)

def extract_sections(text: str) -> dict:
    header_to_section = {}
    for canonical, variants in SECTION_HEADERS.items():
        for h in variants:
            header_to_section[h.lower()] = canonical

    sections = {}
    lines = text.splitlines()
    section_indices = []


    for i, line in enumerate(lines):
        normalized_line = line.strip().lower()
        for h in all_possible_headers:
            h_clean = h.lower()
            if re.match(rf'^{re.escape(h_clean)}\s*[:\-–—]?\s*$', normalized_line):
                section_indices.append((i, h_clean))
                break

    for idx, (line_idx, header) in enumerate(section_indices):
        start = line_idx + 1
        end = section_indices[idx + 1][0] if idx + 1 < len(section_indices) else len(lines)
        section_text = "\n".join(lines[start:end]).strip()
        canonial = header_to_section.get(header)
        if canonial:
            sections[canonial] = section_text
        
    return sections