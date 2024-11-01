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