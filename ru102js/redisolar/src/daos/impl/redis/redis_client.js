const redis = require('redis');
const bluebird = require('bluebird');
const config = require('better-config');

bluebird.promisifyAll(redis);

const client = redis.createClient({
  host: config.get('dataStores.redis.host'),
  port: config.get('dataStores.redis.port'),
});

// TODO deal with optional authentication???

// TODO add client error...

const getClient = () => client; // Later this may need to use param eg for separate pubsub client...

module.exports = {
  getClient,
};
