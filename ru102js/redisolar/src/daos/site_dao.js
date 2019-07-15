const daoLoader = require('./daoloader');

const impl = daoLoader.loadDao('site');

const insert = async site => impl.insert(site);

const findById = async id => impl.findById(id);

const findAll = async () => impl.findAll();

const findByGeo = async (lat, lng, radius, radiusUnit) => impl.findByGeo(
  lat,
  lng,
  radius,
  radiusUnit,
);

const findByGeoWithExcessCapacity = async (lat, lng, radius, radiusUnit) => (
  impl.findByGeoWithExcessCapacity(
    lat,
    lng,
    radius,
    radiusUnit,
  )
);

module.exports = {
  insert,
  findById,
  findAll,
  findByGeo,
  findByGeoWithExcessCapacity,
};
