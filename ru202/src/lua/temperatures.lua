-- RU202 temperatures.lua

-- Scenario:
-- 
-- - We are migrating an application to use streams, some 
--   consumers still use pub/sub.
-- - We want to push all temperature readings to both pub/sub 
--   channel & stream
-- - We also want to push high temperature readings (>= 86.0F) 
--   to an additional stream 

-- Load script into Redis:
--
-- cat temperatures.lua | redis-cli -x script load
--
-- This returns a SHA1 digest for the script e.g. 
-- "51b0e32f6754ea688ddf3ea123a9e527def64f25"

-- Execute script from Redis-CLI:
--
-- evalsha <SHA1 from load command> 0 82.2
--
--    0: number of arguments which are Redis keys
-- 82.2: temperature value to pass to the script

-- Examples:
--
-- redis.enterprise:6379> evalsha 077484cee666053ee7588e0e2a218f66b35c7765 0 82.2
-- 1) "temperatures"
-- 2) "1554420150586-0"
-- redis.enterprise:6379> evalsha 077484cee666053ee7588e0e2a218f66b35c7765 0 86.6
-- 1) "temperatures"
-- 2) "1554420155937-0"
-- 3) "hightemperatures"
-- 4) "1554420155938-0"

local temperature = ARGV[1]
local response = {}

-- Send all temperatures to pubsub 'temperatures' channel.
redis.call("PUBLISH", "temperatures", temperature)

-- Send all temperatures to 'temperatures' stream.
table.insert(response, 'temperatures')
table.insert(response, redis.call("XADD", "temperatures", "*", "t", temperature))

-- Send high temeratures to the 'hightemperatures' stream.
if tonumber(temperature) >= 86.0 then
    table.insert(response, 'hightemperatures')
    table.insert(response, redis.call("XADD", "hightemperatures", "*", "t", temperature))
end

return response