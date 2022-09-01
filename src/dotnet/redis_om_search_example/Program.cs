using System.Text.Json;
using redis_om_search_example;
using Redis.OM;

if (args.Length != 1 || (args[0] != "load" && args[0] != "search"))
{
    Console.WriteLine("Usage: dotnet run load|search");
    System.Environment.Exit(1);
}

var action = args[0];
var uri = Environment.GetEnvironmentVariable("REDIS_OM_URL") ?? "redis://localhost:6379";

var provider = new RedisConnectionProvider(uri);
var books = provider.RedisCollection<Book>();

if (action == "load")
{
    var indexCreated = provider.Connection.CreateIndex(typeof(Book));

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
            Console.WriteLine($"Stored book {book.title}");
        }

        await Task.WhenAll(insertionTasks);
    } else {
        Console.WriteLine("Nothing to do - data was already loaded.");
    }

    System.Environment.Exit(0);
}

// Search action...

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
resultSet = books.Where(b => b.title.Contains("Star") && b.pages > 500).OrderBy(b => b.pages);
PrintResults("Star in title, >500 pages", resultSet);

// Search for books with 'Star' but not 'War' in the title, and
// which don't have 'space' in the description.
resultSet = books.Where(b => b.title.Contains("Star") && b.title != "War" && b.description != "space");
PrintResults("'Star' and not 'War' in title, no 'space' in description", resultSet);

// Search for books by Robert Heinlein published between 1959 and 1973,
// sort by year of publication descending.
resultSet = books.Where(b => b.author == "Robert A. Heinlein" && b.year_published > 1958 && b.year_published < 1974).OrderByDescending(b => b.year_published);
PrintResults("Robert Heinlein books published 1959 to 1973", resultSet);
