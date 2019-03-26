package com.redislabs.university.RU102J.dao;

import com.redislabs.university.RU102J.api.Measurement;
import com.redislabs.university.RU102J.api.ValueUnit;
import com.redislabs.university.RU102J.core.KeyHelper;

import java.time.LocalDateTime;

/**
 * Methods to generate key names for Redis
 * data structures. These key names are used
 * by the RedisDaoImpl classes.
 */
public class RedisSchema {
    public static String getSiteHashKey(Long id) {
        return KeyHelper.getKey("sites:info:" + id);
    }

    public static String getSiteIDsSetKey() {
        return KeyHelper.getKey("sites:ids");
    };


    public static String getCapacityZsetKey() {
        return KeyHelper.getKey("sites:capacity");
    }

    /* The key for these metrics is as follows:
     * metric:day-minute:[unit-name]:[year-month-day]:[site-id]
     */
    public static String getMinuteMetricKey(Long siteId, ValueUnit unit,
                                               LocalDateTime dateTime) {
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

    /* The key for these metrics is as follows:
     * metric:month-hour:[unit-name]:[year-month]:[site-id]
     */
    public static String getHourMetricKey(Measurement measurement) {
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

    // Return the year and month in the form YEAR-MONTH-DAY
    private static String getYearMonthDay(LocalDateTime dateTime) {
        return String.valueOf(dateTime.getYear()) + "-" +
                String.valueOf(dateTime.getMonth()) + "-" +
                String.valueOf(dateTime.getDayOfMonth());
    }

     // Return the year and month in the form YEAR-MONTH
    private static String getYearMonth(LocalDateTime dateTime) {
        return String.valueOf(dateTime.getYear()) + "-" +
                String.valueOf(dateTime.getMonth());
    }

}
