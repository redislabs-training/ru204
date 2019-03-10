package com.redislabs.university.RU102J.api;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.time.LocalDateTime;
import java.util.Objects;

/* Represents a solar meter reading submitted at a particular
 * time through the API. These readings are used to generate
 * charts, to indicate which solar stations have excess
 * capacity, and to maintain leader boards.
 * The temperature is recorded for correlations against energy usage.
 */
public class MeterReading {
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "dd-MM-yyyy hh:mm:ss")
    public Long siteId;
    public LocalDateTime dateTime;
    public Double kwhUsed;
    public Double kwhGenerated;
    public Double tempC;
    public ReportType type;

    public MeterReading() {}

    public MeterReading(Long siteId, LocalDateTime date, Double kwhUsed, Double kwhGenerated, Double tempC, ReportType type) {
        this.siteId = siteId;
        this.dateTime = date;
        this.kwhUsed = kwhUsed;
        this.kwhGenerated = kwhGenerated;
        this.tempC = tempC;
        this.type = type;
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
    public Double getKwhUsed() {
        return kwhUsed;
    }

    @JsonProperty
    public void setKwhUsed(Double kwhUsed) {
        this.kwhUsed = kwhUsed;
    }

    @JsonProperty
    public Double getKwhGenerated() {
        return kwhGenerated;
    }

    @JsonProperty
    public void setKwhGenerated(Double kwhGenerated) {
        this.kwhGenerated = kwhGenerated;
    }

    @JsonProperty
    public Double getTempC() {
        return tempC;
    }

    @JsonProperty
    public void setTempC(Double tempC) {
        this.tempC = tempC;
    }

    @JsonProperty
    public ReportType getType() {
        return type;
    }

    @JsonProperty
    public void setType(ReportType type) {
        this.type = type;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        MeterReading meterReading = (MeterReading) o;
        return Objects.equals(dateTime, meterReading.dateTime) &&
                Objects.equals(kwhUsed, meterReading.kwhUsed) &&
                Objects.equals(kwhGenerated, meterReading.kwhGenerated) &&
                Objects.equals(tempC, meterReading.tempC) &&
                type == meterReading.type;
    }

    @Override
    public int hashCode() {
        return Objects.hash(dateTime, kwhUsed, kwhGenerated, tempC, type);
    }

    @Override
    public String toString() {
        return "MeterReading{" +
                "dateTime=" + dateTime +
                ", kwhUsed=" + kwhUsed +
                ", kwhGenerated=" + kwhGenerated +
                ", tempC=" + tempC +
                ", type=" + type +
                '}';
    }
}
