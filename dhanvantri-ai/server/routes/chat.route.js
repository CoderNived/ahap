const express = require('express');
const router = express.Router();
const {
  createChat,
  getUserChats,
  getChatById,
  addMessage,
  deleteChat,
} = require('../controllers/chat.controller');
const { protect } = require('../middleware/auth.middleware');

// All routes protected
router.use(protect);

router.post('/', createChat);
router.get('/', getUserChats);
router.get('/:chatId', getChatById);
router.post('/:chatId/messages', addMessage);
router.delete('/:chatId', deleteChat);

module.exports = router;