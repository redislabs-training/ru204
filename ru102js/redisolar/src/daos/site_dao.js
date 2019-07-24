const daoLoader = require('./daoloader');

const impl = daoLoader.loadDao('site');

module.exports = {
  insert: async site => impl.insert(site),

  /**
   * Get the site object for a given site ID.
   *
   * @param {number} id - a site ID.
   * @return {Promise} - a Promise, resolving to a site object.
   */
  findById: async id => impl.findById(id),

  /**
   * Get an array of all site objects.
   *
   * @return {Promise} - a Promise, resolving to an array of site objects.
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
