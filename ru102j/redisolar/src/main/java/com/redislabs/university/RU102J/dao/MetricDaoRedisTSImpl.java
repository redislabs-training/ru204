package com.redislabs.university.RU102J.dao;

import com.redislabs.university.RU102J.api.Measurement;
import com.redislabs.university.RU102J.api.MeterReading;
import com.redislabs.university.RU102J.api.MetricUnit;

import java.time.ZonedDateTime;
import java.util.List;

public class MetricDaoRedisTSImpl implements MetricDao {
    @Override
    public void insert(MeterReading reading) {
    }

    @Override
    public List<Measurement> getRecent(Long siteId, MetricUnit unit, ZonedDateTime time, Integer limit) {
        return null;
    }
}
