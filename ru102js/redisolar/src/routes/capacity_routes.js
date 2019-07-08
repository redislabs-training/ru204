const router = require('express').Router();
const { query } = require('express-validator');
const apiErrorReporter = require('../utils/apierrorreporter');
const controller = require('../controllers/capacity_controller');

const getLimit = n => (Number.isNaN(n) ? 10 : n);

router.get(
  '/capacity',
  [
    query('limit').optional().isInt({ min: 1 }).toInt(),
    apiErrorReporter,
  ],
  async (req, res, next) => {
    try {
      const capacityReport = await controller.getCapacityReport(getLimit(req.query.limit));

      return res.status(200).json(capacityReport);
    } catch (err) {
      return next(err);
    }
  },
);

module.exports = router;
