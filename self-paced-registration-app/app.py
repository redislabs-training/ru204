from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import session

import json
import os
import requests
import secrets
import sys

def getEnvVar(varName):
    try:
        return os.environ[varName]
    except KeyError:
        print('Missing required environment variable: ' + varName)
        sys.exit(1)

def isValidEmailDomain(emailAddress):
    validEmailDomains = getEnvVar('WHITELISTED_EMAIL_DOMAINS')
    emailAddressParts = emailAddress.split('@')

    if len(emailAddressParts) != 2:
        # Bad email address
        return False

    return emailAddressParts[1] in validEmailDomains

def enrollStudentWithAppsembler(studentEmail, courses):
    identifiers = []
    identifiers.append(studentEmail)

    response = requests.post(
        'https://' + courseHost + '/tahoe/api/v1/enrollments/',
        json={'action': 'enroll',
              'email_learners': True,
              'auto_enroll': True,
              'courses': courses,
              'identifiers': identifiers},
        headers={'Authorization': 'Token ' + apiToken,
                 'Content-Type': 'application/json',
                 'Cache-Control': 'no-cache'}
    )

    return response.status_code == 201

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)

apiToken = getEnvVar('APPSEMBLER_API_TOKEN')
courseHost = getEnvVar('APPSEMBLER_HOST')

with open('courses.json', 'r') as coursesFile:
    coursesAvailable = json.load(coursesFile)
    coursesAvailable = coursesAvailable['courses']

@app.before_request
def before_request():
    if request.headers.get('X-Forwarded-Proto') == 'http' and app.env != 'development':
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)

@app.route('/')
def home():
    session.clear()
    return render_template('email.html')

@app.route('/selectcourses', methods=['POST'])
def selectCourses():
    studentEmail = request.form['email']

    if isValidEmailDomain(studentEmail):
        session['studentEmail'] = studentEmail

        return render_template('courses.html', courses=coursesAvailable)
    else:
        return render_template('email.html', error='Invalid email address!')
        session.clear()

@app.route('/enroll', methods=['POST'])
def enrollStudent():
    try:
        studentEmail = session['studentEmail']
        selectedCourses = request.form.getlist('courses')

        if len(selectedCourses) == 0:
            return render_template('courses.html', courses=coursesAvailable, error='Please select at least one course.')
        else:
            if (enrollStudentWithAppsembler(studentEmail, selectedCourses)):
                session.clear()
                return render_template('thanks.html', email=studentEmail, loginUrl='https://' + courseHost)
            else:
                return render_template('courses.html', courses=coursesAvailable, error='Registration failed!')
    except KeyError:
        # No session, go home
        session.clear()
        return redirect('/')
    
