const logger = require('../utils/logger');
const capacityDao = require('../daos/capacity_dao');

const getCapacityReport = async (req, res, next) => {
  let capacityReport;

  try {
    const { limit } = req.query;
    logger.debug(`Limit = ${limit}`);
    capacityReport = await capacityDao.getReport(limit);
  } catch (err) {
    return next(err);
  }

  return res.status(200).json(capacityReport);
};

module.exports = {
  getCapacityReport,
};
