package com.redislabs.university.RU102J.dao;

import com.redislabs.university.RU102J.api.Measurement;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;

import java.time.LocalDateTime;

/* Stores one measurement per hour for a given month of the year. Thus,
 * this metric is backed by a hash containing up to 744 entries
 * (31 days * 24 hours). Partial weeks that begin and end the year
 * will contain fewer entries.
 */
public class MonthHourMetricRedisDao implements MonthHourMetricDao {
    private final JedisPool jedisPool;

    // TODO: Create a separate dao that inserts MeterReading with a pipeline
    public MonthHourMetricRedisDao(JedisPool jedisPool) {
        this.jedisPool = jedisPool;
    }

    @Override
    public void insert(Measurement measurement) {
        try (Jedis jedis = jedisPool.getResource()) {
            String metricKey = generateMetricKey(measurement);
            String dayOfMonth = getDayOfMonth(measurement.getDateTime());
            jedis.hincrByFloat(metricKey, dayOfMonth, measurement.getValue());
        }
    }

    /* The key for these metrics is as follows:
     * metric:month-hour:[unit-name]:[year-month]:[site-id]
     */
    private String generateMetricKey(Measurement measurement) {
        StringBuilder builder = new StringBuilder();
        return builder.append("metric:")
                .append("month-hour:")
                .append(measurement.getValueUnit().getShortName())
                .append(":")
                .append(getYearMonth(measurement.getDateTime()))
                .append(":")
                .append(String.valueOf(measurement.getSiteId()))
                .toString();
    }

    // Return the year and month in the form YEAR-MONTH
    private String getYearMonth(LocalDateTime dateTime) {
        return String.valueOf(dateTime.getYear()) + "-" +
                String.valueOf(dateTime.getMonth());
    }

    // Return the day of the month as a string
    private String getDayOfMonth(LocalDateTime dateTime) {
        return String.valueOf(dateTime.getDayOfMonth());
    }
}
