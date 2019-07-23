import org.junit.Before;
import org.junit.Test;
import redis.clients.jedis.*;

import java.util.*;

public class Homework3Test {

    private Jedis jedis;

    @Before
    public void setUp() {
        this.jedis = new Jedis();
    }

    @Test
    public void testLeaderboard() {
        jedis.zremrangeByRank("sites:capacity", 100, -1);
        jedis.zremrangeByScore("sites:capacity", 100, -1);
        jedis.zremrangeByRank("sites:capacity", 0, 99);
        jedis.zremrangeByScore("sites:capacity", 0, 99);
    }

    @Test
    public void testGeoWithCriteria() {
        List<GeoRadiusResponse> radiusResponses =
                jedis.georadius("sites:geo", -122.0, 37.0, 1.0, GeoUnit.KM);
        Pipeline p = jedis.pipelined();
        Map<String, Response<Boolean>> sitesChargers = new HashMap<>();
        for (GeoRadiusResponse response : radiusResponses) {
            String member = response.getMemberByString();
            sitesChargers.put(member, p.sismember("sites:charger", member));
        }
        p.sync();
        //...
    }

    public List<String> getRecentIDs(String key, int limit) {
        List<String> ids = new ArrayList<>(limit);
        List<StreamEntry> entries = jedis.xrevrange(key, null,
                null, limit);
        for (StreamEntry entry : entries) {
            ids.add(entry.getID().toString());
        }
        return ids;
    }
}
