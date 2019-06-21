package com.redislabs.university.RU102J.dao;

import com.redislabs.university.RU102J.api.MeterReading;
import redis.clients.jedis.*;

import java.nio.channels.Pipe;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

public class FeedDaoRedisImpl implements FeedDao {

    private final JedisPool jedisPool;
    private static final long globalMaxFeedLength = 10000;
    private static final long siteMaxFeedLength = 2440;

    public FeedDaoRedisImpl(JedisPool jedisPool) {
        this.jedisPool = jedisPool;
    }

    @Override
    public void insert(MeterReading meterReading) {
        try (Jedis jedis = jedisPool.getResource()) {
            String globalFeedKey = RedisSchema.getGlobalFeedKey();
            String siteFeedKey = RedisSchema.getFeedKey(meterReading.getSiteId());
            Pipeline p = jedis.pipelined();
            p.xadd(globalFeedKey, StreamEntryID.NEW_ENTRY, meterReading.toMap(),
                    globalMaxFeedLength, true);
            p.xadd(siteFeedKey, StreamEntryID.NEW_ENTRY, meterReading.toMap(),
                    siteMaxFeedLength, true);
            p.sync();
        }
    }

    @Override
    public List<MeterReading> getRecentGlobal(int limit) {
        return getRecent(RedisSchema.getGlobalFeedKey(), limit);
    }

    @Override
    public List<MeterReading> getRecentForSite(long siteId, int limit) {
        return getRecent(RedisSchema.getFeedKey(siteId), limit);
    }

    public List<MeterReading> getRecent(String key, int limit) {
        List<MeterReading> readings = new ArrayList<>(limit);
        try (Jedis jedis = jedisPool.getResource()) {
            List<StreamEntry> entries = jedis.xrevrange(key, null,
                    null, limit);
            for (StreamEntry entry : entries) {
                readings.add(new MeterReading(entry.getFields()));
            }
            return readings;
        }
    }
}
