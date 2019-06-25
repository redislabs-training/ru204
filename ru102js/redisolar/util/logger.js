const winston = require('winston');
const config = require('better-config');

const logger = winston.createLogger({
  level: config.get('server.logLevel'),
  transports: [
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        winston.format.simple(),
      ),
    }),
  ],
});

logger.stream = {
  write: (message) => {
    logger.info(message);
  },
};

module.exports = logger;
