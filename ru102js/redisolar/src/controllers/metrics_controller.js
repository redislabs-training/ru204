const metricDao = require('../daos/metric_dao');

const getMetricsForSite = (req, res) => {
  const { siteId } = req.params;

  return res.status(200).json(metricDao.getRecent(siteId));
};

module.exports = {
  getMetricsForSite,
};
