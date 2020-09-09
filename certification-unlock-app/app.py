from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import session

import os
import requests
import secrets
import sys

def getEnvVar(varName):
    try:
        return os.environ[varName]
    except KeyError:
        print("Missing required environment variable: " + varName)
        sys.exit(1)

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)

loginPassword = getEnvVar('CERTIFICATION_UNLOCK_PASSWORD')
apiToken = getEnvVar('APPSEMBLER_API_TOKEN')
courseHost = getEnvVar('APPSEMBLER_HOST')
courseId = getEnvVar('APPSEMBLER_COURSE_ID')
courseUrlPath = getEnvVar('APPSEMBLER_COURSE_URL_PATH')

def enrollStudentWithAppsembler(studentEmail):
    identifiers = []
    identifiers.append(studentEmail)

    courses = []
    courses.append(courseId)

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

@app.before_request
def before_request():
    if request.headers.get('X-Forwarded-Proto') == 'http' and app.env != 'development':
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)

@app.route('/')
def home():
    session.clear()
    return redirect('/login', code=302)

@app.route('/info')
def info():
    return jsonify({ 'courseId': courseId })

@app.route('/login', methods=['GET', 'POST'])
def login():
    if (request.method == 'GET'):
        session.clear()
        return render_template('login.html')
    else:
        if (request.form['password'] == loginPassword):
            session['authenticated'] = True
            return render_template('email.html')
        else:
            session.clear()
            return render_template('login.html', error='Invalid password.')

@app.route('/student', methods=['POST'])
def enrollStudent():
    try:
        if (session['authenticated']):
            if (enrollStudentWithAppsembler(request.form['email'])):
                session.clear()
                return redirect('https://' + courseHost + '/' + courseUrlPath, code=302)
            else:
                return render_template('email.html', error='Registration failed!')
        else:
            # No session, go to login...
            session.clear()
            return redirect('/login', code = 302)
    except KeyError:
        # No session, go to login...
        session.clear()
        return redirect('/login', code = 302)
