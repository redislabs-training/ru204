const redis = require('./redis_client');
const keyGenerator = require('./redis_key_generator');

const insert = async (meterReadings) => {
  const client = redis.getClient();
};

const getRecent = async (key, limit) => {
  const client = redis.getClient();
  let meterReadings = [];
  // const pipeline = client.batch();

  const response = await client.xrevrangeAsync(key, '+', '-', 'COUNT', limit);

  // Stream entries need to be unpacked as the Redis
  // client returns them as an array of arrays, rather
  // than an array of objects.
  if (response && Array.isArray(response)) {
    meterReadings = response.map((entry) => {
      // entry[0] is the stream ID, we don't need that.
      const keyValueArray = entry[1];
      const keyValueObj = {};

      // keyValueArray will always contain an even number of
      // entries, with alternating keys and values.  An empty
      // set of key/value pairs is not permitted in Redis Streams.
      for (let n = 0; n < keyValueArray.length; n += 2) {
        const k = keyValueArray[n];
        const v = keyValueArray[n + 1];

        keyValueObj[k] = v;
      }

      return keyValueObj;
    });
  }

  return meterReadings;
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
