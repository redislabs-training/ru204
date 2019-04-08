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

public class CapacityDaoRedisReservoirImpl implements CapacityDao {

    private final JedisPool jedisPool;

    public CapacityDaoRedisReservoirImpl(JedisPool jedisPool) {
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

    private double calculateCapacity(Long siteId, double currentCapacity) {
        String capacitySampleKey = RedisSchema.getCapacitySampleKey(siteId);
        List<String> values;
        try (Jedis jedis = jedisPool.getResource()) {
            jedis.lpush(capacitySampleKey, String.valueOf(currentCapacity));
            jedis.ltrim(capacitySampleKey, 0, 59);
            values = jedis.lrange(capacitySampleKey, 0, -1);
        }

        return getWeightedAverage(values);
    }

    private double getWeightedAverage(List<String> values) {
        int size = values.size();
        double average = 0.0;
        for (String value : values) {
            average += Double.valueOf(value);
        }

        return average / size;
    }
}
