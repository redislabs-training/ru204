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

TODO

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

TODO