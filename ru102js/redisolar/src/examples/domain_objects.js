/* eslint-disable no-unused-vars */

// Site
const site = {
  id: 1,
  capacity: 4.5,
  panels: 3,
  address: '637 Britannia Drive',
  city: 'Vallejo',
  state: 'CA',
  postalCode: '94591',
  coordinate: {
    lat: 38.10476999999999,
    lng: -122.193849,
  },
};

// Meter Reading
const meterReading = {
  siteId: 999,
  dateTime: 1563985143,
  whUsed: 12.2,
  whGenerated: 20.1,
  tempC: 20,
};

// Measurement
// metric_dao_redis_impl, would need to be synthesized out of it...
const measurement = {
  siteId: 114,
  dateTime: 1563897660,
  value: 4.54,
  metricUnit: 'whGenerated',
};

// Site Stat
const siteStat = {
  lastReportingTime: 1563985467,
  meterReadingCount: 1,
  maxWhGenerated: 12.3,
  minWhGenerated: 12.3,
  maxCapacity: -10.09,
};

/* eslint-enable */
