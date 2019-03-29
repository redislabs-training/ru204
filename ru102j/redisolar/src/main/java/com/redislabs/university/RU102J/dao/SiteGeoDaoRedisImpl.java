package com.redislabs.university.RU102J.dao;

import com.redislabs.university.RU102J.api.Coordinate;
import com.redislabs.university.RU102J.api.Site;
import com.redislabs.university.RU102J.core.KeyHelper;
import redis.clients.jedis.GeoRadiusResponse;
import redis.clients.jedis.GeoUnit;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;

import java.util.*;
import java.util.stream.Collectors;

public class SiteGeoDaoRedisImpl implements SiteGeoDao {
    private JedisPool jedisPool;

    public SiteGeoDaoRedisImpl(JedisPool jedisPool) {
        this.jedisPool = jedisPool;
    }

    @Override
    public Site findById(long id) {
        try (Jedis jedis = jedisPool.getResource()) {
            Map<String, String> fields = jedis.hgetAll(getSiteHashKey(id));
            if (fields != null && !fields.isEmpty())  {
                return new Site(fields);
            } else {
                return null;
            }
        }
    }

    @Override
    public Set<Site> findAll() {
        try (Jedis jedis = jedisPool.getResource()) {
            Set<String> keys = jedis.zrange(getSiteGeoKey(), 0, -1);
            Set<Site> sites = new HashSet<>();
            for (String key : keys) {
                Map<String, String> site = jedis.hgetAll(key);
                if (!site.isEmpty()) {
                    sites.add(new Site(site));
                }
            }
            return sites;
        }
    }

    @Override
    public Set<Site> findByGeo(Coordinate coord, Double radius, String radiusUnit) {
        try (Jedis jedis = jedisPool.getResource()) {
            List<GeoRadiusResponse> radiusResponses = jedis.georadius(getSiteGeoKey(), coord.getLng(), coord.getLat(),
                    radius, GeoUnit.valueOf(radiusUnit));
            List<Site> sites = radiusResponses.stream()
                    .map(response -> jedis.hgetAll(response.getMemberByString()))
                    .filter(Objects::nonNull)
                    .map(Site::new)
                    .collect(Collectors.toList());

            return new HashSet<Site>(sites);
        }
    }

     @Override
    public void insert(Site site) {
         try (Jedis jedis = jedisPool.getResource()) {
             String key = getSiteHashKey(site.getId());
             jedis.hmset(key, site.toMap());

             if (site.getCoordinate() != null) {
                 Double longitude = site.getCoordinate().getGeoCoordinate().getLongitude();
                 Double latitude = site.getCoordinate().getGeoCoordinate().getLatitude();
                 jedis.geoadd(getSiteGeoKey(), longitude, latitude, key);
             }
         }
    }

    private String getSiteHashKey(Long id) {
        return KeyHelper.getKey("sites:info:" + id);
    }

    private String getSiteGeoKey() {
        return KeyHelper.getKey("sites:geo");
    }
}
