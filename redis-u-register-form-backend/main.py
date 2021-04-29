from webargs import fields, validate
from webargs.flaskparser import parser
from datetime import datetime

import analytics
import os
import requests

EMAIL_FIELD = "email"
FIRST_NAME_FIELD = "firstName"
LAST_NAME_FIELD = "lastName"
USERNAME_FIELD = "userName"
JOB_FUNCTION_FIELD = "jobFunction"
COMPANY_FIELD = "company"
PASSWORD_FIELD = "password"
COUNTRY_FIELD = "country"
STATE_FIELD = "state"
PROVINCE_FIELD = "province"
COURSE_ID_FIELD = "courseId"
AGREE_TERMS_FIELD = "agreeTerms"
COUNTRY_USA = "United States"
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
REGISTRATION_REQUIRES_COUNTRY = os.environ.get("REGISTRATION_REQUIRES_COUNTRY")

CORS_ORIGIN = os.environ.get("CORS_ORIGIN")

analytics.write_key = os.environ.get("SEGMENT_WRITE_KEY")

cors_headers = {
    "Access-Control-Allow-Origin": CORS_ORIGIN,
    "Access-Control-Allow-Methods": "POST",
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Max-Age": "3600"
}

COUNTRY_CODE_LOOKUP = {
    "Afghanistan": "AF",
    "Albania": "AL",
    "Algeria": "DZ",
    "American Samoa": "AS",
    "Andorra": "AD",
    "Angola": "AO",
    "Anguilla": "AI",
    "Antarctica": "AQ",
    "Antigua and Barbuda": "AG",
    "Argentina": "AR",
    "Armenia": "AM",
    "Aruba": "AW",
    "Australia": "AU",
    "Austria": "AT",
    "Azerbaijan": "AZ",
    "Bahamas": "BS",
    "Bahrain": "BH",
    "Bangladesh": "BD",
    "Barbados": "BB",
    "Belarus": "BY",
    "Belgium": "BE",
    "Belize": "BZ",
    "Benin": "BJ",
    "Bermuda": "BM",
    "Bhutan": "BT",
    "Bolivia": "BO",
    "Bonaire, Sint Eustatius and Saba": "BQ",
    "Bosnia and Herzegovina": "BA",
    "Botswana": "BW",
    "Bouvet Island": "BV",
    "Brazil": "BR",
    "British Indian Ocean Territory": "IO",
    "Brunei": "BN",
    "Bulgaria": "BG",
    "Burkina Faso": "BF",
    "Burundi": "BI",
    "Cabo Verde": "CV",
    "Cambodia": "KH",
    "Cameroon": "CM",
    "Canada": "CA",
    "Cayman Islands": "KY",
    "Central African Republic": "CF",
    "Chad": "TD",
    "Chile": "CL",
    "China": "CN",
    "Christmas Island": "CX",
    "Cocos (Keeling) Islands": "CC",
    "Colombia": "CO",
    "Comoros": "KM",
    "Congo": "CG",
    "Congo (the Democratic Republic of the)": "CD",
    "Cook Islands": "CK",
    "Costa Rica": "CR",
    "Côte d'Ivoire": "CI",
    "Croatia": "HR",
    "Cuba": "CU",
    "Curaçao": "CW",
    "Cyprus": "CY",
    "Czech Republic": "CZ",
    "Denmark": "DK",
    "Djibouti": "DJ",
    "Dominica": "DM",
    "Dominican Republic": "DO",
    "Ecuador": "EC",
    "Egypt": "EG",
    "El Salvador": "SV",
    "Equatorial Guinea": "GQ",
    "Eritrea": "ER",
    "Estonia": "EE",
    "Ethiopia": "ET",
    "Falkland Islands (Malvinas)": "FK",
    "Faroe Islands": "FO",
    "Fiji": "FJ",
    "Finland": "FI",
    "France": "FR",
    "French Guiana": "GF",
    "French Polynesia": "PF",
    "French Southern Territories": "TF",
    "Gabon": "GA",
    "Gambia": "GM",
    "Georgia": "GE",
    "Germany": "DE",
    "Ghana": "GH",
    "Gibraltar": "GI",
    "Greece": "GR",
    "Greenland": "GL",
    "Grenada": "GD",
    "Guadeloupe": "GP",
    "Guam": "GU",
    "Guatemala": "GT",
    "Guernsey": "GG",
    "Guinea": "GN",
    "Guinea-Bissau": "GW",
    "Guyana": "GY",
    "Haiti": "HT",
    "Heard Island and McDonald Islands": "HM",
    "Holy See": "VA",
    "Honduras": "HN",
    "Hong Kong": "HK",
    "Hungary": "HU",
    "Iceland": "IS",
    "India": "IN",
    "Indonesia": "ID",
    "Iran": "IR",
    "Iraq": "IQ",
    "Ireland": "IE",
    "Isle of Man": "IM",
    "Israel": "IL",
    "Italy": "IT",
    "Jamaica": "JM",
    "Japan": "JP",
    "Jersey": "JE",
    "Jordan": "JO",
    "Kazakhstan": "KZ",
    "Kenya": "KE",
    "Kiribati": "KI",
    "Kosovo": "XK",
    "Kuwait": "KW",
    "Kyrgyzstan": "KG",
    "Laos": "LA",
    "Latvia": "LV",
    "Lebanon": "LB",
    "Lesotho": "LS",
    "Liberia": "LR",
    "Libya": "LY",
    "Liechtenstein": "LI",
    "Lithuania": "LT",
    "Luxembourg": "LU",
    "Macao": "MO",
    "Macedonia": "MK",
    "Madagascar": "MG",
    "Malawi": "MW",
    "Malaysia": "MY",
    "Maldives": "MV",
    "Mali": "ML",
    "Malta": "MT",
    "Marshall Islands": "MH",
    "Martinique": "MQ",
    "Mauritania": "MR",
    "Mauritius": "MU",
    "Mayotte": "YT",
    "Mexico": "MX",
    "Micronesia (Federated States of)": "FM",
    "Moldova": "MD",
    "Monaco": "MC",
    "Mongolia": "MN",
    "Montenegro": "ME",
    "Montserrat": "MS",
    "Morocco": "MA",
    "Mozambique": "MZ",
    "Myanmar": "MM",
    "Namibia": "NA",
    "Nauru": "NR",
    "Nepal": "NP",
    "Netherlands": "NL",
    "New Caledonia": "NC",
    "New Zealand": "NZ",
    "Nicaragua": "NI",
    "Niger": "NE",
    "Nigeria": "NG",
    "Niue": "NU",
    "Norfolk Island": "NF",
    "North Korea": "KP",
    "Northern Mariana Islands": "MP",
    "Norway": "NO",
    "Oman": "OM",
    "Pakistan": "PK",
    "Palau": "PW",
    "Palestine, State of": "PS",
    "Panama": "PA",
    "Papua New Guinea": "PG",
    "Paraguay": "PY",
    "Peru": "PE",
    "Philippines": "PH",
    "Pitcairn": "PN",
    "Poland": "PL",
    "Portugal": "PT",
    "Puerto Rico": "PR",
    "Qatar": "QA",
    "Réunion": "RE",
    "Romania": "RO",
    "Russia": "RU",
    "Rwanda": "RW",
    "Saint Barthélemy": "BL",
    "Saint Helena, Ascension and Tristan da Cunha": "SH",
    "Saint Kitts and Nevis": "KN",
    "Saint Lucia": "LC",
    "Saint Martin (French part)": "MF",
    "Saint Pierre and Miquelon": "PM",
    "Saint Vincent and the Grenadines": "VC",
    "Samoa": "WS",
    "San Marino": "SM",
    "Sao Tome and Principe": "ST",
    "Saudi Arabia": "SA",
    "Senegal": "SN",
    "Serbia": "RS",
    "Seychelles": "SC",
    "Sierra Leone": "SL",
    "Singapore": "SG",
    "Sint Maarten (Dutch part)": "SX",
    "Slovakia": "SK",
    "Slovenia": "SI",
    "Solomon Islands": "SB",
    "Somalia": "SO",
    "South Africa": "ZA",
    "South Georgia and the South Sandwich Islands": "GS",
    "South Korea": "KR",
    "South Sudan": "SS",
    "Spain": "ES",
    "Sri Lanka": "LK",
    "Sudan": "SD",
    "Suriname": "SR",
    "Svalbard and Jan Mayen": "SJ",
    "Swaziland": "SZ",
    "Sweden": "SE",
    "Switzerland": "CH",
    "Syria": "SY",
    "Taiwan": "TW",
    "Tajikistan": "TJ",
    "Tanzania": "TZ",
    "Thailand": "TH",
    "Timor-Leste": "TL",
    "Togo": "TG",
    "Tokelau": "TK",
    "Tonga": "TO",
    "Trinidad and Tobago": "TT",
    "Tunisia": "TN",
    "Turkey": "TR",
    "Turkmenistan": "TM",
    "Turks and Caicos Islands": "TC",
    "Tuvalu": "TV",
    "Uganda": "UG",
    "Ukraine": "UA",
    "United Arab Emirates": "AE",
    "United Kingdom": "GB",
    "United States Minor Outlying Islands": "UM",
    "United States": "US",
    "Uruguay": "UY",
    "Uzbekistan": "UZ",
    "Vanuatu": "VU",
    "Venezuela": "VE",
    "Vietnam": "VN",
    "Virgin Islands (British)": "VG",
    "Virgin Islands (U.S.)": "VI",
    "Wallis and Futuna": "WF",
    "Western Sahara": "EH",
    "Yemen": "YE",
    "Zambia": "ZM",
    "Zimbabwe": "ZW"
}

def lookup_country_code(country_name):
    return COUNTRY_CODE_LOOKUP.get(country_name)

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

def get_org_id_from_course_id(course_id):
    """
    Takes a course_id of the form 'course-v1:redislabs+RU201+SP_2019_01' 
    and returns 'redislabs' or '' if not found.
    """
    
    start_pos = course_id.find(":")
    end_pos = course_id.find("+")

    if start_pos > -1 and end_pos > -1:
        return course_id[start_pos + 1:end_pos]

    return ""

def register_form_processor(request): 
    if request.method == "OPTIONS":
        return "", 204, cors_headers

    if request.method != "POST" or not request.is_json:
        return "Bad request!", BAD_REQUEST_CODE, cors_headers
    
    data = parser.parse({
        EMAIL_FIELD: fields.Str(required = True, validate = [ validate.Email(), validate.Length(min = 1, max = 254) ]),
        FIRST_NAME_FIELD: fields.Str(required = True, validate = validate.Length(min = 1, max = 120)),
        LAST_NAME_FIELD: fields.Str(required = True, validate = validate.Length(min = 1, max = 120)),
        JOB_FUNCTION_FIELD: fields.Str(required = True, validate = validate.Length(min = 1, max = 120)),
        COMPANY_FIELD: fields.Str(required = True, validate = validate.Length(min = 1, max = 250)),
        USERNAME_FIELD: fields.Str(required = True, validate = [ validate.Regexp("^[A-Za-z0-9_-]+$"), validate.Length(min = 2, max = 30) ]),
        PASSWORD_FIELD: fields.Str(required = True, validate = [ validate.Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[\/\?\,\!\@\#\$\%\^\&\*\)\(\+\=\.\<\>\{\}\[\]\:\;\'\"\|\~\`\_\-])(?=.{8,})"), validate.Length(min = 8, max = 128) ]),
        COUNTRY_FIELD: fields.Str(required = True, validate = validate.Length(min = 1, max = 120)),
        STATE_FIELD: fields.Str(validate = validate.Length(min = 1, max = 120)),
        PROVINCE_FIELD: fields.Str(validate = validate.Length(min = 1, max = 120)),
        AGREE_TERMS_FIELD: fields.Bool(required = True, validate = validate.Equal(True)),
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

    if data[EMAIL_FIELD] == data[PASSWORD_FIELD] or data[EMAIL_FIELD] == data[USERNAME_FIELD]:
        return UNPROCESSABLE_ENTITY_MESSAGE, UNPROCESSABLE_ENTITY_CODE, cors_headers

    print(f"Registering user: {data[USERNAME_FIELD]}")

    register_body = {
        "name": f"{data[FIRST_NAME_FIELD]} {data[LAST_NAME_FIELD]}",
        "username": data[USERNAME_FIELD],
        "email": data[EMAIL_FIELD],
        "password": data[PASSWORD_FIELD],
        "send_activation_email": True
    }

    # Our production environment requires the country field as Tahoe is 
    # configured differently.  Need to look up country code from the country
    # name provided by our form as marketing need the full country name.
    if REGISTRATION_REQUIRES_COUNTRY == "True":
        country_code = lookup_country_code(data[COUNTRY_FIELD])

        if country_code is not None:
            register_body["country"] = country_code

    response = call_appsembler_api("registrations", register_body)

    if response.status_code == CONFLICT_CODE:
        print(f"User already exists: {data[USERNAME_FIELD]} {data[EMAIL_FIELD]}")
        return "User already exists.", CONFLICT_CODE, cors_headers
    elif response.status_code == UNPROCESSABLE_ENTITY_CODE:
        print(f"Bad data in one or more registration data fields, user {data[USERNAME_FIELD]}.")
        return "Bad data in one or more registration data fields.", UNPROCESSABLE_ENTITY_CODE, cors_headers
    elif not response.status_code == OK_CODE:
        print(f"{response.status_code} error registering user {data[USERNAME_FIELD]}")
        return "Error processing student registration.", BAD_REQUEST_CODE, cors_headers

    state = ""

    if STATE_FIELD in data:
        state = data[STATE_FIELD]
    elif PROVINCE_FIELD in data:
        state = data[PROVINCE_FIELD]

    response_json = response.json()

    # Send an identify message to Segment...
    # NOTE: Due to a bug in the Appsembler API, the trailing space after user_id is required...
    #       added defensive code in case they fix this...
    appsembler_user_id = response_json.get("user_id ", response_json.get("user_id"))

    analytics.identify(appsembler_user_id, {
        "Email": data[EMAIL_FIELD],
        "FirstName": data[FIRST_NAME_FIELD],
        "LastName": data[LAST_NAME_FIELD],
        "Job_Function_Mktg__c": data[JOB_FUNCTION_FIELD],
        "Company": data[COMPANY_FIELD],
        "UserName": data[USERNAME_FIELD],
        "Country": data[COUNTRY_FIELD],
        "State": state,
        "Lead_Source_New__c": "Redis University",
        "proxySubcenterRedisUniversity": True
    })

    analytics.flush()

    # We are done unless they also wanted to enroll in a course.
    if not COURSE_ID_FIELD in data:
        print(f"Successfully registered user {data[USERNAME_FIELD]}")
        return OK_MESSAGE, OK_CODE, cors_headers

    # Call Appsembler enrollment API if the above succeeded and we have a course to enroll in...
    if COURSE_ID_FIELD in data:
        identifiers = [data[EMAIL_FIELD]]
        courses = [data[COURSE_ID_FIELD]]

        response = call_appsembler_api("enrollments", {
            "action": "enroll",
            "auto_enroll": True,
            "courses": courses,
            "identifiers": identifiers
        })

        if response.status_code == CREATED_CODE:
            # We need to send another Segment message here...
            # edx.course.enrollment.activated - edx doesn't do this when we use the enrollment API...
            analytics.track(appsembler_user_id, "edx.course.enrollment.activated", {
                "context": {
                    "course_id": data[COURSE_ID_FIELD],
                    "host": APPSEMBLER_API_HOST,
                    "org_id": get_org_id_from_course_id(data[COURSE_ID_FIELD]),
                    "user_id": appsembler_user_id,
                    "referer": ""
                },
                "data": {
                    "course_id": data[COURSE_ID_FIELD],
                    "mode": "honor",
                    "user_id": appsembler_user_id
                },
                "label": data[COURSE_ID_FIELD],
                "name": "edx.course.enrollment.activated",
                "nonInteraction": 1,
                "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
            })
            
            analytics.flush()

            print(f"Successfully registered user {data[USERNAME_FIELD]} on course {data[COURSE_ID_FIELD]}")
            return OK_MESSAGE, cors_headers
        
        print(f"Error enrolling user {data[USERNAME_FIELD]} on course {data[COURSE_ID_FIELD]}")
        return "Error with course enrollment.", BAD_REQUEST_CODE, cors_headers

    return OK_MESSAGE, cors_headers