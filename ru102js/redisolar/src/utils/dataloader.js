const config = require('better-config');
const path = require('path');
const redis = require('../daos/impl/redis/redis_client');

config.set('../../config.json');

const client = redis.getClient();

const flushDB = () => {
  // TODO flush DB...
};

const loadData = (filename, flushDb) => {
  /* eslint-disable global-require, import/no-dynamic-require */
  const sampleData = require(filename);

  if (sampleData && flushDb) {
    console.log('Flushing database before loading sample data.');
    flushDB();
  }

  for (const site of sampleData) {
   // console.log(site);
  }

  console.log(`Loaded ${sampleData.length} sites.`);
};

if (process.argv.length !== 4 && process.argv.length !== 5) {
  console.error('Usage: npm run load <path_to_json_data_file> [flushdb]');
} else {
  const filename = process.argv[3];
  let flushDb = false;

  if (process.argv.length === 5 && process.argv[4] === 'flushdb') {
    flushDb = true;
  }

  try {
    loadData(path.resolve(__dirname, '../../', filename), flushDb);
  } catch (e) {
    console.error(`Error loading ${filename}:`);
    console.error(e);
  }

  client.quit();
}
