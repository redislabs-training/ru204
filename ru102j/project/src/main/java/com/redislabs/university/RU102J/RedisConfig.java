package com.redislabs.university.RU102J;

import com.fasterxml.jackson.annotation.JsonProperty;

public class RedisConfig {
    public static final String DEFAULT_HOST = "localhost";
    public static final Integer DEFAULT_PORT = 6379;
    public String host;
    public Integer port;

    @JsonProperty
    public String getHost() {
        if (host == null) {
            return DEFAULT_HOST;
        } else {
            return host;
        }
    }

    @JsonProperty
    public void setHost(String host) {
        this.host = host;
    }

    @JsonProperty
    public Integer getPort() {
        if (port == null) {
            return DEFAULT_PORT;
        } else {
            return port;
        }
    }

    @JsonProperty
    public void setPort(Integer port) {
        this.port = port;
    }
}
