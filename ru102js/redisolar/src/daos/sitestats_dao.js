const daoLoader = require('./daoloader');

const impl = daoLoader.loadDao('sitestats');

const findById = async (siteId, timestamp) => impl.findById(siteId, timestamp);

const update = async meterReading => impl.update(meterReading);

module.exports = {
  findById,
  update,
};
