const redis = require('../redis_client');

let sha;

const getSource = () => `
  local key = KEYS[1]
  local field = ARGV[1]
  local value = ARGV[2] 
  local op = ARGV[3]
  local current = redis.call('hget', key, field)
  if (current == false or current == nil) then
    redis.call('hset', key, field, value)
  elseif op == '>' then
    if tonumber(value) > tonumber(current) then
      redis.call('hset', key, field, value)
    end
  elseif op == '<' then
    if tonumber(value) < tonumber(current) then
      redis.call('hset', key, field, value)
    end
  end `;

const getSha = async () => {
  // Load script on first use...
  if (! sha) {
    const client = redis.getClient();
    sha = await client.scriptAsync('load', getSource());
  }

  return sha;
};

module.exports = {
  getSha,
};
