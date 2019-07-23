const daoLoader = require('./daoloader');

const impl = daoLoader.loadDao('feed');

/**
 * Insert a new meter reading into the system.
 * @param {*} meterReading
 * @returns {Promise} - Promise, resolves on completion.
 */
const insert = async meterReadings => impl.insert(meterReadings);

/**
 * Get recent meter readings for all sites.
 * @param {number} limit - the maximum number of readings to return.
 * @returns {Promise} - Promise that resolves to an array of meter reading objects.
 */
const getRecentGlobal = async limit => impl.getRecentGlobal(limit);

/**
 * Get resent meter readings for a specific solar sites.
 * @param {number} siteId - the ID of the solar site to get readings for.
 * @param {*} limit - the maximum number of readings to return.
 * @returns {Promise} - Promise that resolves to an array of meter reading objects.
 */
const getRecentForSite = async (siteId, limit) => impl.getRecentForSite(siteId, limit);

module.exports = {
  insert,
  getRecentGlobal,
  getRecentForSite,
};
