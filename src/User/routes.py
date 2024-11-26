'''
These are the end points related to the user
'''


# sys.path.append('../src')
from src.app import app
from flask import render_template
from src.User.models import User


@app.route('/user/signup', methods=['GET'])
def showSignupPage():
    return render_template('signup.html')


@app.route('/user/login', methods=['GET'])
def showLoginPage():
    return render_template('login.html')


# @app.route('/user/profile', methods=['GET'])

# def showUserProfile():
#     return User().showProfile()


@app.route('/user/signup', methods=['POST'])
def signup():
    '''
    User signup
    '''
    return User().signup()


@app.route('/user/logout')
def signout():
    '''
    User signout
    '''
    return User().logout()


@app.route('/user/login', methods=['POST'])
def loginUser():
    '''
    User login
    '''
    return User().login()


@app.route('/user/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    '''
    Handle OTP verification
    '''
    return User().verify_otp()


@app.route('/user/resend_login_otp', methods=['GET'])
def resend_login_otp():
    '''
    Resend the OTP code during login verification
    '''
    return User().resend_login_otp()


@app.route('/user/verify_signup_otp', methods=['GET', 'POST'])
def verify_signup_otp():
    '''
    Handle OTP verification after signup
    '''
    return User().verify_signup_otp()


@app.route('/user/resend_signup_otp', methods=['GET'])
def resend_signup_otp():
    '''
    Resend the OTP code during signup verification
    '''
    return User().resend_signup_otp()



@app.route('/user/profile', methods=['GET'])
def showUserProfile():
    '''
    Shows user profile
    '''
    return User().showProfile()


@app.route('/user/saveResume', methods=['POST'])
def saveResume():
    '''
    Saves resume
    '''
    return User().saveResume()


@app.route('/download/<fileid>')
def downloadResume(fileid):
    '''
    Downloads a file from GridFS
    '''
    return User().downloadResume(fileid)


@app.route('/healthcheck', methods=['GET'])
def healthCheck():
    return "Flask is up and running"
