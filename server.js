const express = require('express');
const cors = require('cors');
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 8000;

app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// API Routes
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', message: 'Data Catalog API is running' });
});

app.get('/api/kpis', (req, res) => {
  res.json({
    totalTables: 0,
    tablesWithoutDescription: 0,
    dataVolume: '0 TB'
  });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
