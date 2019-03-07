package com.redislabs.university.api;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.time.LocalDateTime;

/* Model class used to represent a single measurement
 * at a particular time. These objects are returned in API
 * calls that may request a series of points for a chart, for
 * example. */
public class Measurement {
    public Long siteId;
    public LocalDateTime dateTime;
    public Double value;
    public ValueUnit valueUnit;

    public Measurement() {}

    public Measurement(Long siteId, ValueUnit valueUnit, LocalDateTime date, Double value) {
        this.siteId = siteId;
        this.valueUnit = valueUnit;
        this.dateTime = date;
        this.value = value;
    }

    @JsonProperty
    public Long getSiteId() {
        return siteId;
    }

    @JsonProperty
    public void setSiteId(Long siteId) {
        this.siteId = siteId;
    }

    @JsonProperty
    public LocalDateTime getDateTime() {
        return dateTime;
    }

    @JsonProperty
    public void setDateTime(LocalDateTime dateTime) {
        this.dateTime = dateTime;
    }

    @JsonProperty
    public Double getValue() {
        return value;
    }

    @JsonProperty
    public void setValue(Double value) {
        this.value = value;
    }

    @JsonProperty
    public ValueUnit getValueUnit() {
        return valueUnit;
    }

    @JsonProperty
    public void setValueUnit(ValueUnit valueUnit) {
        this.valueUnit = valueUnit;
    }
}
