# test_two_factor_auth.py

import unittest
from unittest.mock import patch
from src.app import app, db
from flask import session
from bson.objectid import ObjectId
from passlib.hash import pbkdf2_sha256
import uuid

import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestTwoFactorAuth(unittest.TestCase):

    def setUp(self):
        # Set up a test client
        self.app = app.test_client()
        self.app.testing = True

        # Create a test user in the database
        self.test_user_email = 'testuser@example.com'
        self.test_user_password = 'TestPassword123'
        self.test_user = {
            '_id': uuid.uuid4().hex,
            'name': 'Test User',
            'email': self.test_user_email,
            'password': pbkdf2_sha256.hash(self.test_user_password),
            'is_verified': True
        }
        db.users.insert_one(self.test_user)

    def tearDown(self):
        # Remove the test user from the database
        db.users.delete_many({'email': {'$in': [self.test_user_email, 'newuser@example.com', 'unverified@example.com']}})
        # Clear session data
        with self.app.session_transaction() as sess:
            sess.clear()

    @patch('src.User.models.User.send_otp_email')
    def test_signup_sends_otp(self, mock_send_email):
        """
        Test that signing up sends an OTP email for verification.
        """
        new_user_email = 'newuser@example.com'
        new_user_password = 'NewUserPassword123'

        # Ensure the email is not already in use
        db.users.delete_one({'email': new_user_email})

        response = self.app.post('/user/signup', data={
            'name': 'New User',
            'email': new_user_email,
            'password': new_user_password
        }, follow_redirects=True)

        # Check that the user is redirected to OTP verification page
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Verify Your Email', response.data)

        # Check that send_otp_email was called
        mock_send_email.assert_called_once_with(new_user_email, unittest.mock.ANY)

        # Verify that the OTP is stored in the user's database record
        user = db.users.find_one({'email': new_user_email})
        self.assertIsNotNone(user)
        self.assertIn('otp', user)
        self.assertFalse(user.get('is_verified', True))

    def test_verify_signup_correct_otp(self):
        """
        Test verifying the correct OTP during signup.
        """
        new_user_email = 'newuser@example.com'
        new_user_password = 'NewUserPassword123'

        # Simulate signing up to get OTP sent
        with patch('src.User.models.User.send_otp_email'):
            self.app.post('/user/signup', data={
                'name': 'New User',
                'email': new_user_email,
                'password': new_user_password
            }, follow_redirects=True)

            # Get the OTP from the user's record
            user = db.users.find_one({'email': new_user_email})
            otp = user.get('otp')

            # Simulate entering the correct OTP
            with self.app.session_transaction() as sess:
                sess['user_email'] = new_user_email

            response = self.app.post('/user/verify_signup_otp', data={
                'otp': otp
            }, follow_redirects=True)

            # Check that the user is redirected to the home page
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Welcome to JobCruncher!', response.data)

            # Verify that the user's email is marked as verified
            user = db.users.find_one({'email': new_user_email})
            self.assertTrue(user.get('is_verified', False))

    def test_verify_signup_incorrect_otp(self):
        """
        Test verifying an incorrect OTP during signup.
        """
        new_user_email = 'newuser@example.com'
        new_user_password = 'NewUserPassword123'

        # Simulate signing up to get OTP sent
        with patch('src.User.models.User.send_otp_email'):
            self.app.post('/user/signup', data={
                'name': 'New User',
                'email': new_user_email,
                'password': new_user_password
            }, follow_redirects=True)

            # Simulate entering an incorrect OTP
            with self.app.session_transaction() as sess:
                sess['user_email'] = new_user_email

            response = self.app.post('/user/verify_signup_otp', data={
                'otp': '000000'  # Incorrect OTP
            }, follow_redirects=True)

            # Check that an error message is displayed
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Invalid OTP. Please try again.', response.data)

    @patch('src.User.models.User.send_otp_email')
    def test_resend_signup_otp(self, mock_send_email):
        """
        Test resending OTP during signup.
        """
        new_user_email = 'newuser@example.com'
        new_user_password = 'NewUserPassword123'

        # Simulate signing up to get OTP sent
        with patch('src.User.models.User.send_otp_email'):
            self.app.post('/user/signup', data={
                'name': 'New User',
                'email': new_user_email,
                'password': new_user_password
            }, follow_redirects=True)

        # Simulate session
        with self.app.session_transaction() as sess:
            sess['user_email'] = new_user_email

        # Call resend OTP
        response = self.app.get('/user/resend_signup_otp', follow_redirects=True)

        print(response.data)

        # Check that the success message is displayed
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'A new OTP has been sent to your email.', response.data)

        # Check that send_otp_email was called
        self.assertTrue(mock_send_email.called)

    @patch('src.User.models.User.send_otp_email')
    def test_login_sends_otp(self, mock_send_email):
        """
        Test that logging in sends an OTP email.
        """
        response = self.app.post('/user/login', data={
            'email': self.test_user_email,
            'password': self.test_user_password
        }, follow_redirects=True)

        # Check that the user is redirected to OTP verification page
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Enter OTP', response.data)

        # Check that send_otp_email was called
        mock_send_email.assert_called_once_with(self.test_user_email, unittest.mock.ANY)

        # Verify that the OTP is stored in the user's database record
        user = db.users.find_one({'email': self.test_user_email})
        self.assertIn('otp', user)

    def test_verify_login_correct_otp(self):
        """
        Test verifying the correct OTP during login.
        """
        # Simulate logging in to get OTP sent
        with patch('src.User.models.User.send_otp_email'):
            self.app.post('/user/login', data={
                'email': self.test_user_email,
                'password': self.test_user_password
            }, follow_redirects=True)

        # Get the OTP from the user's record
        user = db.users.find_one({'email': self.test_user_email})
        otp = user.get('otp')

        # Simulate entering the correct OTP
        with self.app.session_transaction() as sess:
            sess['user_email'] = self.test_user_email

        response = self.app.post('/user/verify_otp', data={
            'otp': otp
        }, follow_redirects=True)

        # Check that the user is redirected to the home page
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to JobCruncher!', response.data)

    def test_verify_login_incorrect_otp(self):
        """
        Test verifying an incorrect OTP during login.
        """
        # Simulate logging in to get OTP sent
        with patch('src.User.models.User.send_otp_email'):
            self.app.post('/user/login', data={
                'email': self.test_user_email,
                'password': self.test_user_password
            }, follow_redirects=True)

        # Simulate entering an incorrect OTP
        with self.app.session_transaction() as sess:
            sess['user_email'] = self.test_user_email

        response = self.app.post('/user/verify_otp', data={
            'otp': '000000'  # Incorrect OTP
        }, follow_redirects=True)

        # Check that an error message is displayed
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid OTP. Please try again.', response.data)

    @patch('src.User.models.User.send_otp_email')
    def test_resend_login_otp(self, mock_send_email):
        """
        Test resending OTP during login.
        """
        # Simulate logging in to get OTP sent
        with patch('src.User.models.User.send_otp_email'):
            self.app.post('/user/login', data={
                'email': self.test_user_email,
                'password': self.test_user_password
            }, follow_redirects=True)

        # Simulate session
        with self.app.session_transaction() as sess:
            sess['user_email'] = self.test_user_email

        # Call resend OTP
        response = self.app.get('/user/resend_login_otp', follow_redirects=True)

        print(response.data)

        # Check that the success message is displayed
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'A new OTP has been sent to your email.', response.data)

        # Check that send_otp_email was called
        self.assertTrue(mock_send_email.called)

    def test_login_unverified_email(self):
        """
        Test that logging in with an unverified email proceeds to OTP verification.
        """
        unverified_email = 'unverified@example.com'
        unverified_password = 'UnverifiedPassword123'

        # Create an unverified user
        db.users.insert_one({
            '_id': uuid.uuid4().hex,
            'name': 'Unverified User',
            'email': unverified_email,
            'password': pbkdf2_sha256.hash(unverified_password),
            'is_verified': False
        })

        with patch('src.User.models.User.send_otp_email'):
            # Attempt to log in
            response = self.app.post('/user/login', data={
                'email': unverified_email,
                'password': unverified_password
            }, follow_redirects=True)

            # Check that the user is redirected to OTP verification page
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Enter OTP', response.data)

        # Clean up by deleting the unverified user
        db.users.delete_one({'email': unverified_email})

    def test_signup_existing_email(self):
        """
        Test that signing up with an existing email returns an error.
        """
        response = self.app.post('/user/signup', data={
            'name': 'Existing User',
            'email': self.test_user_email,  # Existing email
            'password': 'SomePassword123'
        }, follow_redirects=True)

        # Check that the response is a 400 Bad Request
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Email address already in use', response.data)

    def test_login_wrong_password(self):
        """
        Test that logging in with the wrong password redirects back to login.
        """
        response = self.app.post('/user/login', data={
            'email': self.test_user_email,
            'password': 'WrongPassword'
        }, follow_redirects=True)

        # Check that the user is redirected back to login page
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_signup_missing_fields(self):
        """
        Test that signing up with missing fields redirects back to home.
        """
        response = self.app.post('/user/signup', data={
            'name': '',
            'email': '',
            'password': ''
        }, follow_redirects=True)
        print(response.data)
        # Check that the user is redirected to home page
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)


    def test_login_missing_fields(self):
        """
        Test that logging in with missing fields redirects back to login.
        """
        response = self.app.post('/user/login', data={
            'email': '',
            'password': ''
        }, follow_redirects=True)

        # Check that the user is redirected back to login page
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

if __name__ == '__main__':
    unittest.main()
