const router = require('express').Router();
const { param } = require('express-validator');
const apiErrorReporter = require('../util/apierrorreporter');
const controller = require('../controllers/metrics_controller.js');

router.get(
  '/metrics/:siteId',
  [
    param('siteId').isInt(),
    apiErrorReporter,
  ],
  controller.getMetricsForSite,
);

module.exports = router;
