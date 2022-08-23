import { Client } from 'redis-om';
import { bookSchema } from './model.js';

const client = new Client();
await client.open(process.env.REDIS_OM_URL || 'redis://localhost:6379');

const bookRepository = client.fetchRepository(bookSchema);

function printResults(queryDescription, resultSet) {
  console.log(queryDescription);

  for (const result of resultSet) {
    console.log(`${result.title} by ${result.author} ${result.pages} pages, published ${result.yearPublished}.`);
  }

  console.log('-----');
}

// Search for books written by Stephen King... returns a list of Book objects.
let resultSet = await bookRepository.search()
  .where('author').equals('Stephen King')
  .return.all();

printResults("Stephen King Books", resultSet);

// Search for books with 'Star' in the title that are over 500 pages long, 
// order by length.
resultSet = await bookRepository.search()
  .where('title').matches('Star')
  .and('pages').is.greaterThan(500)
  .sortAscending('pages')
  .return.all();

printResults("Star in title, >500 pages", resultSet);

// Search for books with 'Star' but not 'War' in the title, and which don't 
// have 'space' in the description.
resultSet = await bookRepository.search()
  .where('title').matches('Star')
  .and('title').not.matches('War')
  .and('description').not.matches('space')
  .return.all();

printResults("'Star' and not 'War' in title, no 'space' in description", resultSet);

// Search for books by Robert Heinlein published between 1959 and 1973,
// sort by year of publication descending.
resultSet = await bookRepository.search()
  .where('author').equals('Robert A. Heinlein')
  .and('yearPublished').is.greaterThan(1958)
  .and('yearPublished').is.lessThan(1974)
  .sortDescending('yearPublished')
  .return.all();

printResults("Robert Heinlein books published 1959 to 1973", resultSet);

await client.close();
