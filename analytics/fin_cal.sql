create table if not exists financial_calendar (
  start_date timestamp without time zone,
  end_date timestamp without time zone,
  financial_year int,
  financial_quarter int,
  label varchar(24));
 
insert into financial_calendar(label, start_date, end_date, financial_year, financial_quarter) values
('FY19-Q1','2018-02-01','2018-04-30', 2019,1);

insert into financial_calendar(label, start_date, end_date, financial_year, financial_quarter) values
('FY19-Q2','2018-05-01','2018-07-31',2019,2);

insert into financial_calendar(label, start_date, end_date, financial_year, financial_quarter) values
('FY19-Q3','2018-08-01','2018-10-31',2019,3);

insert into financial_calendar(label, start_date, end_date, financial_year, financial_quarter) values
('FY19-Q4','2018-11-01','2019-01-31',2019,4);

insert into financial_calendar(label, start_date, end_date, financial_year, financial_quarter) values
('FY20-Q1','2019-02-01','2019-04-30',2020,1);

insert into financial_calendar(label, start_date, end_date, financial_year, financial_quarter) values
('FY20-Q2','2019-05-01','2019-07-31', 2020, 2);

insert into financial_calendar(label, start_date, end_date, financial_year, financial_quarter) values
('FY20-Q3','2019-08-01','2019-10-31',2020,3);

insert into financial_calendar(label, start_date, end_date, financial_year, financial_quarter) values
('FY20-Q4','2019-11-01','2020-01-31',2020,4);