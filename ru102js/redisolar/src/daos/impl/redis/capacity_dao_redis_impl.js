const redis = require('./redis_client');
const keyGenerator = require('./redis_key_generator');

const remap = (arr) => {
  const remapped = [];

  for (let n = 0; n < arr.length; n += 2) {
    remapped.push({
      siteId: parseInt(arr[n], 10),
      capacity: parseFloat(arr[n + 1], 10),
    });
  }

  return remapped;
};

const update = async (meterReading) => {
  const client = redis.getClient();
  const currentCapacity = meterReading.whGenerated - meterReading.whUsed;

  await client.zaddAsync(
    keyGenerator.getCapacityRankingKey(),
    currentCapacity,
    meterReading.siteId,
  );
};

const getReport = async (limit) => {
  const client = redis.getClient();
  const capacityRankingKey = keyGenerator.getCapacityRankingKey();
  const pipeline = client.batch();

  pipeline.zrange(capacityRankingKey, 0, limit - 1, 'WITHSCORES');
  pipeline.zrevrange(capacityRankingKey, 0, limit - 1, 'WITHSCORES');

  const results = await pipeline.execAsync();

  return {
    lowestCapacity: remap(results[0]),
    highestCapacity: remap(results[1]),
  };
};

const getRank = async (siteId) => {
  const client = redis.getClient();

  const result = await client.zrevrankAsync(
    keyGenerator.getCapacityRankingKey(),
    `${siteId}`,
  );

  return result;
};

module.exports = {
  update,
  getReport,
  getRank,
};
