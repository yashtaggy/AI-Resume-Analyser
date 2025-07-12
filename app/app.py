from flask import Flask, render_template, request
from app.utils.skill_matcher import analyze_resume
import os

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    role = request.form.get('role')
    file = request.files['resume']

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        result = analyze_resume(filepath, role)
        return render_template('result.html', result=result, role=role)
    return "No file uploaded", 400

if __name__ == "__main__":
    app.run(debug=True, port=5000)
