"""
Flask app for analyzing resumes and calculating ATS and matching scores.
This implementation avoids using heavy NLP libraries and focuses on
simple text processing techniques.
"""

import os
import re
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import docx
import pdfplumber
from collections import Counter

# Initialize Flask app
app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure uploads directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """
    Check if the uploaded file has a valid extension.

    Args:
        filename (str): Name of the file being uploaded.

    Returns:
        bool: True if the file extension is valid, otherwise False.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text(file_path):
    """
    Extract text from a PDF or DOCX file.

    Args:
        file_path (str): Path to the uploaded file.

    Returns:
        str: Extracted text from the file.
    """
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
    """
    Preprocess text by removing special characters, converting to lowercase,
    and splitting into words.

    Args:
        text (str): Input text.

    Returns:
        list: List of words in the preprocessed text.
    """
    text = re.sub(r'[^\w\s]', '', text)  # Remove special characters
    text = re.sub(r'\d+', '', text)  # Remove numbers
    return text.lower().split()  # Convert to lowercase and split into words


def calculate_ats_score(resume_words, job_words):
    """
    Calculate ATS score based on keyword overlap between the resume and job description.

    Args:
        resume_words (list): List of words from the resume.
        job_words (list): List of words from the job description.

    Returns:
        float: ATS score as a percentage.
    """
    resume_counter = Counter(resume_words)
    job_counter = Counter(job_words)
    matching_keywords = sum((resume_counter & job_counter).values())
    total_keywords = sum(job_counter.values())
    return (matching_keywords / total_keywords) * 100 if total_keywords > 0 else 0.0


def calculate_matching_score(resume_text, job_description):
    """
    Calculate matching score using TF-IDF and cosine similarity.

    Args:
        resume_text (str): Extracted text from the resume.
        job_description (str): Job description text.

    Returns:
        float: Matching score as a percentage.
    """
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume_text, job_description])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])
    return similarity[0][0] * 100


@app.route('/analyze-resume', methods=['POST'])
def analyze_resume():
    """
    Analyze resumes and calculate ATS and matching scores.

    Returns:
        Response: JSON response containing ATS score, matching score, and job name.
    """
    if 'resume' not in request.files or 'job_name' not in request.form or 'job_description' not in request.form:
        return jsonify({"error": "Missing required fields: resume, job_name, or job_description"}), 400

    job_name = request.form['job_name']
    job_description = request.form['job_description']
    file = request.files['resume']

    if not file or not allowed_file(file.filename):
        return jsonify({"error": "Invalid resume file. Only PDF or DOCX allowed."}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
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


if __name__ == '__main__':
    app.run(debug=True)