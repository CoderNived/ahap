const OpenAI = require('openai');
const path = require('path');
require('dotenv').config({ path: path.resolve(__dirname, '../../.env') });

const aiClient = new OpenAI({
  apiKey: process.env.GROK_API_KEY,
  baseURL: process.env.GROK_BASE_URL,
});

module.exports = aiClient;