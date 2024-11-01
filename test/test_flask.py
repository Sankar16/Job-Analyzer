from src.app import app, add, mongodb_client
import pandas as pd
from werkzeug.datastructures import ImmutableMultiDict

db = mongodb_client.db

client = app.test_client()

def valid_login():
    email = 'ish2@ish.com'
    password = 'ish'
    
    return client.post('/login', data={
        "email": email,
        "password": password
    }, follow_redirects=True)

def invalid_login():
    email = 'not_found@not_found.com'
    password = 'not_found'
    
    return client.post('/login', data={
        "email": email,
        "password": password
    }, follow_redirects=True)

def test_user_singup_ip1():
    email = ""
    password = ""
    name = ""

    response = app.test_client().post('/user/signup', data={
        "name": name,
        "email": email,
        "password": password
    })

def test_user_singup_ip2():
    email = "invlid_email"
    password = ""
    name = ""

    response = app.test_client().post('/user/signup', data={
        "name": name,
        "email": email,
        "password": password
    })

def test_user_singup_ip3():
    email = "invalid_email@"
    password = ""
    name = ""

    response = app.test_client().post('/user/signup', data={
        "name": name,
        "email": email,
        "password": password
    })

def test_user_singup_ip4():
    email = "valid_email@email.com"
    password = ""
    name = ""

    response = app.test_client().post('/user/signup', data={
        "name": name,
        "email": email,
        "password": password
    })

def test_user_singup_ip5():
    email = "valid_email@without_dot_com"
    password = ""
    name = ""

    response = app.test_client().post('/user/signup', data={
        "name": name,
        "email": email,
        "password": password
    })

def test_user_singup_ip6():
    email = "valid_email@email.com"
    password = "non_empty_password"
    name = ""

    response = app.test_client().post('/user/signup', data={
        "name": name,
        "email": email,
        "password": password
    })

def test_user_singup_ip7():
    email = "invalid_email"
    password = "valid_password"
    name = ""

    response = app.test_client().post('/user/signup', data={
        "name": name,
        "email": email,
        "password": password
    })

def test_user_singup_ip8():
    email = "invalid_email"
    password = "valid_password"
    name = ""

    response = app.test_client().post('/user/signup', data={
        "name": name,
        "email": email,
        "password": password
    })

def test_user_singup_ip9():
    email = "valid_email@email.com"
    password = "valid_password"
    name = "non_empty_name"

    response = app.test_client().post('/user/signup', data={
        "name": name,
        "email": email,
        "password": password
    })

def test_user_singup_ip10():
    email = "valid_email@email.com"
    password = "valid_password"
    name = "*****************************"

    response = app.test_client().post('/user/signup', data={
        "name": name,
        "email": email,
        "password": password
    })


def test_user_singup_ip11():
    email = "valid_email@email.com"
    password = "valid_password"
    name = "non_empty_name"

    response = app.test_client().post('/user/signup', data={
        "name": name,
        "email": email,
        "password": password
    })

def test_user_singup_ip12():
    email = "invalid_email"
    password = "valid_password"
    name = "************"

    response = app.test_client().post('/user/signup', data={
        "name": name,
        "email": email,
        "password": password
    })

def test_user_singup_ip13():
    email = "invalid_email"
    password = ""
    name = "************"

    response = app.test_client().post('/user/signup', data={
        "name": name,
        "email": email,
        "password": password
    })


def test_user_singup_ip14():
    email = "invalid_email"
    password = ""
    name = "************"

    response = app.test_client().post('/user/signup', data={
        "name": name,
        "email": email,
        "password": password
    })

def test_user_profile_check_name_and_email():

    response = app.test_client().get('/user/profile')
    assert response.status_code == 200
    assert b"User Profile" in response.data
    assert b"Name" in response.data
    assert b"Email" in response.data


def test_user_profile_check_upload_resume():

    response = app.test_client().get('/user/profile')
    assert response.status_code == 200
    assert b"Upload Resume" in response.data

def test_home_page():
    """
    This test verifies that the home page works correctly
    """

    response = app.test_client().get('/home')
    print(response)
    assert response.status_code == 200
    assert b"Welcome to JobCruncher!" in response.data
    assert b"So why use JobCruncher instead?" in response.data


def test_search_page():
    """
    This test verifies that search page displays the user input form correctly
    """

    response = app.test_client().get('/search')
    assert response.status_code == 200
    assert b"Job Title" in response.data
    assert b"Location" in response.data
    assert b"Company Name" in response.data
    assert b"Technical skills" in response.data
    assert b"Job Type" in response.data


def test_search_page_submit():
    """
    This test verifies that search page filters the data based on the given input
    """

    add_sample_data()
    response = app.test_client().post("/search", data={
        "title": "",
        "type": "",
        "location": "",
        "companyName": "",
        "skills": "",
    })
    assert response.status_code == 200


def test_search_page_submit_zero_results():
    """
    This test verifies that the search page works correctly when given input does not match any entries in the database
    """
    response = app.test_client().post("/search", data={
        "title": "zzzzzzzzzzz",
        "type": "yyyyyyyyyyy",
        "location": "xxxxxxx",
        "companyName": "wwwwwwww",
        "skills": "vvvvvvvvv",
    })
    assert response.status_code == 200
    assert b"Sorry, there are no current openings with given criteria"


def test_add_db():
    """
    This test verifies that sample data can be added to the database successfully
    """

    add_sample_data()


def add_sample_data():
    """
    This function adds sample data entry to the database
    """

    df = pd.DataFrame()

    job_dict = {
        "Job Title": "Software Engineer, New Grad",
        "Company Name": "IXL Learning",
        "Location": "Raleigh, NC",
        "Date Posted": "2 days ago",
        "Total Applicants": "Over 200 applicants",
        "Job Description": "IXL Learning, a leading edtech company with products used by 13 millio…",
        "Job Link": "https://www.linkedin.com/jobs/view/externalApply/3200864048?url=https%…",
        "Seniority level": "Not Applicable",
        "Employment type": "Full-time",
        "Job function": "Engineering and Information Technology",
        "Industries": "E-Learning Providers",
        "skills": "linux,react,ui,scala,sql,python,java"
    }
    df = df.append(job_dict, ignore_index=True)
    add(db, df)
