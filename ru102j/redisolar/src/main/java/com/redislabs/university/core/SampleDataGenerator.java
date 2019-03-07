package com.redislabs.university.core;

import com.redislabs.university.api.Measurement;
import com.redislabs.university.api.Site;
import com.redislabs.university.api.ValueUnit;
import com.redislabs.university.dao.DayMinuteMetricRedisDao;
import com.redislabs.university.dao.SiteRedisDao;
import redis.clients.jedis.JedisPool;

import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.ZoneOffset;
import java.time.temporal.TemporalAmount;
import java.util.List;

public class SampleDataGenerator {
    private final JedisPool jedisPool;

    public SampleDataGenerator(JedisPool jedisPool) {
        this.jedisPool = jedisPool;
    }

    /* Generate historical data for all sites starting from the
     * current time and going back in time for the requested number
     * of days. The max number of permissible days is 365.
     */
    public void generateHistorical(int days) {
        if (days < 0 || days > 365) {
            throw new IllegalArgumentException("Invalid days " + String.valueOf(days) +
                    " for historical request.");
        }

        SiteRedisDao siteDao = new SiteRedisDao(jedisPool);
        DayMinuteMetricRedisDao dayMinute = new DayMinuteMetricRedisDao(jedisPool);
        List<Site> sites = siteDao.findAll();
        int minuteDays = days * 24 * 60;

        LocalDateTime currentTime = LocalDateTime.now(ZoneOffset.UTC);

        // Generate minute-level metrics for the first two days
        for (int i=0; i<minuteDays; i++) {
            for (Site site : sites) {
                Double generatedValue = site.getCapacity();
                Measurement m = new Measurement(site.getId(), ValueUnit.KWHGenerated, currentTime, 1.0);
                dayMinute.insert(m);
            }
            currentTime = currentTime.minusMinutes(1L);
        }
    }

    /* Generate measurement data for all sites for the current
     * minute. This method may be called repeatedly in a loop or
     * as part of a ScheduledExecutorService.
     */
    public void generateCurrent() {
    }
}
