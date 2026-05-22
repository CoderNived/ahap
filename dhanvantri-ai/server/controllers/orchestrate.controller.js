const { orchestrateAnalysis } = require('../services/mlService');

const orchestrate = async (req, res) => {
  try {
    const { text } = req.body;
    const imagePath = req.files?.image?.[0]?.path || null;
    const vitalsPath = req.files?.vitals?.[0]?.path || null;

    if (!text && !imagePath && !vitalsPath) {
      return res.status(400).json({
        status: 'error',
        message: 'At least one input required: text, image, or vitals CSV',
      });
    }

    const result = await orchestrateAnalysis(text, imagePath, vitalsPath);

    res.status(200).json({
      status: 'success',
      data: {
        input: { text, hasImage: !!imagePath, hasVitals: !!vitalsPath },
        orchestration: result.success ? result.data : null,
        error: result.success ? null : result.error,
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

module.exports = { orchestrate };