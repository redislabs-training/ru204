package com.redislabs.university.RU102J.dao;

import com.redislabs.university.RU102J.api.Measurement;
import com.redislabs.university.RU102J.api.MeterReading;
import com.redislabs.university.RU102J.api.ValueUnit;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;

import java.util.List;

public class MetricDaoRedisStreamImpl implements MetricDao {

    private final JedisPool jedisPool;

    public MetricDaoRedisStreamImpl(JedisPool jedisPool) {
        this.jedisPool = jedisPool;
    }

    @Override
    public void insert(MeterReading reading) {
        try (Jedis jedis = jedisPool.getResource()) {
        }
    }

    @Override
    public List<Measurement> getRecent(Long siteId, ValueUnit unit, Integer limit) {
        return null;
    }
}
