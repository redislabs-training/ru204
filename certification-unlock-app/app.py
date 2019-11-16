from flask import Flask
from flask import request
from flask import redirect
from flask import render_template

app = Flask(__name__)

@app.route('/')
def home():
    return redirect("/login", code=302)

# TODO ESTABLISH A SESSION HERE
# TODO PASSWORD FROM ENVIRONMENT
@app.route('/login', methods=['GET', 'POST'])
def login():
    if (request.method == 'GET'):
        return render_template('login.html')
    else:
        if (request.form['password'] == 'secret'):
            return render_template('email.html')
        else:
            return render_template('login.html', error='Invalid password.')

# TODO NEED TO HAVE A SESSION TO CHECK HERE...
@app.route('/student', methods=['POST'])
def enrollStudent():
    return "TODO: Enroll student!"