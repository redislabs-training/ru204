package com.redislabs.university.RU102J.dao;

import com.redislabs.university.RU102J.api.Measurement;
import com.redislabs.university.RU102J.api.ValueUnit;
import redis.clients.jedis.JedisPool;

public class LeaderDaoRedisImpl implements LeaderDao {

    private final JedisPool jedisPool;

    public LeaderDaoRedisImpl(JedisPool jedisPool) {
        this.jedisPool = jedisPool;
    }

    @Override
    public void insert(Measurement measurement) {
    }

    public void getTopN(ValueUnit unit, Integer count) {
    }
}
