const redis = require('./redis_client');
const compareAndUpdateScript = require('./scripts/compare_and_update_script');
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
    await client.hsetAsync(key, 'maxWhGenerated', meterReading.whGenerated);
  }

  const minWh = await client.hgetAsync(key, 'minWhGenerated');
  if (minWh === null || meterReading.whGenerated < parseFloat(minWh, 10)) {
    await client.hsetAsync(key, 'minWhGenerated', meterReading.whGenerated);
  }

  const maxCapacity = await client.hgetAsync(key, 'maxCapacity');
  const readingCapacity = meterReading.whGenerated - meterReading.whUsed;
  if (maxCapacity === null || readingCapacity > parseFloat(maxCapacity, 10)) {
    await client.hsetAsync(key, 'maxCapacity', readingCapacity);
  }
};

const updateImproved = async (key, meterReading) => {
  const client = redis.getClient();

  // Note: this could also be improved to a single hgetall as 
  //       we know the hash is small.
  const [ maxWh, minWh, maxCapacity ] = await Promise.all([
    client.hgetAsync(key, 'maxWhGenerated'),
    client.hgetAsync(key, 'minWhGenerated'),
    client.hgetAsync(key, 'maxCapacity'),
  ]);

  const commands = [
    client.hsetAsync(key, 'lastReportingTime', timeUtils.getCurrentTimestamp()),
    client.hincrbyAsync(key, 'meterReadingCount', 1),
    client.expireAsync(key, weekSeconds),
  ];

  if (maxWh === null || meterReading.whGenerated > parseFloat(maxWh, 10)) {
    commands.push(client.hsetAsync(key, 'maxWhGenerated', meterReading.whGenerated));
  }

  if (minWh === null || meterReading.whGenerated < parseFloat(minWh, 10)) {
    commands.push(client.hsetAsync(key, 'minWhGenerated', meterReading.whGenerated));
  }

  const readingCapacity = meterReading.whGenerated - meterReading.whUsed;
  if (maxCapacity === null || readingCapacity > parseFloat(maxCapacity, 10)) {
    commands.push(client.hsetAsync(key, 'maxCapacity', readingCapacity));
  }

  await Promise.all(commands);
};

const updateOptimized = async (key, meterReading) => {
  const client = redis.getClient();
  const scriptSha = await compareAndUpdateScript.getSha();
  const transaction = client.multi();

  transaction.hset(key, 'lastReportingTime', timeUtils.getCurrentTimestamp());
  transaction.hincrby(key, 'meterReadingCount', 1);
  transaction.expire(key, weekSeconds);
  transaction.evalsha(scriptSha, 1, key, 'maxWhGenerated', meterReading.whGenerated, '>');
  transaction.evalsha(scriptSha, 1, key, 'minWhGenerated', meterReading.whGenerated, '<');
  transaction.evalsha(scriptSha, 1, key, 'maxCapacity', meterReading.whGenerated - meterReading.whUsed, '>');

  await transaction.execAsync();
};

const update = async (meterReading) => {
  const key = keyGenerator.getSiteStatsKey(meterReading.siteId, meterReading.dateTime);

  //await updateBasic(key, meterReading);
  //await updateImproved(key, meterReading);
  await updateOptimized(key, meterReading);
};

module.exports = {
  findById,
  update,
};
