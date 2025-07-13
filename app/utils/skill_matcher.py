import os
import json
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    return text.lower()

def load_role_config(role):
    # role will be like "data_scientist"
    config_path = os.path.join(os.path.dirname(__file__), '..', 'skill_maps', f'{role}.json')
    with open(config_path, "r") as file:
        return json.load(file)


def analyze_resume(resume_path, role):
    role_data = load_role_config(role)
    required_skills = role_data.get("skills", [])

    # Extract resume text
    resume_text = extract_text_from_pdf(resume_path)
    matched_skills = [skill for skill in required_skills if skill.lower() in resume_text]

    # Split matched/missing
    present_skills = []
    missing_skills = []

    for skill in required_skills:
        if skill.lower() in resume_text:
            present_skills.append(skill)
        else:
            missing_skills.append(skill)

    return {
        "matched_skills": present_skills,
        "missing_skills": missing_skills,
        "total_required": len(required_skills),
        "matched_count": len(present_skills)
    }