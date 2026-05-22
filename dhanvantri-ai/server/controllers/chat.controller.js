const Chat = require('../models/Chat');

// ─── Create New Chat ───────────────────────────────────────
const createChat = async (req, res) => {
  try {
    const chat = await Chat.create({
      userId: req.user.id,
      messages: [],
    });

    res.status(201).json({
      status: 'success',
      data: chat,
    });
  } catch (error) {
    res.status(500).json({ status: 'error', message: error.message });
  }
};

// ─── Get All Chats for User ────────────────────────────────
const getUserChats = async (req, res) => {
  try {
    const chats = await Chat.find({
      userId: req.user.id,
      isActive: true,
    })
      .select('title lastActivity createdAt')
      .sort({ lastActivity: -1 })
      .limit(20);

    res.status(200).json({
      status: 'success',
      data: chats,
    });
  } catch (error) {
    res.status(500).json({ status: 'error', message: error.message });
  }
};

// ─── Get Single Chat with Messages ────────────────────────
const getChatById = async (req, res) => {
  try {
    const chat = await Chat.findOne({
      _id: req.params.chatId,
      userId: req.user.id,
    });

    if (!chat) {
      return res.status(404).json({
        status: 'error',
        message: 'Chat not found',
      });
    }

    res.status(200).json({
      status: 'success',
      data: chat,
    });
  } catch (error) {
    res.status(500).json({ status: 'error', message: error.message });
  }
};

// ─── Add Message to Chat ───────────────────────────────────
const addMessage = async (req, res) => {
  try {
    const { chatId } = req.params;
    const { role, content, type, metadata } = req.body;

    const chat = await Chat.findOne({
      _id: chatId,
      userId: req.user.id,
    });

    if (!chat) {
      return res.status(404).json({
        status: 'error',
        message: 'Chat not found',
      });
    }

    chat.messages.push({ role, content, type, metadata });
    await chat.save();

    res.status(200).json({
      status: 'success',
      data: chat.messages[chat.messages.length - 1],
    });
  } catch (error) {
    res.status(500).json({ status: 'error', message: error.message });
  }
};

// ─── Delete Chat ───────────────────────────────────────────
const deleteChat = async (req, res) => {
  try {
    await Chat.findOneAndUpdate(
      { _id: req.params.chatId, userId: req.user.id },
      { isActive: false }
    );

    res.status(200).json({
      status: 'success',
      message: 'Chat deleted',
    });
  } catch (error) {
    res.status(500).json({ status: 'error', message: error.message });
  }
};

module.exports = {
  createChat,
  getUserChats,
  getChatById,
  addMessage,
  deleteChat,
};