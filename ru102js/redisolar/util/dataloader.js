const path = require('path');

const loadData = filename => {
  const sampleData = require(filename);

  for (const site of sampleData) {
    console.log(site);
  }

  console.log(`Loaded ${sampleData.length} sites.`)
} 

if (process.argv.length !== 4) {
  console.error('Usage: npm run load <path_to_json_data_file>')
} else {
  const filename = process.argv[3];

  try {
    loadData(path.resolve(__dirname, '../', filename));
  } catch (e) {
    console.error(`Error loading ${filename}:`)
    console.error(e)
  }
}
