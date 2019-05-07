package com.redislabs.university.RU102J.dao;

import com.redislabs.university.RU102J.api.MeterReading;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.StreamEntry;
import redis.clients.jedis.StreamEntryID;

import java.util.List;
import java.util.stream.Collectors;

public class FeedDaoRedisImpl implements FeedDao {

    private final JedisPool jedisPool;
    private final long maxFeedLength = 10000;

    public FeedDaoRedisImpl(JedisPool jedisPool) {
        this.jedisPool = jedisPool;
    }

    @Override
    public void insert(MeterReading meterReading) {
        try(Jedis jedis = jedisPool.getResource()) {
            String key = RedisSchema.getFeedKey();
            jedis.xadd(key, StreamEntryID.NEW_ENTRY, meterReading.toMap(), maxFeedLength, true);
        }
    }

    @Override
    public List<MeterReading> getRecent(int limit) {
        try (Jedis jedis = jedisPool.getResource()) {
            String key = RedisSchema.getFeedKey();
            List<StreamEntry> values = jedis.xrevrange(key, null,
                    null, limit);
            return values.stream()
                    .map(value -> new MeterReading(value.getFields()))
                    .collect(Collectors.toList());
        }
    }
}
