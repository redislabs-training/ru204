const
  argv = require('yargs')
    .demandOption(['source', 'connection'])
    .boolean('flush')
    .boolean('drop')
    .number('totaldocs')
    .argv,
  csv = require('csv'),
  fs = require('fs'),
  redis = require('redis'),
  _ = require('lodash'),
  connection = require(argv.connection),
  redisearch = require('redis-redisearch'),
  idx = argv.idx || 'permits',
  parser = csv.parse({
    columns: true
  }),
  ProgressBar = require('ascii-progress'),
  parsedDocs = new ProgressBar({
    current: 0,
    schema: 'Parsed   [:bar] :current/:total :percent :elapseds :etas'
  }),
  ingestedDocsBar = new ProgressBar({
    current: 0,
    schema: 'Ingested [:bar] :current/:total :percent :elapseds :etas (Pipeline :pipeline)'
  }),
  speedBar = new ProgressBar({
    current: 0,
    schema: 'Speed    [:bar] :current docs/sec, ~:total doc/sec max'
  });

redisearch(redis);

if (argv.totaldocs) {
  ingestedDocsBar.total = parsedDocs.total = argv.totaldocs;
}

let
  docs = 0,
  i = 0,
  client = redis.createClient(connection),
  clients = [],
  startTime = Date.now();

for (let c = 0; c < 100; c += 1) {
  clients.push(client.duplicate());
}

if (argv.flush || argv.drop) {
  let createBatch = client.batch();

  if (argv.flush) { createBatch.flushdb(); }
  if (argv.drop) { createBatch.ft_drop(idx); }
  createBatch
    .ft_create(
      idx, "SCHEMA",
      "permit_timestamp", "NUMERIC", "SORTABLE",
      "job_category", "TEXT", "NOSTEM",
      "address", "TEXT", "NOSTEM",
      "neighbourhood", "TAG", "SORTABLE",
      "description", "TEXT",
      "building_type", "TEXT", "WEIGHT", "20", "NOSTEM", "SORTABLE",
      "work_type", "TEXT", "NOSTEM", "SORTABLE",
      "floor_area", "NUMERIC", "SORTABLE",
      "construction_value", "NUMERIC", "SORTABLE",
      "zoning", "TAG",
      "units_added", "NUMERIC", "SORTABLE",
      "location", "GEO",
      function (err) {
        if (err) { throw err; }
      }
    ).exec(function (err) {
      if (err) { throw err; }
      console.log('Created index. Starting ingest.');
      fs.createReadStream(argv.source).pipe(parser);

    })
} else {
  console.log('Starting ingest.');
  fs.createReadStream(argv.source).pipe(parser);
}


parser.on('readable', function () {                                         // when the stream gets a readable chunk
  while (record = parser.read()) {
    let transformedRecord = {};
    i += 1;
    let docId = record['PERMIT_NUMBER'];
    transformedRecord.permit_timestamp = Math.round(new Date(record['PERMIT_DATE']).getTime() / 1000);
    transformedRecord.job_category = record['JOB_CATEGORY'];
    transformedRecord.address = record['ADDRESS'];
    transformedRecord.legal_description = record['LEGAL_DESCRIPTION']; // no index
    transformedRecord.description = record['JOB_DESCRIPTION'];
    transformedRecord.building_type = record['BUILDING_TYPE'].replace(/\s+\(\d+\)/gi, '');
    transformedRecord.work_type = record['WORK_TYPE'].replace(/\(\d+\)\s/gi, '');
    transformedRecord.floor_area = Number(record['FLOOR_AREA'].replace(/\,/gi, ''));
    transformedRecord.construction_value = Number(record['CONSTRUCTION_VALUE'].replace(/\,/gi, ''));

    transformedRecord.units_added = Number(record['UNITS_ADDED']);
    let latitude = Number(record['LATITUDE']);
    let longitude = Number(record['LONGITUDE']);
    let zoning = record['ZONING'].split(/\s*,\s*/gi);;
    let neighbourhood = record['NEIGHBOURHOOD'].split(/\s*,\s*/gi);


    let args = [].concat(
      [idx, docId, 1, 'FIELDS'],
      _(transformedRecord).toPairs().flatten().value(),
      [
        'zoning',
        zoning.join(','),
        'neighbourhood',
        neighbourhood.join(',')
      ],
      ['location', `${longitude},${latitude}`]
    );

    _.sample(clients).ft_add(
      args,
      function (err, results) {
        if (err) { throw err; }
        docs += 1;
      }
    );
  }                       // handled CSV errors (should be none)
});
let interval = setInterval(function () {
  if (!argv.totaldocs) {
    ingestedDocsBar.total = i;
  } else {
    parsedDocs.current = i;
    parsedDocs.tick(0);
  }
  ingestedDocsBar.current = docs;
  ingestedDocsBar.tick(0, { pipeline: i - docs });


  if ((csvPermitsLeft === false) && (i === docs)) {
    let totalTime = Math.round((Date.now() - startTime) / 1000);
    console.log(`Ingested ${docs} documents in ${totalTime} seconds. Average rate ${Math.round(i / totalTime)} docs/sec`);
    client.quit();
    clients.forEach(function (aClient) {
      aClient.quit();
    })
    clearInterval(interval);
  }
}, 250);
let speedHighmark = 0; 0
let lastDocs = 0;

let speedInterval = setInterval(() => {
  let docsSec = docs - lastDocs;
  lastDocs = docs;
  if (docsSec > speedHighmark) {
    speedHighmark = docsSec;
    speedBar.total = speedHighmark + 1;
  }

  speedBar.current = docsSec;
  speedBar.tick(0);


  if ((csvPermitsLeft === false) && (i === docs)) {
    clearInterval(speedInterval);
  }
}, 1000);

parser.on('error', function (err) {                                         // when the last readable chunk has been procssed
  console.log('csv parse err', err.message);
});
let csvPermitsLeft;
parser.on('finish', function () {
  csvPermitsLeft = false;

});