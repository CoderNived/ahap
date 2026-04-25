const express = require('express');
const router = express.Router();
const { analyzeText, analyzeVoice } = require('../controllers/analyze.controller');
const { protect } = require('../middleware/auth.middleware');
const { uploadVoice } = require('../utils/upload');

// POST /api/analyze/text
router.post('/text', protect, analyzeText);

// POST /api/analyze/voice
router.post('/voice', protect, uploadVoice.single('audio'), analyzeVoice);

module.exports = router;