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
    config_path = os.path.join("app", "skill_maps", f"{role}.json")
    with open(config_path, "r") as file:
        return json.load(file)

def analyze_resume(pdf_path, role):
    extracted_text = extract_text_from_pdf(pdf_path)
    role_data = load_role_config(role)

    present_skills = []
    missing_skills = []

    for skill in role_data["skills"]:
        if skill.lower() in extracted_text:
            present_skills.append(skill)
        else:
            missing_skills.append(skill)

    return {
        "role": role_data["role"],
        "present_skills": present_skills,
        "missing_skills": missing_skills,
        "tools": role_data["tools"],
        "tips": role_data["formatting_tips"]
    }
