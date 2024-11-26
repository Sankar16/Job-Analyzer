# resume_analyzer.py
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import docx
import pdfplumber
import re
from collections import Counter

resume_analyzer = Blueprint('resume_analyzer', __name__)

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text(file_path):
    if file_path.endswith('.pdf'):
        with pdfplumber.open(file_path) as pdf:
            return "\n".join(
                page.extract_text() for page in pdf.pages if page.extract_text()
            ).strip()
    if file_path.endswith('.docx'):
        doc = docx.Document(file_path)
        return "\n".join(paragraph.text for paragraph in doc.paragraphs).strip()
    return ""


def preprocess_text(text):
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    return text.lower().split()


def calculate_ats_score(resume_words, job_words):
    resume_counter = Counter(resume_words)
    job_counter = Counter(job_words)
    matching_keywords = sum((resume_counter & job_counter).values())
    total_keywords = sum(job_counter.values())
    return (matching_keywords / total_keywords) * 100 if total_keywords > 0 else 0.0


def calculate_matching_score(resume_text, job_description):
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume_text, job_description])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])
    return similarity[0][0] * 100


@resume_analyzer.route('/analyze-resume', methods=['POST'])
def analyze_resume():
    if 'resume' not in request.files or 'job_name' not in request.form or 'job_description' not in request.form:
        return jsonify({"error": "Missing required fields: resume, job_name, or job_description"}), 400

    job_name = request.form['job_name']
    job_description = request.form['job_description']
    file = request.files['resume']

    if not file or not allowed_file(file.filename):
        return jsonify({"error": "Invalid resume file. Only PDF or DOCX allowed."}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    try:
        resume_text = extract_text(filepath)
        if not resume_text:
            raise ValueError("Could not extract text from the resume.")

        resume_words = preprocess_text(resume_text)
        job_words = preprocess_text(job_description)

        ats_score = calculate_ats_score(resume_words, job_words)
        matching_score = calculate_matching_score(resume_text, job_description)

        response = {
            "job_name": job_name,
            "ats_score": f"{round(ats_score, 2)}/100",
            "matching_score": f"{round(matching_score, 2)}/100"
        }
        return jsonify(response), 200

    except Exception as error:
        return jsonify({"error": str(error)}), 500

    finally:
        if os.path.exists(filepath):
            os.remove(filepath)
