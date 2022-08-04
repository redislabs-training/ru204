// See https://aka.ms/new-console-template for more information

using System.Text.Json;
using Redis.OM;
using Redis.OM.Example;

var url = Environment.GetEnvironmentVariable("REDIS_OM_URL") ?? "redis://localhost:6379";
var provider = new RedisConnectionProvider(url);
var books = provider.RedisCollection<Book>();

var book = new Book
{
    Author = "Redis Staff",
    Id="999",
    Description = "This is a book all about Redis.",
    Genres = new List<string>(){"redis","tech","computers"},
    Inventory = new List<InventoryItem>()
    {
        new InventoryItem()
        {
            Status = "on_loan",
            StockId = "999_1"
        },
        new InventoryItem()
        {
            Status = "maintenance",
            StockId = "999_2"
        }
    },
    Metrics = new Metrics()
    {
        RatingVotes = 4000,
        Score = 4.5
    },
    Pages = 1000,
    Title = "Redis for Beginners",
    Url = "https://university.redis.com/courses/ru204/",
    YearPublished = 2022
};

Console.WriteLine($"book ULID: {book.Pk}");

await books.InsertAsync(book);

Console.WriteLine("Saved book in Redis.");

var aBook = books.FindById(book.Pk.ToString());

Console.WriteLine("Retrieved from Redis:");
Console.WriteLine(JsonSerializer.Serialize(aBook));

aBook!.Author = "Redis University";
books.Update(aBook);
Console.WriteLine("Updated author and saved to Redis:");
Console.WriteLine(JsonSerializer.Serialize(books.FindById(aBook.Pk.ToString())));