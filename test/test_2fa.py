# tests/test_2fa.py
import pytest
from src.app import db  # Adjust the import based on your project structure
from datetime import datetime, timedelta

def extract_otp(email_body):
    """
    Helper function to extract the OTP from the email body.
    Assumes OTP is a 6-digit number.
    """
    import re
    match = re.search(r'\b\d{6}\b', email_body)
    if match:
        return match.group(0)
    return None

@pytest.fixture
def register_and_verify_user(client, mock_mail_send):
    """
    Fixture to register and verify a user, returning the user's email.
    """
    # Register a new user
    response = client.post('/user/signup', data={
        'name': 'Test User',
        'email': 'testuser@example.com',
        'password': 'SecurePass123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'OTP sent to your email. Please verify your account.' in response.data
    mock_mail_send.assert_called_once()
    
    # Extract OTP from the mocked email
    msg = mock_mail_send.call_args[0][0]
    otp = extract_otp(msg.body)
    assert otp is not None
    
    # Verify the email
    response = client.post('/verify_email', data={
        'otp': otp
    }, query_string={'email': 'testuser@example.com'}, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Email verified successfully! You can now log in.' in response.data
    
    # Confirm verification in the database
    user = db.users.find_one({'email': 'testuser@example.com'})
    assert user is not None
    assert user['is_verified'] == True

    yield 'testuser@example.com'

def test_successful_login_with_2fa(client, mock_mail_send, register_and_verify_user):
    """
    Test Case 3.1.1: Successful Login with Correct Credentials and OTP
    """
    # Submit login credentials
    response = client.post('/login', data={
        'email': register_and_verify_user,
        'password': 'SecurePass123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'OTP sent to your email. Please enter it below.' in response.data
    mock_mail_send.assert_called_once()
    
    # Extract OTP from the mocked email
    msg = mock_mail_send.call_args[0][0]
    otp = extract_otp(msg.body)
    assert otp is not None
    
    # Submit the correct OTP
    response = client.post('/login_otp', data={
        'otp': otp
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Logged in successfully!' in response.data
    # Optionally, check if the user is redirected to the home page or has session variables set

def test_login_with_incorrect_password(client, mock_mail_send, register_and_verify_user):
    """
    Test Case 3.2.1: Login with Incorrect Password
    """
    # Attempt to log in with incorrect password
    response = client.post('/login', data={
        'email': register_and_verify_user,
        'password': 'WrongPass123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Invalid email or password. Please try again.' in response.data
    mock_mail_send.assert_not_called()

def test_login_with_unverified_email(client, mock_mail_send):
    """
    Test Case 3.3.1: Login with Unverified Email
    """
    # Register a new user but do not verify
    response = client.post('/user/signup', data={
        'name': 'Unverified User',
        'email': 'unverified@example.com',
        'password': 'UnverifiedPass123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'OTP sent to your email. Please verify your account.' in response.data
    mock_mail_send.assert_called_once()
    
    # Attempt to log in without verifying email
    response = client.post('/login', data={
        'email': 'unverified@example.com',
        'password': 'UnverifiedPass123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Please verify your email before logging in.' in response.data
    mock_mail_send.assert_called_once()  # No additional OTP should be sent

def test_otp_verification_with_incorrect_otp(client, mock_mail_send, register_and_verify_user):
    """
    Test Case 3.4.2: OTP Verification with Incorrect OTP
    """
    # Submit login credentials
    response = client.post('/login', data={
        'email': register_and_verify_user,
        'password': 'SecurePass123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'OTP sent to your email. Please enter it below.' in response.data
    mock_mail_send.assert_called_once()
    
    # Submit incorrect OTP
    response = client.post('/login_otp', data={
        'otp': '000000'  # Assuming this is incorrect
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Invalid or expired OTP. Please try again.' in response.data

def test_otp_expiration(client, mock_mail_send, register_and_verify_user, monkeypatch):
    """
    Test Case 3.6.1: OTP Expires After Validity Period
    """
    import datetime
    
    # Submit login credentials
    response = client.post('/login', data={
        'email': register_and_verify_user,
        'password': 'SecurePass123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'OTP sent to your email. Please enter it below.' in response.data
    mock_mail_send.assert_called_once()
    
    # Extract OTP from the mocked email
    msg = mock_mail_send.call_args[0][0]
    otp = extract_otp(msg.body)
    assert otp is not None
    
    # Simulate OTP expiration by advancing the system time
    future_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    monkeypatch.setattr('src.app.datetime.datetime', lambda: future_time)
    
    # Submit the expired OTP
    response = client.post('/login_otp', data={
        'otp': otp
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Invalid or expired OTP. Please try again.' in response.data

def test_resend_otp_success(client, mock_mail_send, register_and_verify_user):
    """
    Test Case 3.5.1: Resend OTP Successfully
    """
    # Submit login credentials
    response = client.post('/login', data={
        'email': register_and_verify_user,
        'password': 'SecurePass123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'OTP sent to your email. Please enter it below.' in response.data
    mock_mail_send.assert_called_once()
    
    # Resend OTP
    response = client.post('/resend_otp', data={
        'email': register_and_verify_user
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'A new OTP has been sent to your email.' in response.data
    assert mock_mail_send.call_count == 2  # Initial OTP + Resent OTP
    
    # Extract the new OTP
    msg = mock_mail_send.call_args[0][0]
    new_otp = extract_otp(msg.body)
    assert new_otp is not None
    assert new_otp != '000000'  # Assuming '000000' is incorrect
    assert new_otp != extract_otp(mock_mail_send.call_args_list[0][0][0].body)  # Ensure it's a new OTP
    
    # Submit the new OTP
    response = client.post('/login_otp', data={
        'otp': new_otp
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Logged in successfully!' in response.data

def test_resend_otp_rate_limit(client, mock_mail_send, register_and_verify_user):
    """
    Test Case 3.5.2: Exceed Resend OTP Rate Limits
    """
    # Submit login credentials
    response = client.post('/login', data={
        'email': register_and_verify_user,
        'password': 'SecurePass123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'OTP sent to your email. Please enter it below.' in response.data
    mock_mail_send.assert_called_once()
    
    # Resend OTP up to the allowed limit (e.g., 3 times)
    for i in range(3):
        response = client.post('/resend_otp', data={
            'email': register_and_verify_user
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'A new OTP has been sent to your email.' in response.data
        assert mock_mail_send.call_count == i + 2  # Initial OTP + Resends
    
    # Attempt to resend OTP exceeding the limit
    response = client.post('/resend_otp', data={
        'email': register_and_verify_user
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Too many resend requests. Please try again later.' in response.data
    assert mock_mail_send.call_count == 5  # Adjust based on your resend limit

def test_otp_reuse_prevention(client, mock_mail_send, register_and_verify_user):
    """
    Test Case 3.8.1: Ensure OTP Cannot Be Reused
    """
    # Submit login credentials
    response = client.post('/login', data={
        'email': register_and_verify_user,
        'password': 'SecurePass123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    mock_mail_send.assert_called_once()
    otp = extract_otp(mock_mail_send.call_args[0][0].body)
    
    # Submit the correct OTP
    response = client.post('/login_otp', data={
        'otp': otp
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Logged in successfully!' in response.data
    
    # Attempt to reuse the same OTP for another login
    response = client.post('/login', data={
        'email': register_and_verify_user,
        'password': 'SecurePass123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'OTP sent to your email. Please enter it below.' in response.data
    mock_mail_send.assert_called_twice()
    
    # Reuse the old OTP
    response = client.post('/login_otp', data={
        'otp': otp  # Old OTP
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Invalid or expired OTP. Please try again.' in response.data

def test_otp_isolation_between_users(client, mock_mail_send):
    """
    Test Case 3.8.2: Ensure OTPs are unique per user and cannot be used across different accounts
    """
    # Register and verify User A
    client.post('/user/signup', data={
        'name': 'User A',
        'email': 'usera@example.com',
        'password': 'UserAPass123'
    }, follow_redirects=True)
    mock_mail_send.assert_called_once()
    otp_a = extract_otp(mock_mail_send.call_args[0][0].body)
    client.post('/verify_email', data={
        'otp': otp_a
    }, query_string={'email': 'usera@example.com'}, follow_redirects=True)
    
    # Register and verify User B
    client.post('/user/signup', data={
        'name': 'User B',
        'email': 'userb@example.com',
        'password': 'UserBPass123'
    }, follow_redirects=True)
    mock_mail_send.assert_called_twice()
    otp_b = extract_otp(mock_mail_send.call_args[0][0].body)
    client.post('/verify_email', data={
        'otp': otp_b
    }, query_string={'email': 'userb@example.com'}, follow_redirects=True)
    
    # User A initiates login and receives OTP_A1
    response_a_login = client.post('/login', data={
        'email': 'usera@example.com',
        'password': 'UserAPass123'
    }, follow_redirects=True)
    assert response_a_login.status_code == 200
    mock_mail_send.assert_called_thrice()
    otp_a1 = extract_otp(mock_mail_send.call_args[0][0].body)
    
    # User B initiates login and receives OTP_B1
    response_b_login = client.post('/login', data={
        'email': 'userb@example.com',
        'password': 'UserBPass123'
    }, follow_redirects=True)
    assert response_b_login.status_code == 200
    mock_mail_send.assert_called_four_times()
    otp_b1 = extract_otp(mock_mail_send.call_args[0][0].body)
    
    # User A attempts to use User B's OTP
    response_a_verify = client.post('/login_otp', data={
        'otp': otp_b1  # User A using User B's OTP
    }, follow_redirects=True)
    assert response_a_verify.status_code == 200
    assert b'Invalid or expired OTP. Please try again.' in response_a_verify.data
    
    # User B uses their correct OTP
    response_b_verify = client.post('/login_otp', data={
        'otp': otp_b1
    }, follow_redirects=True)
    assert response_b_verify.status_code == 200
    assert b'Logged in successfully!' in response_b_verify.data
