insert into offer(offer_id, user_id, full_name, email_address, country)
select 'offer_ru101', r.user_id, r.full_name, r.email_address, r.country
from reg r
where RU101_2018_03 = False 
and r.email_address not in (select g.email_address from grade g where g.course_id in ("RU101_2018_01", "RU101_2018_02", "RU101_SP_2018_01") and g.graduated = True)
;

insert into offer(offer_id, user_id, full_name, email_address, country)
select 'offer_ru201', r.user_id, r.full_name, r.email_address, r.country
from reg r
where RU201_2018_01 = False 
and r.email_address in (select g.email_address from grade g where g.course_id in ("RU101_2018_01", "RU101_2018_02", "RU101_SP_2018_01") and g.graduated = True)
;

insert into offer(offer_id, user_id, full_name, email_address, country)
select 'offer_both', r.user_id, r.full_name, r.email_address, r.country
from reg r
where r.RU101_2018_01 = False
and r.RU101_2018_02 = False
and r.RU101_2018_03 = False
and r.RU101_SP_2018_01 = False
and r.RU201_2018_01 = False
;

select o.full_name, o.email_address, o.country
from offer o
where offer_id = 'offer_ru101'
except
select o.full_name, o.email_address, o.country
from offer o
where o.offer_id in ('offer_both')
INTO OUTFILE '/src/offer_ru101.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

select o.full_name, o.email_address, o.country
from offer o
where offer_id = 'offer_ru201'
except
select o.full_name, o.email_address, o.country
from offer o
where o.offer_id in ('offer_both')
INTO OUTFILE '/src/offer_ru201.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

select o.full_name, o.email_address, o.country
from offer o
where o.offer_id = 'offer_both'
INTO OUTFILE '/src/offer_both.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

