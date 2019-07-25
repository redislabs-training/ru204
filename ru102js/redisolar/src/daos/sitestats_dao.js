const daoLoader = require('./daoloader');

const impl = daoLoader.loadDao('sitestats');

module.exports = {
  findById: async (siteId, timestamp) => impl.findById(siteId, timestamp),

  update: async meterReading => impl.update(meterReading),
};
