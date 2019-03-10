package com.redislabs.university.RU102J.core;

import com.redislabs.university.RU102J.api.Measurement;
import com.redislabs.university.RU102J.api.Site;
import com.redislabs.university.RU102J.dao.DayMinuteMetricRedisDao;
import com.redislabs.university.RU102J.api.ValueUnit;
import com.redislabs.university.RU102J.dao.SiteRedisDao;
import redis.clients.jedis.JedisPool;

import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.util.List;
import java.util.Random;

public class SampleDataGenerator {
    private final JedisPool jedisPool;
    private final Random random;

    public SampleDataGenerator(JedisPool jedisPool) {
        this.jedisPool = jedisPool;
        this.random = new Random();
    }

    /* Generate historical data for all sites starting from the
     * current time and going back in time for the requested number
     * of days. The max number of permissible days is 365.
     */
    public void generateHistorical(int days) {
        System.out.print("Generating sample historical data...");
        if (days < 0 || days > 365) {
            throw new IllegalArgumentException("Invalid days " + String.valueOf(days) +
                    " for historical request.");
        }

        SiteRedisDao siteDao = new SiteRedisDao(jedisPool);
        DayMinuteMetricRedisDao dayMinute = new DayMinuteMetricRedisDao(jedisPool);
        List<Site> sites = siteDao.findAll();
        int minuteDays = days * 24 * 60;


        // Generate minute-level metrics for energy generated and energy used.
        for (Site site : sites) {
            System.out.print(".");
            Double maxCapacity = getMaxMinuteKWHGenerated(site.getCapacity());
            Double currentCapacity = getNextCapacity(maxCapacity);
            Double currentUsage = getInitialMinuteKWHUsed(maxCapacity);
            LocalDateTime currentTime = LocalDateTime.now(ZoneOffset.UTC);
            for (int i=0; i<minuteDays; i++) {
                Double generatedValue = site.getCapacity();
                Measurement generated = new Measurement(site.getId(), ValueUnit.KWHGenerated, currentTime, currentCapacity);
                dayMinute.insert(generated);
                Measurement used = new Measurement(site.getId(), ValueUnit.KWHUsed, currentTime, currentUsage);
                dayMinute.insert(used);
                Measurement temp = new Measurement(site.getId(), ValueUnit.TemperatureCelcius, currentTime, 0.5);
                dayMinute.insert(temp);
                currentTime = currentTime.minusMinutes(1L);
                currentCapacity = getNextCapacity(currentCapacity, maxCapacity);
                currentUsage = getNextUsage(currentUsage, maxCapacity);
            }
        }
        // Print a new line
        System.out.println("");
    }

    // Since site capacity is kWh per day, we need to get a
    // minute-based max to work with.
    private Double getMaxMinuteKWHGenerated(Double capacity) {
        return capacity / 24 / 60 * 1000;
    }

    private Double getNextCapacity(Double maxCapacity) {
        return getNextCapacity(maxCapacity, maxCapacity);
    }

    // Returns the next capacity based on current capacity.
    private Double getNextCapacity(Double currentCapacity, Double maxCapacity) {
        Double stepSize = 0.1 * maxCapacity;
        if (Math.random() > 0.5) {
            if (currentCapacity + stepSize < maxCapacity) {
                return currentCapacity + stepSize / 2;
            } else {
                return currentCapacity;
            }
        } else {
            if (currentCapacity - stepSize < 0.0) {
                return 0.0;
            } else {
                return currentCapacity - stepSize;
            }
        }
    }

    // Returns the next usage based on the current usage.
    private Double getNextUsage(Double currentUsage, Double maxCapacity) {
        Double stepSize = 0.1 * maxCapacity;
        if (Math.random() > 0.5) {
            return currentUsage + stepSize;
        } else {
            if (currentUsage - stepSize < 0.0) {
                return 0.0;
            } else {
                return currentUsage - stepSize;
            }
        }

    }

    // Returns an initial kWhUsed value with a .5 chance of being
    // above the max solar generating capacity.
    private Double getInitialMinuteKWHUsed(Double maxCapacity) {
        if (Math.random() > 0.5) {
            return maxCapacity + maxCapacity * Math.random() * 0.2;
        } else {
            return maxCapacity - maxCapacity * Math.random() * 0.2;
        }
    }

    /* Generate measurement data for all sites for the current
     * minute. This method may be called repeatedly in a loop or
     * as part of a ScheduledExecutorService.
     */
    public void generateCurrent() {
    }
}
