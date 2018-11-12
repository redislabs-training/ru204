create database edu CHARACTER SET = 'utf8';

create or replace table reg (
user_id bigint not null primary key,
username varchar(255) not null,
full_name varchar(255) not null,
email_address varchar(255) not null,
country varchar(255) null,
registration_date datetime not null,
RU000_2018 boolean null,
RU101_2018_01 boolean null,
RU101_2018_02 boolean null,
RU101_2018_03 boolean null,
RU101_SP_2018_01 boolean null,
RU102J_2018_01 boolean null,
RU201_2018_01 boolean null,
RU202_2018_01 boolean null
)
CHARACTER SET = utf8
;

create or replace table grade (
course_id varchar(255) not null,
user_id bigint not null,
username varchar(255) not null,
email_address varchar(255) not null,
grade double,
homework_avg double,
final_exam_avg double,
graduated boolean,
got_cert boolean,
week1 double,
week2 double,
week3 double,
week4 double,
week5 double,
week6 double,
week7 double,
week8 double,
fe1 double,
fe2 double,
fe3 double,
fe4 double,
primary key (course_id, user_id)
)
CHARACTER SET = utf8
;

create or replace table offer (
offer_id varchar(255) not null,
user_id bigint not null,
full_name varchar(255) not null,
email_address varchar(255) not null,
country varchar(255) null,
primary key (offer_id, user_id)
)
CHARACTER SET = utf8
;

DROP FUNCTION IF EXISTS gradescore_conv;

delimiter //
CREATE FUNCTION gradescore_conv(score varchar(50))
    RETURNS int
BEGIN
        DECLARE v double;
        CASE score
            WHEN "Not Attempted" THEN select -1 into v;
            ELSE
                BEGIN
                    select score into v;
                END;
        END CASE;
        RETURN v;
END//
delimiter ;

DROP FUNCTION IF EXISTS boolean_conv;

delimiter //
CREATE FUNCTION boolean_conv(score varchar(1))
    RETURNS boolean
BEGIN
        DECLARE v boolean;
        CASE score
            WHEN "Y" THEN select True into v;
            WHEN "N" THEN select False into v;
        END CASE;
        RETURN v;
END//

delimiter ;


load data infile '/src/redislabs_RU101_2018_01_grade_report_2018-09-25-2257.csv'
into table grade
CHARACTER SET utf8
fields terminated by ','
OPTIONALLY ENCLOSED BY '"'
ignore 1 lines
(@user_id, @email_address, @username, @grade, 
 @week1,  @week2, @week3, @week4, @week5, @homework_avg, 
 @fe1, @fe2, @final_exam_avg, 
 @dummy, @dummy, 
 @graduated, @got_cert, @dummy)
set course_id = 'RU101_2018_01'
, user_id = @user_id
, username = @username
, email_address = @email_address
, grade = @grade
, homework_avg = @homework_avg
, final_exam_avg = @final_exam_avg
, week1 = gradescore_conv(@week1)
, week2 = gradescore_conv(@week2)
, week3 = gradescore_conv(@week3)
, week4 = gradescore_conv(@week4)
, week5 = gradescore_conv(@week5)
, fe1 = gradescore_conv(@fe1)
, fe2 = gradescore_conv(@fe2)
, graduated = boolean_conv(@graduated) 
, got_cert = boolean_conv(@got_cert)
;

load data infile '/src/redislabs_RU101_2018_02_grade_report_2018-10-10-2024.csv'
into table grade
CHARACTER SET utf8
fields terminated by ','
OPTIONALLY ENCLOSED BY '"'
ignore 1 lines
(@user_id, @email_address, @username, @grade, 
 @week1,  @week2, @week3, @week4, @week5, @homework_avg, 
 @fe1, @fe2, @fe3, @final_exam_avg, 
 @dummy, @dummy, 
 @graduated, @got_cert, @dummy)
set course_id = 'RU101_2018_02'
, user_id = @user_id
, username = @username
, email_address = @email_address
, grade = @grade
, homework_avg = @homework_avg
, final_exam_avg = @final_exam_avg
, week1 = gradescore_conv(@week1)
, week2 = gradescore_conv(@week2)
, week3 = gradescore_conv(@week3)
, week4 = gradescore_conv(@week4)
, week5 = gradescore_conv(@week5)
, fe1 = gradescore_conv(@fe1)
, fe2 = gradescore_conv(@fe2)
, fe3 = gradescore_conv(@fe3)
, graduated = boolean_conv(@graduated) 
, got_cert = boolean_conv(@got_cert)
;

load data infile '/src/redislabs_RU101_SP_2018_01_grade_report_2018-11-08-2252.csv'
into table grade
CHARACTER SET utf8
fields terminated by ','
OPTIONALLY ENCLOSED BY '"'
ignore 1 lines
(@user_id, @email_address, @username, @grade, 
 @week1,  @week2, @week3, @week4, @week5, @homework_avg, 
 @fe1, @fe2, @fe3, @final_exam_avg, 
 @dummy, @dummy, 
 @graduated, @got_cert, @dummy)
set course_id = 'RU101_SP_2018_01'
, user_id = @user_id
, username = @username
, email_address = @email_address
, grade = @grade
, homework_avg = @homework_avg
, final_exam_avg = @final_exam_avg
, week1 = gradescore_conv(@week1)
, week2 = gradescore_conv(@week2)
, week3 = gradescore_conv(@week3)
, week4 = gradescore_conv(@week4)
, week5 = gradescore_conv(@week5)
, fe1 = gradescore_conv(@fe1)
, fe2 = gradescore_conv(@fe2)
, fe3 = gradescore_conv(@fe3)
, graduated = boolean_conv(@graduated) 
, got_cert = boolean_conv(@got_cert)
;
