package com.redislabs.university;

import com.redislabs.university.command.LoadCommand;
import com.redislabs.university.dao.SiteRedisDao;
import com.redislabs.university.health.RediSolarHealthCheck;
import com.redislabs.university.resources.Sites;
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
    }

    @Override
    public void run(final RediSolarConfiguration configuration,
                    final Environment environment) {
        // TODO: Make jedisPool a Managed object
        RedisConfig redisConfig = configuration.getRedisConfig();
        JedisPool jedisPool = new JedisPool(new JedisPoolConfig(), redisConfig.getHost(),
                redisConfig.getPort());

        // Create resources
        // TODO: Consider using a DI framework here
        Sites installationResource = new Sites(new SiteRedisDao(jedisPool));
        environment.jersey().register(installationResource);

        // Set up health checks
        // TODO: Create a Redis health check
        RediSolarHealthCheck healthCheck = new RediSolarHealthCheck();
        environment.healthChecks().register("healthy", healthCheck);
    }

}
