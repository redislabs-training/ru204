// See https://aka.ms/new-console-template for more information

using StackExchange.Redis;

const string BOOK_KEY = "ru204:book:3";

var bookJson = await File.ReadAllTextAsync("data/Book.json");


var connectionString = Environment.GetEnvironmentVariable("REDIS_CONNECTION_STRING") ?? "localhost";

Console.WriteLine($"Connecting to redis at {connectionString}");
var muxer = ConnectionMultiplexer.Connect(connectionString);
var db = muxer.GetDatabase();

// Delete any previous data at our book's key
await db.KeyDeleteAsync(BOOK_KEY);

// Store the book in Redis at the key ru204:Book:3
// Response Should be "OK"
var response = await db.ExecuteAsync("JSON.SET", BOOK_KEY, "$", bookJson);
Console.WriteLine($"Book stored: {response}");

// let's get the the author and score for this book
// Response will be:  {"$.metrics.score":[2.3],"$.author":["Redis University"]}
response = await db.ExecuteAsync("JSON.GET", BOOK_KEY, "$.author", "$.metrics.score");
Console.WriteLine($"Author and Score: {response}");

// add one to the number of rating_votes
// Response will be [13]
response = await db.ExecuteAsync("JSON.NUMINCRBY", BOOK_KEY, $"$.metrics.rating_votes", 1);
Console.WriteLine($"rating_votes incremented to {response}");

// add another copy of the book to the inventory
// response will be: 3 (new size of the inventory array)
response = await db.ExecuteAsync("JSON.ARRAPPEND", BOOK_KEY, "$.inventory", "{\"status\":\"available\",\"stock_id\":\"3_3\"}");
var inventoryCount = ((RedisResult[]?) response)?.FirstOrDefault();
Console.WriteLine($"There are now {inventoryCount} copies of the book in the inventory.");