package com.redislabs.university.RU102J.dao;

import com.redislabs.university.RU102J.api.Measurement;
import com.redislabs.university.RU102J.api.ValueUnit;
import redis.clients.jedis.JedisPool;

public class CapacityDaoRedisImpl implements CapacityDao {

    private final JedisPool jedisPool;

    public CapacityDaoRedisImpl(JedisPool jedisPool) {
        this.jedisPool = jedisPool;
    }

    @Override
    public void update(Measurement measurement) {
    }
}
