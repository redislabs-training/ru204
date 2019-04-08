package com.redislabs.university.RU102J.dao;

import com.redislabs.university.RU102J.api.CapacityReport;
import com.redislabs.university.RU102J.api.MeterReading;
import com.redislabs.university.RU102J.api.SiteCapacityTuple;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.Tuple;

import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

public class CapacityDaoRedisImpl implements CapacityDao {

    private final JedisPool jedisPool;

    public CapacityDaoRedisImpl(JedisPool jedisPool) {
        this.jedisPool = jedisPool;
    }

    @Override
    public void update(MeterReading reading) {
        String capacityRankingKey = RedisSchema.getCapacityRankingKey();
        Long siteId = reading.getSiteId();

        double currentCapacity = reading.whGenerated - reading.whUsed;

        try (Jedis jedis = jedisPool.getResource()) {
            jedis.zadd(capacityRankingKey, currentCapacity, String.valueOf(siteId));
        }
    }

    @Override
    public CapacityReport getReport(Integer limit) {
        CapacityReport report;
        String capacityKey = RedisSchema.getCapacityRankingKey();
        try (Jedis jedis = jedisPool.getResource()) {
            Set<Tuple> lowCapacity = jedis.zrangeWithScores(capacityKey, 0, limit);
            Set<Tuple> highCapacity = jedis.zrevrangeWithScores(capacityKey, 0, limit);
            List<SiteCapacityTuple> lowCapacityList = lowCapacity.stream()
                    .map(s -> new SiteCapacityTuple(s))
                    .collect(Collectors.toList());

            List<SiteCapacityTuple> highCapacityList = highCapacity.stream()
                    .map(s -> new SiteCapacityTuple(s))
                    .collect(Collectors.toList());

            report = new CapacityReport(highCapacityList, lowCapacityList);
        }

        return report;
    }
}
