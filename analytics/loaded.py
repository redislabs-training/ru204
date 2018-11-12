import MySQLdb as mariadb
import os

db = mariadb.connect(host=os.environ.get("APP_MARIADB_HOST", "172.17.0.3"),
                     user=os.environ.get("APP_USER","root"),
                     passwd=os.environ.get("APP_USER_PW","passwd"),
                     db=os.environ.get("APP_DATABASE","edu"))




import csv

add_reg = ("INSERT INTO reg "
           "(user_id, username, full_name, email_address, country, registration_date, RU000_2018, RU101_2018_01, RU101_2018_02, RU101_2018_03, RU101_SP_2018_01, RU102J_2018_01, RU201_2018_01, RU202_2018_01) "
           "VALUES (%s, %s, %s, %s, %s, %s, False, False, False, False, False, False, False, False)")
set_course = "UPDATE reg SET %s = %s WHERE user_id = %s"

cursor = db.cursor()

with open("/src/redis_user_reports-2018-11-08.csv", "rb") as f:
    import ast
    reader = csv.reader(f, delimiter=",")
    for i, line in enumerate(reader):
      if i == 0:
        continue
      user_id = line[0]
      username = line[1]
      full_name = line[2]
      email_address = line[3]
      country = line[4]
      if "." in line[5]:
        (registration_date,_) = line[5].split('.')
      else:
        (registration_date,_) = line[5].split('+')
      reg_data = (user_id, username, full_name, email_address, country, registration_date)
      cursor.execute(add_reg, reg_data)
      courses = ast.literal_eval(line[7])
      for j, course in enumerate(courses):
        if course == 'course-v1:redislabs+RLU101+2018-01':
          continue
        (_, course_id) = course.split('+',1)
        course_id = course_id.replace('+','_')
        set_course = "UPDATE reg SET " + course_id + " = 1 where user_id = " + user_id
        cursor.execute(set_course)
      db.commit()

db.close()