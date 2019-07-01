const redis = require('./redis_client');

const remap = (siteHash) => {
  const remappedSiteHash = { ...siteHash };

  remappedSiteHash.id = parseInt(siteHash.id, 10);
  remappedSiteHash.panels = parseInt(siteHash.panels, 10);
  remappedSiteHash.capacity = parseFloat(siteHash.capacity, 10);

  // coordinate is optional.
  if (siteHash.hasOwnProperty('lat') && siteHash.hasOwnProperty('lng')) {
    remappedSiteHash.coordinate = {
      lat: parseFloat(siteHash.lat, 10),
      lng: parseFloat(siteHash.lng, 10),
    };

    // Remove original fields from resulting object.
    delete remappedSiteHash.lat;
    delete remappedSiteHash.lng;
  }

  return remappedSiteHash;
};

const insert = async site => 'Redis TODO';

const findById = async (id) => {
  const client = redis.getClient();

  const siteHash = await client.hgetallAsync(`app:sites:info:${id}`); // TODO generate key names...

  return (siteHash ? remap(siteHash) : null);
};

const findAll = async () => {
  const client = redis.getClient();

  const siteIds = await client.smembersAsync('app:sites:ids'); // TODO generate key names...

  // Lots of Promises...
  // This doesn't deal with string -> int / float conversions...
  // const sites = await Promise.all(siteIds.map(async siteId => client.hgetallAsync(siteId)));

  const sites = await Promise.all(
    siteIds.map(
      async (siteId) => {
        const siteHash = await client.hgetallAsync(siteId);
        return remap(siteHash);
      },
    ),
  );

  // For loop version
  // const sites = [];

  // for (const siteId of siteIds) {
  //   const siteHash = await client.hgetallAsync(siteId);
  
  //   if (siteHash) {
  //     sites.push(remap(siteHash));
  //   }
  // }

  return sites;
};

const findByGeo = async (lat, lng, radius, radiusUnit, onlyExcessCapacity) => 'Redis TODO';

module.exports = {
  insert,
  findById,
  findAll,
  findByGeo,
};
