import json
import re

def load_required_skills(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        return data["required_skills"]

def extract_skills_from_text(text):
    text = text.lower()
    # Tokenize simply by splitting on non-word characters
    words = set(re.findall(r'\b\w+\b', text))
    return words

def compare_skills(resume_text, required_skills):
    resume_words = extract_skills_from_text(resume_text)
    matched = [skill for skill in required_skills if skill.lower() in resume_words]
    missing = [skill for skill in required_skills if skill.lower() not in resume_words]
    return matched, missing
