package com.redislabs.university.RU102J.dao;

import redis.clients.jedis.JedisPool;
import redis.clients.jedis.JedisPoolConfig;

public class MeterReadingRedisImpl implements MeterReading {

    private final JedisPool jedisPool;

    public MeterReadingRedisImpl(JedisPool jedisPool) {
        this.jedisPool = jedisPool;
    }

    /**
     * Inserting a meter reading means doing the following:
     *   - Adding a new Metric
     *   - Updating the Site with the latest reading data
     *   - Updating the Capacity index
     * @param reading
     */
    @Override
    public void insert(MeterReading reading) {
    }
}
