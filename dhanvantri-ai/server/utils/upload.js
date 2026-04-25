const multer = require('multer');
const path = require('path');

// ─── Storage Config ────────────────────────────────────────
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/');
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = `${Date.now()}-${Math.round(Math.random() * 1e9)}`;
    cb(null, `${file.fieldname}-${uniqueSuffix}${path.extname(file.originalname)}`);
  },
});

// ─── Voice File Filter ─────────────────────────────────────
const voiceFilter = (req, file, cb) => {
  const allowedTypes = ['audio/mpeg', 'audio/wav', 'audio/webm', 'audio/mp4', 'audio/ogg'];
  if (allowedTypes.includes(file.mimetype)) {
    cb(null, true);
  } else {
    cb(new Error('Invalid file type. Only audio files are allowed.'), false);
  }
};

// ─── Image File Filter ─────────────────────────────────────
const imageFilter = (req, file, cb) => {
  const allowedTypes = ['image/jpeg', 'image/png', 'image/dicom', 'image/tiff'];
  if (allowedTypes.includes(file.mimetype)) {
    cb(null, true);
  } else {
    cb(new Error('Invalid file type. Only image files are allowed.'), false);
  }
};

// ─── CSV File Filter ───────────────────────────────────────
const csvFilter = (req, file, cb) => {
  const allowedTypes = ['text/csv', 'application/vnd.ms-excel'];
  if (allowedTypes.includes(file.mimetype)) {
    cb(null, true);
  } else {
    cb(new Error('Invalid file type. Only CSV files are allowed.'), false);
  }
};

// ─── Export Uploaders ──────────────────────────────────────
const uploadVoice = multer({
  storage,
  fileFilter: voiceFilter,
  limits: { fileSize: 10 * 1024 * 1024 }, // 10MB max
});

const uploadImage = multer({
  storage,
  fileFilter: imageFilter,
  limits: { fileSize: 20 * 1024 * 1024 }, // 20MB max
});

const uploadCSV = multer({
  storage,
  fileFilter: csvFilter,
  limits: { fileSize: 5 * 1024 * 1024 }, // 5MB max
});

module.exports = { uploadVoice, uploadImage, uploadCSV };