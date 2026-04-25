const express = require('express');
const router = express.Router();

router.use('/health', require('./health.route'));
router.use('/ml', require('./ml.route'));

module.exports = router;