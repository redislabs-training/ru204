const router = require('express').Router();
const { body } = require('express-validator');
const apiErrorReporter = require('../util/apierrorreporter');
const controller = require('../controllers/meterreading_controller.js');

router.post(
  '/meterreading',
  [
    body().isArray(),
    body('*.siteId').isInt(),
    body('*.dateTime').isISO8601(),
    body('*.whUsed').isFloat({ min: 0 }),
    body('*.whGenerated').isFloat({ min: 0 }),
    body('*.tempC').isFloat(),
    apiErrorReporter,
  ],
  controller.createMeterReading,
);

module.exports = router;
