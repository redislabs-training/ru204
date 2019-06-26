const logger = require('../utils/logger');
const capacityDao = require('../daos/capacity_dao');

const getCapacityReport = (req, res) => {
  const limit = req.query.limit;

  logger.debug(`Limit = ${limit}`);

  return res.status(200).json(capacityDao.getReport(limit));
};

module.exports = {
  getCapacityReport,
};
