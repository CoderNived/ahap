const http = require('http');

const ML_SERVICE_URL = process.env.ML_SERVICE_URL || 'http://localhost:8000';

const callMLService = async (endpoint, method = 'GET', body = null) => {
  try {
    const url = `${ML_SERVICE_URL}${endpoint}`;

    const options = {
      method,
      headers: {
        'Content-Type': 'application/json',
      },
    };

    const response = await fetch(url, {
      ...options,
      body: body ? JSON.stringify(body) : null,
    });

    if (!response.ok) {
      throw new Error(`ML Service error: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    return data;

  } catch (error) {
    throw new Error(`Failed to reach ML service: ${error.message}`);
  }
};

module.exports = { callMLService, ML_SERVICE_URL };