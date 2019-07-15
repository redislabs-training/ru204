const metricDao = require('../daos/metric_dao');
const timeUtils = require('../utils/time_utils');

const getMetricsForSite = async (siteId, limit) => {
  const currentTimestamp = timeUtils.getCurrentTimestamp();

  const metrics = await Promise.all([
    metricDao.getRecent(siteId, 'whGenerated', currentTimestamp, limit),
    metricDao.getRecent(siteId, 'whUsed', currentTimestamp, limit),
  ]);

  return ([{
    measurements: metrics[0],
    name: 'Watt-Hours Generated',
  }, {
    measurements: metrics[1],
    name: 'Watt-Hours Used',
  }]);
};

module.exports = {
  getMetricsForSite,
};
