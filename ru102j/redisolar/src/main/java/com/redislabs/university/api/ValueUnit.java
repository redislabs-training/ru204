package com.redislabs.university.api;

public enum ValueUnit {
    KWHGenerated("kwhG"),
    KWHUsed("kwhU"),
    TemperatureCelcius("tempC");

    private final String shortName;

    ValueUnit(String shortName) {
        this.shortName = shortName;
    }

    public String getShortName() {
        return shortName;
    }
}
