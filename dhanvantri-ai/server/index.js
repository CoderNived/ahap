const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const helmet = require('helmet');
const dotenv = require('dotenv');
const path = require('path');

// Load environment variables from root .env file
dotenv.config({ path: path.resolve(__dirname, '../.env') });

// Initialize express app
const app = express();
const PORT = process.env.PORT || 5000;

// ─── Middleware ───────────────────────────────────────────
app.use(helmet());                          // Secure HTTP headers
app.use(cors());                            // Allow cross-origin requests
app.use(morgan('dev'));                      // Log every request
app.use(express.json());                    // Parse JSON request bodies
app.use(express.urlencoded({ extended: true })); // Parse form data

// ─── Test Route ───────────────────────────────────────────
app.get('/api/health', (req, res) => {
  res.status(200).json({
    status: 'ok',
    service: 'dhanvantri-api',
    environment: process.env.NODE_ENV,
    timestamp: new Date().toISOString()
  });
});

// ─── 404 Handler ──────────────────────────────────────────
app.use((req, res) => {
  res.status(404).json({
    status: 'error',
    message: `Route ${req.originalUrl} not found`
  });
});

// ─── Start Server ─────────────────────────────────────────
app.listen(PORT, () => {
  console.log(`✅ Server running on http://localhost:${PORT}`);
  console.log(`🌍 Environment: ${process.env.NODE_ENV}`);
});