const insert = site => 'Static TODO';

const findById = id => [{
  id,
  capacity: 7.5,
  panels: 5,
  address: '894 Windmill Park Lane ',
  city: 'Mountain View',
  state: 'CA',
  postalCode: '94043',
  coordinate: {
    lng: -122.077478,
    lat: 37.399505,
  },
  lastReportingTime: 1560967216.141000000,
  meterReadingCount: 180,
}];

const findAll = () => [{
  id: 149,
  capacity: 9.0,
  panels: 6,
  address: '856 Milton Street ',
  city: 'Oakland',
  state: 'CA',
  postalCode: '94607',
  coordinate: {
    lng: -122.276749,
    lat: 37.817176,
  },
  lastReportingTime: 1560967226.262000000,
  meterReadingCount: 180,
}, {
  id: 31,
  capacity: 7.5,
  panels: 5,
  address: '894 Windmill Park Lane ',
  city: 'Mountain View',
  state: 'CA',
  postalCode: '94043',
  coordinate: {
    lng: -122.077478,
    lat: 37.399505,
  },
  lastReportingTime: 1560967216.141000000,
  meterReadingCount: 180,
}];

const findByGeo = query => [{
  id: 149,
  capacity: 9.0,
  panels: 6,
  address: '856 Milton Street ',
  city: 'Oakland',
  state: 'CA',
  postalCode: '94607',
  coordinate: {
    lng: -122.276749,
    lat: 37.817176,
  },
  lastReportingTime: 1560967226.262000000,
  meterReadingCount: 180,
}, {
  id: 31,
  capacity: 7.5,
  panels: 5,
  address: '894 Windmill Park Lane ',
  city: 'Mountain View',
  state: 'CA',
  postalCode: '94043',
  coordinate: {
    lng: -122.077478,
    lat: 37.399505,
  },
  lastReportingTime: 1560967216.141000000,
  meterReadingCount: 180,
}];

module.exports = {
  insert,
  findById,
  findAll,
  findByGeo,
};
