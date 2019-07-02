const redis = require('redis');

const client = redis.createClient({
  host: 'localhost',
  port: 6379,
});

client.set('hello', 'world', (err, reply) => {
  if (err) {
    console.log(err);
    client.quit();
  } else {
    console.log(reply); // OK

    client.get('hello', (getErr, getReply) => {
      if (getErr) {
        console.log(getErr);
      } else {
        console.log(getReply); // world
      }

      client.quit();
    });
  }
});
