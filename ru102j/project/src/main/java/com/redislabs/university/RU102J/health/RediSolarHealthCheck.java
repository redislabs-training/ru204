package com.redislabs.university.RU102J.health;

import com.codahale.metrics.health.HealthCheck;
import com.codahale.metrics.health.HealthCheck.Result;

public class RediSolarHealthCheck extends HealthCheck {

    public RediSolarHealthCheck() {
    }

    @Override
    protected Result check() {
        return Result.healthy();
    }
}
