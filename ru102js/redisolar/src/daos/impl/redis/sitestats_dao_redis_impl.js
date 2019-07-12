const redis = require('./redis_client');
const keyGenerator = require('./redis_key_generator');
const timeUtils = require('../../../utils/time_utils');

const weekSeconds = 60 * 60 * 24 * 7;

const findById = (siteId, timestamp) => 'Redis TODO';

const updateBasic = async (key, meterReading) => {
  const client = redis.getClient();

  await client.hsetAsync(key, 'lastReportingTime', timeUtils.getCurrentTimestamp());
  await client.hincrbyAsync(key, 'meterReadingCount', 1);
  await client.expireAsync(key, weekSeconds);

  const maxWh = await client.hgetAsync(key, 'maxWhGenerated');
  if (maxWh === null || meterReading.whGenerated > parseFloat(maxWh, 10)) {
    await client.hset(key, 'maxWhGenerated', meterReading.whGenerated);
  }

  const minWh = await client.hgetAsync(key, 'minWhGenerated');
  if (minWh === null || meterReading.whGenerated < parseFloat(minWh, 10)) {
    await client.hset(key, 'minWhGenerated', meterReading.whGenerated);
  }

  const maxCapacity = await client.hgetAsync(key, 'maxCapacity');
  const thisReadingCapacity = meterReading.whGenerated - meterReading.whUsed;
  if (maxCapacity === null || thisReadingCapacity > parseFloat(maxCapacity, 10)) {
    await client.hset(key, 'maxCapacity', thisReadingCapacity);
  }
};

const updateOptimized = async (key, meterReading) => {
  const client = redis.getClient();

  // TODO implementation...
};

const update = async (meterReading) => {
  const key = keyGenerator.getSiteStatsKey(meterReading.siteId, meterReading.dateTime);

  await updateBasic(key, meterReading);
  // await updateOptimized(key, meterReading);
};

module.exports = {
  findById,
  update,
};
