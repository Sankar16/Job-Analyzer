import pytest
from unittest import mock
from src.app import app, send_notification_email, run_periodically
from unittest.mock import patch, MagicMock
import pandas as pd
import threading


@pytest.fixture
def client():
    """Fixture to set up a test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['user'] = 'testuser'
        yield client


def test_notifications_route(client):
    """Test that the notifications route renders the correct template."""
    response = client.get('/notifications')
    assert response.status_code == 200


def test_send_notification_email_success():
    jobs_list = [
        {'Job Title': 'Software Engineer', 'Company Name': 'Tech Co', 'Location': 'Remote', 'Job function': 'Development', 'Employment type': 'Full-time', 'Industries': 'Technology', 'Date Posted': '2024-01-01', 'Job Description': 'Develop software solutions.'},
        {'Job Title': 'Data Scientist', 'Company Name': 'Data Inc', 'Location': 'New York', 'Job function': 'Analysis', 'Employment type': 'Part-time', 'Industries': 'Data', 'Date Posted': '2024-01-02', 'Job Description': 'Analyze data trends.'}
    ]

    with mock.patch('smtplib.SMTP_SSL') as mock_smtp:
        mock_smtp.return_value.__enter__.return_value.sendmail = mock.Mock()
        send_notification_email(jobs_list)
        mock_smtp.return_value.__enter__.return_value.sendmail.assert_called_once()


def test_send_notification_email_content():
    jobs_list = [
        {'Job Title': 'Software Engineer', 'Company Name': 'Tech Co', 'Location': 'Remote', 'Job function': 'Development', 'Employment type': 'Full-time', 'Industries': 'Technology', 'Date Posted': '2024-01-01', 'Job Description': 'Develop software solutions.'}
    ]

    with mock.patch('smtplib.SMTP_SSL') as mock_smtp:
        mock_smtp.return_value.__enter__.return_value.sendmail = mock.Mock()
        send_notification_email(jobs_list)

        args, _ = mock_smtp.return_value.__enter__.return_value.sendmail.call_args
        email_body = args[2]

        assert 'Job Listings:' in email_body
        assert 'Job Title: Software Engineer' in email_body
        assert 'Company: Tech Co' in email_body
        assert 'Location: Remote' in email_body


def test_send_notification_email_empty_jobs_list():
    jobs_list = []

    with mock.patch('smtplib.SMTP_SSL') as mock_smtp:
        mock_smtp.return_value.__enter__.return_value.sendmail = mock.Mock()
        send_notification_email(jobs_list)

        mock_smtp.return_value.__enter__.return_value.sendmail.assert_called_once()

        args, _ = mock_smtp.return_value.__enter__.return_value.sendmail.call_args
        email_body = args[2]

        assert 'Job Listings:' in email_body
        assert 'For more details, please check the job postings on our platform.' in email_body


def test_smtp_configuration():
    jobs_list = [{'Job Title': 'Software Engineer', 'Company Name': 'Tech Co', 'Location': 'Remote', 'Job function': 'Development', 'Employment type': 'Full-time', 'Industries': 'Technology', 'Date Posted': '2024-01-01', 'Job Description': 'Develop software solutions.'}]

    with mock.patch('smtplib.SMTP_SSL') as mock_smtp:
        mock_smtp.return_value.__enter__.return_value.login = mock.Mock()
        mock_smtp.return_value.__enter__.return_value.sendmail = mock.Mock()

        send_notification_email(jobs_list)

        mock_smtp.assert_called_with('smtp.gmail.com', 465, context=mock.ANY)
        mock_smtp.return_value.__enter__.return_value.login.assert_called_with('burnoutapp123@gmail.com', 'xszyjpklynmwqsgh')
        mock_smtp.return_value.__enter__.return_value.sendmail.assert_called_with('burnoutapp123@gmail.com', 'shubhamkulkarni2421@gmail.com', mock.ANY)


def test_send_notification_email_invalid_jobs():
    jobs_list = [
        {'Job Title': 'Software Engineer', 'Company Name': 'Tech Co'},
        {'Job Title': 'Data Scientist'}
    ]

    with mock.patch('smtplib.SMTP_SSL') as mock_smtp:
        mock_smtp.return_value.__enter__.return_value.sendmail = mock.Mock()
        send_notification_email(jobs_list)

        assert mock_smtp.return_value.__enter__.return_value.sendmail.called

        args, _ = mock_smtp.return_value.__enter__.return_value.sendmail.call_args
        email_body = args[2]

        assert 'Job Listings:' in email_body
        assert 'For more details, please check the job postings on our platform.' in email_body


def test_send_notification_email_multiple_jobs():
    jobs_list = [
        {
            'Job Title': 'Software Engineer',
            'Company Name': 'Tech Co',
            'Location': 'Remote',
            'Job function': 'Development',
            'Employment type': 'Full-time',
            'Industries': 'Technology',
            'Date Posted': '2024-01-01',
            'Job Description': 'Develop software solutions.'
        },
        {
            'Job Title': 'Data Scientist',
            'Company Name': 'Data Corp',
            'Location': 'New York',
            'Job function': 'Analytics',
            'Employment type': 'Contract',
            'Industries': 'Data Science',
            'Date Posted': '2024-01-02',
            'Job Description': 'Analyze large datasets and create predictive models.'
        },
        {
            'Job Title': 'Product Manager',
            'Company Name': 'Innovate Inc',
            'Location': 'San Francisco',
            'Job function': 'Management',
            'Employment type': 'Full-time',
            'Industries': 'Product Development',
            'Date Posted': '2024-01-03',
            'Job Description': 'Lead product development from conception to launch.'
        }
    ]

    with app.app_context():
        with mock.patch('smtplib.SMTP_SSL') as mock_smtp:
            mock_smtp_instance = mock_smtp.return_value.__enter__.return_value
            send_notification_email(jobs_list)

            assert mock_smtp_instance.sendmail.called
            call_args = mock_smtp_instance.sendmail.call_args
            email_content = call_args[0][2]
            assert 'Software Engineer' in email_content
            assert 'Data Scientist' in email_content
            assert 'Product Manager' in email_content
            assert 'Tech Co' in email_content
            assert 'Data Corp' in email_content
            assert 'Innovate Inc' in email_content


_thread_lock = threading.Lock()


def test_run_periodically_single_thread():
    mock_func = MagicMock()
    with patch('src.app.threading.Thread') as mock_thread:
        run_periodically(1, mock_func)
        run_periodically(1, mock_func)
        mock_thread.assert_called_once()


def test_notificaionconfigured(client):
    with patch('src.app.read_from_db') as mock_read_db, \
         patch('src.app.run_periodically') as mock_run_periodically:
        mock_df = pd.DataFrame({
            'Job Title': ['Software Engineer'],
            'Company Name': ['Tech Co'],
            'Location': ['Remote'],
            'Job function': ['Development'],
            'Employment type': ['Full-time'],
            'Industries': ['Technology'],
            'Date Posted': ['2024-01-01'],
            'Job Description': ['Develop software solutions.']
        })
        mock_read_db.return_value = mock_df
        response = client.post('/notificaionconfigured')
        assert response.status_code == 200
        mock_read_db.assert_called_once()
        mock_run_periodically.assert_called_once_with(60, send_notification_email, mock_df.to_dict(orient="records"))
        assert b'<!doctype html>\n\n<html lang="en">\n\n<style>' in response.data


def test_notificaionconfigured_no_jobs(client):
    with patch('src.app.read_from_db') as mock_read_db, \
         patch('src.app.run_periodically') as mock_run_periodically:
        # Mock an empty DataFrame
        mock_read_db.return_value = pd.DataFrame()
        response = client.post('/notificaionconfigured')
        assert response.status_code == 200
        mock_read_db.assert_called_once()
        mock_run_periodically.assert_not_called()
        assert b'<!doctype html>\n\n<html lang="en">' in response.data


def test_notifications(client):
    response = client.get('/notifications')
    assert response.status_code == 200