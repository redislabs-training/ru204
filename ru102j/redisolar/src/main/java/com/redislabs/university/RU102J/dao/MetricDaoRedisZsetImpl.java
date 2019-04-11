package com.redislabs.university.RU102J.dao;

import com.redislabs.university.RU102J.api.Measurement;
import com.redislabs.university.RU102J.api.MeterReading;
import com.redislabs.university.RU102J.api.MetricUnit;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.Tuple;

import java.text.DecimalFormat;
import java.time.ZoneOffset;
import java.time.ZonedDateTime;
import java.util.*;

// Stores one measurement per minute for a given day in a Redis hash.
public class MetricDaoRedisZsetImpl implements MetricDao {
    private final Integer maxMinuteLevelMetricsRequestDays = 14;
    private final Integer metricsPerDay = 60 * 24;
    private final JedisPool jedisPool;

    public MetricDaoRedisZsetImpl(JedisPool jedisPool) {
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

    private void insertMetric(Jedis jedis, long siteId, double value, MetricUnit unit,
                              ZonedDateTime dateTime) {
           String metricKey = RedisSchema.getDayMetricKey(siteId, unit, dateTime);
           Integer minuteOfDay = getMinuteOfDay(dateTime);
           jedis.zadd(metricKey, minuteOfDay, new MeasurementMinute(value, minuteOfDay).toString());
    }

    /**
     *  Return the N most-recent minute-level measurements starting at the provided day.
     */
    @Override
    public List<Measurement> getRecent(Long siteId, MetricUnit unit, ZonedDateTime time, Integer limit) {
        if (limit > metricsPerDay * maxMinuteLevelMetricsRequestDays) {
            throw new IllegalArgumentException("Cannot request more than two weeks of " +
                    "minute-level data");
        }

        List<Measurement> measurements = new ArrayList<>();
        ZonedDateTime currentDate = time;
        Integer count = limit;
        Integer iterations = 0;

        // This loop extracts the elements of successive
        // sorted sets until it reaches the requested limit.
        do {
            List<Measurement> ms = getMeasurementsForDate(siteId, currentDate, unit, count);
            measurements.addAll(0, ms);
            count -= ms.size();
            currentDate = currentDate.minusDays(1);
            iterations += 1;
        } while (count > 0 && iterations < metricsPerDay);

        return measurements;
    }

    // Return up to count elements from the sorted set corresponding to the siteId, date, and
    // metric unit specified here.
    private List<Measurement> getMeasurementsForDate(Long siteId, ZonedDateTime date,
                                                     MetricUnit unit, Integer count) {
        // A list of Measurement objects to return.
        List<Measurement> measurements = new ArrayList<>();

        try (Jedis jedis = jedisPool.getResource()) {
            // Get the metric key for the day implied by the date.
            // metric:[unit-name]:[year-month-day]:[site-id]
            // e.g.: metrics:whU:2020-01-01:1
            String metricKey = RedisSchema.getDayMetricKey(siteId, unit, date);

            // Return a reverse range so that we're always consuming from the end of the
            // sorted set.
            Set<Tuple> metrics = jedis.zrevrangeWithScores(metricKey, 0, count - 1);
            for (Tuple minuteValue : metrics) {
                // Elements of the set are of the form [measurement]-[minute]
                // The MeasurementMinute class abstracts this for us.
                MeasurementMinute mm = MeasurementMinute.fromZSetValue(minuteValue.getElement());

                // Derive the dateTime for the measurement using the date and the minute of
                // the day.
                ZonedDateTime dateTime = getDateFromDayMinute(date, mm.getMinuteOfDay());

                // Add a new measurement to the list of measurements.
                measurements.add(new Measurement(siteId, unit, dateTime, mm.getMeasurement()));
            }
        }

        Collections.reverse(measurements);
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
    public Integer getMinuteOfDay(ZonedDateTime dateTime) {
        int hour = dateTime.getHour();
        int minute = dateTime.getMinute();
        return hour * 60 + minute;
    }

    /**
     * Utility class to convert between our sorted set members and their
     * constituent measurement and minute values.
     *
     * Also rounds decimals before storing them.
     */
    public static class MeasurementMinute {
        private final Double measurement;
        private final Integer minuteOfDay;
        private final DecimalFormat decimalFormat;

        // For a sorted set value of "22.0-1", this classes provides
        // the measurement value of 22.0 and the minuteOfDay value of 1.
        public static MeasurementMinute fromZSetValue(String zSetValue) {
            String[] parts = zSetValue.split("-");
            if (parts.length == 2) {
                return new MeasurementMinute(Double.valueOf(parts[0]), Integer.valueOf(parts[1]));
            } else {
                throw new IllegalArgumentException("Cannot convert zSetValue " + zSetValue +
                        " into MeasurementMinute");
            }
        }

        public MeasurementMinute(Double measurement, Integer minuteOfDay) {
            this.measurement = measurement;
            this.minuteOfDay = minuteOfDay;
            this.decimalFormat = new DecimalFormat("#.##");
        }

        public Integer getMinuteOfDay() {
            return minuteOfDay;
        }

        public Double getMeasurement() {
            return measurement;
        }

        public String toString() {
            return decimalFormat.format(measurement) + '-' + String.valueOf(minuteOfDay);
        }
    }
}
