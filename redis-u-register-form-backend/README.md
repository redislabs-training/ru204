# Redis University Registration Form Backend

This is a Google Cloud function, written in Python 3, that validates POST requests from the Redis University registration form page (source in: [the Redis University static site GitHub repo](https://github.com/redislabs-training/redis-university-static-site)) and then registers the user with Appsembler and enrolls them on a course if one was provided in the POST request.

To do this it uses these Appsembler APIs:

* [Registration](https://help.appsembler.com/article/438-tahoe-registration-api)
* [Enrollment](https://help.appsembler.com/article/437-tahoe-enrollment-api)

So that Marketing receive information about enrollments, the code also generates Segment events.  Segment then routes these to Marketo.

## Setup

To set up your environment:

```bash
$ git clone https://github.com/RedisLabs/ed-courseware.git
$ cd redis-u-register-form-backend
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
```

## Running the Cloud Function Locally

You can run the Cloud Function locally like so (don't forget to set an environment variable for each value in `example_env.yaml` and to use values for the environment you're working with!):

```bash
$ export APPSEMBLER_API_HOST=university.redis.com
$ export APPSEMBLER_API_KEY=123abc456
$ export SEGMENT_WRITE_KEY=123abc456
$ export CORS_ORIGIN=https://university.redis.com
$ export REGISTRATION_REQUIRES_COUNTRY=True
$ functions-framework --target=register_form_processor --debug
```

To test it, you'll want to use Postman to create an appropriate POST request and set it to the function's local URL, which you can find in the log from where you started functions-framework.

Or, you could use curl... here's an example request (you may need to update the URL for your environment):

```
curl --location --request POST 'http://localhost:8080/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "simon+202101201757@redislabs.com",
    "firstName": "Simon",
    "lastName": "Prickett",
    "jobFunction": "DevOps/Technical Operations",
    "company": "Redis Labs",
    "userName": "simonprickett202101201757",
    "country": "United States",
    "agreeTerms": true,
    "state": "California",
    "courseId": "course-v1:redislabs+RU102JS+2021_01"
}'
```

## Deploying the Cloud Function

Deploy the Cloud Function to either the stage or production environments.  Each environment should use its own YAML environment variables file, containing the following values set appropriately for the environment that you are deploying to...

Example YAML (see `example_env.yaml`):

```yaml
APPSEMBLER_API_HOST: university.redis.com
APPSEMBLER_API_KEY: 123abc456def
SEGMENT_WRITE_KEY: 123abc456def
CORS_ORIGIN: https://university.redis.com
REGISTRATION_REQUIRES_COUNTRY: "True"
```

You should always set `REGISTRATION_REQUIRES_COUNTRY` to `True` for the production environment. 

**Do not commit your YAML files to GitHub, as they contain secrets!**

You will need appropriate permissions (deploy / update Cloud Functions) in the redislabs-university project in Google Cloud, and to have configured and authenticated the `gcloud` command on your laptop.

### Deploying to Stage

```bash
$ gcloud functions deploy stage-register-form-processor --entry-point register_form_processor --trigger-http --runtime python38 --allow-unauthenticated --env-vars-file stage_env.yaml --project redislabs-university
```

The function will then be available at:

```
https://us-central1-redislabs-university.cloudfunctions.net/stage-register-form-processor
```

Access the logs via the Google Cloud console.  

Access the Segment debugger / logging [here](https://app.segment.com/redis-university/sources/stage_redis_university_registrations/overview).

### Deploying to Production

```bash
$ gcloud functions deploy register-form-processor --entry-point register_form_processor --trigger-http --runtime python38 --allow-unauthenticated --env-vars-file prod_env.yaml --project redislabs-university
```

The function will then be available at:

```
https://us-central1-redislabs-university.cloudfunctions.net/register-form-processor
```

Access the logs via the Google Cloud console.  

Access the Segment debugger / logging [here](https://app.segment.com/redis-university/sources/production_redis_university_registrations/overview).