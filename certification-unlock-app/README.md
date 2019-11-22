# certification-unlock-app

This is a Python 3 / [Flask](https://flask.palletsprojects.com/) application that adds students to the Redis Certified Developer Exam course run in Appsembler.

## Workflow

The application workflow is as follows:

* Present a login screen.  The proctor uses this to enter a password that unlocks the rest of the application for the student to use.
* If the wrong password was entered, remain on the login screen and show an error.
* If the correct password was entered, present a form asking the student for their email address.
* On submit, use the Appsembler API to enroll the email address provided onto the course run for Redis Certified Developer Exam.
* If the enrollment API call succeeded (201 response), redirect to the course page on Appsembler.
* If the enrollment API call failed (non 201 response), remain on the email address capture screen and show an error.

## Setup

To get the application running on your local machine you'll want to clone the repo and use a Python virtual environment:

```
$ cd certification-unlock-app
$ python3 -m venv venv
$ pip3 install -r requirements.txt

```

## Configuration

This application is configured through environment variables, which all need to be set for the application to start up:

* `CERTIFICATION_UNLOCK_PASSWORD` - set this to the password that you want the proctor to enter to unlock the application.
* `APPSEMBLER_API_TOKEN` - API token used to access Appsembler API, provided by Appsembler.
* `APPSEMBLER_HOST` - host name to use when connecting to Appsembler and its API, e.g. `university.redislabs.com` for production or `redisu-staging.tahoe.appsembler.com` for stage.
* `APPSEMBLER_COURSE_ID` - the full course ID of the course run that the application will enroll students into (e.g. `ourse-v1:redisu-staging+CERT-TEST+2019-01`)
* `APPSEMBLER_COURSE_URL_PATH` - the path on `APPSEMBLER_HOST` that the user is redirected to once the application has enrolled them in the course run.  e.g. `dashboard` for the dashboard page.

## Starting the Application

```
$ export CERTIFICATION_UNLOCK_PASSWORD=<your choice of password>
$ export APPSEMBLER_API_TOKEN=<api token for appsembler>
$ export APPSEMBLER_HOST=redisu-staging.tahoe.appsembler.com
$ export APPSEMBLER_COURSE_ID=course-v1:redisu-staging+CERT-TEST+2019-01
$ export APPSEMBLER_COURSE_URL_PATH=dashboard
$ export FLASK_APP = app.py
$ export FLASK_ENV = development
$ flask run
```

The application should be available at:

```
http://localhost:5000
```

## Deploying the Application

The application is deployed to AppEngine on Google Cloud in the `redislabs-university` project.  When deployed, it's accessible at:

```
https://redislabs-university.appspot.com/
```

and is the `default` service in AppEngine in the Google Cloud project.  This should be considered "production".  If you need to deploy it with staging configuration, you should configure both the staging credentials in `app.yaml` and also add a service name (see next section).

### Editing app.yaml

When deploying to AppEngine, environment variables and other information about the runtime environment are configured in `app.yaml`.

You should edit this to include the correct values for each of the environment variables that the application uses, and do **not** commit this version of `app.yaml` to source control!

The file `app_example.yaml` is provided as a start point for you.  Copy this to `app.yaml` then add the real values to that file before deploying.

If you want to deploy the service to test it, add a service name in `app.yaml`.  For example:

```
service: stage-certification-unlock
```

This will deploy to a different URL that you will see when deployment is finished.  It will also create a new AppEngine application that you will need permissions to be allowed to do (ask an account owner).  When you are done testing, be sure to delete this application in the AppEngine console so that it doesn't run continuously and cost money.

A guide to the contents of the `app.yaml` file can be [found here](https://cloud.google.com/appengine/docs/flexible/nodejs/reference/app-yaml).

Note that whenever you deploy to AppEngine you **must** set `FLASK_ENV` to `production` in `app.yaml` otherwise you will get redirect loops due to the way SSL termination works on AppEngine.

### Deploying to AppEngine

To deploy, you'll need the Google Cloud Platform `gcloud` tools / SDK installed.  You will also need to be authenticated to Google Cloud as a user that can access the `redislabs-university` project with at least "App Engine Admin" rights for the project.

Once you have those, deployment is simple... edit `app.yaml` to contain the correct environment variable values, then:

```
$ gcloud app deploy --project redislabs-university
```

Answer `Y` when asked if you are sure you want to do this.  Deployments can take some time to complete, like 3-5 minutes.

If you want to use separate `app.yaml` files for different environments etc, you need to specify the name of the file when deploying like so:

```
$ gcloud app deploy staging_app.yaml --project redislabs-university
```

## Forcing SSL on AppEngine

AppEngine allows the application to be reached on both `http` and `https` URLs... this is not desirable as this application has a password field and also collects (but does not store) an email address.  To force use of the application via SSL only, there's code in `app.py` that detects whether the incoming request is on a `http` URL and redirects it to a `https` URL.

This will only work when running on AppEngine because it's looking at the value of the `X-Forwarded-Proto` header.  Google terminates SSL upstream from AppEngine so all requests hitting the application are actually `http`, so we need to look at the header they set to see what the original protocol was.  If that was `http` then we redirect.  Note also that this functionality is disabled when running locally in the Flask `development` environment.  The code looks like this and runs before each route handler:

```python
@app.before_request
def before_request():
    if request.headers.get('X-Forwarded-Proto') == 'http' and app.env != 'development':
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)
```