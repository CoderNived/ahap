const OpenAI = require('openai');

const aiClient = new OpenAI({
  apiKey: process.env.GROK_API_KEY,
  baseURL: process.env.GROK_BASE_URL,
});

module.exports = aiClient;