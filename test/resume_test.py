import os
import pytest
from flask import Flask
from src.resume_analyzer import resume_analyzer, allowed_file, preprocess_text, calculate_ats_score, calculate_matching_score

# Test Data Path
TEST_DATA_DIR = "/Users/prabhudattamishra/Job-Analyzer/test/test_data"
TEST_RESUME_DOCX = os.path.join(TEST_DATA_DIR, "test_resume.docx")
TEST_RESUME_PDF = os.path.join(TEST_DATA_DIR, "test_resume.pdf")
TEST_RESUME_TXT = os.path.join(TEST_DATA_DIR, "test_resume.txt")
TEST_JOB_DESCRIPTION = "Looking for a Cloud Engineer with expertise in AWS, Kubernetes, and Terraform."
UPLOAD_FOLDER = "./uploads"

# Flask App Configuration
@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(resume_analyzer)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['TESTING'] = True
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    yield app
    # Cleanup after tests
    for file in os.listdir(UPLOAD_FOLDER):
        os.remove(os.path.join(UPLOAD_FOLDER, file))
    os.rmdir(UPLOAD_FOLDER)

@pytest.fixture
def client(app):
    return app.test_client()

# Functional Tests
def test_allowed_file_valid_extensions():
    assert allowed_file("resume.pdf") is True
    assert allowed_file("resume.docx") is True
    assert allowed_file("resume.txt") is False
    assert allowed_file("resume") is False

def test_preprocess_text():
    text = "This is a Test! 123"
    result = preprocess_text(text)
    assert result == ["this", "is", "a", "test"]

def test_calculate_ats_score():
    resume_words = ["aws", "kubernetes", "terraform", "python"]
    job_words = ["aws", "kubernetes", "terraform", "docker"]
    ats_score = calculate_ats_score(resume_words, job_words)
    assert round(ats_score, 2) == 75.0

def test_calculate_ats_score_no_overlap():
    resume_words = ["python", "java"]
    job_words = ["aws", "kubernetes"]
    ats_score = calculate_ats_score(resume_words, job_words)
    assert ats_score == 0.0

def test_calculate_matching_score():
    resume_text = "AWS Kubernetes Terraform"
    job_description = "Looking for AWS Kubernetes and Terraform experts"
    matching_score = calculate_matching_score(resume_text, job_description)
    assert round(matching_score, 2) > 50.0

def test_calculate_matching_score_no_match():
    resume_text = "Python Java SQL"
    job_description = "AWS Kubernetes Terraform"
    matching_score = calculate_matching_score(resume_text, job_description)
    assert round(matching_score, 2) < 10.0

def test_upload_docx_resume(client):
    if not os.path.exists(TEST_RESUME_DOCX):
        pytest.skip(f"File not found: {TEST_RESUME_DOCX}")
    with open(TEST_RESUME_DOCX, "rb") as resume:
        data = {
            "job_name": "Cloud Engineer",
            "job_description": TEST_JOB_DESCRIPTION,
            "resume": (resume, "test_resume.docx"),
        }
        response = client.post(
            "/analyze-resume", data=data, content_type="multipart/form-data"
        )
        assert response.status_code == 200

def test_upload_pdf_resume(client):
    if not os.path.exists(TEST_RESUME_PDF):
        pytest.skip(f"File not found: {TEST_RESUME_PDF}")
    with open(TEST_RESUME_PDF, "rb") as resume:
        data = {
            "job_name": "Cloud Engineer",
            "job_description": TEST_JOB_DESCRIPTION,
            "resume": (resume, "test_resume.pdf"),
        }
        response = client.post(
            "/analyze-resume", data=data, content_type="multipart/form-data"
        )
        assert response.status_code == 200

def test_invalid_file_type(client):
    if not os.path.exists(TEST_RESUME_TXT):
        pytest.skip(f"File not found: {TEST_RESUME_TXT}")
    with open(TEST_RESUME_TXT, "rb") as resume:
        data = {
            "job_name": "Cloud Engineer",
            "job_description": TEST_JOB_DESCRIPTION,
            "resume": (resume, "test_resume.txt"),
        }
        response = client.post(
            "/analyze-resume", data=data, content_type="multipart/form-data"
        )
        assert response.status_code == 200
        assert "Invalid resume file" in response.get_data(as_text=True)

# Non-Functional Tests
def test_large_job_description(client):
    large_description = "AWS " * 1000
    if not os.path.exists(TEST_RESUME_DOCX):
        pytest.skip(f"File not found: {TEST_RESUME_DOCX}")
    with open(TEST_RESUME_DOCX, "rb") as resume:
        data = {
            "job_name": "Cloud Engineer",
            "job_description": large_description,
            "resume": (resume, "test_resume.docx"),
        }
        response = client.post(
            "/analyze-resume", data=data, content_type="multipart/form-data"
        )
        assert response.status_code == 200

def test_missing_resume_field(client):
    response = client.post(
        "/analyze-resume",
        data={"job_name": "Cloud Engineer", "job_description": TEST_JOB_DESCRIPTION},
        content_type="multipart/form-data",
    )
    assert response.status_code == 200
    assert "All fields are required" in response.get_data(as_text=True)

def test_missing_job_name_field(client):
    if not os.path.exists(TEST_RESUME_DOCX):
        pytest.skip(f"File not found: {TEST_RESUME_DOCX}")
    with open(TEST_RESUME_DOCX, "rb") as resume:
        data = {
            "job_description": TEST_JOB_DESCRIPTION,
            "resume": (resume, "test_resume.docx"),
        }
        response = client.post(
            "/analyze-resume", data=data, content_type="multipart/form-data"
        )
        assert response.status_code == 200
        assert "All fields are required" in response.get_data(as_text=True)

def test_invalid_job_name_length(client):
    if not os.path.exists(TEST_RESUME_DOCX):
        pytest.skip(f"File not found: {TEST_RESUME_DOCX}")
    with open(TEST_RESUME_DOCX, "rb") as resume:
        data = {
            "job_name": "A" * 256,  # Exceed reasonable length
            "job_description": TEST_JOB_DESCRIPTION,
            "resume": (resume, "test_resume.docx"),
        }
        response = client.post(
            "/analyze-resume", data=data, content_type="multipart/form-data"
        )
        assert response.status_code == 200
        assert "Job name is too long" not in response.get_data(as_text=True)

# Add other edge cases as necessary
