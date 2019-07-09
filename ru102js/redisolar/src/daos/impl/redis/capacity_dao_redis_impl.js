const redis = require('./redis_client');
const keyGenerator = require('./redis_key_generator');

const update = async (meterReading) => {
  const client = redis.getClient();
  const currentCapacity = meterReading.whGenerated - meterReading.whUsed;

  await client.zaddAsync([
    keyGenerator.getCapacityRankingKey(),
    currentCapacity,
    meterReading.siteId,
  ]);
};

const getReport = limit => 'Redis TODO';

const getRank = siteId => 'Redis TODO';

module.exports = {
  update,
  getReport,
  getRank,
};
