const daoLoader = require('./daoloader');

const impl = daoLoader.loadDao('site');

module.exports = {
  /**
   * Insert a new site.
   *
   * @param {Object} site - a site object.
   * @returns {Promise} - a Promise, resolving to the string value
   *   for the ID of the site in the database.
   */
  insert: async site => impl.insert(site),

  /**
   * Get the site object for a given site ID.
   *
   * @param {number} id - a site ID.
   * @returns {Promise} - a Promise, resolving to a site object.
   */
  findById: async id => impl.findById(id),

  /**
   * Get an array of all site objects.
   *
   * @returns {Promise} - a Promise, resolving to an array of site objects.
   */
  findAll: async () => impl.findAll(),

  findByGeo: async (lat, lng, radius, radiusUnit) => impl.findByGeo(
    lat,
    lng,
    radius,
    radiusUnit,
  ),

  findByGeoWithExcessCapacity: async (lat, lng, radius, radiusUnit) => (
    impl.findByGeoWithExcessCapacity(
      lat,
      lng,
      radius,
      radiusUnit,
    )
  ),
};
