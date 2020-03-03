import argparse
import csv
import re
import sys
from datetime import date

parser = argparse.ArgumentParser(description='Grade a Redis Certified Developer Exam')
parser.add_argument('--table', nargs=1, help='The name of the file storing the mapping from questions to catgories', required=True)
parser.add_argument('--grades-csv', dest='grades_csv', nargs=1, help='The name of the csv file containing the raw grades', required=True)
parser.add_argument('--profile-csv', dest='profile_csv', nargs=1, help='The name of the csv file containing the student profile information', required=True)

args = parser.parse_args()

CUTOFF_SCORE = 500

# We're not doing anything fancy with score
# scaling just yet. We are saying that
# a passing score is at least 500 out 700
# possible points.
def calculate_scaled_score(score):
    return int(float(score) * 700)

# Map topic names to numbers
field_names = ['email',
               'name',
               'scaled_score',
               'General_Redis_Knowledge',
               'Keys',
               'Data_Structures',
               'Data_Modeling',
               'Debugging',
               'Performance_and_Correctness',
               'Redis_Clustering']

accredible_field_names = ['Recipient Name', 'Recipient Email', 'Issued On', 'Expiry Date']

# The topic map is just a single column of numbers,
# where row+1 indicates the question number and the values
# represents which topic.
def load_topic_map(filename):
    with open(filename) as topic_file:
        lines = topic_file.readlines()
    return list(map(lambda x: int(x.strip('\r\n')), lines))

def load_profile_info(filename):
    mapping = {}
    with open(filename) as profile_file:
        profile_info = csv.reader(profile_file, delimiter=',')
        for row in profile_info:
            mapping[row[3]] = row[2]
    return mapping

# Questions start at the 5th column and show up every
# other column after that. That's why 'question' is
# advanced by 1 whereas 'position' is advanced by 2.
# Questions are derived from 7 different topics, hence
# the lengths of the 'scores' and 'totals' lists.
# There are 80 total questions on the v1 exam,
# hence the magic number 80.
def calculate_percentage_per_topic(row):
    position = 5
    question = 1
    scores = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    totals = [0, 0, 0, 0, 0, 0, 0]
    while question <= 80:
        result = row[position]
        totals[question_topic_mapping[question-1]-1] += 1
        if result == '1.0':
            scores[question_topic_mapping[question-1]-1] += 1.0
        position += 2
        question += 1

    print(scores)
    print(totals)
    percentages = [0, 0, 0, 0, 0, 0, 0]
    for x in range(7):
        if totals[x] == 0:
            continue
        percentages[x] = str(int(round(scores[x] / totals[x] * 100))) + '%'

    return percentages

# Load the files mapping questions to topics
question_topic_mapping = load_topic_map(str(args.table[0]))

# Load the profile info to match emails to field_names
email_name_mapping = load_profile_info(str(args.profile_csv[0]))
print(email_name_mapping)

redis_email_matcher = re.compile('.*redislabs.com')
float_matcher = re.compile('\d+[.]\d+')
pass_file = open('pass-' + str(date.today()) + '.csv', "w", newline='')
accredible_file = open('accredible-' + str(date.today()) + '.csv', "w", newline='')
fail_file = open('fail-' + str(date.today()) + '.csv', "w", newline='')
pass_csv = csv.writer(pass_file)
pass_csv.writerow(field_names)
accredible_csv = csv.writer(accredible_file)
accredible_csv.writerow(accredible_field_names)
fail_csv = csv.writer(fail_file)
fail_csv.writerow(field_names)
with open(str(args.grades_csv[0])) as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        email = row[1]
        matches = redis_email_matcher.match(email)
        if matches != None:
            continue

        grade = row[4]
        if float_matcher.match(grade):
            print()
            print(email)
            scaled_score = calculate_scaled_score(grade)
            accredible_row = [email_name_mapping[email], email, str(date.today())]
            new_row = [email, email_name_mapping[email], scaled_score]
            new_row.extend(calculate_percentage_per_topic(row))
            if scaled_score >= CUTOFF_SCORE:
                pass_csv.writerow(new_row)
                accredible_csv.writerow(accredible_row)
            else:
                fail_csv.writerow(new_row)
