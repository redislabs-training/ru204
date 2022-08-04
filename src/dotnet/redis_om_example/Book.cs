using Redis.OM.Modeling;

namespace Redis.OM.Example;

[Document(StorageType = StorageType.Json, Prefixes = new []{"ru204:redis-om-dotnet:Book"})]
public class Book
{
    [RedisIdField]
    public Ulid Pk { get; set; }
    public string? Id { get; set; }
    public string? Author { get; set; }
    public string? Description { get; set; }
    public List<string>? Genres { get; set; }
    public List<InventoryItem>? Inventory { get; set; }
    public Metrics? Metrics { get; set; }
    public uint Pages { get; set; }
    public string? Title { get; set; }
    public string? Url { get; set; }
    public uint YearPublished { get; set; }
}