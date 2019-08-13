import org.junit.Before;
import org.junit.Test;
import redis.clients.jedis.*;

import java.time.Instant;
import java.util.*;

public class FinalExam {

    private JedisPool jedisPool;
    private Jedis jedis;

    @Before
    public void setUp() {
        this.jedisPool = new JedisPool(new JedisPoolConfig(), "localhost", 6379);
        this.jedis = jedisPool.getResource();
    }

    @Test
    public void testGet() {
        try (Jedis jedis = jedisPool.getResource()) {
            String result = jedis.get("nonexistent");
            System.out.println(result);
        }
    }

    @Test
    public void sendCommands1() {
        Transaction t = jedis.multi();
        t.lpush("foo", "A");
        t.incr("bar");
        t.exec();
    }

    @Test
    public void sendCommands2() {
        Pipeline p = jedis.pipelined();
        p.lpush("foo", "A");
        p.incr("bar");
        p.sync();
    }

    public Long testStream(String userId ,Map<String, String> action) {
        Long result = 0L;
        String userStream = "user-" + userId;
        Pipeline p = jedis.pipelined();
        p.xadd("global", StreamEntryID.NEW_ENTRY, action);
        p.xadd(userStream, StreamEntryID.NEW_ENTRY, action);
        Response<Long> length = p.xlen(userStream);
        result = length.get();

        return result;
    }

    @Test
    public void updateTemperature(Double currentTemperature) {
        String maxTemperature = jedis.hget("metrics", "maxTemp");
        if (currentTemperature > Double.valueOf(maxTemperature)) {
            jedis.hset("metrics", "maxTemp", String.valueOf(currentTemperature));
        }
    }

    @Test
    public void hit(String userId, Integer maxHits) throws RateLimitExceededException {
        try (Jedis jedis = jedisPool.getResource()) {
            String key = "limiter-" + Instant.now().getEpochSecond() + "-" + userId;
            Pipeline p = jedis.pipelined();
            p.lpush(key, Instant.now().toString());
            p.expire(key, 1);
            Response<List<String>> responses = p.lrange(key, 0, -1);
            p.sync();
            if (responses.get().size() > maxHits) {
                throw new RateLimitExceededException();
            }
        }
    }

    @Test
    public void testZSet() {
        jedis.del("z");
        jedis.zadd("z", 0, "A");
        jedis.zadd("z", 1, "B");
        jedis.zadd("z", 2, "C");
        jedis.zadd("z", 3, "A");

        Set<String> results = jedis.zrange("z", 0, -1);
        System.out.println(results);

    }

    public Set<String> getMembers(String key) {
        Set<String> members = new HashSet<>();
        ScanResult<String> scanResult;
        ScanParams scanParams = new ScanParams().count(10).match("*");
        String cursor = ScanParams.SCAN_POINTER_START;
        do {
            scanResult = jedis.sscan(key, cursor, scanParams);
            members.addAll(scanResult.getResult());
        } while (!scanResult.isCompleteIteration());

        return members;
    }

    @Test
    public void testCounter() {
        for (int i=0; i<10000; i++) {
            Jedis jedis = jedisPool.getResource();
            jedis.incr("counter");
            jedis.close();
        }
    }
}
