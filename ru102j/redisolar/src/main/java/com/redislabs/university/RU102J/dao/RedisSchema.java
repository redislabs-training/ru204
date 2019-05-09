package com.redislabs.university.RU102J.dao;

import com.redislabs.university.RU102J.api.MetricUnit;
import com.redislabs.university.RU102J.core.KeyHelper;

import java.time.ZonedDateTime;

/**
 * Methods to generate key names for Redis
 * data structures. These key names are used
 * by the RedisDaoImpl classes.
 */
public class RedisSchema {
    // sites:info:[siteId]
    public static String getSiteHashKey(long siteId) {
        return KeyHelper.getKey("sites:info:" + siteId);
    }

    // sites:ids
    public static String getSiteIDsSetKey() {
        return KeyHelper.getKey("sites:ids");
    }

    // sites:capacity:ranking
    public static String getCapacityRankingKey() {
        return KeyHelper.getKey("sites:capacity:ranking");
    }

    // sites:capacity:sample:[siteId]
    public static String getCapacitySampleKey(long siteId) {
        return KeyHelper.getKey("sites:capacity:sample:" + siteId);
    }

    /* The key for these metrics is as follows:
     * metric:[unit-name]:[year-month]:[site-id]
     */
    public static String getMonthMetricKey(Long siteId, MetricUnit unit,
                                           ZonedDateTime dateTime) {
        StringBuilder builder = new StringBuilder();
        return builder.append(KeyHelper.getPrefix())
                .append(":metric:")
                .append(unit.getShortName())
                .append(":")
                .append(getYearMonth(dateTime))
                .append(":")
                .append(String.valueOf(siteId))
                .toString();

    }

    /* The key for these metrics is as follows:
     * metric:[unit-name]:[year-month-day]:[site-id]
     */
    public static String getDayMetricKey(Long siteId, MetricUnit unit,
                                         ZonedDateTime dateTime) {
        StringBuilder builder = new StringBuilder();
        return builder.append(KeyHelper.getPrefix())
                .append(":metric:")
                .append(unit.getShortName())
                .append(":")
                .append(getYearMonthDay(dateTime))
                .append(":")
                .append(String.valueOf(siteId))
                .toString();
    }

    // Return the year and month in the form YEAR-MONTH-DAY
    private static String getYearMonthDay(ZonedDateTime dateTime) {
        return String.valueOf(dateTime.getYear()) + "-" +
                String.valueOf(dateTime.getMonth()) + "-" +
                String.valueOf(dateTime.getDayOfMonth());
    }

     // Return the year and month in the form YEAR-MONTH
    private static String getYearMonth(ZonedDateTime dateTime) {
        return String.valueOf(dateTime.getYear()) + "-" +
                String.valueOf(dateTime.getMonth());
    }

    public static String getFeedKey() {
        return "feed:readings";
    }
}
