using Redis.OM.Modeling;

namespace redis_om_search_example;

public class Metrics
{
    [Indexed]
    public long rating_votes { get; set; }

    [Indexed]
    public float score { get; set; }
}