const config = require('better-config');

config.set('config.json');

const express = require('express');
const morgan = require('morgan');
const bodyParser = require('body-parser');
const cors = require('cors');
const path = require('path');
const logger = require('./util/logger');
const routes = require('./routes');
const banner = require('./util/banner');

const app = express();


app.use(morgan('combined', { stream: logger.stream }));
app.use(bodyParser.json());
app.use(cors());
app.use(express.static(path.join(__dirname, 'public')));
app.use('/api', routes);

const port = config.get('server.port');

app.listen(port, () => {
  banner();
  logger.info(`RediSolar listening on port: ${port}`);
});
