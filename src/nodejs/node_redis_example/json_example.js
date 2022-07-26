import { createClient } from 'redis';

const BOOK_KEY = 'ru204:book:3';

const BOOK = {
  author: 'Redis University',
  id: 3,
  description: 'This is a fictional book used to demonstrate RedisJSON!',
  editions: [
    'english',
    'french'
  ],
  genres: [
    'education',
    'technology'
  ],
  inventory: [
    {
      status: 'available',
      stock_id: 3_1
    },
    {
      status: 'on_loan',
      stock_id: 3_2
    }
  ],
  metrics: {
    rating_votes: 12,
    score: 2.3
  },
  pages: 1000,
  title: 'Up and Running with RedisJSON',
  url: 'https://university.redis.com/courses/ru204/',
  year_published: 2022
};

// Create a connection to Redis and connect to the server.
const REDIS_URL = process.env.REDIS_URL || 'redis://localhost:6379/';
console.log(`Connecting to Redis at ${REDIS_URL}`);

const r = createClient({
  url: REDIS_URL
});
await r.connect();

// Delete any previous data at our book's key
await r.del(BOOK_KEY);

// Store the book in Redis at key ru204:book:3...
// Response will be: OK
let response = await r.json.set(BOOK_KEY, '$', BOOK);
console.log(`Book stored: ${response}`);

// Let's get the author and score for this book...
// Response will be:
// { '$.author': 'Redis University', '$.metrics.score': 2.3 }
response = await r.json.get(BOOK_KEY, {
  path: [
    '$.author',
    '$.metrics.score'
  ]
});

console.log('Author and score:');
console.log(response);

// Add one to the number of rating_votes:
// Response will be: 13
response = await r.json.numIncrBy(BOOK_KEY, '$.metrics.rating_votes', 1);
console.log(`rating_votes incremented to ${response}`);

// Add another copy of the book to the inventory.
// Response will be: 3 (new size of the inventory array)
response = await r.json.arrAppend(BOOK_KEY, '$.inventory', {
  status: 'available',
  stock_id: '3_3'
});
console.log(`There are now ${response} copies of the book in the inventory.`);

// Disconnect from Redis.
await r.disconnect();