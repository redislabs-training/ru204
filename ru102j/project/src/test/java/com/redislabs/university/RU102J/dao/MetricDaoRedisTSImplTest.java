package com.redislabs.university.RU102J.dao;

import com.redislabs.redistimeseries.RedisTimeSeries;
import com.redislabs.university.RU102J.HostPort;
import com.redislabs.university.RU102J.TestKeyManager;
import com.redislabs.university.RU102J.api.Measurement;
import com.redislabs.university.RU102J.api.MeterReading;
import com.redislabs.university.RU102J.api.MetricUnit;
import org.junit.After;
import org.junit.Before;
import org.junit.Ignore;
import org.junit.Test;
import redis.clients.jedis.Jedis;

import java.time.ZoneOffset;
import java.time.ZonedDateTime;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

import static org.junit.Assert.*;
import static org.hamcrest.CoreMatchers.is;

public class MetricDaoRedisTSImplTest {

    private ArrayList<MeterReading> readings;
    private Long siteId = 1L;
    private ZonedDateTime startingDate = ZonedDateTime.now(ZoneOffset.UTC);
    private Jedis jedis;
    private TestKeyManager keyManager;
    private RedisTimeSeries rts;

    @Before
    public void setUp() {
        this.jedis = new Jedis(HostPort.getRedisHost(), HostPort.getRedisPort());
        this.rts = new RedisTimeSeries(HostPort.getRedisHost(),
                HostPort.getRedisPort());
        this.keyManager = new TestKeyManager("test");
    }

    @After
    public void tearDown() {
        keyManager.deleteKeys(jedis);
    }

    /**
     * Generate 72 hours worth of data.
    */
    @Before
    public void generateData() {
        readings = new ArrayList<>();
        ZonedDateTime time = startingDate;
        for (int i=0; i <  72 * 60; i++) {
            MeterReading reading = new MeterReading();
            reading.setSiteId(siteId);
            reading.setTempC(i * 1.0);
            reading.setWhUsed(i * 1.0);
            reading.setWhGenerated(i * 1.0);
            reading.setDateTime(time);
            readings.add(reading);
            time = time.minusMinutes(1);
        }
        Collections.reverse(readings);
    }

    @Test
    @Ignore
    public void testSmall() {
        testInsertAndRetrieve(1);
    }

    @Test
    @Ignore
    public void testOneDay() {
        testInsertAndRetrieve(60 * 24);
    }


    @Test
    @Ignore
    public void testMultipleDays() {
        testInsertAndRetrieve(60 * 70);
    }

    private void testInsertAndRetrieve(int limit) {
        MetricDao metricDao = new MetricDaoRedisTSImpl(rts);
        for (MeterReading reading : readings) {
            metricDao.insert(reading);
        }

        List<Measurement> measurements = metricDao.getRecent(siteId, MetricUnit.WHGenerated,
         startingDate, limit);
        assertThat(measurements.size(), is(limit));
        int i = limit;
        for (Measurement measurement : measurements) {
            assertThat(measurement.getValue(), is((i - 1) * 1.0));
            i -= 1;
        }
    }
}