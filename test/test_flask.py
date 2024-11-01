from src.app import app, add, mongodb_client
import pandas as pd
from werkzeug.datastructures import ImmutableMultiDict

db = mongodb_client.db

client = app.test_client()

def test_invalid_login_empty_ip1():
    email = ''  # empty email
    password = ''    # empty password
    
    return client.post('/login', data={
        "email": email,
        "password": password
    }, follow_redirects=True)

def test_invalid_login_empty_ip2():
    email = ''  # empty email
    password = 'xyz'    # some random password
    
    return client.post('/login', data={
        "email": email,
        "password": password
    }, follow_redirects=True)

def test_invalid_login_empty_ip3():
    email = 'abc'  # some random email
    password = ''    # empty password
    
    return client.post('/login', data={
        "email": email,
        "password": password
    }, follow_redirects=True)

def test_invalid_login_empty_ip4():
    email = ''                     # empty email
    password = 'correct_password'    # scorrect password password
    
    return client.post('/login', data={
        "email": email,
        "password": password
    }, follow_redirects=True)

def test_invalid_login_empty_ip5():
    email = 'valid@gmail.com'   # valid email
    password = ''               # empty password
    
    return client.post('/login', data={
        "email": email,
        "password": password
    }, follow_redirects=True)

def test_reset_password_ip1():
    email = ""               # all 3 fields empty
    New_Password = ""
    Confirm_password = ""

    response = app.test_client().post('/reset', data={
        "email": email,
        "new_password": New_Password,
        "confirm_password": Confirm_password
    })

def test_reset_password_ip2():
    email = "valid@email.com"            
    New_Password = "abc"
    Confirm_password = ""     # confirm password blank

    response = app.test_client().post('/reset', data={
        "email": email,
        "new_password": New_Password,
        "confirm_password": Confirm_password
    })

def test_reset_password_ip3():
    email = "invalid@email.com"    # invalid email        
    New_Password = "abc"
    Confirm_password = ""     # confirm password blank

    response = app.test_client().post('/reset', data={
        "email": email,
        "new_password": New_Password,
        "confirm_password": Confirm_password
    })

def test_reset_password_ip4():
    email = "valid@email.com"            
    New_Password = "abc"
    Confirm_password = "abc"     # all fields are correct

    response = app.test_client().post('/reset', data={
        "email": email,
        "new_password": New_Password,
        "confirm_password": Confirm_password
    })

def test_reset_password_ip5():
    email = "valid@email.com"            
    New_Password = "abc"
    Confirm_password = "cba"     # both paswords didn't match

    response = app.test_client().post('/reset', data={
        "email": email,
        "new_password": New_Password,
        "confirm_password": Confirm_password
    })

def test_reset_password_ip6():
    email = "valid@email"    # valid email without '.com'        
    New_Password = "abc"
    Confirm_password = "abc"     

    response = app.test_client().post('/reset', data={
        "email": email,
        "new_password": New_Password,
        "confirm_password": Confirm_password
    })

def test_reset_password_ip7():
    email = ""                    # empty email field            
    New_Password = "abc"
    Confirm_password = "abc"     # passwords match

    response = app.test_client().post('/reset', data={
        "email": email,
        "new_password": New_Password,
        "confirm_password": Confirm_password
    })

def test_reset_password_ip8():
    email = "valid@email.com"                         
    New_Password = ""                # new password nil
    Confirm_password = "abc"    

    response = app.test_client().post('/reset', data={
        "email": email,
        "new_password": New_Password,
        "confirm_password": Confirm_password
    })

def test_reset_password_ip9():
    email = "valid@email.com"                         
    New_Password = ""                # new password nil
    Confirm_password = "abc"    

    response = app.test_client().post('/reset', data={
        "email": email,
        "new_password": New_Password,
        "confirm_password": Confirm_password
    })

def test_reset_password_ip10():
    email = "valid@email.com"                         
    New_Password = ""                
    Confirm_password = ""    # no passwords 

    response = app.test_client().post('/reset', data={
        "email": email,
        "new_password": New_Password,
        "confirm_password": Confirm_password
    })

def test_reset_password_ip11():
    email = "invalid@email.com"    # invalid email        
    New_Password = "abc"
    Confirm_password = "abc"     # password's match

    response = app.test_client().post('/reset', data={
        "email": email,
        "new_password": New_Password,
        "confirm_password": Confirm_password
    })

def test_reset_password_ip12():
    email = "invalid@email.com"    # invalid email        
    New_Password = ""         # new password blank
    Confirm_password = "abc"
    
    response = app.test_client().post('/reset', data={
        "email": email,
        "new_password": New_Password,
        "confirm_password": Confirm_password
    })

def test_reset_password_ip13():
    email = "invalid@email.com"    # wrong email         
    New_Password = "abc"
    Confirm_password = "abc"     # passwords match

    response = app.test_client().post('/reset', data={
        "email": email,
        "new_password": New_Password,
        "confirm_password": Confirm_password
    })

def test_reset_password_ip14():
    email = "invalid@email.com"       # wrong email      
    New_Password = "abc"
    Confirm_password = "cba"     # both paswords didn't match

    response = app.test_client().post('/reset', data={
        "email": email,
        "new_password": New_Password,
        "confirm_password": Confirm_password
    })

def test_reset_password_ip15():
    email = ""       # no email      
    New_Password = "abc"
    Confirm_password = "abc"     # paswords match

    response = app.test_client().post('/reset', data={
        "email": email,
        "new_password": New_Password,
        "confirm_password": Confirm_password
    })

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

def test_search_page_submit():
    """
    This test verifies that search page filters the data based on the given input
    """
    test_user = db.users.find_one({'email': 'test@test.com'})
    del test_user['password']

    with app.test_client() as client:
        with client.session_transaction() as session:
            session['user'] = test_user
            session['logged_in'] = True
        
        add_sample_data()
        response = client.post("/search", data={
            "title": "",
            "type": "",
            "location": "",
            "companyName": "",
            "skills": "",
        })
        assert response.status_code == 200

def test_search_page_submit_1():
    """
    This test verifies that search page filters the data based on the given input
    """

    test_user = db.users.find_one({'email': 'test@test.com'})
    del test_user['password']

    with app.test_client() as client:
        with client.session_transaction() as session:
            session['user'] = test_user
            session['logged_in'] = True
        
        add_sample_data()
        response = client.post("/search", data={
        "title": "Software Engineer",
        "type": "",
        "location": "",
        "companyName": "",
        "skills": "",
    })
        assert response.status_code == 200


def test_search_page_submit_2():
    """
    This test verifies that search page filters the data based on the given input
    """

    test_user = db.users.find_one({'email': 'test@test.com'})
    del test_user['password']

    with app.test_client() as client:
        with client.session_transaction() as session:
            session['user'] = test_user
            session['logged_in'] = True
        
        add_sample_data()
        response = client.post("/search", data={
        "title": "SRE",
        "type": "",
        "location": "",
        "companyName": "",
        "skills": "",
        })
        assert response.status_code == 200

def test_search_page_submit_3():
    """
    This test verifies that search page filters the data based on the given input
    """

    test_user = db.users.find_one({'email': 'test@test.com'})
    del test_user['password']

    with app.test_client() as client:
        with client.session_transaction() as session:
            session['user'] = test_user
            session['logged_in'] = True
        
        add_sample_data()
        response = client.post("/search", data={
        "title": "Software Engineer",
        "type": "",
        "location": "",
        "companyName": "TechCorp",
        "skills": "",
        })
        assert response.status_code == 200

def test_search_page_submit_4():
    """
    This test verifies that search page filters the data based on the given input
    """

    test_user = db.users.find_one({'email': 'test@test.com'})
    del test_user['password']

    with app.test_client() as client:
        with client.session_transaction() as session:
            session['user'] = test_user
            session['logged_in'] = True
        
        add_sample_data()
        response = client.post("/search", data={
        "title": "Software Engineer",
        "type": "",
        "location": "",
        "companyName": "Fidelity",
        "skills": "",
        })
        assert response.status_code == 200

def test_search_page_submit_5():
    """
    This test verifies that search page filters the data based on the given input
    """

    test_user = db.users.find_one({'email': 'test@test.com'})
    del test_user['password']

    with app.test_client() as client:
        with client.session_transaction() as session:
            session['user'] = test_user
            session['logged_in'] = True
        
        add_sample_data()
        response = client.post("/search", data={
        "title": "Software Engineer",
        "type": "",
        "location": "San Francisco, CA",
        "companyName": "",
        "skills": "",
        })
        assert response.status_code == 200

def test_search_page_submit_6():
    """
    This test verifies that search page filters the data based on the given input
    """

    test_user = db.users.find_one({'email': 'test@test.com'})
    del test_user['password']

    with app.test_client() as client:
        with client.session_transaction() as session:
            session['user'] = test_user
            session['logged_in'] = True
        
        add_sample_data()
        response = client.post("/search", data={
        "title": "",
        "type": "",
        "location": "San Francisco, CA",
        "companyName": "",
        "skills": "",
    })
    assert response.status_code == 200

def test_search_page_submit_7():
    """
    This test verifies that search page filters the data based on the given input
    """

    test_user = db.users.find_one({'email': 'test@test.com'})
    del test_user['password']

    with app.test_client() as client:
        with client.session_transaction() as session:
            session['user'] = test_user
            session['logged_in'] = True
        
        add_sample_data()
        response = client.post("/search", data={
        "title": "Software Engineer",
        "type": "Full-time",
        "location": "San Francisco, CA",
        "companyName": "",
        "skills": "",
        })
        assert response.status_code == 200

def test_search_page_submit_8():
    """
    This test verifies that search page filters the data based on the given input
    """

    test_user = db.users.find_one({'email': 'test@test.com'})
    del test_user['password']

    with app.test_client() as client:
        with client.session_transaction() as session:
            session['user'] = test_user
            session['logged_in'] = True
        
        add_sample_data()
        response = client.post("/search", data={
        "title": "Software Engineer",
        "type": "",
        "location": "",
        "companyName": "",
        "skills": "Python",
        })
        assert response.status_code == 200

def test_search_page_submit_9():
    """
    This test verifies that search page filters the data based on the given input
    """

    test_user = db.users.find_one({'email': 'test@test.com'})
    del test_user['password']

    with app.test_client() as client:
        with client.session_transaction() as session:
            session['user'] = test_user
            session['logged_in'] = True
        
        add_sample_data()
        response = client.post("/search", data={
        "title": "Software Engineer",
        "type": "",
        "location": "",
        "companyName": "C#",
        "skills": "",
        })
        assert response.status_code == 200

def test_search_page_submit_10():
    """
    This test verifies that search page filters the data based on the given input
    """

    test_user = db.users.find_one({'email': 'test@test.com'})
    del test_user['password']

    with app.test_client() as client:
        with client.session_transaction() as session:
            session['user'] = test_user
            session['logged_in'] = True
        
        add_sample_data()
        response = client.post("/search", data={
        "title": "SRE",
        "type": "",
        "location": "San Francisco, CA",
        "companyName": "Google",
        "skills": "",
        })
        assert response.status_code == 200

def test_search_page_submit_11():
    """
    This test verifies that search page filters the data based on the given input
    """

    test_user = db.users.find_one({'email': 'test@test.com'})
    del test_user['password']

    with app.test_client() as client:
        with client.session_transaction() as session:
            session['user'] = test_user
            session['logged_in'] = True
        
        add_sample_data()
        response = client.post("/search", data={
        "title": "",
        "type": "",
        "location": "San Francisco, CA",
        "companyName": "Amazon",
        "skills": "",
        })
        assert response.status_code == 200

def test_search_page_submit_12():
    """
    This test verifies that search page filters the data based on the given input
    """

    test_user = db.users.find_one({'email': 'test@test.com'})
    del test_user['password']

    with app.test_client() as client:
        with client.session_transaction() as session:
            session['user'] = test_user
            session['logged_in'] = True
        
        add_sample_data()
        response = client.post("/search", data={
        "title": "Software Engineer",
        "type": "",
        "location": "San Francisco, CA",
        "companyName": "TechCorp",
        "skills": "Azure",
        })
        assert response.status_code == 200

def test_search_page_submit_13():
    """
    This test verifies that search page filters the data based on the given input
    """

    test_user = db.users.find_one({'email': 'test@test.com'})
    del test_user['password']

    with app.test_client() as client:
        with client.session_transaction() as session:
            session['user'] = test_user
            session['logged_in'] = True
        
        add_sample_data()
        response = client.post("/search", data={
        "title": "Software Engineer",
        "type": "",
        "location": "Durham, NC",
        "companyName": "",
        "skills": "",
        })
        assert response.status_code == 200

def test_search_page_submit_14():
    """
    This test verifies that search page filters the data based on the given input
    """

    test_user = db.users.find_one({'email': 'test@test.com'})
    del test_user['password']

    with app.test_client() as client:
        with client.session_transaction() as session:
            session['user'] = test_user
            session['logged_in'] = True
        
        add_sample_data()
        response = client.post("/search", data={
        "title": "Software Engineer",
        "type": "",
        "location": "San Francisco, CA",
        "companyName": "",
        "skills": "ML",
        })
        assert response.status_code == 200

def test_search_page_submit_15():
    """
    This test verifies that search page filters the data based on the given input
    """

    test_user = db.users.find_one({'email': 'test@test.com'})
    del test_user['password']

    with app.test_client() as client:
        with client.session_transaction() as session:
            session['user'] = test_user
            session['logged_in'] = True
        
        add_sample_data()
        response = client.post("/search", data={
        "title": "Software Engineer",
        "type": "",
        "location": "Raleigh, NC",
        "companyName": "",
        "skills": "Azure",
        })
        assert response.status_code == 200

def test_search_page_submit_16():
    """
    This test verifies that search page filters the data based on the given input
    """

    test_user = db.users.find_one({'email': 'test@test.com'})
    del test_user['password']

    with app.test_client() as client:
        with client.session_transaction() as session:
            session['user'] = test_user
            session['logged_in'] = True
        
        add_sample_data()
        response = client.post("/search", data={
        "title": "Software Engineer",
        "type": "",
        "location": "Raleigh, NC",
        "companyName": "",
        "skills": "ML",
        })
        assert response.status_code == 200

def test_search_page_submit_16():
    """
    This test verifies that search page filters the data based on the given input
    """

    test_user = db.users.find_one({'email': 'test@test.com'})
    del test_user['password']

    with app.test_client() as client:
        with client.session_transaction() as session:
            session['user'] = test_user
            session['logged_in'] = True
        
        add_sample_data()
        response = client.post("/search", data={
        "title": "Software Engineer",
        "type": "",
        "location": "Raleigh, NC",
        "companyName": "",
        "skills": "ML",
        })
        assert response.status_code == 200

def test_search_page_submit_17():
    """
    This test verifies that search page filters the data based on the given input
    """

    test_user = db.users.find_one({'email': 'test@test.com'})
    del test_user['password']

    with app.test_client() as client:
        with client.session_transaction() as session:
            session['user'] = test_user
            session['logged_in'] = True
        
        add_sample_data()
        response = client.post("/search", data={
        "title": "IXL",
        "type": "",
        "location": "Raleigh, NC",
        "companyName": "",
        "skills": "ML",
        })
        assert response.status_code == 200

def test_search_page_submit_18():
    """
    This test verifies that search page filters the data based on the given input
    """

    test_user = db.users.find_one({'email': 'test@test.com'})
    del test_user['password']

    with app.test_client() as client:
        with client.session_transaction() as session:
            session['user'] = test_user
            session['logged_in'] = True
        
        add_sample_data()
        response = client.post("/search", data={
        "title": "IXL",
        "type": "",
        "location": "",
        "companyName": "",
        "skills": "",
        })
        assert response.status_code == 200


def test_joblistings_page():
    test_user = db.users.find_one({'email': 'test@test.com'})
    del test_user['password']

    with app.test_client() as client:
        with client.session_transaction() as session:
            session['user'] = test_user
            session['logged_in'] = True
        
        response = client.get('/joblistings')
        assert response.status_code == 200
        assert b"Find your jobs here" in response.data

def test_user_profile_check_name_and_email():

    test_user = db.users.find_one({'email': 'test@test.com'})
    del test_user['password']

    with app.test_client() as client:
        with client.session_transaction() as session:
            session['user'] = test_user
            session['logged_in'] = True

        response = client.get('/user/profile')
        assert response.status_code == 200
        assert b"User Profile" in response.data
        assert b"Name" in response.data
        assert b"Email" in response.data


def test_user_profile_check_upload_resume():

    test_user = db.users.find_one({'email': 'test@test.com'})
    del test_user['password']

    with app.test_client() as client:
        with client.session_transaction() as session:
            session['user'] = test_user
            session['logged_in'] = True

        response = client.get('/user/profile')
        assert response.status_code == 200
        assert b"Upload Resume" in response.data

def test_home_page():
    """
    This test verifies that the home page works correctly
    """
    test_user = db.users.find_one({'email': 'test@test.com'})
    del test_user['password']

    with app.test_client() as client:
        with client.session_transaction() as session:
            session['user'] = test_user
            session['logged_in'] = True

        response = client.get('/home', follow_redirects = True)
        print(response)
        assert response.status_code == 200
        assert b"Welcome to JobCruncher!" in response.data
        assert b"So why use JobCruncher instead?" in response.data


def test_search_page():
    """
    This test verifies that search page displays the user input form correctly
    """

    test_user = db.users.find_one({'email': 'test@test.com'})
    del test_user['password']

    with app.test_client() as client:
        with client.session_transaction() as session:
            session['user'] = test_user
            session['logged_in'] = True

        response = client.get('/search')
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

    test_user = db.users.find_one({'email': 'test@test.com'})
    del test_user['password']

    with app.test_client() as client:
        with client.session_transaction() as session:
            session['user'] = test_user
            session['logged_in'] = True

        add_sample_data()
        response = client.post("/search", data={
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

    test_user = db.users.find_one({'email': 'test@test.com'})
    del test_user['password']

    with app.test_client() as client:
        with client.session_transaction() as session:
            session['user'] = test_user
            session['logged_in'] = True

        response = client.post("/search", data={
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

    sequence_document = db.counter.find_one_and_update(
        {"name": "job-counter"},
        {"$inc": {"value": 1}},
        return_document=True
    )

    next_id = sequence_document["value"]

    job_dict = {
        "_id": next_id,
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
