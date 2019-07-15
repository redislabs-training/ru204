const siteDao = require('../daos/site_dao');

const createSite = async site => siteDao.insert(site);

const getSites = async () => siteDao.findAll();

const getSite = async siteId => siteDao.findById(siteId);

const getSitesNearby = async (lat, lng, radius, radiusUnit, onlyExcessCapacity) => {
  const matchingSites = onlyExcessCapacity
    ? await siteDao.findByGeoWithExcessCapacity(
      lat,
      lng,
      radius,
      radiusUnit,
    )
    : await siteDao.findByGeo(
      lat,
      lng,
      radius,
      radiusUnit,
    );

  return matchingSites;
};

module.exports = {
  createSite,
  getSites,
  getSite,
  getSitesNearby,
};
