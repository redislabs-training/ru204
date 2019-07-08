const moment = require('moment');

const meterReadingsController = require('../controllers/meterreadings_controller');

// const metricDao = require('../daos/metric_dao');
// const siteStatsDao = require('../daos/sitestats_dao');
// const capacityDao = require('../daos/capacity_dao');
// const feedDao = require('../daos/feed_dao');

const maxTempC = 30;

const getMaxMinuteWHGenerated = capacity => capacity * 1000 / 24 / 60;

const getInitialMinuteWHUsed = maxCapacity => (
  Math.random() > 0.5 ? maxCapacity + 0.1 : maxCapacity - 0.1
);

const getNextValueInSeries = (current, max) => {
  const stepSize = 0.1 * max;

  if (Math.random() < 0.5) {
    return current + stepSize;
  } else {
    if (current - stepSize < 0) {
      return 0;
    } else {
      return current - stepSize;
    }
  }
};

const getNextValue = max => getNextValueInSeries(max, max);

const generateHistorical = async (site, days) => {
  if (days < 1 || days > 365) {
    throw { error: `Historical data generation requests must be for 1-365 days, not ${days}.` };
  }

  console.log(`Site: ${site.id} - Generating ${days} day${days !== 1 ? 's' : ''} sample data.`);

  const maxCapacity = getMaxMinuteWHGenerated(site.capacity);
  let currentCapacity = getNextValue(maxCapacity);
  let currentTemperature = getNextValue(maxTempC);
  let currentUsage = getInitialMinuteWHUsed(maxCapacity);
  let readingTime = moment().utc();

  const numMinutesToGenerate = (60 * 24 * days);

  for (let n = 0; n < numMinutesToGenerate; n += 1) {
    const meterReading = {
      siteId: site.id,
      dateTime: readingTime.unix(),
      whUsed: currentUsage,
      whGenerated: currentCapacity,
      tempC: currentTemperature,
    };

    await meterReadingsController.createMeterReadings([meterReading]);

    readingTime = readingTime.subtract(1, 'minutes');
    currentTemperature = getNextValue(currentTemperature);
    currentCapacity = getNextValue(currentCapacity, maxCapacity);
    currentUsage = getNextValue(currentUsage, maxCapacity);
  }

  return true;
};

module.exports = {
  generateHistorical,
};
