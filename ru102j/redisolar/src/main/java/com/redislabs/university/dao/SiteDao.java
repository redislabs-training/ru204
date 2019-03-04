package com.redislabs.university.dao;

import com.redislabs.university.api.Coordinate;
import com.redislabs.university.api.Site;

import java.util.List;

public interface SiteDao {
    List<Site> findAll();
    List<Site> findByGeo(Coordinate coordinate, Double radius, String radiusUnit);
    Site findById(Long id);
    void insert(Site site);
}
