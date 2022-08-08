import { Client, Entity, Schema } from 'redis-om';

const client = new Client();
await client.open(process.env.REDIS_OM_URL || 'redis://localhost:6379');

class Book extends Entity {};

const bookSchema = new Schema(Book, {
  author: { type: 'string' },
  id: { type: 'string' }, 
  description: { type: 'string' },
  genres:  { type: 'string[]' },
  pages: { type: 'number' },
  title: { type: 'string' },
  url: { type: 'string' },
  yearPublished:  { type: 'number' },
  // Redis OM Node does not yet support embedded objects, 
  // so the metrics object has been flattened to the following
  // two fields, and we have omitted the inventory array of 
  // objects for the same reason.
  ratingVotes: { type: 'number' },
  score: { type: 'number' }
}, {
  prefix: 'ru204:redis-om-node:book'
});

const bookRepository = client.fetchRepository(bookSchema);

const newBook = bookRepository.createEntity({
  author: 'Redis Staff',
  id: '999',
  description: 'This is a book all about Redis.',
  genres: [ 'redis', 'tech', 'computers' ],
  pages: 1000,
  title: 'Redis for Beginners',
  url: 'https://university.redis.com/courses/ru204/',
  yearPublished: 2022,
  ratingVotes: 4000,
  score: 4.5
});

// Get the locally generated ULID for this book.
console.log(`newBook ULID: ${newBook.entityId}`);

// Save the book to Redis.
await bookRepository.save(newBook);
console.log('Saved book in Redis.');

// Retrieve the book from Redis.
const aBook = await bookRepository.fetch(newBook.entityId);
console.log('Retrieved from Redis:');
console.log(aBook.toJSON());

// Update the author field and save it.
aBook.author = 'Redis University';
await bookRepository.save(aBook);
console.log('Updated author and saved to Redis:');
const updatedBook = await bookRepository.fetch(aBook.entityId);
console.log(updatedBook.toJSON());

await client.close();
