from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import session
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)

@app.route('/')
def home():
    return redirect('/login', code=302)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if (request.method == 'GET'):
        return render_template('login.html')
    else:
        # TODO PASSWORD FROM ENVIRONMENT
        if (request.form['password'] == 'secret'):
            #session['authenticated'] = True
            return render_template('email.html')
        else:
            return render_template('login.html', error='Invalid password.')

# TODO NEED TO HAVE A SESSION TO CHECK HERE...
@app.route('/student', methods=['POST'])
def enrollStudent():
    try:
        if (session['authenticated']):
            return "TODO: Enroll student!"
            # TODO END THE SESSION WHEN THEY ARE SUCCESSFULLY REGISTERED
        else:
            # No session, go to login...
            return redirect('/login', code = 302)
    except KeyError:
        # No session, go to login...
        return redirect('/login', code = 302)
