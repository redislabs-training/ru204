package com.redislabs.university;

import com.google.inject.AbstractModule;
import com.google.inject.Provides;
import io.dropwizard.Configuration;
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.JedisPoolConfig;

public class ApplicationModule extends AbstractModule {

    private final JedisPool jedisPool;

    public ApplicationModule(JedisPool jedisPool) {
        this.jedisPool = jedisPool;
    }

    @Provides
    public RediSolarConfiguration configuration(Configuration configuration)
    {
        return (RediSolarConfiguration) configuration;
    }

    @Provides
    public JedisPool provideJedisPool() {
        return jedisPool;
    }
}
