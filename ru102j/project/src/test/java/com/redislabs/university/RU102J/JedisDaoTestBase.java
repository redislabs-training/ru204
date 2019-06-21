package com.redislabs.university.RU102J;

import org.junit.AfterClass;
import org.junit.BeforeClass;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;


public class JedisDaoTestBase {

    protected static JedisPool jedisPool;
    protected static Jedis jedis;
    protected static TestKeyManager keyManager;

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

}
