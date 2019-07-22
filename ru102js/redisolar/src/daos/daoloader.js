const config = require('better-config');

/* eslint-disable import/no-dynamic-require, global-require */
const loadDao = (daoName) => {
  const currentDatabase = config.get('application.dataStore');
  return require(`./impl/${currentDatabase}/${daoName}_dao_${currentDatabase}_impl`);
};
/* eslint-enable */

module.exports = {
  loadDao,
};
