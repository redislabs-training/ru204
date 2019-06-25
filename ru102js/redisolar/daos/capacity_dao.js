const daoLoader = require('./daoloader');

const impl = daoLoader.loadDao('capacity');

const update = meterReading => impl.update(meterReading);

module.exports = {
  update,
};
