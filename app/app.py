from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename

from pdfminer.high_level import extract_text as extract_pdf_text
from docx import Document
from utils.skill_matcher import load_required_skills, compare_skills

# Configuration
UPLOAD_FOLDER = 'app/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

# Flask app setup
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Helper to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Extract text from PDF
def extract_text_from_pdf(file_path):
    return extract_pdf_text(file_path)

# Extract text from DOCX
def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return '\n'.join([para.text for para in doc.paragraphs])

# Unified text extractor
def extract_resume_text(file_path):
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    else:
        return ""

# Route: Resume upload and processing
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        uploaded_file = request.files['resume']
        if uploaded_file and allowed_file(uploaded_file.filename):
            filename = secure_filename(uploaded_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(filepath)

            # Extract text
            resume_text = extract_resume_text(filepath)

            # Load required skills for DevOps role
            required_skills = load_required_skills('app/skill_maps/devops.json')

            # Compare skills
            matched, missing = compare_skills(resume_text, required_skills)

            # Show result
            result_html = f"""
            <h2>Uploaded: {filename}</h2>
            <h3>Skills Found in Resume:</h3>
            <ul>{''.join(f'<li>{skill}</li>' for skill in matched)}</ul>
            <h3>Missing Skills for DevOps Role:</h3>
            <ul>{''.join(f'<li>{skill}</li>' for skill in missing)}</ul>
            """

            return result_html

        else:
            return "Invalid file type. Please upload a PDF or DOCX."

    return render_template('index.html')

# Run app
if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    import os
    port = int(os.environ.get("PORT", 5000))  # default to 5000 for local dev
    app.run(host="0.0.0.0", port=port, debug=True)


