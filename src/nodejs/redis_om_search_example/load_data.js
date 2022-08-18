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
  console.log(`${FILE_PATH}${pathSeparator}${fileName}`);
  const bookData = JSON.parse(await readFile(`${FILE_PATH}${pathSeparator}${fileName}`));
  console.log(bookData);
}

await client.close();