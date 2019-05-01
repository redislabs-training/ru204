"""Utility to dump and load keys from Redis. Key values are encoded in JSON. In
this module the following functions are available:

  * dump(fn, compress, match)
  * load(fn, compress)

"""
import sys

def create_grades(con):
    import psycopg2.errors

    try:
        cursor = con.cursor()
        find_grades = "select * from grade_reports where 1=2"
        cursor.execute(find_grades)
    except (Exception, psycopg2.DatabaseError) as error:
        try:
            con.rollback()
            create_grade_reports = ("CREATE TABLE IF NOT EXISTS grade_reports ("
                                    "course_id VARCHAR(255) not null,"
                                    "run VARCHAR(255) not null,"
                                    "user_id BIGINT not null,"
                                    "username VARCHAR(255) not null,"
                                    "grade FLOAT,"
                                    "homework_avg FLOAT,"
                                    "final_exam_avg FLOAT,"
                                    "graduated BOOLEAN,"
                                    "got_cert BOOLEAN,"
                                    "hw1 FLOAT,"
                                    "hw2 FLOAT,"
                                    "hw3 FLOAT,"
                                    "hw4 FLOAT,"
                                    "hw5 FLOAT,"
                                    "hw6 FLOAT,"
                                    "hw7 FLOAT,"
                                    "hw8 FLOAT,"
                                    "fe1 FLOAT,"
                                    "fe2 FLOAT,"
                                    "fe3 FLOAT,"
                                    "fe4 FLOAT,"
                                    "fe5 FLOAT,"
                                    "fe6 FLOAT,"
                                    "PRIMARY KEY (course_id, run, user_id)"
                                    ")"
                                   )
            cursor.execute(create_grade_reports)
            con.commit()
        finally:
            print("grade_reports table created")
    finally:
        cursor.close()
        print("tables initalized")

    try:
        cursor = con.cursor()
        create_cp = (   "create or replace view course_performance as "
                        "select a.course_id as course,"
                        "a.run as run,"
                        "a.total as enrolled,"
                        "k.total as graduated,"
                        "b.total as week1,"
                        "c.total as week2,"
                        "d.total as week3,"
                        "e.total as week4,"
                        "f.total as week5,"
                        "j.total as final "
                        "from (select a.course_id, a.run, count(*) as total from grade_reports a where not exists (select 1 from excluded_users b where b.username = a.username) group by 1, 2) a "  
                        "FULL OUTER JOIN (select a.course_id as course_id, a.run as run, count(*) as total from grade_reports a where a.hw1 >= 0 and not exists (select 1 from excluded_users b where b.username = a.username) group by 1, 2) b ON a.course_id = b.course_id AND a.run = b.run "
                        "FULL OUTER JOIN (select a.course_id as course_id, a.run as run, count(*) as total from grade_reports a where a.hw2 >= 0 and not exists (select 1 from excluded_users b where b.username = a.username) group by 1, 2) c ON a.course_id = c.course_id AND a.run = c.run "
                        "FULL OUTER JOIN (select a.course_id as course_id, a.run as run, count(*) as total from grade_reports a where a.hw3 >= 0 and not exists (select 1 from excluded_users b where b.username = a.username) group by 1, 2) d ON a.course_id = d.course_id AND a.run = d.run "
                        "FULL OUTER JOIN (select a.course_id as course_id, a.run as run, count(*) as total from grade_reports a where a.hw4 >= 0 and not exists (select 1 from excluded_users b where b.username = a.username) group by 1, 2) e ON a.course_id = e.course_id AND a.run = e.run "
                        "FULL OUTER JOIN (select a.course_id as course_id, a.run as run, count(*) as total from grade_reports a where a.hw5 >= 0 and not exists (select 1 from excluded_users b where b.username = a.username) group by 1, 2) f ON a.course_id = f.course_id AND a.run = f.run "
                        "FULL OUTER JOIN (select a.course_id as course_id, a.run as run, count(*) as total from grade_reports a where a.final_exam_avg > 0 and not exists (select 1 from excluded_users b where b.username = a.username) group by 1, 2) j ON a.course_id = j.course_id AND a.run = j.run "
                        "FULL OUTER JOIN (select a.course_id as course_id, a.run as run, count(*) as total from grade_reports a where a.grade >= 0.65 and not exists (select 1 from excluded_users b where b.username = a.username) group by 1, 2) k ON a.course_id = k.course_id AND a.run = k.run "
                        "order by 1,2")
        cursor.execute(create_cp)
    finally:
        cursor.close()
        print("views initalized")

_valid_fields = [("Student ID", "user_id", True),
                 ("Username", "username", True),
                 ("Grade", "grade", True),
                 ("Homework 1: Homework", "hw1", True),
                 ("Homework 2: Homework", "hw2", True),
                 ("Homework 3: Homework", "hw3", True),
                 ("Homework 4: Homework", "hw4", True),
                 ("Homework 5: Homework", "hw5", True),
                 ("Homework 6: Homework", "hw6", True),
                 ("Homework 7: Homework", "hw7", True),
                 ("Homework 8: Homework", "hw8", True),
                 ("Homework (Avg)", "homework_avg", True),
                 ("Final Exam 1: Final Exam - Part One", "fe1", True),
                 ("Final Exam 2: Final Exam - Part Two", "fe2", True),
                 ("Final Exam 3: Final Exam - Part Three", "fe3", True),
                 ("Final Exam 4: Final Exam - Part Four", "fe4", True),
                 ("Final Exam 5: Final Exam - Part Five", "fe5", True),
                 ("Final Exam 6: Final Exam - Part Six", "fe6", True),
                 ("Final Exam (Avg)", "final_exam_avg", True),
                 ("Certificate Eligible", "graduated", True),
                 ("Certificate Delivered", "got_cert", True)
                 ]
def map_row_definition(row_headers):
    columns_required = []
    for i in range(len(row_headers)):
        found_one=False
        for t in _valid_fields:
            if row_headers[i] in t:
                columns_required.append(t)
                found_one=True
                break
        if ( found_one  != True):
            columns_required.append((row_headers[i], "", False))
    return columns_required

def build_insert_sql(columns_required):
    insert_sql = "insert into grade_reports (course_id,run"
    for i in range(len(columns_required)):
        _, col, use = columns_required[i]
        if use != True:
            continue
        insert_sql += ',' + col
    insert_sql += ") values (%s,%s"
    for u in range(len(columns_required)):
        _, _, use = columns_required[u]
        if ( use != False):
            insert_sql += ',' + "%s"
    insert_sql += ")"
    return insert_sql

def remove_existing(con, course, run):
    rm_sql = "delete from grade_reports where course_id = %s and run = %s"
    try:
        cursor = con.cursor()
        cursor.execute(rm_sql, (course, run))
        con.commit()
    finally:
        cursor.close()
        print("removed previous course run data")

def load_grades(con, course, run, filename):
    import csv

    try:
        cursor = con.cursor()
        columns = []
        transform = ('Not Attempted','Not Available')
        with open(filename, 'rt') as f:
            remove_existing(con, course, run)
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if i == 0:
                    columns = map_row_definition(row)
                    insert_sql = build_insert_sql(columns)
                    print(columns)
                    print(insert_sql)
                    continue
                vals = [course, run]
                for j in range(len(columns)):
                    _,_,use = columns[j]
                    if ( use != False):
                        if row[j] in transform:
                            vals.append(None)
                        else:
                            vals.append(row[j])
                print(vals)
                cursor.execute(insert_sql, vals)
    finally:
        con.commit()
        cursor.close()
        print("Last good row imported '{}'".format(i))



def main(pw, course, run, datafile):
    """Entry point to execute either the dump or load"""
    import os
    import psycopg2

    try:

        con=psycopg2.connect("dbname=lms host=lms.c3ewdu0ze66e.us-east-1.redshift.amazonaws.com port=5439 user=lmsfeed password=" + pw)

        create_grades(con)
        load_grades(con, course, run, datafile)

    finally:
        con.close()

if __name__ == "__main__":
  main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
