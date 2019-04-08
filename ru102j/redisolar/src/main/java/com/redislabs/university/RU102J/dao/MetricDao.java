package com.redislabs.university.RU102J.dao;

import com.redislabs.university.RU102J.api.Measurement;
import com.redislabs.university.RU102J.api.MeterReading;
import com.redislabs.university.RU102J.api.ValueUnit;

import java.util.List;

public interface MetricDao {
    public void insert(MeterReading reading);
    public List<Measurement> getRecent(Long siteId, ValueUnit unit, Integer limit);
}
