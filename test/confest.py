# tests/conftest.py
import pytest
from src.app import app, mongodb_client
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_mail_send(mocker):
    with mocker.patch('src.app.mail.send') as mock_send:
        yield mock_send
