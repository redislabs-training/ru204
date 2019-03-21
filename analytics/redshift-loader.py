"""Utility to dump and load keys from Redis. Key values are encoded in JSON. In
this module the following functions are available:

  * dump(fn, compress, match)
  * load(fn, compress)

"""
import sys

def load_registrations(con, filename="/src/redis_user_reports_Feb_13th.csv"):
    import csv
    """Shoudl be javascript.users"""
    add_reg = ( "INSERT INTO javascript.users "
                "(id, username, name, email, country, received_at, context_library_name) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)" )

    cursor = con.cursor()

    try:
        with open(filename, 'rt') as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if i == 0:
                    continue
                user_id = row[0]
                username = row[1]
                full_name = row[2]
                email_address = row[3]
                country = row[4]
                if "." in row[5]:
                    (registration_date,_) = row[5].split('.')
                else:
                    (registration_date,_) = row[5].split('+')
                reg_data = (user_id, username, full_name, email_address, country, registration_date, "redshift-loader.py")
                cursor.execute(add_reg, reg_data)
                
                print(reg_data)
    finally:
        con.commit()
        print("Last good row imported '{}'".format(i))

def load_enrollments(con, filename="/src/redis_user_reports_Feb_13th.csv"):
    import csv
    import uuid
    import ast
    """Should be javascript.edx_course_enrollment_activated"""
    add_enroll = ( "INSERT INTO javascript.edx_course_enrollment_activated"
                " (id, context_course_id, name, user_id, label,"
                " data_course_id, data_user_id, event, context_user_id, context_username,"
                " received_at, sent_at, original_timestamp, timestamp, uuid_ts, context_library_name)"
                " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" )

    cursor = con.cursor()

    try:
        with open(filename, 'rt') as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if i == 0:
                    continue
                id = str(uuid.uuid4())
                user_id = row[0]
                username = row[1]
                full_name = row[2]
                email_address = row[3]
                country = row[4]
                if "." in row[5]:
                    (registration_date,_) = row[5].split('.')
                else:
                    (registration_date,_) = row[5].split('+')
                reg_data = (id, )
                courses = ast.literal_eval(row[7])
                for j, course in enumerate(courses):
                    if course == 'course-v1:redislabs+RLU101+2018-01':
                        continue
                    (_, course_id) = course.split('+',1)
                    course_id = course_id.replace('+','_')
                    enroll_data = (id, course, "edx.course.enrollment.activated", user_id, course, 
                                   course, user_id, "edx.course.enrollment.activated", user_id, username, 
                                   registration_date, registration_date, registration_date, registration_date, registration_date,
                                   "redshift-loader.py")
                    cursor.execute(add_enroll, enroll_data)
                print (row)
                
    finally:
        con.commit()
        print("Last good row imported '{}'".format(i))



def main(command, datafile):
    """Entry point to execute either the dump or load"""
    import os
    import psycopg2

    try:

        con=psycopg2.connect("dbname=lms host=lms.c3ewdu0ze66e.us-east-1.redshift.amazonaws.com port=5439 user=lmsfeed password=rlisgr8RS!")

        if command == "reg":
            load_registrations(con, filename=datafile)
        elif command == "reg2":
            load_registrations2(con, filename=datafile)
        elif command == "enroll":
            load_enrollments(con, filename=datafile)
        else:
            print("Don't know how to do '{}'".format(command))
    finally:
        con.close()

if __name__ == "__main__":
  main(sys.argv[1], sys.argv[2])
