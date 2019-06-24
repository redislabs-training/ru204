const router = require('express').Router();
const { param, query } = require('express-validator');
const apiErrorReporter = require('../util/apierrorreporter');
const controller = require('../controllers/sites_controller.js');

const geoParamsValidator = (value, { req }) => {
  const {
    lat, lng, radius, radiusUnit,
  } = req.query;

  if (lat && lng && radius && radiusUnit) {
    return true;
  }

  throw new Error('When using geo lookup, params lat, lng, radius, radiusUnit are required.');
};


router.get(
  '/sites',
  [
    /* eslint-disable newline-per-chained-call */
    query('lat').optional().custom(geoParamsValidator).isFloat().toFloat(),
    query('lng').optional().custom(geoParamsValidator).isFloat().toFloat(),
    query('radius').optional().custom(geoParamsValidator).isFloat({ min: 0.1 }).toFloat(),
    query('radiusUnit').optional().custom(geoParamsValidator).isIn(['MI', 'KM']),
    query('onlyExcessCapacity').optional().isBoolean(),
    /* eslint-enable */
    apiErrorReporter,
  ],
  (req, res) => (
    req.query.lat ? controller.getSitesNearby(req, res) : controller.getSites(req, res)
  ),
);

router.get(
  '/sites/:siteId',
  [
    param('siteId').isInt().toInt(),
    apiErrorReporter,
  ],
  controller.getSite,
);


module.exports = router;
