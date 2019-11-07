const fs = require('fs');
const cheerio = require('cheerio');

const GOOGLE_LINK_PREFIX = 'https://www.google.com/url?q=';
const GOOGLE_REQUEST_PARAMS_START = '&sa=D';
const FILE_ENCODING = 'utf8';

try {
  if (process.argv.length !== 4) {
    console.error('You must provide a filename.');
    process.exit(1);
  }

  const fileName = process.argv[3];
  const htmlFromFile = fs.readFileSync(fileName, FILE_ENCODING);
  const $ = cheerio.load(htmlFromFile);

  $('a').each(function () {
    const href = $(this).attr('href');

    if (href && href.startsWith(GOOGLE_LINK_PREFIX)) {
      const googleParamsStartPos = href.indexOf(GOOGLE_REQUEST_PARAMS_START);

      const newHref = googleParamsStartPos === -1 
        ? href.substring(GOOGLE_LINK_PREFIX.length)
        : href.substring(GOOGLE_LINK_PREFIX.length, googleParamsStartPos);

      $(this).attr('href', decodeURIComponent(newHref));
    }
  });

  const outputFileName = `fixed_${fileName}`;
  fs.writeFileSync(outputFileName, $.root().html(), FILE_ENCODING);
  console.log(`Wrote: ${outputFileName}`);
} catch (e) {
  console.log('Error:', e.stack);
}