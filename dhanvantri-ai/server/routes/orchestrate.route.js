const express = require('express');
const router = express.Router();
const { orchestrate } = require('../controllers/orchestrate.controller');
const { protect } = require('../middleware/auth.middleware');
const { uploadImage, uploadCSV } = require('../utils/upload');
const multer = require('multer');

const upload = multer({
  storage: multer.diskStorage({
    destination: (req, file, cb) => cb(null, 'uploads/'),
    filename: (req, file, cb) => {
      const uniqueSuffix = `${Date.now()}-${Math.round(Math.random() * 1e9)}`;
      cb(null, `${file.fieldname}-${uniqueSuffix}-${file.originalname}`);
    },
  }),
});

// POST /api/orchestrate
router.post(
  '/',
  protect,
  upload.fields([
    { name: 'image', maxCount: 1 },
    { name: 'vitals', maxCount: 1 },
  ]),
  orchestrate
);

module.exports = router;