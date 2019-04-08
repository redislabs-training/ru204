package com.redislabs.university.RU102J.dao;

import com.redislabs.university.RU102J.JedisDaoTestBase;
import com.redislabs.university.RU102J.api.MeterReading;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import redis.clients.jedis.Tuple;

import java.time.ZoneOffset;
import java.time.ZonedDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.*;

public class CapacityDaoRedisImplTest extends JedisDaoTestBase {

    private List<MeterReading> readings;

    @After
    public void flush() {
        keyManager.deleteKeys(jedis);
    }

    @Before
    public void generateData() {
        readings = new ArrayList<>();
        ZonedDateTime time = ZonedDateTime.now(ZoneOffset.UTC);
        for (int i=0; i < 10; i++) {
            MeterReading reading = new MeterReading();
            reading.setSiteId(Long.valueOf(i));
            reading.setTempC(22.0);
            reading.setWhUsed(1.2);
            reading.setWhGenerated(Double.valueOf(i));
            reading.setDateTime(time);
            readings.add(reading);
        }
    }

    @Test
    public void update() {
        CapacityDao dao = new CapacityDaoRedisImpl(jedisPool);
        for (MeterReading reading : readings) {
            System.out.println(reading);
            dao.update(reading);
        }
        Set<Tuple> results = jedis.zrevrangeWithScores(RedisSchema.getCapacityRankingKey(), 0, 20);
        assertThat(results.size(), is(10));
        results.toArray();
    }

    @Test
    public void getReport() {
    }
}