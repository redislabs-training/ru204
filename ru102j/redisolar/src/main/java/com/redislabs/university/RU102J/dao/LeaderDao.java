package com.redislabs.university.RU102J.dao;

import com.redislabs.university.RU102J.api.Measurement;

public interface LeaderDao {
    void insert(Measurement amountGenerated);
}
