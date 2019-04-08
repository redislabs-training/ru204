package com.redislabs.university.RU102J.api;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.time.ZonedDateTime;
import java.util.Objects;

/* Represents a solar meter reading submitted at a particular
 * time through the API. These readings are used to generate
 * charts, to indicate which solar stations have excess
 * capacity, and to maintain leader boards.
 * The temperature is recorded for correlations against energy usage.
 * The kwhUsed and kwhGenerated values represent an amount of energy
 * in the minute the reading was created.
 */
public class MeterReading {
    public Long siteId;
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd hh:mm:ss")
    public ZonedDateTime dateTime;
    public Double kwhUsed;
    public Double kwhGenerated;
    public Double tempC;

    public MeterReading() {}

    @JsonCreator
    public MeterReading(@JsonProperty("siteId") Long siteId,
                        @JsonProperty ("dateTime") ZonedDateTime date,
                        @JsonProperty("kwhUsed") Double kwhUsed,
                        @JsonProperty("kwhGenerated") Double kwhGenerated,
                        @JsonProperty("tempC") Double tempC) {
        this.siteId = siteId;
        this.dateTime = date;
        this.kwhUsed = kwhUsed;
        this.kwhGenerated = kwhGenerated;
        this.tempC = tempC;
    }

    @JsonProperty("siteId")
    public Long getSiteId() {
        return siteId;
    }

    @JsonProperty("siteId")
    public void setSiteId(Long siteId) {
        this.siteId = siteId;
    }

    @JsonProperty("dateTime")
    public ZonedDateTime getDateTime() {
        return dateTime;
    }

    @JsonProperty("dateTime")
    public void setDateTime(ZonedDateTime dateTime) {
        this.dateTime = dateTime;
    }

    @JsonProperty("kwhUsed")
    public Double getKwhUsed() {
        return kwhUsed;
    }

    @JsonProperty("kwhUsed")
    public void setKwhUsed(Double kwhUsed) {
        this.kwhUsed = kwhUsed;
    }

    @JsonProperty("kwhGenerated")
    public Double getKwhGenerated() {
        return kwhGenerated;
    }

    @JsonProperty("kwhGenerated")
    public void setKwhGenerated(Double kwhGenerated) {
        this.kwhGenerated = kwhGenerated;
    }

    @JsonProperty("tempC")
    public Double getTempC() {
        return tempC;
    }

    @JsonProperty("tempC")
    public void setTempC(Double tempC) {
        this.tempC = tempC;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        MeterReading meterReading = (MeterReading) o;
        return Objects.equals(dateTime, meterReading.dateTime) &&
                Objects.equals(kwhUsed, meterReading.kwhUsed) &&
                Objects.equals(kwhGenerated, meterReading.kwhGenerated) &&
                Objects.equals(tempC, meterReading.tempC);
    }

    @Override
    public int hashCode() {
        return Objects.hash(dateTime, kwhUsed, kwhGenerated, tempC);
    }

    @Override
    public String toString() {
        return "MeterReading{" +
                "siteId=" + siteId +
                ", dateTime=" + dateTime +
                ", kwhUsed=" + kwhUsed +
                ", kwhGenerated=" + kwhGenerated +
                ", tempC=" + tempC +
                '}';
    }
}
