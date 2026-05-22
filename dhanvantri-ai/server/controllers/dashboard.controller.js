const Chat = require('../models/Chat');

// ─── Get Dashboard Data ────────────────────────────────────
const getDashboard = async (req, res) => {
  try {
    const userId = req.user.id;

    // Get all active chats with messages
    const chats = await Chat.find({
      userId,
      isActive: true,
    }).select('messages title createdAt lastActivity');

    // ── Aggregate All Messages ─────────────────────────────
    const allMessages = chats.flatMap(chat => chat.messages);
    const aiMessages = allMessages.filter(m => m.role === 'ai');
    const userMessages = allMessages.filter(m => m.role === 'user');

    // ── Symptom Frequency ──────────────────────────────────
    const symptomCount = {};
    aiMessages.forEach(msg => {
      const symptoms = msg.metadata?.symptoms || [];
      symptoms.forEach(symptom => {
        symptomCount[symptom] = (symptomCount[symptom] || 0) + 1;
      });
    });

    const topSymptoms = Object.entries(symptomCount)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .map(([symptom, count]) => ({ symptom, count }));

    // ── Urgency Distribution ───────────────────────────────
    const urgencyCount = { low: 0, medium: 0, high: 0, unknown: 0 };
    aiMessages.forEach(msg => {
      const level = msg.metadata?.urgencyLevel || 'unknown';
      urgencyCount[level] = (urgencyCount[level] || 0) + 1;
    });

    // ── Confidence Trend ───────────────────────────────────
    const confidenceTrend = aiMessages
      .filter(msg => msg.metadata?.confidence !== undefined)
      .slice(-10)
      .map(msg => ({
        timestamp: msg.timestamp,
        confidence: msg.metadata.confidence,
      }));

    // ── Severity Distribution ──────────────────────────────
    const severityCount = {};
    aiMessages.forEach(msg => {
      const severity = msg.metadata?.severity;
      if (severity) {
        severityCount[severity] = (severityCount[severity] || 0) + 1;
      }
    });

    // ── Activity Timeline ──────────────────────────────────
    const activityTimeline = chats
      .slice(-7)
      .map(chat => ({
        date: chat.createdAt,
        title: chat.title,
        messageCount: chat.messages.length,
      }));

    res.status(200).json({
      status: 'success',
      data: {
        summary: {
          totalChats: chats.length,
          totalMessages: allMessages.length,
          totalUserMessages: userMessages.length,
          totalAiResponses: aiMessages.length,
        },
        topSymptoms,
        urgencyDistribution: urgencyCount,
        severityDistribution: severityCount,
        confidenceTrend,
        activityTimeline,
        disclaimer: '⚠️ This dashboard is for informational purposes only. Not a medical diagnosis.',
      },
    });

  } catch (error) {
    res.status(500).json({ status: 'error', message: error.message });
  }
};

module.exports = { getDashboard };