import { Entity, Schema } from 'redis-om';

class Book extends Entity { };

export const bookSchema = new Schema(Book, {
  author: { type: 'string' },
  id: { type: 'string' },
  description: { type: 'text' },
  genres: { type: 'string[]' },
  pages: { type: 'number' },
  title: { type: 'text' },
  url: { type: 'string' },
  yearPublished: { type: 'number' },
  // Redis OM Node does not yet support embedded objects, 
  // so the metrics object has been flattened to the following
  // two fields, and we have omitted the inventory array of 
  // objects for the same reason.
  ratingVotes: { type: 'number' },
  score: { type: 'number' }
}, {
  prefix: 'ru204:redis-om-node:book'
});