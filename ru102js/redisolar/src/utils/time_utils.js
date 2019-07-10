const moment = require('moment');

const getMinuteOfDay = (timestamp) => {
  const ts = moment.unix(timestamp).utc();
  const dayStart = moment.unix(timestamp).utc().startOf('day');

  return ts.diff(dayStart, 'minutes');
};

const getTimestampForMinuteOfDay = (timestamp, minute) => {
  const dayStart = moment.unix(timestamp).utc().startOf('day');

  return dayStart.add(minute, 'minutes').unix();
};

module.exports = {
  getMinuteOfDay,
  getTimestampForMinuteOfDay,
};
