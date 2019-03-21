create table users_20190321 as select * from javascript.users;

UPDATE javascript.users
SET name=coalesce(b.name, javascript.users.name), 
    country=coalesce(b.country, javascript.users.country)
FROM (SELECT a.id id, a.name name, a.country country
      FROM  javascript.users a
      where a.name is not null
        and a.context_library_name = 'redshift-loader.py') AS b
WHERE javascript.users.id=b.id
  and javascript.users.name is null
  and javascript.users.context_library_name != 'redshift-loader.py';

DELETE from javascript.users
where context_library_name = 'redshift-loader.py'
and id in (select id from javascript.users where name is not null group by 1 having count(*) > 1);