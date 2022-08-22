using Redis.OM.Modeling;

namespace redis_om_search_example;

[Document(StorageType = StorageType.Json, Prefixes = new []{"book"})]
public class Book
{
    [Indexed]
    public string author { get; set; }

    [Indexed]
    public string id { get; set; }

    [Searchable]
    public string description { get; set; }

    [Indexed]
    public List<string> genres { get; set; }

    [Indexed(JsonPath = "$.status")]
    [Indexed(JsonPath = "$.stock_id")]
    public List<InventoryItem> items { get; set; }

    [Indexed(CascadeDepth = 1)]
    public Metrics metrics { get; set; }

    [Indexed]
    public ulong pages { get; set; }

    [Searchable]
    public string title { get; set; }

    [Indexed]
    public ulong year_published { get; set; }
}