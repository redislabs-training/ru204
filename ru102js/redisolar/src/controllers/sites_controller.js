const siteDao = require('../daos/site_dao');

const getSites = async (req, res, next) => {
  try {
    const sites = await siteDao.findAll();
    return res.status(200).json(sites);
  } catch (err) {
    return next(err);
  }
};

const getSite = async (req, res, next) => {
  try {
    const { siteId } = req.params;

    const site = await siteDao.findById(siteId);
    return (site ? res.status(200).json(site) : res.sendStatus(404));
  } catch (err) {
    return next(err);
  }
};

const getSitesNearby = async (req, res, next) => {
  try {
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

    return res.status(200).json(
      siteDao.findByGeo(
        lat,
        lng,
        radius,
        radiusUnit,
        onlyExcessCapacity,
      ),
    );
  } catch (err) {
    return next(err);
  }
};

module.exports = {
  getSites,
  getSite,
  getSitesNearby,
};
