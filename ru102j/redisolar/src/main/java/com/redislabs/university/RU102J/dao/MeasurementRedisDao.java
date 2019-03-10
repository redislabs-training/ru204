package com.redislabs.university.RU102J.dao;

import redis.clients.jedis.JedisPool;

public class MeasurementRedisDao {
    private final JedisPool jedisPool;

    public MeasurementRedisDao(JedisPool jedisPool) {
        this.jedisPool = jedisPool;
    }
}
