package com.redislabs.university.RU102J;

import com.redislabs.university.RU102J.command.LoadCommand;
import com.redislabs.university.RU102J.command.RunCommand;
import com.redislabs.university.RU102J.dao.CapacityDaoRedisImpl;
import com.redislabs.university.RU102J.dao.FeedDaoRedisImpl;
import com.redislabs.university.RU102J.dao.MetricDaoRedisZsetImpl;
import com.redislabs.university.RU102J.dao.SiteDaoRedisImpl;
import com.redislabs.university.RU102J.health.RediSolarHealthCheck;
import com.redislabs.university.RU102J.resources.CapacityResource;
import com.redislabs.university.RU102J.resources.MeterReadingResource;
import com.redislabs.university.RU102J.resources.MetricsResource;
import com.redislabs.university.RU102J.resources.SiteResource;
import io.dropwizard.Application;
import io.dropwizard.assets.AssetsBundle;
import io.dropwizard.setup.Bootstrap;
import io.dropwizard.setup.Environment;
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.JedisPoolConfig;

public class RediSolarApplication extends Application<RediSolarConfiguration> {

    public static void main(final String[] args) throws Exception {
        new RediSolarApplication().run(args);
    }

    @Override
    public String getName() {
        return "RediSolar";
    }

    @Override
    public void initialize(final Bootstrap<RediSolarConfiguration> bootstrap) {
        bootstrap.addBundle(new AssetsBundle("/dashboard/dist", "/", "index.html"));
        bootstrap.addCommand(new LoadCommand());
        bootstrap.addCommand(new RunCommand());
    }

    @Override
    public void run(final RediSolarConfiguration configuration,
                    final Environment environment) {
        // TODO: Make jedisPool a Managed object
        RedisConfig redisConfig = configuration.getRedisConfig();
        JedisPool jedisPool = new JedisPool(new JedisPoolConfig(), redisConfig.getHost(),
                redisConfig.getPort());

        // Create resources and inject dependencies
        SiteResource siteResource = new SiteResource(new SiteDaoRedisImpl(jedisPool));
        environment.jersey().register(siteResource);

        MetricsResource metricsResource = new MetricsResource(new MetricDaoRedisZsetImpl(jedisPool));
        environment.jersey().register(metricsResource);

        CapacityResource capacityResource =
                new CapacityResource(new CapacityDaoRedisImpl(jedisPool));
        environment.jersey().register(capacityResource);

        MeterReadingResource meterResource =
                new MeterReadingResource(new SiteDaoRedisImpl(jedisPool),
                        new MetricDaoRedisZsetImpl(jedisPool),
                        new CapacityDaoRedisImpl(jedisPool),
                        new FeedDaoRedisImpl(jedisPool));
        environment.jersey().register(meterResource);

        // Set up health checks
        // TODO: Create a Redis health check
        RediSolarHealthCheck healthCheck = new RediSolarHealthCheck();
        environment.healthChecks().register("healthy", healthCheck);
    }

}
