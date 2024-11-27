# Resume Analyzer Module

The Resume Analyzer module provides functionality to analyze resumes by comparing them with job descriptions to calculate scores like ATS (Applicant Tracking System) and matching scores. This document explains the functionality, methods, and routes in the module.

---

## Features
- Extract text from uploaded PDF and DOCX resumes.
- Preprocess the extracted text by removing special characters and numbers.
- Calculate:
  - **ATS Score**: Based on keyword overlap between resume and job description.
  - **Matching Score**: Using TF-IDF and cosine similarity to evaluate textual similarity.
- Provide results through a web interface built with Flask.


---

## Configuration
- **UPLOAD_FOLDER**: `./uploads`  
  Directory for storing resumes temporarily. This folder is automatically created if it does not exist.
- **ALLOWED_EXTENSIONS**: `{pdf, docx}`  
  Defines the allowed file types for resume uploads.

---

## Functions

### `allowed_file(filename)`
Checks if the uploaded file has a valid extension.

- **Input**: `filename (str)`
- **Returns**: `bool`

### `extract_text(file_path)`
Extracts text content from PDF or DOCX files.

- **Input**: `file_path (str)`
- **Returns**: `str` (extracted text)

### `preprocess_text(text)`
Preprocesses the input text by removing special characters, numbers, and converting it to lowercase.

- **Input**: `text (str)`
- **Returns**: `list` (processed words)

### `calculate_ats_score(resume_words, job_words)`
Calculates ATS score based on keyword overlap.

- **Input**: 
  - `resume_words (list)`
  - `job_words (list)`
- **Returns**: `float` (percentage score)

### `calculate_matching_score(resume_text, job_description)`
Calculates matching score using TF-IDF and cosine similarity.

- **Input**: 
  - `resume_text (str)`
  - `job_description (str)`
- **Returns**: `float` (percentage score)

---

## Routes

### `@resume_analyzer.route('/analyzer', methods=['GET'])`
Renders the **Resume Analyzer Input Page**.

### `@resume_analyzer.route('/analyze-resume', methods=['POST'])`
Handles the resume analysis process:
1. Validates input fields.
2. Extracts text from the uploaded resume.
3. Calculates ATS and matching scores.
4. Renders the results page with calculated scores.

---

## Templates

### `resume_analyzer.html`
- Input form for:
  - Job Name
  - Job Description
  - Resume Upload (PDF/DOCX)

### `resume_results.html`
- Displays:
  - Job Name
  - ATS Score
  - Matching Score

---

## Error Handling
- Displays user-friendly error messages for:
  - Missing fields
  - Unsupported file formats
  - Errors during text extraction

---

## Cleanup
Uploaded files are deleted after analysis to maintain security and storage efficiency.

---

## Example Usage
1. Start the Flask application:
   ```bash
   flask run

