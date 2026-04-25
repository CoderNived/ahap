const express = require('express');
const router = express.Router();

router.use('/health', require('./health.route'));
router.use('/ml', require('./ml.route'));
router.use('/auth', require('./auth.route'));

module.exports = router;