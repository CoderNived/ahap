const express = require('express');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Test route
app.get('/api/health', (req, res) => {
  res.json({ status: 'Dhanvantri backend is alive!' });
});
// Chat route
app.post('/api/chat', (req, res) => {
  const { message } = req.body;

  console.log('User said:', message);

res.json({ status: 'Dhanvantri AI is alive!' });
});
// Start server
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});