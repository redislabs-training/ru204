package com.redislabs.university.RU102J.dao;

import com.redislabs.university.RU102J.api.Measurement;
import com.redislabs.university.RU102J.api.MeterReading;
import com.redislabs.university.RU102J.api.MetricUnit;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;

import java.time.ZonedDateTime;
import java.util.List;

/**
 * Retain metrics using the Redis Time Series module
 * (see https://github.com/RedisLabsModules/RedisTimeSeries)
 *
 */
public class MetricDaoRedisTSImpl implements MetricDao {
    private JedisPool jedisPool;

    public MetricDaoRedisTSImpl(JedisPool jedisPool) {
        this.jedisPool = jedisPool;
    }

    @Override
    public void insert(MeterReading reading) {
        try (Jedis jedis = jedisPool.getResource()) {
            insertMetric(jedis, reading.getSiteId(), reading.getWhGenerated(),
                    MetricUnit.WHGenerated, reading.getDateTime());
            insertMetric(jedis, reading.getSiteId(), reading.getWhUsed(),
                    MetricUnit.WHUsed, reading.getDateTime());
            insertMetric(jedis, reading.getSiteId(), reading.getTempC(),
                    MetricUnit.TemperatureCelcius, reading.getDateTime());
        }
    }

    private void insertMetric(Jedis jedis, Long siteId, Double value, MetricUnit unit,
                              ZonedDateTime dateTime) {
    }

    @Override
    public List<Measurement> getRecent(Long siteId, MetricUnit unit, ZonedDateTime time, Integer limit) {
        return null;
    }
}
