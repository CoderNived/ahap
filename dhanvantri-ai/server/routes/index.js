const express = require('express');
const router = express.Router();

router.use('/health', require('./health.route'));
router.use('/ml', require('./ml.route'));
router.use('/auth', require('./auth.route'));
router.use('/analyze', require('./analyze.route'));
router.use('/orchestrate', require('./orchestrate.route'));
router.use('/chats', require('./chat.route'));

module.exports = router;