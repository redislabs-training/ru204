const metricDao = require('../daos/metric_dao');

const getMetricsForSite = async (siteId, limit) => {
  const currentTimestamp = new Date().getTime();

  const metrics = await Promise.all([
    metricDao.getRecent(siteId, 'generated unit', currentTimestamp, limit),
    metricDao.getRecent(siteId, 'used unit', currentTimestamp, limit),
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
