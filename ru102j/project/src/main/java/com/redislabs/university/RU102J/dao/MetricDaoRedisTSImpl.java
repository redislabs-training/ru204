package com.redislabs.university.RU102J.dao;

import com.redislabs.redistimeseries.RedisTimeSeries;
import com.redislabs.redistimeseries.Value;
import com.redislabs.university.RU102J.api.Measurement;
import com.redislabs.university.RU102J.api.MeterReading;
import com.redislabs.university.RU102J.api.MetricUnit;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.exceptions.JedisDataException;

import java.time.Instant;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;

/**
 * Retain metrics using the Redis Time Series module
 * (see https://github.com/RedisLabsModules/RedisTimeSeries)
 *
 */
public class MetricDaoRedisTSImpl implements MetricDao {
    static private final Integer METRIC_EXPIRATION_SECONDS =
            60 * 60 * 24 * 14;
    private final RedisTimeSeries rts;
    private final HashSet<String> metricNameCache;
    private JedisPool jedisPool;

    public MetricDaoRedisTSImpl(RedisTimeSeries rts) {
        this.rts = rts;
        this.metricNameCache = new HashSet<>();
    }

    @Override
    public void insert(MeterReading reading) {
        insertMetric(reading.getSiteId(), reading.getWhGenerated(),
                MetricUnit.WHGenerated, reading.getDateTime());
        insertMetric(reading.getSiteId(), reading.getWhUsed(),
                MetricUnit.WHUsed, reading.getDateTime());
        insertMetric(reading.getSiteId(), reading.getTempC(),
                MetricUnit.TemperatureCelsius, reading.getDateTime());
    }

    private void insertMetric(Long siteId, Double value, MetricUnit unit,
                              ZonedDateTime dateTime) {
        String metricKey = RedisSchema.getTSKey(siteId, unit);
        ensureCreated(metricKey);
        rts.add(metricKey, dateTime.toEpochSecond(), value);
    }

    @Override
    public List<Measurement> getRecent(Long siteId, MetricUnit unit, ZonedDateTime time, Integer limit) {
        List<Measurement> measurements = new ArrayList<>();
        String metricKey = RedisSchema.getTSKey(siteId, unit);

        Long now = ZonedDateTime.now().toEpochSecond();
        Long initialTimestamp = now - limit * 60;
        Value[] values = rts.range(metricKey, initialTimestamp, now);

        for (Value value : values) {
            Measurement m = new Measurement();
            m.setSiteId(siteId);
            m.setMetricUnit(unit);
            Instant i = Instant.ofEpochSecond(value.getTime());
            m.setDateTime(ZonedDateTime.ofInstant(i, ZoneId.of("UTC")));
            m.setValue(value.getValue());
            measurements.add(m);
        }

        return measurements;
    }

    private void ensureCreated(String metricName) {
        if (!metricNameCache.contains(metricName)) {
            metricNameCache.add(metricName);
            try {
                rts.create(metricName, METRIC_EXPIRATION_SECONDS);
            } catch (Exception e) {
                System.out.println(e);
            }
        }
    }
}
