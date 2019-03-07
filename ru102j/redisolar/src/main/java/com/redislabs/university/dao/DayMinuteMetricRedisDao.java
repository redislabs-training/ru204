package com.redislabs.university.dao;

import com.redislabs.university.api.Measurement;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;

import java.time.LocalDateTime;

// Stores one measurement per minute for a give day in a Redis List.
public class DayMinuteMetricRedisDao implements DayMinuteMetricDao {
    private final JedisPool jedisPool;

    public DayMinuteMetricRedisDao(JedisPool jedisPool) {
        this.jedisPool = jedisPool;
    }

    @Override
    public void insert(Measurement measurement) {
        try (Jedis jedis = jedisPool.getResource()) {
            String metricKey = generateMetricKey(measurement);
            String hour = getMinuteOfDay(measurement.getDateTime());
            jedis.hset(metricKey, hour, String.valueOf(measurement.getValue()));
        }
    }

    /* The key for these metrics is as follows:
     * metric:day-minute:[unit-name]:[year-month-day]:[site-id]
     */
    private String generateMetricKey(Measurement measurement) {
        StringBuilder builder = new StringBuilder();
        return builder.append("metric:")
                .append("day-minute:")
                .append(measurement.getValueUnit().getShortName())
                .append(":")
                .append(getYearMonthDay(measurement.getDateTime()))
                .append(":")
                .append(String.valueOf(measurement.getSiteId()))
                .toString();
    }

    // Return the year and month in the form YEAR-MONTH-DAY
    private String getYearMonthDay(LocalDateTime dateTime) {
        return String.valueOf(dateTime.getYear()) + "-" +
                String.valueOf(dateTime.getMonth()) + "-" +
                String.valueOf(dateTime.getDayOfMonth());
    }

    // Return the minute of the day. For example:
    //  01:12 is the 72nd minute of the day
    //  5:00 is the 300th minute of the day
    private String getMinuteOfDay(LocalDateTime dateTime) {
        int hour = dateTime.getHour();
        int minute = dateTime.getMinute();
        return String.valueOf(hour * minute + minute);
    }
}
