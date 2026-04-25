const express = require('express');
const router = express.Router();
const { callMLService } = require('../services/mlService');

// GET /api/ml/health - Check ML service health
router.get('/health', async (req, res) => {
  try {
    const response = await callMLService('/api/health');
    res.status(200).json({
      status: 'ok',
      ml_service: response,
    });
  } catch (error) {
    res.status(503).json({
      status: 'error',
      message: 'ML service is unavailable',
      detail: error.message,
    });
  }
});

module.exports = router;