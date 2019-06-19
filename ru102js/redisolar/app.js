const express = require('express');
const path = require('path');
const routes = require('./routes');
const banner = require('./resources/banner');

const port = process.env.port || 8080;
const app = express();

app.use(express.static(path.join(__dirname, 'public')));
app.use('/api', routes);

app.listen(port, () => {
  banner();
  console.log(`RediSolar listening on port: ${port}`);
});
