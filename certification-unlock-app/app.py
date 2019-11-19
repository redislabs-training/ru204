from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import session

import os
import secrets
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)

try:
    loginPassword = os.environ['CERTIFICATION_UNLOCK_PASSWORD']
except KeyError:
    print("Missing required environment variabe: CERTIFICATION_UNLOCK_PASSWORD")
    sys.exit(1)

@app.route('/')
def home():
    session.clear()
    return redirect('/login', code=302)

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
            print(request.form['email'])
            return "TODO: Enroll student!"
            # TODO END THE SESSION WHEN THEY ARE SUCCESSFULLY REGISTERED
            # TODO REDIRECT TO THE COURSE URL WHEN THEY ARE SUCCESSFULLY REGISTERED
            # session.clear()
        else:
            # No session, go to login...
            session.clear()
            return redirect('/login', code = 302)
    except KeyError:
        # No session, go to login...
        session.clear()
        return redirect('/login', code = 302)
