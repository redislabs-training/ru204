const config = require('better-config');

/* eslint-disable import/no-dynamic-require global-require */
const loadDao = daoName => require(`./impl/${config.get('application.dataStore')}/${daoName}_dao_${config.get('application.dataStore')}_impl`);
/* eslint-enable */

module.exports = {
  loadDao,
};
