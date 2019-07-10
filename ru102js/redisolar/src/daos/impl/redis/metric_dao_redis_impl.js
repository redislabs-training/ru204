const roundTo = require('round-to');
const redis = require('./redis_client');
const keyGenerator = require('./redis_key_generator');
const timeUtils = require('../../../utils/time_utils');

const metricsPerDay = 60 * 24;
const maxMetricRetentionDays = 30;
const metricExpirationSeconds = 60 * 60 * 24 * maxMetricRetentionDays + 1;
const maxDaysToReturn = 7;

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
    currentTimestamp -= 24 * 60 * 60; // One day, seconds.
  } while (count > 0 && iterations < maxDaysToReturn);

  return measurements;
};

module.exports = {
  insert,
  getRecent,
};
