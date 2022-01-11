import csv
import json
import os
import re
import sys
from datetime import date
import requests

ACCREDIBLE_API_KEY = os.environ.get('ACCREDIBLE_API_KEY')
CUTOFF_SCORE = 500

# Map topic names to numbers
field_names = ['email',
    'name',
    'scaled_score',
    'general_redis_knowledge',
    'keys',
    'data_structures',
    'data_modeling',
    'debugging',
    'performance_and_correctness',
    'redis_clustering']

d = date.today()
month = '{0:%B}'.format(d)
year = '20{0:%y}'.format(d)

email_pass_global_vars = { "global_vars": {"course_id": "Certification", "course_run_id": month + ' ' + year, "exam_month": month, "exam_year": year}, "user_vars":[], "template":"certification-passed"}

email_fail_global_vars = { "global_vars": {"course_id": "Certification", "course_run_id": month + ' ' + year, "exam_month": month, "exam_year": year}, "user_vars":[], "template":"certification-failed"}

def insert_user_into_emailer(scaled_score, scored_user, template):
    user_row = {  
            "email": scored_user[0], 
            "name": scored_user[1], 
            "first_name": scored_user[1], 
            "scaled_score": scaled_score, 
            "general_redis_knowledge": scored_user[3], 
            "keys": scored_user[4], 
            "data_structures": scored_user[5], 
            "data_modeling": scored_user[6], 
            "debugging": scored_user[7], 
            "performance_and_correctness": scored_user[8], 
            "redis_clustering": scored_user[9]
        }
    if template == "pass":
        email_pass_global_vars["user_vars"].append(user_row)
    else:
        email_fail_global_vars["user_vars"].append(user_row)


def calculate_scaled_score(score):
    """ We're not doing anything fancy with score scaling just yet. We are saying that
        a passing score is at least 500 out 700 possible points.
    """
    return int(float(score) * 700)

# loads in a list of emails from previous graduates to skip
# preiously graded students
def load_graduates():
    with open('graduates') as grad_list:
        lines = grad_list.readlines()
    return list(map(lambda x: x.strip('\r\n'), lines))


def add_graduate(email):
    # open graduates.js and add email to list
    with open("graduates", "a+") as grad_list:
        # Append text at the end of file
        grad_list.write('\n')
        grad_list.write(email)


def load_topic_map(filename):
    """ The topic map is just a single column of numbers,
        where row+1 indicates the question number and the values
        represents which topic.
    """
    with open(filename) as topic_file:
        lines = topic_file.readlines()
    return list(map(lambda x: int(x.strip('\r\n')), lines))


def load_profile_info(filename):
    mapping = {}
    with open(filename) as profile_file:
        profile_info = csv.reader(profile_file, delimiter=',')
        for line in profile_info:
            mapping[line[3]] = line[2]
    return mapping


def accredible_format(pass_name, pass_email):
    """ Returns a dict of user email and name along with specific data for 
        Accredible bulk_create API call
    """
    return {'recipient':{'email': pass_email, 'name': pass_name }, 
    'group': 'Redis Certified Developer' , 'group_id': 163205, 'approve': False}


def bulk_create_accredible(credentials):
    """ API call to Accredible to create credentials """
    url = 'https://api.accredible.com/v1/credentials/bulk_create'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token token={ACCREDIBLE_API_KEY}'
    }
    response = requests.post(url=url, json={'credentials': credentials}, headers=headers)
    if 'errors' in response.json():
        error_list = response.json()['errors']
        print(f'There was an error attempting to create credentials: \n {error_list}')
    elif len(response.json()['credentials']) == 0:
        print("No Credentials to issue")
    else:
        print(response.json())
        print('Successfully created credentials') 


def calculate_percentage_per_topic(row):
    """ Questions start at the 5th column and show up every
        other column after that. That's why 'question' is
        advanced by 1 whereas 'position' is advanced by 2.
        Questions are derived from 7 different topics, hence
        the lengths of the 'scores' and 'totals' lists.
        There are 80 total questions on the v1 exam,
        hence the magic number 80.
    """
    position = 5
    question = 1
    scores = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    totals = [0, 0, 0, 0, 0, 0, 0]
    total_score = 0
    while question <= 80:
        result = row[position]
        totals[question_topic_mapping[question-1]-1] += 1
        if result == '1.0':
            total_score += 1
            scores[question_topic_mapping[question-1]-1] += 1.0
        position += 2
        question += 1

    percentages = [0, 0, 0, 0, 0, 0, 0]
    for x in range(7):
        if totals[x] == 0:
            continue
        percentages[x] = str(int(round(scores[x] / totals[x] * 100))) + '%'

    percentages.append(total_score / 80)
    return percentages


# Load the files mapping questions to topics
question_topic_mapping = load_topic_map('exam-topic-key.csv')

# Load the profile info to match emails to field_names
email_name_mapping = load_profile_info('profile_info.csv')

redis_email_matcher = re.compile('.*redislabs.com')
float_matcher = re.compile(r'\d+[.]\d+')

grad_list = load_graduates()

with open('grade_report.csv') as csvfile:
    reader = csv.reader(csvfile)
    credentials_list= []
    for csv_row in reader:
        email = csv_row[1]

        # check if a past graduate
        if email in grad_list:
            continue
        
        # check if redis employee
        matches = redis_email_matcher.match(email)
        if matches is not None:
            continue


        grade = csv_row[4]
        if float_matcher.match(grade):
            scaled_score = calculate_scaled_score(grade)
            name = email_name_mapping[email]
            accredible_row = [name, email, str(date.today())]
            new_row = [email, name, scaled_score]
            new_row.extend(calculate_percentage_per_topic(csv_row))
            scaled_score = calculate_scaled_score(new_row.pop())
            if scaled_score > 0:
                if email != 'Email':
                    add_graduate(email)
            if scaled_score >= CUTOFF_SCORE:
                new_row[2] = scaled_score
                insert_user_into_emailer(scaled_score, new_row, "pass")   
                credentials_list.append(accredible_format(name, email))
            elif scaled_score > 0:
                insert_user_into_emailer(scaled_score, new_row, "fail")   
                
bulk_create_accredible(credentials_list)

if(email_pass_global_vars['user_vars']):
    pass_json = open('pass-json-' + str(date.today()) + '.json', "w")
    pass_json.write(str(json.dumps(email_pass_global_vars)))
    print(json.dumps(email_pass_global_vars, indent=2))

if(email_fail_global_vars['user_vars']):
    fail_json = open('fail-json-' + str(date.today()) + '.json', "w")
    fail_json.write(str(json.dumps(email_fail_global_vars)))
    print(json.dumps(email_fail_global_vars, indent=2))