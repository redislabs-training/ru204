create or replace view users
as
select * 
from javascript.users a
where not exists (select 1 from excluded_users b where b.id = a.id);


-- Old Definition

--  SELECT users.id, users.received_at, users.uuid, users.context_accept_language, users.activated, users.context_client_id, users.context_page_url, users.year_of_birth, users.uuid_ts, users.context_agent, users.context_ip, users.context_session, users.context_user_agent, users.name, users.username, users.age, users.context_page_referrer, users.context_path, users.context_site_id, users.context_host, users.context_library_version, users.context_page_title, users.context_event_source, users.context_user_id, users.context_library_name, users.context_page_path, users.context_page_search, users.context_referer, users.email, users.country, users.context_campaign_name, users.context_campaign_medium, users.context_campaign_source
--    FROM javascript.users
-- EXCEPT 
--  SELECT excluded_users.id, excluded_users.received_at, excluded_users.uuid, excluded_users.context_accept_language, excluded_users.activated, excluded_users.context_client_id, excluded_users.context_page_url, excluded_users.year_of_birth, excluded_users.uuid_ts, excluded_users.context_agent, excluded_users.context_ip, excluded_users.context_session, excluded_users.context_user_agent, excluded_users.name, excluded_users.username, excluded_users.age, excluded_users.context_page_referrer, excluded_users.context_path, excluded_users.context_site_id, excluded_users.context_host, excluded_users.context_library_version, excluded_users.context_page_title, excluded_users.context_event_source, excluded_users.context_user_id, excluded_users.context_library_name, excluded_users.context_page_path, excluded_users.context_page_search, excluded_users.context_referer, excluded_users.email, excluded_users.country, excluded_users.context_campaign_name, excluded_users.context_campaign_medium, excluded_users.context_campaign_source
--    FROM excluded_users;
