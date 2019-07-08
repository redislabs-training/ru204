const config = require('better-config');
const path = require('path');
const redis = require('../daos/impl/redis/redis_client');

config.set('../../config.json');

const client = redis.getClient();
const siteDAO = require('../daos/site_dao');
const dataGenerator = require('./sample_data_generator');

const dataDaysToGenerate = 1;

const flushDB = async () => client.flushdbAsync();

const loadData = async (filename, flushDb) => {
  /* eslint-disable global-require, import/no-dynamic-require */
  const sampleData = require(filename);
  /* eslint-enable */

  if (sampleData && flushDb) {
    console.log('Flushing database before loading sample data.');
    await flushDB();
  }

  for (const site of sampleData) {
    await dataGenerator.generateHistorical(site, 1);
  }

  //await Promise.all(sampleData.map(site => siteDAO.insert(site)));
  // await Promise.all(
  //   sampleData.map(
  //     async site => {
  //       await siteDAO.insert(site);
  //       await dataGenerator.generateHistorical(site, 1);
  //     },
  //   ),
  // );
  //await dataGenerator.generateHistorical(dataDaysToGenerate, client);

  // for (const site of sampleData) {
  //   siteDAO.insert(site);
  //   console.log(site);
  // }

  console.log(`Loaded ${sampleData.length} sites, with ${dataDaysToGenerate} day${dataDaysToGenerate !== 1 ? 's' : ''} of sample data.`);
};

const runDataLoader = async (params) => {
  if (params.length !== 4 && params.length !== 5) {
    console.error('Usage: npm run load <path_to_json_data_file> [flushdb]');
  } else {
    const filename = params[3];
    let flushDb = false;

    if (params.length === 5 && params[4] === 'flushdb') {
      flushDb = true;
    }

    try {
      await loadData(path.resolve(__dirname, '../../', filename), flushDb);
    } catch (e) {
      console.error(`Error loading ${filename}:`);
      console.error(e);
    }

    client.quit();
  }
};

runDataLoader(process.argv);
