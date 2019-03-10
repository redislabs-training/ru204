package com.redislabs.university.RU102J.dao;

import com.redislabs.university.RU102J.api.Coordinate;
import com.redislabs.university.RU102J.api.Site;
import redis.clients.jedis.GeoRadiusResponse;
import redis.clients.jedis.GeoUnit;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;

import java.util.*;
import java.util.stream.Collectors;

public class SiteRedisDao implements SiteDao {

    private final JedisPool jedisPool;

    public SiteRedisDao(JedisPool jedisPool) {
        this.jedisPool = jedisPool;
    }

    // We know that all sites are stored in the
    // the sorted set that backs our geo index. Therefore,
    // we can run the ZRANGE command on the sorted set
    // to get all of its elements.
    @Override
    public List<Site> findAll() {
        try (Jedis jedis = jedisPool.getResource()) {
            Set<String> keys = jedis.zrange(getSiteGeoKey(), 0, -1);
            List<Site> sites = new ArrayList<>();
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
    public List<Site> findByGeo(Coordinate coord, Double radius, String radiusUnit) {
        try (Jedis jedis = jedisPool.getResource()) {
            List<GeoRadiusResponse> radiusResponses = jedis.georadius(getSiteGeoKey(), coord.getLng(), coord.getLat(),
                    radius, GeoUnit.valueOf(radiusUnit));
            List<Site> sites = radiusResponses.stream()
                    .map(response -> jedis.hgetAll(response.getMemberByString()))
                    .filter(Objects::nonNull)
                    .map(Site::new)
                    .collect(Collectors.toList());

            return sites;
        }
    }

    @Override
    public Site findById(Long id) {
        try (Jedis jedis = jedisPool.getResource()) {
            Map<String, String> fields = jedis.hgetAll(getSiteHashKey(id));
            if (fields != null && !fields.isEmpty()) {
                return new Site(fields);
            } else {
                return null;
            }
        }
    }

    // When we insert a site, we add its values as a hash,
    // and we put it into a geo key as well.
    @Override
    public void insert(Site site) {
        try (Jedis jedis = jedisPool.getResource()) {
            String key = getSiteHashKey(site.getId());
            jedis.hmset(key, site.toMap());

            Double longitude = site.getCoordinate().getGeoCoordinate().getLongitude();
            Double latitude = site.getCoordinate().getGeoCoordinate().getLatitude();
            jedis.geoadd(getSiteGeoKey(), longitude, latitude, key);
        }
    }

    private String getSiteHashKey(Long id) {
        return "sites:info:" + id;
    }

    private String getSiteGeoKey() {
        return "sites:geo";
    }
}
