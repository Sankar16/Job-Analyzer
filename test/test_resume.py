"""
test_resume.py
This file contains unit tests for the Resume Analyzer module.
It tests both functional and non-functional aspects of the application.
"""

import os
import sys
import unittest
from io import BytesIO
from threading import Thread  # Standard library imports go first
from flask import Flask, render_template  # Third-party imports go next

# Dynamically adjust the Python path to include the src directory
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(TEST_DIR, '..'))
SRC_DIR = os.path.join(PROJECT_ROOT, 'src')
sys.path.insert(0, SRC_DIR)

from resume_analyzer import resume_analyzer, UPLOAD_FOLDER, extract_text  # noqa: E402

# Set the templates directory (inside src)
TEMPLATES_DIR = os.path.join(SRC_DIR, 'templates')

# Create a Flask app for testing, specifying the templates directory
app = Flask(__name__, template_folder=TEMPLATES_DIR)
app.register_blueprint(resume_analyzer)
app.config['TESTING'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'raven@3004'  # Added a secret key for session management


@app.route('/home')
def home():
    """Render the home page."""
    return render_template('index.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    """Render the search page."""
    return "Search Page"


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Render the signup page."""
    return "Sign Up"


@app.route('/signout', methods=['GET', 'POST'])
def signout():
    """Render the signout page."""
    return "Sign out"


@app.route('/showUserProfile', methods=['GET', 'POST'])
def showUserProfile():  # noqa: N802 (allow camel case for backward compatibility)
    """Render the user profile page."""
    return "showUserProfile"


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Render the login page."""
    return "Login Page"


@app.route('/notifications', methods=['GET', 'POST'])
def notifications():
    """Render the notifications page."""
    return "Notifications Page"


# Path to the test_files directory
TEST_FILES_DIR = os.path.join(PROJECT_ROOT, 'test_files')


class ResumeAnalyzerTestCase(unittest.TestCase):
    """Test case class for Resume Analyzer."""

    @staticmethod
    def create_pdf(content, file_path):
        """Helper method to create a PDF file with the given content."""
        from reportlab.pdfgen import canvas  # noqa: E402
        pdf_canvas = canvas.Canvas(file_path)
        text_object = pdf_canvas.beginText()
        text_object.setTextOrigin(10, 800)
        text_object.textLines(content)
        pdf_canvas.drawText(text_object)
        pdf_canvas.save()

    def setUp(self):
        """Set up the test client and ensure the upload folder exists."""
        self.app = app.test_client()
        self.app.testing = True
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    def tearDown(self):
        """Clean up uploaded files after each test."""
        for filename in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)

    def upload_resume(self, data, resume_filename):
        """Helper method to upload a resume."""
        resume_path = os.path.join(TEST_FILES_DIR, resume_filename)
        with open(resume_path, 'rb') as resume_file:
            data['resume'] = (BytesIO(resume_file.read()), resume_filename)
            with self.app.session_transaction() as sess:
                sess['user'] = {'_id': 'test_user_id'}
            response = self.app.post(
                '/analyze-resume',
                data=data,
                content_type='multipart/form-data'
            )
        return response

    def test_valid_pdf_upload(self):
        """Test uploading a valid PDF resume."""
        data = {
            'job_name': 'Software Engineer',
            'job_description': 'Develop and maintain software applications.'
        }
        response = self.upload_resume(data, 'sample_resume.pdf')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ATS Score', response.data)

    def test_valid_docx_upload(self):
        """Test uploading a valid DOCX resume."""
        data = {
            'job_name': 'Data Analyst',
            'job_description': 'Analyze data to support business decisions.'
        }
        response = self.upload_resume(data, 'sample_resume.docx')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ATS Score', response.data)

    def test_no_keyword_overlap(self):
        """Test a job description with no overlapping keywords."""
        data = {
            'job_name': 'Chemist',
            'job_description': 'Conduct chemical experiments and analyses.'
        }
        response = self.upload_resume(data, 'software_resume.pdf')
        self.assertIn(b'ATS Score', response.data)
        self.assertIn(b'0.0%', response.data)

    def test_identical_resume_and_job_description(self):
        """Test an identical resume and job description."""
        data = {'job_name': 'Copywriter'}
        resume_filename = 'sample_resume.pdf'
        resume_path = os.path.join(TEST_FILES_DIR, resume_filename)
        with open(resume_path, 'rb') as resume_file:
            resume_content = resume_file.read()
            data['resume'] = (BytesIO(resume_content), resume_filename)
            resume_file_path = os.path.join(UPLOAD_FOLDER, 'temp_resume.pdf')
            with open(resume_file_path, 'wb') as temp_resume_file:
                temp_resume_file.write(resume_content)
            try:
                resume_text = extract_text(resume_file_path)
                data['job_description'] = resume_text
                with self.app.session_transaction() as sess:
                    sess['user'] = {'_id': 'test_user_id'}
                response = self.app.post(
                    '/analyze-resume',
                    data=data,
                    content_type='multipart/form-data'
                )
                self.assertIn(b'ATS Score', response.data)
                self.assertIn(b'100.0%', response.data)
            finally:
                if os.path.exists(resume_file_path):
                    os.remove(resume_file_path)

    def test_file_deletion_after_processing(self):
        """Test that uploaded files are deleted after processing."""
        data = {
            'job_name': 'Consultant',
            'job_description': 'Provide expert advice to clients.'
        }
        filename = 'sample_resume.pdf'
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        self.upload_resume(data, filename)
        self.assertFalse(os.path.exists(filepath))

    def test_response_time_for_large_files(self):
        """Test response time for analyzing large resumes."""
        import time  # noqa: E402
        data = {
            'job_name': 'Senior Researcher',
            'job_description': 'A' * 10000
        }
        resume_filename = 'large_resume.pdf'
        resume_path = os.path.join(TEST_FILES_DIR, resume_filename)
        if not os.path.exists(resume_path):
            with open(os.path.join(TEST_FILES_DIR, 'sample_resume.pdf'), 'rb') as sample_file:
                sample_content = sample_file.read()
            with open(resume_path, 'wb') as large_file:
                large_file.write(sample_content * 50)
        start_time = time.time()
        response = self.upload_resume(data, resume_filename)
        end_time = time.time()
        self.assertIn(b'ATS Score', response.data)
        self.assertLess(end_time - start_time, 10)

    def test_multiple_users_simultaneously(self):
        """Test multiple users uploading resumes simultaneously."""

        def worker():
            data = {
                'job_name': 'User Test',
                'job_description': 'Test job description.'
            }
            response = self.upload_resume(data, 'sample_resume.pdf')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'ATS Score', response.data)

        threads = [Thread(target=worker) for _ in range(5)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    def test_resume_with_unicode_characters(self):
        """Test resumes with Unicode characters."""
        data = {
            'job_name': 'International Relations Specialist',
            'job_description': 'Work on international projects and coordinate with global teams.'
        }
        resume_filename = 'unicode_resume.pdf'
        resume_path = os.path.join(TEST_FILES_DIR, resume_filename)
        if not os.path.exists(resume_path):
            self.create_pdf(
                "Experienced in international affairs. Fluent in Spanish, Français, 中文.",
                resume_path
            )
        response = self.upload_resume(data, resume_filename)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ATS Score', response.data)

    def test_resume_with_common_keywords(self):
        """Test resumes with common keywords for a high ATS score."""
        data = {
            'job_name': 'Marketing Manager',
            'job_description': (
                'Lead marketing campaigns and strategies to increase brand awareness.'
            )
        }
        resume_filename = 'marketing_resume.pdf'
        resume_path = os.path.join(TEST_FILES_DIR, resume_filename)
        if not os.path.exists(resume_path):
            self.create_pdf(
                "Experienced in leading marketing campaigns and increasing brand awareness.",
                resume_path
            )
        response = self.upload_resume(data, resume_filename)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ATS Score', response.data)
        self.assertNotIn(b'0.0%', response.data)


if __name__ == '__main__':
    unittest.main()
