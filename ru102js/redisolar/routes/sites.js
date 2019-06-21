const router = require('express').Router();
const { param } = require('express-validator');
const apiErrorReporter = require('../util/apierrorreporter');
const controller = require('../controllers/sites_controller.js');

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
