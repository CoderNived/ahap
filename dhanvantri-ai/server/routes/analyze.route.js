const express = require('express');
const router = express.Router();
const { analyzeText } = require('../controllers/analyze.controller');
const { protect } = require('../middleware/auth.middleware');

// POST /api/analyze/text — protected route
router.post('/text', protect, analyzeText);

module.exports = router;