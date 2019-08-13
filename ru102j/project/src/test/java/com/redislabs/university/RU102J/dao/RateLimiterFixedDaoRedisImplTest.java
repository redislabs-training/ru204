package com.redislabs.university.RU102J.dao;

import com.redislabs.university.RU102J.HostPort;
import com.redislabs.university.RU102J.TestKeyManager;
import org.junit.*;
import org.junit.rules.ExpectedException;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;

import javax.validation.constraints.Min;

import static org.hamcrest.Matchers.is;
import static org.junit.Assert.*;

public class RateLimiterFixedDaoRedisImplTest {

    private static JedisPool jedisPool;
    private static Jedis jedis;
    private static TestKeyManager keyManager;

    @Rule
    public ExpectedException thrown = ExpectedException.none();

    @BeforeClass
    public static void setUp() throws Exception {
        jedisPool = new JedisPool(HostPort.getRedisHost(), HostPort.getRedisPort());
        jedis = new Jedis(HostPort.getRedisHost(), HostPort.getRedisPort());
        keyManager = new TestKeyManager("test");
    }

    @AfterClass
    public static void tearDown() {
        jedisPool.destroy();
        jedis.close();
    }

    @After
    public void flush() {
        keyManager.deleteKeys(jedis);
    }

    @Test
    public void hit() {
        int exceptionCount = 0;
        RateLimiter limiter = new RateLimiterFixedDaoRedisImpl(jedisPool,
                MinuteInterval.ONE, 10);
        for (int i=0; i<10; i++) {
            try {
                limiter.hit("foo");
            } catch (RateLimitExceededException e) {
                exceptionCount += 1;
            }
        }

        assertThat(exceptionCount, is(0));
    }

    @Test
    public void getMinuteOfDayBlock() {
    }
}