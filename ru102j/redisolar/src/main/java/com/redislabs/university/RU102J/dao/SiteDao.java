package com.redislabs.university.RU102J.dao;

import com.redislabs.university.RU102J.api.Coordinate;
import com.redislabs.university.RU102J.api.Site;

import java.util.List;

public interface SiteDao {
    List<Site> findAll();
    List<Site> findByGeo(Coordinate coordinate, Double radius, String radiusUnit);
    Site findById(Long id);
    void insert(Site site);
}
