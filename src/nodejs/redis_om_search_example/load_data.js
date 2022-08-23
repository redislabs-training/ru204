import { Client } from 'redis-om';
import { bookSchema } from './model.js';
import { readdir, readFile } from 'node:fs/promises';
import { sep as pathSeparator } from 'node:path';

const FILE_PATH = '../../../data/books';

const client = new Client();
await client.open(process.env.REDIS_OM_URL || 'redis://localhost:6379');

const bookRepository = client.fetchRepository(bookSchema);

const fileNames = await readdir(FILE_PATH);
for (const fileName of fileNames) {
  const bookData = JSON.parse(await readFile(`${FILE_PATH}${pathSeparator}${fileName}`));
  const newBook = bookRepository.createEntity({
    author: bookData.author,
    id: bookData.id,
    description: bookData.description,
    genres: bookData.genres,
    pages: bookData.pages,
    title: bookData.title,
    url: bookData.url,
    yearPublished: bookData.year_published,
    ratingVotes: bookData.metrics.rating_votes,
    score: bookData.metrics.score
  });

  await bookRepository.save(newBook);
  console.log(`Stored book ${newBook.title}.`);
}

await bookRepository.createIndex();
console.log('Created search index.');

await client.close();