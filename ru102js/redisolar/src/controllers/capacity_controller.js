const capacityDao = require('../daos/capacity_dao');

const getCapacityReport = async limit => capacityDao.getReport(limit);

module.exports = {
  getCapacityReport,
};
