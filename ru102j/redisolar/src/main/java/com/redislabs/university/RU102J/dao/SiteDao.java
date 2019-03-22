package com.redislabs.university.RU102J.dao;

import com.redislabs.university.RU102J.api.Coordinate;
import com.redislabs.university.RU102J.api.Site;

import java.util.Set;

public interface SiteDao {
    Site findById(Long id);
    Set<Site> findAll();
    void insert(Site site);
    Set<Site> findAllGeo();
    Set<Site> findByGeo(Coordinate coordinate, Double radius, String radiusUnit);
}
