from webargs import fields, validate
from webargs.flaskparser import use_args

import os
import requests

COUNTRY_FIELD = "country"
STATE_FIELD = "state"
PROVINCE_FIELD = "province"
COURSE_ID_FIELD = "courseId"
COUNTRY_USA = "United States of America"
COUNTRY_CANADA = "Canada"
UNPROCESSABLE_ENTITY_MESSAGE = "Unprocessable Entity!"

@use_args({
    "email": fields.Str(required = True, validate = [ validate.Email(), validate.Length(min = 1, max = 254) ]),
    "firstName": fields.Str(required = True, validate = validate.Length(min = 1, max = 120)),
    "lastName": fields.Str(required = True, validate = validate.Length(min = 1, max = 120)),
    "jobFunction": fields.Str(required = True, validate = validate.Length(min = 1, max = 120)),
    "company": fields.Str(required = True, validate = validate.Length(min = 1, max = 250)),
    "userName": fields.Str(required = True, validate = validate.Length(min = 2, max = 30)),
    "password": fields.Str(required = True, validate = [ validate.Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[\/\?\,\!\@\#\$\%\^\&\*\)\(\+\=\.\<\>\{\}\[\]\:\;\'\"\|\~\`\_\-])(?=.{8,})"), validate.Length(min = 8, max = 128) ]),
    "country": fields.Str(required = True, validate = validate.Length(min = 1, max = 120)),
    STATE_FIELD: fields.Str(validate = validate.Length(min = 1, max = 120)),
    PROVINCE_FIELD: fields.Str(validate = validate.Length(min = 1, max = 120)),
    "agreeTerms": fields.Bool(required = True, validate = validate.Equal(True)),
    COURSE_ID_FIELD: fields.Str(validate = validate.Length(min = 1, max = 120))
})
def register_form_processor(request, args):
    if (request.method != "POST" or not request.is_json):
        return "Bad Request!", 400
    
    data = request.json

    if (data[COUNTRY_FIELD] == COUNTRY_USA):
        if (STATE_FIELD not in data):
            return UNPROCESSABLE_ENTITY_MESSAGE, 422
    elif (data[COUNTRY_FIELD] == COUNTRY_CANADA):
        if (PROVINCE_FIELD not in data):
            return UNPROCESSABLE_ENTITY_MESSAGE, 422
    else:
        if (STATE_FIELD in data or PROVINCE_FIELD in data):
            return UNPROCESSABLE_ENTITY_MESSAGE, 422

    print(data)

    # Call Appsembler registration API.... 200 = OK, 400 = return 400, 409 = username or email taken...
    # TODO can we determine if it is the username or the email?
    print("Need to register the user...")

    # Call Appsembler enrollment API if the above succeeded and we have a course to enroll in...
    if (COURSE_ID_FIELD in data):
        print("Need to enroll the user too!")
        # TODO

    return "OK"