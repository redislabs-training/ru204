package com.redislabs.university.dao;

import com.redislabs.university.api.Measurement;

public interface DayMinuteMetricDao {
    public void insert(Measurement measurement);
}
