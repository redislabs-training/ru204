package com.redislabs.university.RU102J.dao;

import com.redislabs.university.RU102J.api.Measurement;
import com.redislabs.university.RU102J.api.ValueUnit;
import com.redislabs.university.RU102J.core.KeyHelper;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;

import java.time.LocalDateTime;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

// Stores one measurement per minute for a give day in a Redis List.
public class DayMinuteMetricRedisDao implements DayMinuteMetricDao {
    private final JedisPool jedisPool;

    public DayMinuteMetricRedisDao(JedisPool jedisPool) {
        this.jedisPool = jedisPool;
    }

    @Override
    public void insert(Measurement m) {
        try (Jedis jedis = jedisPool.getResource()) {
            String metricKey = generateMetricKey(m.getSiteId(), m.getValueUnit(), m.getDateTime());
            String hour = getMinuteOfDay(m.getDateTime());
            jedis.hset(metricKey, hour, String.valueOf(m.getValue()));
        }
    }

    public void insertAll(List<Measurement> measurements) {
        // Build a map of measurements
        Map<DayMinuteIdentifier, Map<String, String>> map = new ConcurrentHashMap<>();
        for (Measurement m : measurements) {
            DayMinuteIdentifier id = new DayMinuteIdentifier(m.getSiteId(), m.getValueUnit(), m.getDateTime());
            if (!map.containsKey(id)) {
                map.put(id, new HashMap<String, String>());
            }
            Map<String, String> measurementMap = map.get(id);
            measurementMap.put(getMinuteOfDay(m.getDateTime()), String.valueOf(m.getValue()));
        }

        // Populate the entries
        try (Jedis jedis = jedisPool.getResource()) {
            for (Map.Entry<DayMinuteIdentifier, Map<String, String>> dayMinuteIdEntry : map.entrySet()) {
                DayMinuteIdentifier identifer = dayMinuteIdEntry.getKey();
                String metricKey = generateMetricKey(identifer.getSiteId(), identifer.getUnit(), identifer.getDateTime());
                jedis.hmset(metricKey, dayMinuteIdEntry.getValue());
            }
        }
    }

    @Override
    public List<Measurement> getMeasurements(Long siteId, ValueUnit unit) {
        List<Measurement> results = new ArrayList<>();
        List<LocalDateTime> dates = new ArrayList<>();

        // For now, return results from the past two days
        dates.add(LocalDateTime.now());
        //dates.add(LocalDateTime.now().minusDays(1));
        try (Jedis jedis = jedisPool.getResource()) {
            for (LocalDateTime date : dates) {
                String metricKey = generateMetricKey(siteId, unit, date);
                Map<String, String> values = jedis.hgetAll(metricKey);
                for (Map.Entry<String, String> minuteValue : values.entrySet()) {
                    LocalDateTime dateTime = getDateFromDayMinute(date, Integer.valueOf(minuteValue.getKey()));
                    results.add(new Measurement(siteId, unit, dateTime, Double.valueOf(minuteValue.getValue())));
                }
            }
        }

        Collections.sort(results, (a, b) -> a.getDateTime().compareTo(b.getDateTime()));

        return results.subList(results.size() - 100, results.size()-1);
    }

    private LocalDateTime getDateFromDayMinute(LocalDateTime dateTime, Integer dayMinute) {
       Integer minute = dayMinute % 60;
       Integer hour = dayMinute / 60;
       return dateTime.withHour(hour).withMinute(minute);
    }

    // TODO: Insert multiple measurements
    public void insertAll(Map<String, Measurement> measurements) {
    }

    /* The key for these metrics is as follows:
     * metric:day-minute:[unit-name]:[year-month-day]:[site-id]
     */
    private String generateMetricKey(Long siteId, ValueUnit unit, LocalDateTime dateTime) {
        StringBuilder builder = new StringBuilder();
        return builder.append(KeyHelper.getPrefix())
                .append(":")
                .append("metric:")
                .append("day-minute:")
                .append(unit.getShortName())
                .append(":")
                .append(getYearMonthDay(dateTime))
                .append(":")
                .append(String.valueOf(siteId))
                .toString();
    }

    // Return the year and month in the form YEAR-MONTH-DAY
    private String getYearMonthDay(LocalDateTime dateTime) {
        return String.valueOf(dateTime.getYear()) + "-" +
                String.valueOf(dateTime.getMonth()) + "-" +
                String.valueOf(dateTime.getDayOfMonth());
    }

    // Return the minute of the day. For examples:
    //  01:12 is the 72nd minute of the day
    //  5:00 is the 300th minute of the day
    private String getMinuteOfDay(LocalDateTime dateTime) {
        int hour = dateTime.getHour();
        int minute = dateTime.getMinute();
        return String.valueOf(hour * 60 + minute);
    }

    private static class DayMinuteIdentifier {

        private final Long siteId;
        private final ValueUnit unit;
        private final LocalDateTime dateTime;

        public DayMinuteIdentifier(Long siteId, ValueUnit unit, LocalDateTime dateTime) {
            this.siteId = siteId;
            this.unit = unit;
            this.dateTime = dateTime;
        }

        public Long getSiteId() {
            return siteId;
        }

        public ValueUnit getUnit() {
            return unit;
        }

        public LocalDateTime getDateTime() {
            return dateTime;
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;
            DayMinuteIdentifier that = (DayMinuteIdentifier) o;
            return Objects.equals(siteId, that.siteId) &&
                    unit == that.unit &&
                    Objects.equals(dateTime, that.dateTime);
        }

        @Override
        public int hashCode() {
            return Objects.hash(siteId, unit, dateTime);
        }

        @Override
        public String toString() {
            return "DayMinuteIdentifier{" +
                    "siteId=" + siteId +
                    ", unit=" + unit +
                    ", dateTime=" + dateTime +
                    '}';
        }
    }
}
