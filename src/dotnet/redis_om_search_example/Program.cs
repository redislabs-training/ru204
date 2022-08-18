// See https://aka.ms/new-console-template for more information

using System.Text.Json;
using redis_om_search_example;
using Redis.OM;

Console.WriteLine("Hello, World!");
var provider = new RedisConnectionProvider("redis://localhost:6379");
var indexCreated = provider.Connection.CreateIndex(typeof(Book));
var books = provider.RedisCollection<Book>();

if (indexCreated)
{
    var insertionTasks = new List<Task>();
    foreach (var file in Directory.GetFiles("../../../data/books"))
    {
        var book = JsonSerializer.Deserialize<Book>(await File.ReadAllTextAsync(file));
        if (book == null)
        {
            continue;
        }

        insertionTasks.Add(books.InsertAsync(book));
    }

    await Task.WhenAll(insertionTasks);
}


void PrintResults(string queryDescription, IEnumerable<Book> results)
{
    Console.WriteLine($"==={queryDescription}===");
    foreach (var result in results)
    {
        Console.WriteLine(($"{result.title} by {result.author} {result.pages} pages, published {result.year_published}."));
    }
}

// Search for books written by Stephen King... returns a list of Book objects.
var resultSet = books.Where(b => b.author == "Stephen King");
PrintResults("Books by Stephen King", resultSet);

//Search for books with 'Star' in the title that are over 500 pages long, order by length.
resultSet = books.Where(b => b.title.Contains("Star") && b.pages > 500);
PrintResults("Star in title, >500 pages", resultSet);

// Search for books with 'Star' but not 'War' in the title, and
// which don't have 'space' in the description.
resultSet = books.Where(b => b.title.Contains("Star") && b.title != "War" && b.description != "space");
PrintResults("'Star' and not 'War' in title, no 'space' in description", resultSet);

// Search for books by Robert Heinlein published between 1959 and 1973,
// sort by year of publication descending.
resultSet = books.Where(b => b.author == "Robert A. Heinlein" && b.year_published > 1958 && b.year_published < 1974);
PrintResults("Robert Heinlein books published x to y", resultSet);