const { analyzeWithAI } = require('../services/ai.service');
// ─── Text Analysis ────────────────────────────────────────
const analyzeText = async (req, res) => {
  try {
    const { text } = req.body;

    // Validate input
    if (!text || text.trim().length === 0) {
      return res.status(400).json({
        status: 'error',
        message: 'Text input is required',
      });
    }

    if (text.trim().length < 10) {
      return res.status(400).json({
        status: 'error',
        message: 'Please provide more detail — minimum 10 characters',
      });
    }

    // Call Grok AI
    const aiResult = await analyzeWithAI(text);

    if (!aiResult.success) {
      return res.status(500).json({
        status: 'error',
        message: 'AI analysis failed. Please try again.',
        detail: aiResult.error,
      });
    }

    res.status(200).json({
      status: 'success',
      data: {
        input: text,
        type: 'text',
        analysis: aiResult.data,
        timestamp: new Date().toISOString(),
        userId: req.user.id,
      },
    });

  } catch (error) {
    res.status(500).json({
      status: 'error',
      message: error.message,
    });
  }
};
// ─── Voice Analysis ────────────────────────────────────────
const analyzeVoice = async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({
        status: 'error',
        message: 'Audio file is required',
      });
    }

    const response = {
      file: req.file.filename,
      originalName: req.file.originalname,
      size: req.file.size,
      type: 'voice',
      status: 'received',
      message: 'Audio file received. Speech-to-text coming in Phase 5.',
      disclaimer: '⚠️ This is not a medical diagnosis. Please consult a healthcare professional.',
      timestamp: new Date().toISOString(),
      userId: req.user.id,
    };

    res.status(200).json({
      status: 'success',
      data: response,
    });

  } catch (error) {
    res.status(500).json({
      status: 'error',
      message: error.message,
    });
  }
};
// ─── Image Analysis ────────────────────────────────────────
const analyzeImage = async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({
        status: 'error',
        message: 'Image file is required',
      });
    }

    const response = {
      file: req.file.filename,
      originalName: req.file.originalname,
      size: req.file.size,
      mimeType: req.file.mimetype,
      type: 'image',
      status: 'received',
      message: 'Image received. Computer vision analysis coming in Phase 6.',
      disclaimer: '⚠️ This is not a medical diagnosis. Please consult a healthcare professional.',
      timestamp: new Date().toISOString(),
      userId: req.user.id,
    };

    res.status(200).json({
      status: 'success',
      data: response,
    });

  } catch (error) {
    res.status(500).json({
      status: 'error',
      message: error.message,
    });
  }
};
// ─── Vitals Analysis ───────────────────────────────────────
const analyzeVitals = async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({
        status: 'error',
        message: 'CSV file is required',
      });
    }

    const response = {
      file: req.file.filename,
      originalName: req.file.originalname,
      size: req.file.size,
      type: 'vitals',
      status: 'received',
      message: 'Vitals CSV received. Time-series forecasting coming in Phase 7.',
      disclaimer: '⚠️ This is not a medical diagnosis. Please consult a healthcare professional.',
      expectedFormat: {
        columns: ['timestamp', 'heart_rate', 'blood_pressure_sys', 'blood_pressure_dia', 'temperature', 'spo2'],
        example: '2026-01-01 08:00,72,120,80,98.6,99'
      },
      timestamp: new Date().toISOString(),
      userId: req.user.id,
    };

    res.status(200).json({
      status: 'success',
      data: response,
    });

  } catch (error) {
    res.status(500).json({
      status: 'error',
      message: error.message,
    });
  }
};
module.exports = { analyzeText, analyzeVoice, analyzeImage, analyzeVitals };