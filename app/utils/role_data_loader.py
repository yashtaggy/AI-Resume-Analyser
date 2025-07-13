import json
import os

def load_role_skills(role):
    data_path = os.path.join(os.path.dirname(__file__), '../../data/role_skills.json')
    with open(data_path, 'r') as file:
        skills_data = json.load(file)
    return skills_data.get(role, [])
