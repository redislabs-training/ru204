package com.redislabs.university.RU102J.dao;

import com.redislabs.university.RU102J.api.Measurement;
import com.redislabs.university.RU102J.api.ValueUnit;

import java.util.List;

public interface DayMinuteMetricDao {
    public void insert(Measurement measurement);
    public List<Measurement> getMeasurements(Long siteId, ValueUnit unit);
}
