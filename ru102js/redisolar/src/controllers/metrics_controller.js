const moment = require('moment');
const metricDao = require('../daos/metric_dao');

const getMetricsForSite = async (siteId, limit) => {
  const currentTimestamp = moment().utc().unix();

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
