import org.junit.Before;
import org.junit.Test;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.Pipeline;
import redis.clients.jedis.Response;

import java.time.ZonedDateTime;
import java.util.ArrayList;
import java.util.List;

public class Homework2Test {

    private Jedis jedis;

    @Before
    public void setUp() {
        this.jedis = new Jedis();
    }

    private List<Long> getCounts(Integer num) {
        List<Long> results = new ArrayList<>(num);
        for (int i=0; i<num; i++) {
            String key = String.valueOf(i);
            if (jedis.exists(key)) {
                Long c = jedis.zcount(key, "-inf", "+inf");
                results.add(c);
                jedis.expire(key, 1000);
            }
        }

        return results;
    }

    private void insert(Integer minuteOfDay, String measurement) {
        jedis.zadd("metrics", minuteOfDay, measurement);
    }

    @Test
    public void compare() {
        Pipeline p = jedis.pipelined();

        Response<Long> length = p.zcard("set");
        if (length.get() < 1000) {
            String element = "foo" + String.valueOf(Math.random());
            p.zadd("set", Math.random(), element);
        }

        p.sync();
    }

    @Test
    public void zSets(ZonedDateTime day, Integer value) {

    }
}
