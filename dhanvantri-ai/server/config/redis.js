const Redis = require('ioredis');

let redis = null;

const connectRedis = () => {
  try {
    redis = new Redis({
      host: process.env.REDIS_HOST || 'localhost',
      port: process.env.REDIS_PORT || 6379,
      retryStrategy: (times) => {
        if (times > 3) {
          console.log('⚠️  Redis unavailable — caching disabled');
          return null;
        }
        return Math.min(times * 100, 3000);
      },
    });

    redis.on('connect', () => {
      console.log('✅ Redis Connected');
    });

    redis.on('error', (err) => {
      console.log('⚠️  Redis Error:', err.message);
    });

  } catch (error) {
    console.log('⚠️  Redis setup failed:', error.message);
  }

  return redis;
};

const getRedis = () => redis;

module.exports = { connectRedis, getRedis };