const siteDao = require('../daos/site_dao');

const getSites = async () => siteDao.findAll();

const getSite = async siteId => siteDao.findById(siteId);

const getSitesNearby = async (lat, lng, radius, radiusUnit, onlyExcessCapacity) => {
  console.log(`lat: ${lat}`);
  console.log(`lng: ${lng}`);
  console.log(`radius: ${radius}`);
  console.log(`radiusUnit: ${radiusUnit}`);
  console.log(`onlyExcessCapacity: ${onlyExcessCapacity}`);

  return siteDao.findByGeo(
    lat,
    lng,
    radius,
    radiusUnit,
    onlyExcessCapacity,
  );
};

module.exports = {
  getSites,
  getSite,
  getSitesNearby,
};
