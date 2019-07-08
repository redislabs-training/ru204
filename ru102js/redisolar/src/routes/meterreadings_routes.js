const router = require('express').Router();
const { body, param, query } = require('express-validator');
const apiErrorReporter = require('../utils/apierrorreporter');
const controller = require('../controllers/meterreadings_controller');

const getLimit = (n) => {
  if (Number.isNaN(n)) {
    return 100;
  }

  return (n > 1000 ? 1000 : n);
};

router.post(
  '/meterreadings',
  [
    body().isArray(),
    body('*.siteId').isInt(),
    body('*.dateTime').isInt({ min: 0 }),
    body('*.whUsed').isFloat({ min: 0 }),
    body('*.whGenerated').isFloat({ min: 0 }),
    body('*.tempC').isFloat(),
    apiErrorReporter,
  ],
  async (req, res, next) => {
    try {
      await controller.createMeterReadings(req.body);
      return res.status(201).send('OK');
    } catch (err) {
      return next(err);
    }
  }
);

router.get(
  '/meterreadings',
  [
    query('n').optional().isInt({ min: 1 }).toInt(),
    apiErrorReporter,
  ],
  async (req, res, next) => {
    try {
      const readings = await controller.getMeterReadings(getLimit(req.query.n));
      return res.status(200).json(readings);
    } catch (err) {
      return next(err);
    }  
  },
);

router.get(
  '/meterreadings/:siteId',
  [
    param('siteId').isInt().toInt(),
    query('n').optional().isInt({ min: 1 }).toInt(),
    apiErrorReporter,
  ],
  async (req, res, next) => {
    try {
      const readings = await controller.getMeterReadingsForSite(req.params.siteId, getLimit(req.query.n));
  
      return res.status(200).json(readings);
    } catch (err) {
      return next(err);
    }
  },
);

module.exports = router;
