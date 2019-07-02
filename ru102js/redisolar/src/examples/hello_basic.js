const redis = require('redis');

const client = redis.createClient({
  host: 'localhost',
  port: 6379,
});

client.set('hello', 'world', (err, reply) => {
  console.log(reply); // OK

  client.get('hello', (getErr, getReply) => {
    console.log(getReply); // world

    client.quit();
  });
});
