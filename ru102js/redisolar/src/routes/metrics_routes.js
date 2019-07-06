const router = require('express').Router();
const { param, query } = require('express-validator');
const apiErrorReporter = require('../utils/apierrorreporter');
const controller = require('../controllers/metrics_controller.js');

router.get(
  '/metrics/:siteId',
  [
    param('siteId').isInt().toInt(),
    query('n').optional().isInt({ min: 1 }).toInt(),
    apiErrorReporter,
  ],
  controller.getMetricsForSite,
);

module.exports = router;
