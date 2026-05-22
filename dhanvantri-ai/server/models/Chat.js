const mongoose = require('mongoose');

const messageSchema = new mongoose.Schema({
  role: {
    type: String,
    enum: ['user', 'ai'],
    required: true,
  },
  content: {
    type: String,
    required: true,
  },
  type: {
    type: String,
    enum: ['text', 'image', 'vitals', 'voice'],
    default: 'text',
  },
  metadata: {
    intent: String,
    confidence: Number,
    urgencyLevel: String,
    urgencyColor: String,
    symptoms: [String],
    bodyParts: [String],
    severity: String,
    duration: String,
  },
  timestamp: {
    type: Date,
    default: Date.now,
  },
});

const chatSchema = new mongoose.Schema(
  {
    userId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User',
      required: true,
    },
    title: {
      type: String,
      default: 'New Chat',
      maxlength: 100,
    },
    messages: [messageSchema],
    isActive: {
      type: Boolean,
      default: true,
    },
    lastActivity: {
      type: Date,
      default: Date.now,
    },
  },
  {
    timestamps: true,
  }
);

// Auto-generate title from first user message
chatSchema.pre('save', async function () {
  if (this.messages.length > 0 && this.title === 'New Chat') {
    const firstMessage = this.messages.find(m => m.role === 'user');
    if (firstMessage) {
      this.title = firstMessage.content.substring(0, 50) +
        (firstMessage.content.length > 50 ? '...' : '');
    }
  }
  this.lastActivity = new Date();
});
const Chat = mongoose.model('Chat', chatSchema);
module.exports = Chat;