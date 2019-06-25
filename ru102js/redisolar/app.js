const express = require('express');
const morgan = require('morgan');
const bodyParser = require('body-parser');
const cors = require('cors');
const path = require('path');
const logger = require('./util/logger');
const routes = require('./routes');
const banner = require('./util/banner');

const port = process.env.port || 8080; // TODO from config.json
const app = express();

app.use(morgan('combined', { stream: logger.stream }));
app.use(bodyParser.json());
app.use(cors());
app.use(express.static(path.join(__dirname, 'public')));
app.use('/api', routes);

app.listen(port, () => {
  banner();
  logger.info(`RediSolar listening on port: ${port}`);
});
