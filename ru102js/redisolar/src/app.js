const config = require('better-config');

config.set('../config.json');

const express = require('express');
const morgan = require('morgan');
const bodyParser = require('body-parser');
const cors = require('cors');
const path = require('path');
const logger = require('./utils/logger');
const routes = require('./routes');
const banner = require('./utils/banner');

const app = express();

app.use(morgan('combined', { stream: logger.stream }));
app.use(bodyParser.json());
app.use(cors());
app.use(express.static(path.join(__dirname, '../public')));
app.use('/api', routes);

const port = config.get('application.port');

const capacityDao = require('./daos/capacity_dao');

console.log(capacityDao.update({}));

app.listen(port, () => {
  banner();
  logger.info(`RediSolar listening on port ${port}, using database: ${config.get('application.dataStore')}`);
});
