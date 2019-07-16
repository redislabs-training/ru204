const roundTo = require('round-to');
const redis = require('./redis_client');
const keyGenerator = require('./redis_key_generator');
const timeUtils = require('../../../utils/time_utils');

const metricIntervalSeconds = 60;
const metricsPerDay = metricIntervalSeconds * 24;
const maxMetricRetentionDays = 30;
const metricExpirationSeconds = 60 * 60 * 24 * maxMetricRetentionDays + 1;
const maxDaysToReturn = 7;
const daySeconds = 24 * 60 * 60;
const timeSeriesMetricRetention = daySeconds * maxMetricRetentionDays;

const formatMeasurementMinute = (measurement, minuteOfDay) => `${roundTo(measurement, 2)}:${minuteOfDay}`;

const extractMeasurementMinute = (measurementMinute) => {
  const arr = measurementMinute.split(':');
  return {
    measurement: parseFloat(arr[0], 10),
    minute: parseInt(arr[1], 10),
  };
};

const insertMetric = async (siteId, metricValue, metricName, timestamp) => {
  const client = redis.getClient();

  const metricKey = keyGenerator.getDayMetricKey(siteId, metricName, timestamp);
  const minuteOfDay = timeUtils.getMinuteOfDay(timestamp);

  const pipeline = client.batch();

  pipeline.zadd(metricKey, minuteOfDay, formatMeasurementMinute(metricValue, minuteOfDay));
  pipeline.expire(metricKey, metricExpirationSeconds);

  await pipeline.execAsync();
};

/* eslint-disable no-unused-vars */
const insertMetricTS = async (siteId, metricValue, metricName, timestamp) => {
  const client = redis.getClient();

  await client.send_commandAsync('TS.ADD', [
    keyGenerator.getTSKey(siteId, metricName),
    timestamp * 1000, // Use millseconds
    metricValue,
    'RETENTION',
    timeSeriesMetricRetention,
  ]);
};
/* eslint-enable */

const getMeasurementsForDate = async (siteId, metricUnit, timestamp, limit) => {
  const client = redis.getClient();

  const key = keyGenerator.getDayMetricKey(siteId, metricUnit, timestamp);

  const metrics = await client.zrevrangeAsync(key, 0, limit - 1);

  const formattedMeasurements = [];

  for (let n = 0; n < metrics.length; n += 1) {
    const { measurement, minute } = extractMeasurementMinute(metrics[n]);

    // Add in reverse order.
    formattedMeasurements.unshift({
      siteId,
      dateTime: timeUtils.getTimestampForMinuteOfDay(timestamp, minute),
      value: measurement,
      metricUnit,
    });
  }

  return formattedMeasurements;
};

const insert = async (meterReading) => {
  await Promise.all([
    insertMetric(meterReading.siteId, meterReading.whGenerated, 'whGenerated', meterReading.dateTime),
    insertMetric(meterReading.siteId, meterReading.whUsed, 'whUsed', meterReading.dateTime),
    insertMetric(meterReading.siteId, meterReading.tempC, 'tempC', meterReading.dateTime),
  ]);
};

/* eslint-disable no-unused-vars */
const getRecent = async (siteId, metricUnit, timestamp, limit) => {
  if (limit > (metricsPerDay * maxMetricRetentionDays)) {
    const err = new Error(`Cannot request more than ${maxMetricRetentionDays} days of minute level data.`);
    err.name = 'TooManyMetricsError';

    throw err;
  }

  let currentTimestamp = timestamp;
  let count = limit;
  let iterations = 0;
  const measurements = [];

  do {
    /* eslint-disable no-await-in-loop */
    const dateMeasurements = await getMeasurementsForDate(
      siteId,
      metricUnit,
      currentTimestamp,
      count,
    );
    /* eslint-enable */

    measurements.unshift(...dateMeasurements);
    count -= dateMeasurements.length;
    iterations += 1;
    currentTimestamp -= daySeconds;
  } while (count > 0 && iterations < maxDaysToReturn);

  return measurements;
};
/* eslint-enable */

/* eslint-disable no-unused-vars */
const insertTS = async (meterReading) => {
  await Promise.all([
    insertMetricTS(meterReading.siteId, meterReading.whGenerated, 'whGenerated', meterReading.dateTime),
    insertMetricTS(meterReading.siteId, meterReading.whUsed, 'whUsed', meterReading.dateTime),
    insertMetricTS(meterReading.siteId, meterReading.tempC, 'tempC', meterReading.dateTime),
  ]);
};
/* eslint-enable */

/* eslint-disable no-unused-vars */
const getRecentTS = async (siteId, metricUnit, timestamp, limit) => {
  if (limit > (metricsPerDay * maxMetricRetentionDays)) {
    const err = new Error(`Cannot request more than ${maxMetricRetentionDays} days of minute level data.`);
    err.name = 'TooManyMetricsError';

    throw err;
  }

  const client = redis.getClient();

  // End at the provided start point.
  const toMillis = timestamp * 1000;

  // Start as far back as we are allowed to go.
  const fromMillis = toMillis - (maxDaysToReturn * daySeconds * 1000);

  // Get the samples from RedisTimeSeries.
  const samples = await client.send_commandAsync('ts.range', [
    keyGenerator.getTSKey(siteId, metricUnit),
    fromMillis,
    toMillis,
  ]);

  // Truncate array if needed.
  if (samples.length > limit) {
    samples.length = limit;
  }

  const measurements = [];

  // Samples is an array of arrays [ timestamp in millis, 'value as string' ]
  for (const sample of samples) {
    measurements.push({
      siteId,
      dateTime: Math.floor(sample[0] / 1000),
      value: parseFloat(sample[1], 10),
      metricUnit,
    });
  }

  return measurements;
};
/* eslint-enable */

module.exports = {
  insert, // : insertTS,
  getRecent, // : getRecentTS,
};
