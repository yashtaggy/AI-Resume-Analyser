from flask import Flask, render_template, request
from utils.skill_matcher import analyze_resume
from utils.role_data_loader import load_role_skills
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    role = request.form['role']
    resume_file = request.files['resume']

    if resume_file:
        # Save the uploaded resume temporarily
        upload_dir = os.path.join(os.path.dirname(__file__), 'uploads')
        os.makedirs(upload_dir, exist_ok=True)  # Create folder if missing

        filepath = os.path.join(upload_dir, resume_file.filename)
        resume_file.save(filepath)


        # Load role-specific skills
        required_skills = load_role_skills(role)

        # Analyze the resume
        result = analyze_resume(filepath, role)

        # Delete the uploaded file after processing
        os.remove(filepath)

        return render_template('result.html', result=result, role=role)

    return "No resume uploaded", 400

if __name__ == '__main__':
    app.run(debug=True)
