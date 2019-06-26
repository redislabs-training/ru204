const daoLoader = require('./daoloader');

const impl = daoLoader.loadDao('site');

const insert = site => impl.insert(site);

const findById = id => impl.findById(id);

const findAll = () => impl.findAll();

const findByGeo = (lat, lng, radius, radiusUnit, onlyExcessCapacity) => 
  impl.findByGeo(lat, lng, radius, radiusUnit, onlyExcessCapacity);

module.exports = {
  insert,
  findById,
  findAll,
  findByGeo,
};
