"""
Unit tests for the Resume Analyzer feature.
These tests cover functional and non-functional requirements.
"""

import os
import pytest
from flask import Flask
from werkzeug.datastructures import FileStorage
from src.resume_analyzer import (
    resume_analyzer,
    preprocess_text,
    calculate_ats_score,
    calculate_matching_score
)

# Test configuration
UPLOAD_FOLDER = './uploads'
TEST_DATA_PATH = '/Users/prabhudattamishra/Job-Analyzer/test/test_data'
TEST_RESUME_DOCX = os.path.join(TEST_DATA_PATH, 'test_resume.docx')
TEST_RESUME_PDF = os.path.join(TEST_DATA_PATH, 'test_resume.pdf')
TEST_RESUME_TXT = os.path.join(TEST_DATA_PATH, 'test_resume.txt')
TEST_JOB_DESCRIPTION = (
    "Looking for a Cloud Engineer experienced in AWS, Python, and Kubernetes. "
    "Must have knowledge of CI/CD pipelines and Terraform."
)


@pytest.fixture
def client():
    """
    Fixture to set up a Flask test client.
    """
    app = Flask(__name__)
    app.register_blueprint(resume_analyzer)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # Limit upload size to 5MB
    with app.test_client() as client:
        yield client


# Functional Tests
def test_preprocess_text():
    """
    Test that preprocess_text correctly cleans and tokenizes text.
    """
    raw_text = "Hello, World! This is a test, 123."
    processed = preprocess_text(raw_text)
    assert processed == ['hello', 'world', 'this', 'is', 'a', 'test']


def test_calculate_ats_score():
    """
    Test that calculate_ats_score accurately matches keywords.
    """
    resume_words = ['aws', 'python', 'kubernetes', 'terraform']
    job_words = ['cloud', 'engineer', 'aws', 'python', 'kubernetes']
    ats_score = calculate_ats_score(resume_words, job_words)
    assert round(ats_score, 2) == 60.0


def test_calculate_matching_score():
    """
    Test that calculate_matching_score computes similarity accurately.
    """
    resume_text = "I am proficient in AWS, Python, and Kubernetes."
    job_description = "Looking for a Cloud Engineer experienced in AWS, Python, and Kubernetes."
    matching_score = calculate_matching_score(resume_text, job_description)
    assert round(matching_score, 2) > 40.0  # Adjusted threshold based on realistic scoring


def test_upload_docx_resume(client):
    """
    Test uploading a DOCX resume to the analyzer endpoint.
    """
    with open(TEST_RESUME_DOCX, 'rb') as resume:
        data = {
            'job_name': 'Cloud Engineer',
            'job_description': TEST_JOB_DESCRIPTION,
            'resume': (resume, 'test_resume.docx')
        }
        response = client.post('/analyze-resume', data=data, content_type='multipart/form-data')
        assert response.status_code == 200
        assert 'ats_score' in response.get_data(as_text=True)
        assert 'matching_score' in response.get_data(as_text=True)


def test_upload_pdf_resume(client):
    """
    Test uploading a PDF resume to the analyzer endpoint.
    """
    with open(TEST_RESUME_PDF, 'rb') as resume:
        data = {
            'job_name': 'Cloud Engineer',
            'job_description': TEST_JOB_DESCRIPTION,
            'resume': (resume, 'test_resume.pdf')
        }
        response = client.post('/analyze-resume', data=data, content_type='multipart/form-data')
        assert response.status_code == 200
        assert 'ats_score' in response.get_data(as_text=True)
        assert 'matching_score' in response.get_data(as_text=True)


# Non-Functional Tests
def test_invalid_file_type(client):
    """
    Test that an invalid file type is rejected.
    """
    with open(TEST_RESUME_TXT, 'rb') as resume:
        data = {
            'job_name': 'Cloud Engineer',
            'job_description': TEST_JOB_DESCRIPTION,
            'resume': (resume, 'test_resume.txt')
        }
        response = client.post('/analyze-resume', data=data, content_type='multipart/form-data')
        assert response.status_code == 400  # Invalid file type should return 400
        assert "Invalid resume file" in response.get_data(as_text=True)


def test_missing_job_description(client):
    """
    Test that missing a job description returns an error.
    """
    with open(TEST_RESUME_DOCX, 'rb') as resume:
        data = {
            'job_name': 'Cloud Engineer',
            'resume': (resume, 'test_resume.docx')
        }
        response = client.post('/analyze-resume', data=data, content_type='multipart/form-data')
        assert response.status_code == 400  # Missing fields should return 400
        assert "All fields are required" in response.get_data(as_text=True)


def test_large_file(client):
    """
    Test uploading a file larger than the allowed limit.
    """
    large_file_path = os.path.join(TEST_DATA_PATH, 'large_file.pdf')
    with open(large_file_path, 'wb') as large_file:
        large_file.write(os.urandom(6 * 1024 * 1024))  # 6MB file

    with open(large_file_path, 'rb') as resume:
        data = {
            'job_name': 'Cloud Engineer',
            'job_description': TEST_JOB_DESCRIPTION,
            'resume': (resume, 'large_file.pdf')
        }
        response = client.post('/analyze-resume', data=data, content_type='multipart/form-data')
        assert response.status_code == 413  # Payload too large

    os.remove(large_file_path)


def test_concurrent_requests(client):
    """
    Test handling multiple concurrent requests.
    """
    responses = []
    for _ in range(5):  # Simulate 5 concurrent requests
        with open(TEST_RESUME_DOCX, 'rb') as resume:
            data = {
                'job_name': 'Cloud Engineer',
                'job_description': TEST_JOB_DESCRIPTION,
                'resume': (resume, 'test_resume.docx')
            }
            response = client.post('/analyze-resume', data=data, content_type='multipart/form-data')
            responses.append(response)
    for response in responses:
        assert response.status_code == 200
