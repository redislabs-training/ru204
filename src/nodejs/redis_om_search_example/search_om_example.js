import { Client } from 'redis-om';
import { bookSchema } from './model.js';

const client = new Client();
await client.open(process.env.REDIS_OM_URL || 'redis://localhost:6379');

const bookRepository = client.fetchRepository(bookSchema);

console.log('TODO search examples...');

await client.close();