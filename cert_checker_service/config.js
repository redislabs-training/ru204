export default {
    'PORT': process.env.CERT_PORT || 8080,
    'TAHOEENDPOINT': 'https://university.redis.com/tahoe/api/v1/',
    'APPSEMBLER_TOKEN': `Token ${process.env.APPSEMBLER_PROD}`,
    'LMSDB' : {
        user: process.env.PGUSER,
        host: process.env.PGHOST,
        database: process.env.PGDATABASE,
        password: process.env.PGPASSWORD,
        port: process.env.PGPORT,
      }
}