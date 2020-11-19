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

BAD_REQUEST_MESSAGE = 'Bad Request!'
BAD_REQUEST_CODE = 400
UNPROCESSABLE_ENTITY_MESSAGE = "Unprocessable Entity!"
UNPROCESSABLE_ENTITY_CODE = 422

APPSEMBLER_API_KEY = os.environ.get("APPSEMBLER_API_KEY")
APPSEMBLER_API_HOST = os.environ.get("APPSEMBLER_API_HOST")

analytics.write_key = os.environ.get("SEGMENT_WRITE_KEY")

def call_appsembler_api(endpoint, data):
    api_endpoint = f"https://{APPSEMBLER_API_HOST}/tahoe/api/v1/{endpoint}/"

    print(api_endpoint)
    print(data)

    # return requests.post(
    #     api_endpoint,
    #     json = data,
    #     headers = { 
    #         "Authorization": f"Token {APPSEMBLER_API_KEY}",
    #         "Content-Type": "application/json",
    #         "Cache-Control": "no-cache"
    #     }
    # )

def register_form_processor(request):
    if request.method == "OPTIONS":
        return "", 204, {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Max-Age": "3600"
        }

    if request.method != "POST" or not request.is_json:
        return BAD_REQUEST_MESSAGE, BAD_REQUEST_CODE
    
    data = parser.parse({
        EMAIL_FIELD: fields.Str(required = True, validate = [ validate.Email(), validate.Length(min = 1, max = 254) ]),
        FIRST_NAME_FIELD: fields.Str(required = True, validate = validate.Length(min = 1, max = 120)),
        LAST_NAME_FIELD: fields.Str(required = True, validate = validate.Length(min = 1, max = 120)),
        "jobFunction": fields.Str(required = True, validate = validate.Length(min = 1, max = 120)),
        "company": fields.Str(required = True, validate = validate.Length(min = 1, max = 250)),
        USERNAME_FIELD: fields.Str(required = True, validate = validate.Length(min = 2, max = 30)),
        PASSWORD_FIELD: fields.Str(required = True, validate = [ validate.Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[\/\?\,\!\@\#\$\%\^\&\*\)\(\+\=\.\<\>\{\}\[\]\:\;\'\"\|\~\`\_\-])(?=.{8,})"), validate.Length(min = 8, max = 128) ]),
        COUNTRY_FIELD: fields.Str(required = True, validate = validate.Length(min = 1, max = 120)),
        STATE_FIELD: fields.Str(validate = validate.Length(min = 1, max = 120)),
        PROVINCE_FIELD: fields.Str(validate = validate.Length(min = 1, max = 120)),
        "agreeTerms": fields.Bool(required = True, validate = validate.Equal(True)),
        COURSE_ID_FIELD: fields.Str(validate = validate.Length(min = 1, max = 120))
    }, request)

    if data[COUNTRY_FIELD] == COUNTRY_USA:
        if STATE_FIELD not in data:
            return UNPROCESSABLE_ENTITY_MESSAGE, UNPROCESSABLE_ENTITY_CODE
    elif data[COUNTRY_FIELD] == COUNTRY_CANADA:
        if PROVINCE_FIELD not in data:
            return UNPROCESSABLE_ENTITY_MESSAGE, UNPROCESSABLE_ENTITY_CODE
    else:
        if STATE_FIELD in data or PROVINCE_FIELD in data:
            return UNPROCESSABLE_ENTITY_MESSAGE, UNPROCESSABLE_ENTITY_CODE

    print(data)

    # Call Appsembler registration API.... 200 = OK, 400 = return 400, 409 = username or email taken...
    # TODO can we determine if it is the username or the email?
    print("Need to register the user...")
    response = call_appsembler_api("registrations", {
        "name": f"{data[FIRST_NAME_FIELD]} {data[LAST_NAME_FIELD]}",
        "username": data[USERNAME_FIELD],
        "email": data[EMAIL_FIELD],
        "password": data[PASSWORD_FIELD]
    })

    # TODO check what happened... response.status_code

    # Call Appsembler enrollment API if the above succeeded and we have a course to enroll in...
    if COURSE_ID_FIELD in data:
        print("Need to enroll the user too!")

        identifiers = []
        identifiers.append(data[EMAIL_FIELD])
        courses = []
        courses.append(data[COURSE_ID_FIELD])

        response = call_appsembler_api("enrollments", {
            "action": "enroll",
            "email_learners": True,
            "auto_enroll": True,
            "courses": courses,
            "identifiers": identifiers
        })

        # TODO check what happened... response.status_code

    return "OK", 200, {
        "Access-Control-Allow-Origin": "*"
    }