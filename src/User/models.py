'''
Contains user model functions
'''

from flask import jsonify, request, session, redirect, render_template, url_for, send_file
from passlib.hash import pbkdf2_sha256
from src.app import db, mongodb_client
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
        User signup using credentials
        '''
        # print(request.form)
        user = {
            '_id': uuid.uuid4().hex,
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'password': request.form.get('password')}
        user['password'] = pbkdf2_sha256.hash(user['password'])
        if db.users.find_one({'email': user['email']}):
            return (jsonify({'error': 'Email address already in use'}),
                    400)

        if db.users.insert_one(user):
            self.startSession(user)
            return redirect('/home')



        return (jsonify({'error': 'Signup failed'}), 400)

    def logout(self):
        '''
        Session Logout
        '''
        session.clear()
        return redirect('/')

    def login(self):
        '''
        Session Login
        '''
        session['isCredentialsWrong'] = False
        user = db.users.find_one({'email': request.form.get('email')})
        print(user)
        if user and pbkdf2_sha256.verify(str(request.form.get('password')), user['password']):
            self.startSession(user)
            session['isCredentialsWrong'] = False
            return redirect('/home')
        elif user and not pbkdf2_sha256.verify(str(request.form.get('password')), user['password']):
            session['isCredentialsWrong'] = True
            return redirect('/')
        else:
            return redirect('/')

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
            # print(resume)
            # mongodb_client.save_file(resume.filename, resume)

            file_id = fs.put(resume, filename=resume.filename)
            file_id_str = str(file_id)
            
            # Update the user in the database
            user_email = session['user']['email']  # Get the current user's email
            db.users.update_one(
                {'email': user_email},  # Find the user by email
                {'$set': {'resume_filename': resume.filename, 'resume_fileid' : file_id_str}}  # Update the resume filename
            )
            
            # Update the session data with the new filename
            session['user']['resume_filename'] = resume.filename
            session['user']['resume_fileid'] = file_id

        return render_template('user_profile.html', user=session['user'])

    def downloadResume(self, fileid):
        file_data = fs.get(ObjectId(fileid))
        return send_file(BytesIO(file_data.read()), mimetype='application/pdf', as_attachment=False, download_name=file_data.filename)