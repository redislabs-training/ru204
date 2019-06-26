const router = require('express').Router();
const { query } = require('express-validator');
const apiErrorReporter = require('../utils/apierrorreporter');
const controller = require('../controllers/capacity_controller');

router.get(
  '/capacity',
  [
    query('limit').optional().isInt({ min: 1 }).toInt(),
    apiErrorReporter,
  ],
  controller.getCapacityReport,
);

module.exports = router;
