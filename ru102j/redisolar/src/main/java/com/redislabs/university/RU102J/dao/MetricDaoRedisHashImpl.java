package com.redislabs.university.RU102J.dao;

import com.redislabs.university.RU102J.api.Measurement;
import com.redislabs.university.RU102J.api.MeterReading;
import com.redislabs.university.RU102J.api.ValueUnit;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;

import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.time.ZonedDateTime;
import java.util.*;

// Stores one measurement per minute for a given day in a Redis hash.
public class MetricDaoRedisHashImpl implements MetricDao {
    private final JedisPool jedisPool;

    public MetricDaoRedisHashImpl(JedisPool jedisPool) {
        this.jedisPool = jedisPool;
    }

    @Override
    public void insert(MeterReading reading) {
        try (Jedis jedis = jedisPool.getResource()) {
            insertMetric(jedis, reading.getSiteId(), reading.getKwhGenerated(),
                    ValueUnit.KWHGenerated, reading.getDateTime());
            insertMetric(jedis, reading.getSiteId(), reading.getKwhUsed(),
                    ValueUnit.KWHUsed, reading.getDateTime());
            insertMetric(jedis, reading.getSiteId(), reading.getTempC(),
                    ValueUnit.TemperatureCelcius, reading.getDateTime());
        }
    }

    private void insertMetric(Jedis jedis, long siteId, double value, ValueUnit unit,
                              ZonedDateTime dateTime) {
           String metricKey = RedisSchema.getMinuteMetricKey(siteId, unit, dateTime);
           String minuteOfDay = getMinuteOfDay(dateTime);
           jedis.hset(metricKey, minuteOfDay, String.valueOf(value));
    }

    /**
     *  Return the N most-recent minute-level measurements starting at the current day.
     */
    @Override
    public List<Measurement> getRecent(Long siteId, ValueUnit unit, Integer limit) {
        List<Measurement> measurements = new ArrayList<>();
        ZonedDateTime currentDate = ZonedDateTime.now(ZoneOffset.UTC);

        measurements.addAll(getMeasurementsForDate(siteId, currentDate, unit));
        while (measurements.size() < limit) {
            currentDate = currentDate.minusDays(1);
            measurements.addAll(getMeasurementsForDate(siteId, currentDate, unit));
        }

        Collections.sort(measurements, (a, b) -> a.getDateTime().compareTo(b.getDateTime()));

        return measurements.subList(measurements.size() - limit, measurements.size()-1);
    }

    private List<Measurement> getMeasurementsForDate(Long siteId, ZonedDateTime date,
                                                     ValueUnit unit) {
        List<Measurement> measurements = new ArrayList<>();

        try (Jedis jedis = jedisPool.getResource()) {
            String metricKey = RedisSchema.getMinuteMetricKey(siteId, unit, date);
            Map<String, String> metrics = jedis.hgetAll(metricKey);
            for (Map.Entry<String, String> minuteValue : metrics.entrySet()) {
                ZonedDateTime dateTime = getDateFromDayMinute(date, Integer.valueOf(minuteValue.getKey()));
                measurements.add(new Measurement(siteId, unit, dateTime,
                        Double.valueOf(minuteValue.getValue())));
            }
        }

        return measurements;
    }

    private ZonedDateTime getDateFromDayMinute(ZonedDateTime dateTime, Integer dayMinute) {
       Integer minute = dayMinute % 60;
       Integer hour = dayMinute / 60;
       return dateTime.withHour(hour).withMinute(minute).withZoneSameInstant(ZoneOffset.UTC);
    }

    // Return the minute of the day. For example:
    //  01:12 is the 72nd minute of the day
    //  5:00 is the 300th minute of the day
    public String getMinuteOfDay(ZonedDateTime dateTime) {
        int hour = dateTime.getHour();
        int minute = dateTime.getMinute();
        return String.valueOf(hour * 60 + minute);
    }
}
