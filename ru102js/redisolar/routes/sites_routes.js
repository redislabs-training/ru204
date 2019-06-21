const router = require('express').Router();
const { param } = require('express-validator');
const apiErrorReporter = require('../util/apierrorreporter');
const controller = require('../controllers/sites_controller.js');

// TODO /sites?lat=37.4337786&lng=-122.1833425&radius=10&radiusUnit=MI
// also onlyExcessCapacity true|false
// radiusUnit = MI || KM
// Can respond [] for now.
// Need to make sure we can route this and not confuse with GET /sites
// or do like java and work this out in controller.getSites

router.get('/sites', controller.getSites);

router.get(
  '/sites/:siteId',
  [
    param('siteId').isInt(),
    apiErrorReporter,
  ],
  controller.getSite,
);


module.exports = router;
