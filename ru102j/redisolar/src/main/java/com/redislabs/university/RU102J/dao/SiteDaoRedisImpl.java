package com.redislabs.university.RU102J.dao;

import com.redislabs.university.RU102J.api.Site;
import com.redislabs.university.RU102J.core.KeyHelper;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;

import java.util.*;

public class SiteDaoRedisImpl implements SiteDao {

    private final JedisPool jedisPool;

    public SiteDaoRedisImpl(JedisPool jedisPool) {
        this.jedisPool = jedisPool;
    }

    // When we insert a site, we set all of its values into a single hash.
    // We then store the site's id in a set for easy access.
    @Override
    public void insert(Site site) {
        try (Jedis jedis = jedisPool.getResource()) {
            String hashKey = RedisSchema.getSiteHashKey(site.getId());
            String siteIdKey = RedisSchema.getSiteIDsSetKey();
            jedis.hmset(hashKey, site.toMap());
            jedis.sadd(siteIdKey, hashKey);
        }
    }

    @Override
    public void updateLatest(Site site, Double currentCapacity) {
    }

    @Override
    public Site findById(Long id) {
        try (Jedis jedis = jedisPool.getResource()) {
            Map<String, String> fields = jedis.hgetAll(RedisSchema.getSiteHashKey(id));
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
            Set<String> keys = jedis.smembers(RedisSchema.getSiteIDsSetKey());
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
}
