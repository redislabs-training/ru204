const redis = require('./redis_client');
const keyGenerator = require('./redis_key_generator');

const insert = async meterReadings => 'Redis TODO';

const getRecent = async (key, limit) => {
  const client = redis.getClient();

  let entries;

  if (limit) {
    entries = await client.xrevrangeAsync(key, '+', '-', 'COUNT', limit);
  } else {
    entries = await client.xrevrangeAsync(key, '+', '-');
  }

  // TODO entries needs to be reformatted as the Redis
  // client doesn't unpack it into objects for us...

  return entries;
};

const getRecentGlobal = async limit => getRecent(keyGenerator.getGlobalFeedKey(), limit);

const getRecentForSite = async (siteId, limit) => getRecentForSite(
  keyGenerator.getFeedKey(siteId),
  limit,
);

module.exports = {
  insert,
  getRecentGlobal,
  getRecentForSite,
};
