package com.redislabs.university.RU102J.dao;

import com.redislabs.university.RU102J.api.Measurement;
import com.redislabs.university.RU102J.api.MeterReading;

import java.util.List;

public interface FeedDao {
    void insert(MeterReading meterReading);
    List<MeterReading> getRecent(int limit);
}
