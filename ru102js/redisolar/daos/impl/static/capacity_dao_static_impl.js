const update = meterReading => 'Static TODO';

const getReport = limit => ({
  highestCapacity: [{
    capacity: 26.04166666666668,
    siteId: 49,
  }, {
    capacity: 23.369296109745815,
    siteId: 184,
  }, {
    capacity: 21.5625,
    siteId: 150,
  }, {
    capacity: 20.914808589737653,
    siteId: 28,
  }, {
    capacity: 20.65860051923529,
    siteId: 156,
  }, {
    capacity: 19.999999999999986,
    siteId: 114,
  }, {
    capacity: 19.791666666666668,
    siteId: 124,
  }, {
    capacity: 17.463404300591677,
    siteId: 34,
  }, {
    capacity: 17.20265373409468,
    siteId: 5,
  }, {
    capacity: 16.875,
    siteId: 75,
  }, {
    capacity: 16.25,
    siteId: 199,
  }],
  lowestCapacity: [{
    capacity: -31.15831921813782,
    siteId: 16,
  }, {
    capacity: -28.507067761609054,
    siteId: 104,
  }, {
    capacity: -27.70861195348253,
    siteId: 68,
  }, {
    capacity: -26.02601644117098,
    siteId: 205,
  }, {
    capacity: -25.672502203639926,
    siteId: 24,
  }, {
    capacity: -24.84298901858617,
    siteId: 11,
  }, {
    capacity: -23.89569613040233,
    siteId: 42,
  }, {
    capacity: -22.783605785029255,
    siteId: 141,
  }, {
    capacity: -22.720797301112505,
    siteId: 174,
  }, {
    capacity: -22.5857426032668,
    siteId: 96,
  }, {
    capacity: -20.080815379948707,
    siteId: 48,
  }],
});

const getRank = siteId => 'Static TODO';

module.exports = {
  update,
  getReport,
  getRank,
};
