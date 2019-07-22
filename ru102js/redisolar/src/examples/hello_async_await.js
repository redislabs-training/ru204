const redis = require('redis');
const bluebird = require('bluebird');

bluebird.promisifyAll(redis);

const runApplication = async () => {
  const client = redis.createClient({
    host: 'localhost',
    port: 6379,
  });

  const reply = await client.setAsync('hello', 'world');
  console.log(reply); // OK

  const keyValue = await client.getAsync('hello');
  console.log(keyValue); // world

  client.quit();
};

try {
  runApplication();
} catch (e) {
  console.log(e);
}
