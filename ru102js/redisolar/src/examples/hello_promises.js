const redis = require('redis');
const { promisify } = require('util');

const client = redis.createClient({
  host: 'localhost',
  port: 6379,
});

const setAsync = promisify(client.set).bind(client);
const getAsync = promisify(client.get).bind(client);

setAsync('hello', 'world')
  .then(res => console.log(res)) // OK
  .then(() => getAsync('hello'))
  .then(res => console.log(res)) // world
  .then(() => client.quit());
