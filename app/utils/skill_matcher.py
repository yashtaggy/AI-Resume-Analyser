import os
import json
import fitz  # PyMuPDF
from fuzzywuzzy import fuzz

def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    return text.lower()

def load_role_config(role):
    config_path = os.path.join(os.path.dirname(__file__), '..', 'skill_maps', f'{role}.json')
    with open(config_path, "r") as file:
        return json.load(file)

def fuzzy_match(skill, text, threshold=80):
    # Token sort ratio works well for unordered keywords
    return fuzz.token_sort_ratio(skill.lower(), text.lower()) >= threshold

def analyze_resume(resume_path, role):
    role_data = load_role_config(role)
    required_skills = role_data.get("skills", [])

    resume_text = extract_text_from_pdf(resume_path)

    matched_skills = []
    missing_skills = []

    for skill in required_skills:
        if fuzzy_match(skill, resume_text):
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "total_required": len(required_skills),
        "matched_count": len(matched_skills)
    }
