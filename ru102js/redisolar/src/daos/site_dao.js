const daoLoader = require('./daoloader');

const impl = daoLoader.loadDao('site');

const insert = async site => impl.insert(site);

const findById = async id => impl.findById(id);

const findAll = async () => impl.findAll();

const findByGeo = async (lat, lng, radius, radiusUnit, onlyExcessCapacity) => impl.findByGeo(
  lat,
  lng,
  radius,
  radiusUnit,
  onlyExcessCapacity,
);

module.exports = {
  insert,
  findById,
  findAll,
  findByGeo,
};
