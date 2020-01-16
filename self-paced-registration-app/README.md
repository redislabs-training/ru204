# self-paced-registration-app

This is a Python 3 / [Flask](https://flask.palletsprojects.com/) application that adds Redis Labs employees to the Redis University self paced course runs in Appsembler.

## Workflow

The application workflow is as follows:

* Present a form asking for the user's email address.
* On submit, verify that the user's email address is from a whitelisted domain (only certain domains, right now just `redislabs.com` email addresses are allowed on self paced courses). If the email is invalid, display an error.
* If the email was valid, display a form allowing the user to choose at least one of the available self paced courses.  The list of courses comes from a JSON configuratin file.
* On submit, check if the user selected any courses and error if none are selected.
* If courses were selected, call the Appsembler API to enroll the email address provided onto the course runs corresponding to the selected courses.
* If the enrollment API call succeeded (201 response), show a Thank You page encouraging the user to check their email and/or login to Redis University.
* If the enrollment API call failed (non 201 response), remain on the course selection screen and show an error.

## Setup

To get the application running on your local machine you'll want to clone the repo and use a Python virtual environment:

```
$ cd self-paced-registration-app
$ python3 -m venv venv
$ ./venv/bin/activate
$ pip3 install -r requirements.txt
```

## Configuration

This application is configured through environment variables and a JSON file containing course details.

For the application to start up, you need to set all of the following environment variables:

* `APPSEMBLER_API_TOKEN` - API token used to access Appsembler API, provided by Appsembler.
* `APPSEMBLER_HOST` - host name to use when connecting to Appsembler and its API, e.g. `university.redislabs.com` for production or `redisu-staging.tahoe.appsembler.com` for stage.
* `FLASK_APP` - where the Flask app lives, set to `app.py`.
* `FLASK_ENV` - set to `production`
* `WHITELISTED_EMAIL_DOMAINS` - comma separated list of email domains that are allowed to use this application e.g. `redislabs.com,redislabs.co.uk`

Courses are configured in the `courses.json` file which looks like this:

```
{
    "courses": [
        {
            "name": "RU101 Introduction to Redis Data Structures",
            "id": "course-v1:redislabs+RU101+SP_2019_01"
        },
        {
            "name": "RU102J Redis for Java Developers",
            "id": "course-v1:redislabs+RU102J+SP_2019_04"
        },
        ...
    ]
}
```

## Starting the Application

```
$ export APPSEMBLER_API_TOKEN=<api token for appsembler>
$ export APPSEMBLER_HOST=redisu-staging.tahoe.appsembler.com
$ export WHITELISTED_EMAIL_DOMAINS=redislabs.com
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
https://self-paced-registration-dot-redislabs-university.appspot.com/
```

and is the `self-paced-registration` service in AppEngine in the Google Cloud project.  This should be considered "production".  If you need to deploy it with staging configuration, you should configure both the staging credentials in `app.yaml` and also add a different service name (see next section).

### Editing app.yaml

When deploying to AppEngine, environment variables and other information about the runtime environment are configured in `app.yaml`.

You should edit this to include the correct values for each of the environment variables that the application uses, and do **not** commit this version of `app.yaml` to source control!

The file `app_example.yaml` is provided as a start point for you.  Copy this to `app.yaml` then add the real values to that file before deploying.

If you want to deploy the service to test it, add change the service name in `app.yaml`.  For example:

```
service: stage-self-paced-registration
```

This will deploy to a different URL that you will see when deployment is finished.  It will also create a new AppEngine application that you will need permissions to be allowed to do (ask an account owner).  When you are done testing, be sure to delete this application in the AppEngine console so that it doesn't run continuously and cost money.

When deploying for production, use the `self-paced-registration` service in your YAML:

```
service: self-paced-registration
```

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

#### Error with specific version of `gcloud` command

If you see this when deploying:

```
ERROR: (gcloud.app.deploy) Failed to parse YAML from [gs://runtime-builders/experiments.yaml]: mapping values are not allowed here
  in "<file>", line 2, column 14
```

Then the problem isn't with your YAML file it's a bug in the `gcloud` tools.  Revert to version 271.0.0 and retry:

```
gcloud components update --version=271.0.0
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