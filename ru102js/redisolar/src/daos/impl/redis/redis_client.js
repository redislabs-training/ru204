const redis = require('redis');
const bluebird = require('bluebird');
const config = require('better-config');

// Add extra definitions for RedisTimeSeries commands.
redis.addCommand('ts.add'); // redis.ts_addAsync
redis.addCommand('ts.range'); // redis.ts_rangeAsync

bluebird.promisifyAll(redis);

const client = redis.createClient({
  host: config.get('dataStores.redis.host'),
  port: config.get('dataStores.redis.port'),
});

// TODO add better client error...
client.on('error', error => console.log(error));

const getClient = () => client; // Later this may need to use param eg for separate pubsub client...

module.exports = {
  getClient,
};
