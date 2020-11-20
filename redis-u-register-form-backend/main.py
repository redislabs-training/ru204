from webargs import fields, validate
from webargs.flaskparser import parser

import analytics
import os
import requests

EMAIL_FIELD = "email"
FIRST_NAME_FIELD = "firstName"
LAST_NAME_FIELD = "lastName"
USERNAME_FIELD = "userName"
PASSWORD_FIELD = "password"
COUNTRY_FIELD = "country"
STATE_FIELD = "state"
PROVINCE_FIELD = "province"
COURSE_ID_FIELD = "courseId"
COUNTRY_USA = "United States of America"
COUNTRY_CANADA = "Canada"

OK_CODE = 200
CREATED_CODE = 201
BAD_REQUEST_CODE = 400
CONFLICT_CODE = 409
OK_MESSAGE = "OK"
UNPROCESSABLE_ENTITY_MESSAGE = "Unprocessable Entity!"
UNPROCESSABLE_ENTITY_CODE = 422

APPSEMBLER_API_KEY = os.environ.get("APPSEMBLER_API_KEY")
APPSEMBLER_API_HOST = os.environ.get("APPSEMBLER_API_HOST")

analytics.write_key = os.environ.get("SEGMENT_WRITE_KEY")

cors_headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST",
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Max-Age": "3600"
}

def call_appsembler_api(endpoint, data):
    api_endpoint = f"https://{APPSEMBLER_API_HOST}/tahoe/api/v1/{endpoint}/"

    return requests.post(
        api_endpoint,
        json = data,
        headers = { 
            "Authorization": f"Token {APPSEMBLER_API_KEY}",
            "Content-Type": "application/json",
            "Cache-Control": "no-cache"
        }
    )

def register_form_processor(request): 
     
    if request.method == "OPTIONS":
        return "", 204, cors_headers

    if request.method != "POST" or not request.is_json:
        return "Bad request!", BAD_REQUEST_CODE, cors_headers
    
    data = parser.parse({
        EMAIL_FIELD: fields.Str(required = True, validate = [ validate.Email(), validate.Length(min = 1, max = 254) ]),
        FIRST_NAME_FIELD: fields.Str(required = True, validate = validate.Length(min = 1, max = 120)),
        LAST_NAME_FIELD: fields.Str(required = True, validate = validate.Length(min = 1, max = 120)),
        "jobFunction": fields.Str(required = True, validate = validate.Length(min = 1, max = 120)),
        "company": fields.Str(required = True, validate = validate.Length(min = 1, max = 250)),
        USERNAME_FIELD: fields.Str(required = True, validate = validate.Length(min = 2, max = 30)),
        # PASSWORD_FIELD: fields.Str(required = True, validate = [ validate.Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[\/\?\,\!\@\#\$\%\^\&\*\)\(\+\=\.\<\>\{\}\[\]\:\;\'\"\|\~\`\_\-])(?=.{8,})"), validate.Length(min = 8, max = 128) ]),
        COUNTRY_FIELD: fields.Str(required = True, validate = validate.Length(min = 1, max = 120)),
        STATE_FIELD: fields.Str(validate = validate.Length(min = 1, max = 120)),
        PROVINCE_FIELD: fields.Str(validate = validate.Length(min = 1, max = 120)),
        "agreeTerms": fields.Bool(required = True, validate = validate.Equal(True)),
        COURSE_ID_FIELD: fields.Str(validate = validate.Length(min = 1, max = 120))
    }, request)

    if data[COUNTRY_FIELD] == COUNTRY_USA:
        if STATE_FIELD not in data:
            return UNPROCESSABLE_ENTITY_MESSAGE, UNPROCESSABLE_ENTITY_CODE, cors_headers
    elif data[COUNTRY_FIELD] == COUNTRY_CANADA:
        if PROVINCE_FIELD not in data:
            return UNPROCESSABLE_ENTITY_MESSAGE, UNPROCESSABLE_ENTITY_CODE, cors_headers
    else:
        if STATE_FIELD in data or PROVINCE_FIELD in data:
            return UNPROCESSABLE_ENTITY_MESSAGE, UNPROCESSABLE_ENTITY_CODE, cors_headers

    # if data[EMAIL_FIELD] == data[PASSWORD_FIELD] or data[EMAIL_FIELD] == data[USERNAME_FIELD]:
    #     return UNPROCESSABLE_ENTITY_MESSAGE, UNPROCESSABLE_ENTITY_CODE, cors_headers

    print(f"Registering user: {data[USERNAME_FIELD]}")

    response = call_appsembler_api("registrations", {
        "name": f"{data[FIRST_NAME_FIELD]} {data[LAST_NAME_FIELD]}",
        "username": data[USERNAME_FIELD],
        "email": data[EMAIL_FIELD]#,
        # Remove this due to bug in Appsembler API that accidentally activates the user.
        #"password": data[PASSWORD_FIELD],
        #"send_activation_email": True
    })

    if response.status_code == CONFLICT_CODE:
        print(f"User already exists: {data[USERNAME_FIELD]} {data[EMAIL_FIELD]}")
        return "User already exists.", CONFLICT_CODE, cors_headers
    elif response.status_code == UNPROCESSABLE_ENTITY_CODE:
        print(f"Bad data in one or more registration data fields, user {data[USERNAME_FIELD]}.")
        return "Bad data in one or more registration data fields.", UNPROCESSABLE_ENTITY_CODE, cors_headers
    elif not response.status_code == OK_CODE:
        print(f"{response.status_code} error registering user {data[USERNAME_FIELD]}")
        return "Error processing student registration.", BAD_REQUEST_CODE, cors_headers

    # We are done unless they also wanted to enroll in a course.
    if not COURSE_ID_FIELD in data:
        print(f"Successfully registered user {data[USERNAME_FIELD]}")
        return OK_MESSAGE, OK_CODE, cors_headers

    # Call Appsembler enrollment API if the above succeeded and we have a course to enroll in...
    if COURSE_ID_FIELD in data:
        identifiers = []
        identifiers.append(data[EMAIL_FIELD])
        courses = []
        courses.append(data[COURSE_ID_FIELD])

        response = call_appsembler_api("enrollments", {
            "action": "enroll",
            "auto_enroll": True,
            "courses": courses,
            "identifiers": identifiers
        })

        if response.status_code == CREATED_CODE:
            print(f"Successfully registered user {data[USERNAME_FIELD]} on course {data[COURSE_ID_FIELD]}")
            return OK_MESSAGE, cors_headers
        
        print(f"Error enrolling user {data[USERNAME_FIELD]} on course {data[COURSE_ID_FIELD]}")
        return "Error with course enrollment.", BAD_REQUEST_CODE, cors_headers

    return OK_MESSAGE, cors_headers