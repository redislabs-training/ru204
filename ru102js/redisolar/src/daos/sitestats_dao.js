const daoLoader = require('./daoloader');

const impl = daoLoader.loadDao('sitestats');

const findById = (siteId, timestamp) => impl.findById(siteId, timestamp);

const update = meterReading => impl.update(meterReading);

module.exports = {
  findById,
  update,
};
