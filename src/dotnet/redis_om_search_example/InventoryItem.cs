using Redis.OM.Modeling;

namespace redis_om_search_example;

public class InventoryItem
{
    [Indexed]
    public string? status { get; set; }

    [Indexed]
    public string? stock_id { get; set; }
}