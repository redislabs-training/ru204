from webargs import fields, validate
from webargs.flaskparser import use_args

@use_args({
    "email": fields.Str(required = True, validate = validate.Email()),
    "firstName": fields.Str(required = True, validate = validate.Length(min = 1, max = 120)),
    "lastName": fields.Str(required = True, validate = validate.Length(min = 1, max = 120)),
    "jobFunction": fields.Str(required = True, validate = validate.Length(min = 1, max = 120)),
    "company": fields.Str(required = True, validate = validate.Length(min = 1, max = 250)),
    "userName": fields.Str(required = True, validate = validate.Length(min = 2, max = 30)),
    "password": fields.Str(required = True, validate = validate.Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[\/\?\,\!\@\#\$\%\^\&\*\)\(\+\=\.\<\>\{\}\[\]\:\;\'\"\|\~\`\_\-])(?=.{8,})")),
    "country": fields.Str(required = True, validate = validate.Length(min = 1, max = 120)),
    "state": fields.Str(), # optional, ideally depends on country value, length requirements
    "province": fields.Str(), # optional, ideally depends on country value, length requirements
    "agreeTerms": fields.Bool(required = True, validate = validate.Equal(True))
})
def register_form_processor(request, args):
    if (request.method != "POST" or not request.is_json):
        return "Bad Request!"
    data = request.json
    print(data)


    return "TODO"