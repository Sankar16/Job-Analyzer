# Resume Analyzer Module

The Two-Factor Authentication (2FA) module enhances account security by requiring users to verify their identity through an email-based One-Time Password (OTP) during signup and login. This document explains the functionality, methods, and routes in the module.

---

## Features
- **Email-Based OTP Verification**: Sends a unique OTP to the user's email during signup and login for identity verification.
- **Resend OTP Functionality**: Allows users to request a new OTP if they haven't received the original one.
- **Email Verification**: Confirms the validity of the user's email address during signup, adding an extra layer of security.
- **Secure Session Management**: Manages user sessions securely after successful OTP verification.
- **Error Handling and User Feedback**: Provides user-friendly messages for errors and successful actions.


---

## Configuration
smtp_server = 'smtp.gmail.com'
smtp_port = 465  # SSL port
smtp_username = 'email address'  
smtp_password = 'password'  

---

## Functions

### `generate_otp()`
Generates a random numeric OTP of a specified length.

- **Input**: `None`
- **Returns**: `str` (e.g., `'123456'`)

### `send_otp_email(email, otp)`
Sends an email containing the OTP to the user's email address.

- **Input**:
  - `email (str)`: Recipient's email address.
  - `otp (str)`: The generated OTP.
- **Returns**: `None`

### `verify_otp(input_otp, stored_otp, expiry_time)`
Verifies whether the input OTP matches the stored OTP and checks if it's within the valid time frame.

- **Input**:
  - `input_otp (str)`: OTP entered by the user.
  - `stored_otp (str)`: OTP stored in the database.
- **Returns**: `bool` (`True` if OTP is valid; `False` otherwise)

### `resend_otp(user_email)`
Generates a new OTP, updates it in the database, and sends it to the user's email.

- **Input**:
  - `user_email (str)`: The user's email address.
- **Returns**: `None`

### `hash_password(password)`
Hashes the user's password for secure storage.

- **Input**:
  - `password (str)`: Plain-text password.
- **Returns**: `str` (hashed password)

### `check_password(password, hashed_password)`
Verifies that the provided password matches the stored hashed password.

- **Input**:
  - `password (str)`: Plain-text password entered by the user.
  - `hashed_password (str)`: Hashed password from the database.
- **Returns**: `bool` (`True` if passwords match; `False` otherwise)

---

---

## Routes

### `@app.route('/user/signup', methods=['GET', 'POST'])`
Handles user signup.

- **GET**: Renders the signup form.
- **POST**:
  1. Validates input fields (`name`, `email`, `password`).
  2. Checks if the email is already registered.
  3. Hashes the password.
  4. Stores the user in the database with `is_verified` set to `False`.
  5. Generates an OTP and expiry time.
  6. Sends the OTP via email.
  7. Stores the OTP and expiry time in the user's record.
  8. Redirects to `/user/verify_signup_otp`.

### `@app.route('/user/verify_signup_otp', methods=['GET', 'POST'])`
Handles OTP verification during signup.

- **GET**: Renders `verify_signup_otp.html`.
- **POST**:
  1. Retrieves the OTP entered by the user.
  2. Fetches the stored OTP and expiry time from the database.
  3. Calls `verify_otp` to validate the OTP.
  4. If valid, updates `is_verified` to `True`.
  5. Redirects to the login page.
  6. If invalid, displays an error message.

### `@app.route('/user/resend_signup_otp', methods=['GET'])`
Handles resending OTP during signup verification.

- **GET**:
  1. Calls `resend_otp` with the user's email.
  2. Displays a success message indicating that a new OTP has been sent.
  3. Renders `verify_signup_otp.html`.

### `@app.route('/user/login', methods=['GET', 'POST'])`
Handles user login.

- **GET**: Renders the login form.
- **POST**:
  1. Validates input fields (`email`, `password`).
  2. Fetches the user's record from the database.
  3. Checks if the user exists and is verified.
  4. Calls `check_password` to verify the password.
  5. Generates an OTP and expiry time.
  6. Sends the OTP via email.
  7. Stores the OTP and expiry time in the user's record.
  8. Redirects to `/user/verify_login_otp`.

### `@app.route('/user/verify_login_otp', methods=['GET', 'POST'])`
Handles OTP verification during login.

- **GET**: Renders `verify_login_otp.html`.
- **POST**:
  1. Retrieves the OTP entered by the user.
  2. Fetches the stored OTP and expiry time from the database.
  3. Calls `verify_otp` to validate the OTP.
  4. If valid, creates a user session.
  5. Redirects to the home page.
  6. If invalid, displays an error message.

### `@app.route('/user/resend_login_otp', methods=['GET'])`
Handles resending OTP during login verification.

- **GET**:
  1. Calls `resend_otp` with the user's email.
  2. Displays a success message indicating that a new OTP has been sent.
  3. Renders `verify_login_otp.html`.

### `@app.route('/user/logout', methods=['GET'])`
Logs the user out by clearing the session.

- **GET**:
  1. Clears the user's session data.
  2. Redirects to the login page.

---

## Templates

### `signup.html`

- Input form for:
  - **Name**
  - **Email**
  - **Password**
- Links to the login page if the user already has an account.

### `verify_signup_otp.html`

- Input field for **OTP**.
- Button to **Verify OTP**.
- Link to **Resend OTP** if the user didn't receive it.
- Displays success or error messages.

### `login.html`

- Input form for:
  - **Email**
  - **Password**
- Links to the signup page if the user doesn't have an account.

### `verify_login_otp.html`

- Input field for **OTP**.
- Button to **Verify OTP**.
- Link to **Resend OTP** if the user didn't receive it.
- Displays success or error messages.
---

## Error Handling
- **Missing Fields**: Alerts the user if required fields are empty.
- **Invalid Credentials**: Notifies the user if the email or password is incorrect.
- **Unverified Email**: Informs the user to verify their email address.
- **Incorrect OTP**: Displays an error if the entered OTP is incorrect or expired.
- **Email Sending Failure**: Alerts if there's an issue sending the OTP email.
- **Account Already Exists**: Notifies if the email is already registered during signup.


---
## Dependencies

- **Flask**: Web framework for routing and session management.
- **Flask-Mail**: Extension for sending emails through SMTP.
- **Passlib**: Library for secure password hashing.
- **Random and String Modules**: For OTP generation.
- **Datetime**: For handling OTP expiry times.
- **Database Driver**: Such as `PyMongo` for MongoDB to interact with the database.

---

## Setup and Configuration

1. **Install Dependencies**:
   ```bash
   pip install flask flask-mail passlib pymongo
