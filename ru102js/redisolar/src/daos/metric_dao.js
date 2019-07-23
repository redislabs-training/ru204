const daoLoader = require('./daoloader');

const impl = daoLoader.loadDao('metric');

/**
 * Insert a new meter reading into the database.
 * @param {Object} meterReading - the meter reading to insert.
 * @returns {Promise} - Promise that resolves when the operation is completed.
 */
const insert = async meterReading => impl.insert(meterReading);

/**
 * Get recent metrics for a specific solar site on a given date with
 * an optional limit.
 * @param {number} siteId - the ID of the solar site to get metrics for.
 * @param {string} metricUnit - the name of the metric to get.
 * @param {number} timestamp - UNIX timestamp for the date to get metrics for.
 * @param {number} limit - maximum number of metrics to be returned.
 * @returns {Promise} - Promise resolving to an array of measurement objects.
 */
const getRecent = async (siteId, metricUnit, timestamp, limit) => impl.getRecent(
  siteId,
  metricUnit,
  timestamp,
  limit,
);

module.exports = {
  insert,
  getRecent,
};
