const siteDao = require('../daos/site_dao');

const getSites = (req, res) => res.status(200).json(siteDao.findAll());

const getSite = (req, res) => {
  const { siteId } = req.params;

  return res.status(200).json(siteDao.findById(siteId));
};

const getSitesNearby = (req, res) => {
  const { siteId } = req.params;
  const {
    lat, lng, radius, radiusUnit, onlyExcessCapacity,
  } = req.query;

  console.log(`siteId: ${siteId}`);
  console.log(`lat: ${lat}`);
  console.log(`lng: ${lng}`);
  console.log(`radius: ${radius}`);
  console.log(`radiusUnit: ${radiusUnit}`);
  console.log(`onlyExcessCapacity: ${onlyExcessCapacity}`);

  return res.status(200).json(siteDao.findByGeo(lat, lng, radius, radiusUnit, onlyExcessCapacity));
}

module.exports = {
  getSites,
  getSite,
  getSitesNearby,
};
