package com.redislabs.university.RU102J.api;

public enum ValueUnit {
    WHGenerated("whG"),
    WHUsed("whU"),
    TemperatureCelcius("tempC");

    private final String shortName;

    ValueUnit(String shortName) {
        this.shortName = shortName;
    }

    public String getShortName() {
        return shortName;
    }
}
