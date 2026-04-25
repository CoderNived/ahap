const express = require('express');
const router = express.Router();
const { analyzeText, analyzeVoice, analyzeImage, analyzeVitals } = require('../controllers/analyze.controller');
const { protect } = require('../middleware/auth.middleware');
const { uploadVoice, uploadImage, uploadCSV } = require('../utils/upload');

// POST /api/analyze/text
router.post('/text', protect, analyzeText);

// POST /api/analyze/voice
router.post('/voice', protect, uploadVoice.single('audio'), analyzeVoice);

// POST /api/analyze/image
router.post('/image', protect, uploadImage.single('image'), analyzeImage);

// POST /api/analyze/vitals
router.post('/vitals', protect, uploadCSV.single('vitals'), analyzeVitals);
const multer = require('multer');

// Multer error handler
router.use((err, req, res, next) => {
  if (err instanceof multer.MulterError) {
    if (err.code === 'LIMIT_FILE_SIZE') {
      return res.status(400).json({
        status: 'error',
        message: 'File too large. Maximum size allowed is 5MB for CSV files.',
      });
    }
  }
  next(err);
});
module.exports = router;