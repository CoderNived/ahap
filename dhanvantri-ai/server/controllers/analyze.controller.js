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

    // Placeholder response — NLP module connects here in Phase 5
    const response = {
      input: text,
      type: 'text',
      status: 'received',
      message: 'Text received successfully. NLP analysis coming in Phase 5.',
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

module.exports = { analyzeText, analyzeVoice };