# Job Notification Feature

The Job Notification feature allows users to receive email notifications about new job postings that match their configured preferences, such as job title, location, company name, and required skills. This document outlines the functionality, configuration, and integration points of the feature.

---

## Features

- **User Preferences**: Users can configure notifications based on job title, location, company name, and skills.
- **Real-Time Updates**: Sends notifications whenever matching job postings are available.
- **Email Notifications**: Notifies users via email with detailed job information.
- **Job Bookmarking**: Highlights bookmarked jobs for easy access.
- **Periodic Execution**: Runs checks for new jobs periodically and notifies users.

---

## Configuration

- **Email Sender Account**:  
  - **Email**: `burnoutapp123@gmail.com`  
  - **App Password**: `xszyjpklynmwqsgh`  
- **Notification Interval**:  
  - Default is set to `one day` between periodic job checks.  

---

## Functions

### `read_from_db(request, db)`
Fetches jobs matching user preferences from the database.

- **Input**: 
  - `request (Flask request object)`: Contains user-defined filters.
  - `db (MongoDB client)`: Database connection to fetch job data.
- **Output**: 
  - `DataFrame`: Jobs data with bookmarking details.

---

### `run_periodically(interval, func, *args, **kwargs)`
Ensures a single thread periodically executes a given function.

- **Input**:
  - `interval (int)`: Time in seconds between executions.
  - `func (callable)`: Function to execute.
  - `*args, **kwargs`: Arguments and keyword arguments for the function.
- **Usage**: Keeps checking for new job postings at specified intervals.

---

### `send_notification_email(jobs_list)`
Sends an email to the user with details of matching job postings.

- **Input**:
  - `jobs_list (list)`: List of jobs to include in the email.
- **Output**: Sends an email and logs any errors during the process.
- **Details Included**:
  - Job Title  
  - Company Name  
  - Location  
  - Job Function  
  - Employment Type  
  - Industries  
  - Job Description (truncated to 200 characters)

---

## Flask Routes

### `@app.route('/notificationconfigured', methods=['GET', 'POST'])`
Configures user notifications based on their preferences and starts the periodic check for job updates.

- **Behavior**:
  - Reads user preferences from the form.
  - Fetches matching jobs from the database.
  - Starts periodic email notifications.

---

### `@app.route('/notifications', methods=['GET', 'POST'])`
Enables the notification feature through a toggle.

- **Behavior**:
  - Displays the notification configuration toggle to the user.

---

## Email Template

### Subject: **Job-Cruncher: New Job Notification**

**Body Example**:

Job Listings:

Job Title: Software Engineer
Company: Example Corp
Location: San Francisco, CA
Job Function: Engineering
Employment Type: Full-Time
Industries: Technology
Date Posted: 2024-11-25
Job Description: Develop and maintain scalable software solutions...

For more details, please check the job postings on our platform.


---

## Error Handling

- **Database Issues**: Logs errors if job data retrieval fails.
- **Email Sending Errors**: Logs any SMTP or email-related errors and flashes appropriate messages to users.

---

## Example Usage

1. **Start the Flask Application**:  
   ```bash
   flask run
2. **Enable Notifications**:
  - Visit /notifications to toggle notifications.

3. **Configure Preferences**:
  - Submit job preferences at /notificationconfigured.

4. **Receive Email Alerts**:
  - Check your email for new job notifications periodically.

## Periodic Job Check
The notification system periodically checks for new job postings every day by default and sends email updates to users with matching preferences.

