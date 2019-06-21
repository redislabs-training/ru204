const router = require('express').Router();
const { body } = require('express-validator');
const apiErrorReporter = require('../util/apierrorreporter');
const controller = require('../controllers/meterreadings_controller');

router.post(
  '/meterreadings',
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

router.get('/meterreadings', controller.getMeterReadings);

module.exports = router;
