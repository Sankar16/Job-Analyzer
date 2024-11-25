from functools import wraps
from flask import Flask, render_template, request, session, redirect, url_for, flash  # noqa: E402
from flask_pymongo import PyMongo  # noqa: E402

from passlib.hash import pbkdf2_sha256
from pandas import DataFrame  # noqa: E402
import re  # noqa: E402
import numpy as np  # noqa: E402

from flask_mail import Mail, Message
import random
"""
The module app holds the function related to flask app and database.
"""
"""Copyright 2024 Ishwarya Anandakrishnan, Abishek Viswanath Pittamandalam, Ashwinkumar Manickam Vaithiyanathan

Use of this source code is governed by an MIT-style
license that can be found in the LICENSE file or at
https://opensource.org/licenses/MIT.
"""

app = Flask(__name__)
'''
Variable to load the app module
'''

app.secret_key = b'\xe1\x04B6\x89\xf7\xa0\xab\xd1L\x0e\xfb\x1c\x08"\xf6'
# client = pymongo.MongoClient('localhost', 27017)
# db = client.user_system

mongo_conn = "mongodb+srv://abivis2k:7aNqw7B9gsAfxznS@job-cluster.ayr8p.mongodb.net/db"
'''
Mongo connection string
'''
mongo_params = "?tlsAllowInvalidCertificates=true&retryWrites=true&w=majority"
'''
Mongo parameters
'''
app.config["MONGO_URI"] = mongo_conn + mongo_params

mongodb_client = PyMongo(app)
'''
Client connection
'''
db = mongodb_client.db

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'burnoutapp123@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'xszyjpklynmwqsgh'  # Replace with your email password
app.config['MAIL_DEFAULT_SENDER'] = 'burnoutapp123@gmail.com'

mail = Mail(app)


def login_required(f):
    """
    This function required login functionality
    """

    @wraps(f)
    def wrap(*args, **kwargs):
        '''
        This wrap function renders the redirect page
        '''
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')

    return wrap


@app.route('/reset', methods=["GET", "POST"])
def Reset_password():
    """
    Route : '/reset'
    Forgot password feature; also updates the password in MongoDB
    """
    # mongodb_client.db.users.find_one({"_id": user_id})
    # mongodb_client.db.users.find_one({'email': user['email']})

    if request.method == "POST":
        email = request.form["email"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        # Check if new passwords match
        if new_password != confirm_password:
            flash("New passwords do not match.", "danger")
            return redirect(url_for("reset"))

        if mongodb_client.db.users.find_one({'email': email}):

            # Hash and update the new password
            hashed_password = pbkdf2_sha256.hash(new_password)
            mongodb_client.db.users.update_one({"email": email}, {"$set": {"password": hashed_password}})

            flash("Your password has been updated successfully.", "success")
            return redirect("/")

    return render_template("reset-password.html")


@app.route('/signup', methods =["GET", "POST"])
def sgup():
    """
    Route: '/'
    The index function renders the index.html page.
    """
    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip().lower()
        password = request.form['password']
        otp = generate_otp()
        print(otp)
        # Validate input fields
        if not name or not email or not password:
            flash("All fields are required.", "danger")
            return redirect(url_for('signup'))

        # Check if the user already exists
        if db.users.find_one({'email': email}):
            flash("Email already exists! Please log in.", "danger")
            return redirect(url_for('login'))

        # Hash the password
        hashed_password = pbkdf2_sha256.hash(password)
        print("otp",otp)
        # Generate OTP
        otp = generate_otp()
        print(otp)
        # Insert the new user into the database with is_verified=False
        try:
            db.users.insert_one({
                'name': name,
                'email': email,
                'password': hashed_password,
                'otp': otp,                # Store OTP
                'is_verified': False       # Email verification status
            })
        except Exception as e:
            flash("An error occurred during registration. Please try again.", "danger")
            return redirect(url_for('signup'))

        # Send OTP via email for verification
        try:
            msg = Message("Verify Your Email for Job Analyzer", sender=app.config['MAIL_USERNAME'], recipients=[email])
            msg.body = f"Hello {name},\n\nYour OTP for email verification is: {otp}\n\nThank you for registering with Job Analyzer."
            mail.send(msg)
            flash("OTP sent to your email. Please verify your account.", "info")
            return redirect(url_for('verify_email', email=email))
        except Exception as e:
            # Optionally, delete the user from the database if email sending fails
            db.users.delete_one({'email': email})
            flash("Failed to send OTP. Please try again.", "danger")
            return redirect(url_for('signup'))
    return render_template('signup.html')



@app.route('/verify_email', methods=['GET', 'POST'])
def verify_email():
    """
    Route: '/verify_email'
    Handles OTP verification for email.
    """
    email = request.args.get('email')

    if not email:
        flash("Invalid verification link.", "danger")
        return redirect(url_for('login'))

    if request.method == 'POST':
        entered_otp = request.form['otp']
        user = db.users.find_one({'email': email})

        if user and user['otp'] == entered_otp:
            # Update the user's verification status
            db.users.update_one(
                {'email': email},
                {'$set': {'is_verified': True}, '$unset': {'otp': ""}}
            )
            flash("Email verified successfully! You can now log in.", "success")
            return redirect(url_for('login'))
        else:
            flash("Invalid OTP. Please try again.", "danger")

    return render_template('verify-email.html', email=email)



@app.route('/bookmark')
def bookmark():
    """
    Route: '/bookmark'
    Bookmark a job.
    """
    jobid = request.args.get('jobid')
    bookmarked_job = {
        'user_id': session['user']['_id'],
        'job_id': int(jobid)
    }
    db.userjob.insert_one(bookmarked_job)

    return redirect('/joblistings')


@app.route('/unbookmark')
def unbookmark():
    """
    Route: '/unbookmark'
    Unbookmark a job.
    """
    jobid = request.args.get('jobid')
    db.userjob.delete_one({'user_id': session['user']['_id'], 'job_id': int(jobid)})

    return redirect('/joblistings')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Route: '/'
    The login function renders login.html page.
    """
    print("Login page accessed")
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '').strip()
        
        if not email or not password:
            flash("Please enter both email and password.", "warning")
            return redirect(url_for('login'))
        
        user = db.users.find_one({'email': email})
        
        if user:
            # Verify the password
            is_password_correct = pbkdf2_sha256.verify(password, user['password'])
            print(f"Password verification result: {is_password_correct}")
            
            if is_password_correct:
                if not user.get('is_verified'):
                    flash("Please verify your email before logging in.", "danger")
                    return redirect(url_for('login'))
                
                # Generate OTP for login
                print("Generating OTP for login")
                otp = generate_otp()
                db.users.update_one({'email': email}, {'$set': {'otp': otp}})
                print(f"Generated OTP: {otp}")
                
                # Send OTP via email
                try:
                    msg = Message(
                        subject="Your Login OTP for Job Analyzer",
                        sender=app.config['MAIL_USERNAME'],
                        recipients=[email]
                    )
                    msg.body = (
                        f"Hello {user['name']},\n\n"
                        f"Your OTP for logging in is: {otp}\n\n"
                        "If you did not attempt to log in, please ignore this email."
                    )
                    mail.send(msg)
                    print("OTP email sent successfully")
                except Exception as e:
                    print(f"Error sending OTP email: {e}")
                    flash("Failed to send OTP. Please try again.", "danger")
                    return redirect(url_for('login'))
                
                # Store the email in session for OTP verification
                session['temp_email'] = email
                flash("OTP sent to your email. Please enter it below.", "info")
                return redirect(url_for('login_otp'))
            else:
                flash("Invalid email or password. Please try again.", "danger")
        else:
            flash("Invalid email or password. Please try again.", "danger")
        
        # Handle incorrect credentials
        session['isCredentialsWrong'] = True
        return redirect(url_for('login'))
    
    return render_template('login.html')

def generate_otp():
    """
    Generate a 6-digit OTP.
    """
    return str(random.randint(100000, 999999))

@app.route('/login_otp', methods=['GET', 'POST'])
def login_otp():
    """
    Route: '/login_otp'
    Handles OTP verification during login.
    """
    email = session.get('temp_email', '').strip().lower()
    
    if not email:
        flash("Session expired. Please log in again.", "danger")
        return redirect(url_for('login'))
    
    user = db.users.find_one({'email': email})
    
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        entered_otp = request.form.get('otp', '').strip()
        print(f"Entered OTP: {entered_otp}")
        print(f"Stored OTP: {user.get('otp')}")
        
        if user.get('otp') == entered_otp:
            # OTP is correct; log the user in
            try:
                session['logged_in'] = True
                session['user'] = {
                    '_id': str(user['_id']),
                    'name': user['name'],
                    'email': user['email']
                }
                # Remove OTP from the database
                db.users.update_one({'email': email}, {'$unset': {'otp': ""}})
                session.pop('temp_email', None)
                print(f"User {email} logged in successfully.")
                flash("Logged in successfully!", "success")
                return redirect(url_for('home'))
            except Exception as e:
                print(f"Error during user login: {e}")
                flash("An error occurred during login. Please try again.", "danger")
        else:
            flash("Invalid OTP. Please try again.", "danger")
    
    return render_template('login-otp.html', email=email)


@app.route('/resend_otp', methods=['POST'])
def resend_otp():
    """
    Route: '/resend_otp'
    Allows users to request a new OTP.
    """
    email = request.form.get('email', '').strip().lower()
    user = db.users.find_one({'email': email})
    
    if user and not user.get('is_verified'):
        # Generate a new OTP
        otp = generate_otp()
        db.users.update_one({'email': email}, {'$set': {'otp': otp}})
        print(f"Generated new OTP: {otp}")
        
        # Send OTP via email
        try:
            msg = Message(
                subject="Your New OTP for Job Analyzer",
                sender=app.config['MAIL_DEFAULT_SENDER'],
                recipients=[email]
            )
            msg.body = (
                f"Hello {user['name']},\n\n"
                f"Your new OTP for logging in is: {otp}\n\n"
                "If you did not attempt to log in, please ignore this email."
            )
            mail.send(msg)
            print("New OTP email sent successfully")
            flash("A new OTP has been sent to your email.", "info")
        except Exception as e:
            print(f"Error sending new OTP email: {e}")
            flash("Failed to resend OTP. Please try again.", "danger")
    else:
        flash("Invalid request. Please try again.", "danger")
    
    return redirect(url_for('login_otp'))



@app.route('/')
def index():
    """
    Route: '/'
    The index function renders the login.html page.
    """
    return redirect(url_for('login'))


@app.route('/home')
@login_required
def home():
    """
    Route: '/home'
    The home function renders the index.html page
    """

    return render_template('index.html')


# @app.route('/login')
# def login():
#     """
#     Route: '/login'
#     The index function renders the login.html page.
#     """
#     session['isCredentialsWrong'] = False
#     return render_template('login.html')


@app.route('/joblistings', methods=('GET','POST'))
def joblistings():
    '''
    This function fetches data from database on the search filter
    '''
    if request.method == 'POST':
        print("into req post")
        print(db.get_collection)
        job_df = read_from_db(request, db)
        job_count = job_df.shape[0]
        print(job_count)
        if job_df.empty:
            job_count = 0
            return render_template('no_jobs.html', job_count=job_count)
        job_df = job_df.drop('Job Description', axis=1)
        job_df = job_df.drop('_id', axis=1)
        job_df = job_df.drop('Industries', axis=1)
        job_df = job_df.drop('Job function', axis=1)
        job_df = job_df.drop('Total Applicants', axis=1)
        job_df['Job Link'] = '<a href=' + job_df['Job Link'] + '><div>' + " Apply " + '</div></a>'
        job_link = job_df.pop("Job Link")
        job_df.insert(7, "Job Link", job_link)
        job_df['Job Link'] = job_df['Job Link'].fillna('----')
        return render_template('job_posting.html', job_count=job_count,
                               tables=['''
                <style>
                    .table-class {border-collapse: collapse;    margin: 24px 0;
                        font-size: 15px; background-color: #000000;
                    font-family: sans-serif;    min-width: 500px;    }
                    .table-class thead tr {background-color: #002147;    color: #ffffff;
                    text-align: left; font-weight: 600; }
                    .table-class th,.table-class td {    text-align:center; padding: 12.4px 15.2px;}
                    .table-class tbody tr {border-bottom: 1px solid #ffffff; border-top-left-radius: 20px;
                    margin: 10px 0; border: 1px;border-color: white;}
                    .table-class tbody tr:nth-of-type(even) {    background-color: #20b2aa; color: white;}
                    .table-class tbody tr:nth-of-type(odd) {    background-color: #ffe4c4; }
                    .table-class tbody tr:last-of-type {    border-bottom: 2.1px solid #009878;}
                    .table-class tbody tr.active-row {  font-weight: bold;    color: #009878;}
                    table tr th { text-align:center; }
                </style>
            ''' + job_df.to_html(classes="table-class", render_links=True, escape=False)],
                               titles=job_df.columns.values)

    elif request.method == 'GET':  # If we hit redirect after bookmarking/unbookmarking a job listing.
        print("into req get")
        # Initializing a dummy POST data for the read_from_db function
        request.form = {}
        request.form['title'] = ''
        request.form['location'] = ''
        request.form['companyName'] = ''
        request.form['skills'] = ''
        job_df = read_from_db(request, db)
        job_count = job_df.shape[0]
        if job_df.empty:
            job_count = 0
            return render_template('no_jobs.html', job_count=job_count)
        job_df = job_df.drop('Job Description', axis=1)
        job_df = job_df.drop('_id', axis=1)
        job_df = job_df.drop('Industries', axis=1)
        job_df = job_df.drop('Job function', axis=1)
        job_df = job_df.drop('Total Applicants', axis=1)
        job_df['Job Link'] = '<a href=' + job_df['Job Link'] + '><div>' + " Apply " + '</div></a>'
        job_link = job_df.pop("Job Link")
        job_df.insert(7, "Job Link", job_link)
        job_df['Job Link'] = job_df['Job Link'].fillna('----')
        return render_template('job_posting.html', job_count=job_count,
                               tables=['''
                <style>
                    .table-class {border-collapse: collapse;    margin: 24px 0;
                        font-size: 15px; background-color: #000000;
                    font-family: sans-serif;    min-width: 500px;    }
                    .table-class thead tr {background-color: #002147;    color: #ffffff;
                    text-align: left; font-weight: 600; }
                    .table-class th,.table-class td {    text-align:center; padding: 12.4px 15.2px;}
                    .table-class tbody tr {border-bottom: 1px solid #ffffff; border-top-left-radius: 20px;
                    margin: 10px 0; border: 1px;border-color: white;}
                    .table-class tbody tr:nth-of-type(even) {    background-color: #20b2aa; color: white;}
                    .table-class tbody tr:nth-of-type(odd) {    background-color: #ffe4c4; }
                    .table-class tbody tr:last-of-type {    border-bottom: 2.1px solid #009878;}
                    .table-class tbody tr.active-row {  font-weight: bold;    color: #009878;}
                    table tr th { text-align:center; }
                </style>
            ''' + job_df.to_html(classes="table-class", render_links=True, escape=False)],
                               titles=job_df.columns.values)


@app.route('/search', methods=('GET', 'POST'))
def search():
    '''
    This functions fetches data from database on the search filter
    '''
    print(f"into search function ${request.method}")

    print(request)
    """
    Route: '/search'
    The search function renders the get_job_postings.html.
    Upon submission fetches the job postings from the database and renders job_posting.html
    """
    # if request.method == 'POST':
    #     print("into req post")
    #     print(db.get_collection)
    #     job_df = read_from_db(request, db)
    #     job_count = job_df.shape[0]
    #     print(job_count)
    #     if job_df.empty:
    #         job_count = 0
    #         return render_template('no_jobs.html', job_count=job_count)
    #     job_df = job_df.drop('Job Description', axis=1)
    #     job_df = job_df.drop('_id', axis=1)
    #     job_df = job_df.drop('Industries', axis=1)
    #     job_df = job_df.drop('Job function', axis=1)
    #     job_df = job_df.drop('Total Applicants', axis=1)
    #     job_df['Job Link'] = '<a href=' + job_df['Job Link'] + '><div>' + " Apply " + '</div></a>'
    #     job_link = job_df.pop("Job Link")
    #     job_df.insert(7, "Job Link", job_link)
    #     job_df['Job Link'] = job_df['Job Link'].fillna('----')
    #     return render_template('job_posting.html', job_count=job_count,
    #                            tables=['''
    # <style>
    #     .table-class {border-collapse: collapse;    margin: 24px 0;
    #         font-size: 15px; background-color: #000000;
    #     font-family: sans-serif;    min-width: 500px;    }
    #     .table-class thead tr {background-color: #002147;    color:#ffffff;
    #        text-align: left; font-weight: 600; }
    #     .table-class th,.table-class td {    text-align:center; padding: 12.4px 15.2px;}
    #     .table-class tbody tr {border-bottom: 1px solid #ffffff; border-top-left-radius: 20px;
    #      margin: 10px 0; border: 1px;border-color: white;}
    #     .table-class tbody tr:nth-of-type(even) {    background-color: #20b2aa; color: white;}
    #     .table-class tbody tr:nth-of-type(odd) {    background-color: #ffe4c4; }
    #     .table-class tbody tr:last-of-type {    border-bottom: 2.1px solid #009878;}
    #     .table-class tbody tr.active-row {  font-weight: bold;    color: #009878;}
    #     table tr th { text-align:center; }
    # </style>
    # ''' + job_df.to_html(classes="table-class", render_links=True, escape=False)],
    #         titles=job_df.columns.values)
    return render_template('get_job_postings.html')
#         .table-class tbody tr:nth-of-type(odd) {    background-color: #e4ad46; }
# ffe4c4


def add(db, job_data):
    """
    The add function adds the skills column and adds the job data to the database.
    """
    job_data['skills'] = [','.join(map(str, skill)) for skill in job_data['skills']]
    job_data['skills'] = job_data['skills'].replace(r'^\s*$', np.nan, regex=True)
    job_data['skills'] = job_data['skills'].fillna('----')
    db.jobs.insert_many(job_data.to_dict('records'))


def read_from_db(request, db):
    """
    The read_from_db function reads the job details based on the input provided using regex.
    Returns a DataFrame with the details
    """
    job_title = request.form['title']
    job_location = request.form['location']
    company_name = request.form['companyName']
    skills = request.form['skills']
    regex_char = ['.', '+', '*', '?', '^', '$', '(', ')', '[', ']', '{', '}', '|']

    for char in regex_char:
        skills = skills.replace(char, '\\' + char)

    rgx_title = re.compile('.*' + job_title + '.*', re.IGNORECASE)
    rgx_location = re.compile('.*' + job_location + '.*', re.IGNORECASE)
    rgx_company_name = re.compile('.*' + company_name + '.*', re.IGNORECASE)
    rgx_skills = re.compile('.*' + skills + '.*', re.IGNORECASE)

    data_filter = {}
    if job_title != '':
        data_filter['Job Title'] = rgx_title
    if job_location != '':
        data_filter['Location'] = rgx_location
    if company_name != '':
        data_filter['Company Name'] = rgx_company_name
    if skills != '':
        data_filter['skills'] = rgx_skills

    data = list(db.jobs.find(data_filter))
    user_id = session['user']['_id']
    bookmarked_jobs = list(db.userjob.find({'user_id': user_id}))
    for job in data:

        job_id = job['_id']
        flag = False

        for bookmarked_job in bookmarked_jobs:
            if bookmarked_job['job_id'] == job_id:
                flag = True
                break

        if flag:
            job['bookmarked'] = '1'
        else:
            job['bookmarked'] = '0'

    data = sorted(data, key=lambda x: x['bookmarked'], reverse=True)

    for job in data:
        if job['bookmarked'] == '1':
            job['bookmarked'] = '<a href="/unbookmark?jobid=' + str(job['_id']) + '">📍</a>'
        else:
            job['bookmarked'] = '<a href="/bookmark?jobid=' + str(job['_id']) + '">📌</a>'

    return DataFrame(list(data))
