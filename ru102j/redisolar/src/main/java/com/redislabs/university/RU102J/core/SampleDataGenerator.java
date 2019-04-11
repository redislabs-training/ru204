package com.redislabs.university.RU102J.core;

import com.redislabs.university.RU102J.api.*;
import com.redislabs.university.RU102J.dao.*;
import com.redislabs.university.RU102J.resources.MeterReadingResource;
import redis.clients.jedis.JedisPool;

import java.time.ZoneOffset;
import java.time.ZonedDateTime;
import java.util.List;
import java.util.Random;
import java.util.Set;
import java.util.stream.Collectors;

public class SampleDataGenerator {
    private final Integer seed = 42;
    private final double maxTemperatureC = 30.0;
    private final JedisPool jedisPool;
    private final Random random;

    public SampleDataGenerator(JedisPool jedisPool) {
        this.jedisPool = jedisPool;
        this.random = new Random(seed);
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

        SiteDao siteDao = new SiteDaoRedisImpl(jedisPool);
        CapacityDao capacityDao = new CapacityDaoRedisImpl(jedisPool);
        MetricDao metricDao = new MetricDaoRedisZsetImpl(jedisPool);
        FeedDao feedDao = new FeedDaoRedisImpl(jedisPool);
        MeterReadingResource meterResource = new MeterReadingResource(siteDao, metricDao,
                capacityDao, feedDao);

        Set<Site> sites = siteDao.findAll();
        int minuteDays = days * 3 * 60;

        List<Site> sortedSites =
                sites.stream().sorted().collect(Collectors.toList());

        // Generate minute-level metrics for energy generated and energy used.
        for (Site site : sortedSites) {
            System.out.print(".");
            Double maxCapacity = getMaxMinuteWHGenerated(site.getCapacity());
            Double currentCapacity = getNextValue(maxCapacity);
            Double currentTemperature = getNextValue(maxTemperatureC);
            Double currentUsage = getInitialMinuteWHUsed(maxCapacity);
            ZonedDateTime currentTime = ZonedDateTime.now(ZoneOffset.UTC).minusMinutes(minuteDays);

            for (int i=0; i<minuteDays; i++) {
                MeterReading reading = new MeterReading(site.getId(), currentTime, currentUsage,
                        currentCapacity, currentTemperature);

                // This is where we insert the meter reading
                meterResource.add(reading);

                currentTime = currentTime.plusMinutes(1L);
                currentTemperature = getNextValue(currentTemperature);
                currentCapacity = getNextValue(currentCapacity, maxCapacity);
                currentUsage = getNextValue(currentUsage, maxCapacity);
            }
        }
    }

    // Since site capacity is measured in kWh per day, we need to get a
    // minute-based maximum watt-hours to work with.
    private Double getMaxMinuteWHGenerated(Double capacity) {
        return capacity * 1000 / 24 / 60;
    }

    private Double getNextValue(Double max) {
        return getNextValue(max, max);
    }

    // Returns the next value in the series
    private Double getNextValue(Double current, Double max) {
        Double stepSize = 0.1 * max;
        if (Math.random() > 0.5) {
            return current + stepSize;
        } else {
            if (current - stepSize < 0.0) {
                return 0.0;
            } else {
                return current - stepSize;
            }
        }
    }

    // Returns an initial kWhUsed value with a .5 chance of being
    // above the max solar generating capacity.
    private Double getInitialMinuteWHUsed(Double maxCapacity) {
        if (Math.random() > 0.5) {
            return maxCapacity + maxCapacity * randomValue() * 0.1;
        } else {
            return maxCapacity - maxCapacity * randomValue() * 0.1;
        }
    }

    private Double randomValue() {
        return Math.random();
    }

    /* Generate measurement data for all sites for the current
     * minute. This method may be called repeatedly in a loop or
     * as part of a ScheduledExecutorService.
     */
    public void generateCurrent() {
    }
}
