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

const analyzeTextNLP = async (text) => {
  try {
    const result = await callMLService('/api/nlp/analyze', 'POST', { text });
    return { success: true, data: result.data };
  } catch (error) {
    return { success: false, error: error.message };
  }
};
const forecastVitals = async (filePath) => {
  try {
    const fs = require('fs');
    const path = require('path');

    const fileBuffer = fs.readFileSync(filePath);
    const fileName = path.basename(filePath);

    const boundary = '----FormBoundary' + Date.now();

    const body = Buffer.concat([
      Buffer.from(`--${boundary}\r\nContent-Disposition: form-data; name="file"; filename="${fileName}"\r\nContent-Type: text/csv\r\n\r\n`),
      fileBuffer,
      Buffer.from(`\r\n--${boundary}\r\nContent-Disposition: form-data; name="steps"\r\n\r\n3\r\n--${boundary}--\r\n`)
    ]);

    const response = await fetch(`${ML_SERVICE_URL}/api/forecast/analyze`, {
      method: 'POST',
      body: body,
      headers: {
        'Content-Type': `multipart/form-data; boundary=${boundary}`,
        'Content-Length': body.length,
      },
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Forecast service error: ${response.status} - ${errorText}`);
    }

    const data = await response.json();
    return { success: true, data: data.data };

  } catch (error) {
    return { success: false, error: error.message };
  }
};
module.exports = { callMLService, analyzeTextNLP, forecastVitals, ML_SERVICE_URL };