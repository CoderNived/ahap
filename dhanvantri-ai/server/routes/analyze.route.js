const express = require('express');
const router = express.Router();
const { analyzeText, analyzeVoice, analyzeImage } = require('../controllers/analyze.controller');
const { protect } = require('../middleware/auth.middleware');
const { uploadVoice, uploadImage } = require('../utils/upload');

// POST /api/analyze/text
router.post('/text', protect, analyzeText);

// POST /api/analyze/voice
router.post('/voice', protect, uploadVoice.single('audio'), analyzeVoice);

// POST /api/analyze/image
router.post('/image', protect, uploadImage.single('image'), analyzeImage);

module.exports = router;