const redis = require('./redis_client');
const keyGenerator = require('./redis_key_generator');

const globalMaxFeedLength = 10000;
const siteMaxFeedLength = 2440;

/**
 * Take an Object representing a meter reading that was
 * read from a stream, and transform the key values to
 * the appropriate types from strings.
 * @param {Object} streamEntry - An object that was read from a stream.
 * @returns {Object} - A meter reading object.
 * @private
 */
const remap = (streamEntry) => {
  const remappedStreamEntry = { ...streamEntry };

  remappedStreamEntry.siteId = parseInt(streamEntry.siteId, 10);
  remappedStreamEntry.whUsed = parseFloat(streamEntry.whUsed);
  remappedStreamEntry.whGenerated = parseFloat(streamEntry.whGenerated);
  remappedStreamEntry.tempC = parseFloat(streamEntry.tempC);
  remappedStreamEntry.dateTime = parseInt(streamEntry.dateTime, 10);

  return remappedStreamEntry;
};

/**
 * Takes the array of arrays response from a Redis stream
 * XRANGE / XREVRANGE command and unpacks it into an array
 * of meter readings.
 * @param {Array} streamResponse - An array of arrays returned from a Redis stream command.
 * @returns {Array} - An array of meter reading objects.
 * @private
 */
const unpackStreamEntries = (streamResponse) => {
  // Stream entries need to be unpacked as the Redis
  // client returns them as an array of arrays, rather
  // than an array of objects.
  let meterReadings = [];

  if (streamResponse && Array.isArray(streamResponse)) {
    meterReadings = streamResponse.map((entry) => {
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

      return remap(keyValueObj);
    });
  }

  return meterReadings;
};

/**
 * Insert a new meter reading into the system.
 * @param {*} meterReading
 * @returns {Promise} - Promise, resolves on completion.
 */
const insert = async (meterReading) => {
  // Unpack meterReading into array of alternating key
  // names and values for addition to the stream.

  // START Challenge #6
  const fields = [];

  for (const k in meterReading) {
    if (meterReading.hasOwnProperty(k)) {
      fields.push(k);
      fields.push(meterReading[k]);
    }
  }

  const client = redis.getClient();
  const pipeline = client.batch();

  pipeline.xadd(keyGenerator.getGlobalFeedKey(), 'MAXLEN', '~', globalMaxFeedLength, '*', ...fields);
  pipeline.xadd(keyGenerator.getFeedKey(meterReading.siteId), 'MAXLEN', '~', siteMaxFeedLength, '*', ...fields);

  await pipeline.execAsync();
  // END Challenge #6
};

/**
 * Get recent meter reading data.
 * @param {string} key - Key name of Redis Stream to read data from.
 * @param {number} limit - the maximum number of readings to return.
 * @returns {Promise} - Promise that resolves to an array of meter reading objects.
 * @private
 */
const getRecent = async (key, limit) => {
  const client = redis.getClient();
  const response = await client.xrevrangeAsync(key, '+', '-', 'COUNT', limit);

  return unpackStreamEntries(response);
};

/**
 * Get recent meter readings for all sites.
 * @param {number} limit - the maximum number of readings to return.
 * @returns {Promise} - Promise that resolves to an array of meter reading objects.
 */
const getRecentGlobal = async limit => getRecent(keyGenerator.getGlobalFeedKey(), limit);

/**
 * Get resent meter readings for a specific solar sites.
 * @param {number} siteId - the ID of the solar site to get readings for.
 * @param {*} limit - the maximum number of readings to return.
 * @returns {Promise} - Promise that resolves to an array of meter reading objects.
 */
const getRecentForSite = async (siteId, limit) => getRecent(
  keyGenerator.getFeedKey(siteId),
  limit,
);

module.exports = {
  insert,
  getRecentGlobal,
  getRecentForSite,
};
