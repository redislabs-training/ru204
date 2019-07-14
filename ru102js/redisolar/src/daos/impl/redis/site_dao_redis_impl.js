const redis = require('./redis_client');
const keyGenerator = require('./redis_key_generator');

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

const flatten = (site) => {
  const flattenedSite = { ...site };

  if (flattenedSite.hasOwnProperty('coordinate')) {
    flattenedSite.lat = flattenedSite.coordinate.lat;
    flattenedSite.lng = flattenedSite.coordinate.lng;
    delete flattenedSite.coordinate;
  }

  return flattenedSite;
};

const insert = async (site) => {
  const client = redis.getClient();

  const siteHashKey = keyGenerator.getSiteHashKey(site.id);

  await client.hmsetAsync(siteHashKey, flatten(site));
  await client.saddAsync(keyGenerator.getSiteIDsKey(), siteHashKey);

  // Co-ordinates are optional.
  if (site.hasOwnProperty('coordinate')) {
    await client.geoaddAsync(
      keyGenerator.getSiteGeoKey(), 
      site.coordinate.lng, 
      site.coordinate.lat, 
      siteHashKey,
    );
  }

  return siteHashKey;
};

const findById = async (id) => {
  const client = redis.getClient();

  const siteHash = await client.hgetallAsync(keyGenerator.getSiteHashKey(id));

  return (siteHash ? remap(siteHash) : null);
};

const findAll = async () => {
  const client = redis.getClient();

  const siteIds = await client.smembersAsync(keyGenerator.getSiteIDsKey());

  // Lots of Promises...
  // This doesn't deal with string -> int / float conversions...
  // const sites = await Promise.all(siteIds.map(async siteId => client.hgetallAsync(siteId)));

  // const sites = await Promise.all(
  //   siteIds.map(
  //     async (siteId) => {
  //       const siteHash = await client.hgetallAsync(siteId);
  //       return remap(siteHash);
  //     },
  //   ),
  // );

  // For loop version
  const sites = [];

  for (const siteId of siteIds) {
    /* eslint-disable no-await-in-loop */
    const siteHash = await client.hgetallAsync(siteId);
    /* eslint-enable */

    if (siteHash) {
      sites.push(remap(siteHash));
    }
  }

  return sites;
};

const findByGeo = async (lat, lng, radius, radiusUnit, onlyExcessCapacity) => {
  const client = redis.getClient();

  // TODO handling of onlyExcessCapacity...
  const response = client.georadiusAsync(key, lat, lng, radius, radiusUnit);


};

module.exports = {
  insert,
  findById,
  findAll,
  findByGeo,
};
