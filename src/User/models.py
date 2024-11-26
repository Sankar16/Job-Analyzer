'''
Contains user model functions
'''

from flask import jsonify, request, session, redirect, render_template, send_file
from passlib.hash import pbkdf2_sha256
from src.app import db
import uuid
import gridfs
from io import BytesIO
from bson import ObjectId

fs = gridfs.GridFS(db)


class User:
    '''
    This class handles user session and profile operations
    '''

    def startSession(self, user):
        '''
        Start the user session
        '''
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return (jsonify(user), 200)


    def signup(self):
        '''
        User signup with email verification
        '''
        if not request.form.get('name') or not request.form.get('email') or not request.form.get('password'):
            return redirect('/')

        user = {
            '_id': uuid.uuid4().hex,
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'password': pbkdf2_sha256.hash(request.form.get('password')),
            'is_verified': False
        }

        if db.users.find_one({'email': user['email']}):
            return jsonify({'error': 'Email address already in use'}), 400

        if db.users.insert_one(user):
            # Generate OTP
            import random
            otp = str(random.randint(100000, 999999))  # 6-digit OTP

            # Save OTP in user's record
            db.users.update_one({'email': user['email']}, {'$set': {'otp': otp}})

            # Send email with OTP
            self.send_otp_email(user['email'], otp)

            # Save user's email in session
            session['user_email'] = user['email']

            # Redirect to OTP verification page
            return redirect('/user/verify_signup_otp')

        return jsonify({'error': 'Signup failed'}), 400
    

    def verify_signup_otp(self):
        '''
        Verify the OTP code entered by the user during signup
        '''
        if request.method == 'GET':
            return render_template('verify_signup_otp.html')
        else:
            # POST request: process the OTP entered by the user
            entered_otp = request.form.get('otp')
            email = session.get('user_email')

            if not email:
                return redirect('/')

            user = db.users.find_one({'email': email})
            if user and 'otp' in user and user['otp'] == entered_otp:
                # OTP is correct
                # Remove the otp from the user's record
                db.users.update_one({'email': email}, {'$unset': {'otp': ''}})
                # Set is_verified to True
                db.users.update_one({'email': email}, {'$set': {'is_verified': True}})
                # Start the session
                self.startSession(user)
                # Remove user_email from session
                session.pop('user_email', None)
                return redirect('/home')
            else:
                # OTP is incorrect
                error = 'Invalid OTP. Please try again.'
                return render_template('verify_signup_otp.html', error=error)



    def logout(self):
        '''
        Session Logout
        '''
        session.clear()
        return redirect('/')


    def login(self):
        '''
        Session Login with 2FA via email OTP
        '''
        session['isCredentialsWrong'] = False

        if not request.form.get('email') or not request.form.get('password'):
            session['isCredentialsWrong'] = True
            return redirect('/')

        user = db.users.find_one({'email': request.form.get('email')})
        print(user)
        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            # Generate OTP
            import random
            otp = str(random.randint(100000, 999999))  # 6-digit OTP

            # Save OTP in the user's record
            db.users.update_one({'email': user['email']}, {'$set': {'otp': otp}})

            # Send email with OTP
            self.send_otp_email(user['email'], otp)

            # Save user's email in session
            session['user_email'] = user['email']

            # Redirect to OTP verification page
            return redirect('/user/verify_otp')

        elif user:
            session['isCredentialsWrong'] = True
            return redirect('/')
        else:
            return redirect('/')


    def send_otp_email(self, email, otp):
        '''
        Send an email with the OTP code using SSL
        '''
        import smtplib
        from email.mime.text import MIMEText
        import ssl

        # Set up your SMTP server settings
        smtp_server = 'smtp.gmail.com'
        smtp_port = 465  # SSL port
        smtp_username = 'burnoutapp123@gmail.com'  # Replace with your email
        smtp_password = 'xszyjpklynmwqsgh'   # Replace with your email password or app password

        # Create the email content
        subject = 'Your OTP Code'
        body = f'Your OTP code is: {otp}'

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = smtp_username
        msg['To'] = email

        # Create SSL context
        context = ssl.create_default_context()

        # Send the email using SMTP_SSL
        try:
            with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
                server.login(smtp_username, smtp_password)
                server.sendmail(smtp_username, email, msg.as_string())
        except Exception as e:
            print('Failed to send email:', e)


    def verify_otp(self):
        '''
        Verify the OTP code entered by the user
        '''
        if request.method == 'GET':
            return render_template('verify_otp.html')
        else:
            # POST request: process the OTP entered by the user
            entered_otp = request.form.get('otp')
            email = session.get('user_email')

            if not email:
                return redirect('/')

            user = db.users.find_one({'email': email})
            if user and 'otp' in user and user['otp'] == entered_otp:
                # OTP is correct
                # Remove the otp from the user's record
                db.users.update_one({'email': email}, {'$unset': {'otp': ''}})

                # Start the session
                self.startSession(user)
                # Remove user_email from session
                session.pop('user_email', None)
                return redirect('/home')
            else:
                # OTP is incorrect
                error = 'Invalid OTP. Please try again.'
                return render_template('verify_otp.html', error=error)


    def showProfile(self):
        '''
        Renders User Profile
        '''
        user = session['user']
        return render_template('user_profile.html', user=user)

    def saveResume(self):
        '''
        Saves resume and renders User profile
        '''
        if 'resume_file' in request.files:
            resume = request.files['resume_file']

            file_id = fs.put(resume, filename=resume.filename)
            file_id_str = str(file_id)

            # Update the user in the database
            user_email = session['user']['email']  
            db.users.update_one(
                {'email': user_email},  
                {'$set': {'resume_filename': resume.filename, 'resume_fileid' : file_id_str}}  
            )

            # Update the session data with the new filename
            session['user']['resume_filename'] = resume.filename
            session['user']['resume_fileid'] = file_id

        return render_template('user_profile.html', user=session['user'])

    def downloadResume(self, fileid):
        file_data = fs.get(ObjectId(fileid))
        return send_file(BytesIO(file_data.read()), mimetype='application/pdf', as_attachment=False, download_name=file_data.filename)
