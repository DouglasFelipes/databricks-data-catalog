const express = require('express');
const cors = require('cors');
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 8000;

app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Databricks SQL Connection (will use Databricks SDK in production)
const dbsql = null; // Using REST API instead for better compatibility

// Helper function to execute SQL via Databricks REST API
async function executeDatabricksSQL(query) {
  // For now, return null to use mock data
  // In production, this would use Databricks REST API or SDK
  return null;
}

// API Routes
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', message: 'Data Catalog API is running' });
});

// Get KPIs
app.get('/api/kpis', async (req, res) => {
  try {
    // TODO: Integrate with Databricks SQL API
    // For now, returning sample data
    res.json({
      totalTables: 247,
      tablesWithoutDescription: 89,
      dataVolume: '12.4 TB',
      piiColumns: 156,
      lastUpdated: new Date().toISOString()
    });
  } catch (error) {
    console.error('Error fetching KPIs:', error);
    res.status(500).json({ error: error.message });
  }
});

// Get catalogs
app.get('/api/catalogs', async (req, res) => {
  try {
    // TODO: Integrate with Databricks SQL API
    res.json(['main', 'samples', 'analytics']);
  } catch (error) {
    console.error('Error fetching catalogs:', error);
    res.status(500).json({ error: error.message });
  }
});

// Get schemas
app.get('/api/schemas/:catalog', async (req, res) => {
  try {
    const { catalog } = req.params;
    // TODO: Integrate with Databricks SQL API
    res.json(['default', 'bronze', 'silver', 'gold']);
  } catch (error) {
    console.error('Error fetching schemas:', error);
    res.status(500).json({ error: error.message });
  }
});

// Get tables
app.get('/api/tables/:catalog/:schema', async (req, res) => {
  try {
    const { catalog, schema } = req.params;
    // TODO: Integrate with Databricks SQL API
    const mockTables = [
      { table_name: 'customers', table_type: 'TABLE', comment: 'Customer data' },
      { table_name: 'orders', table_type: 'TABLE', comment: 'Order transactions' },
      { table_name: 'products', table_type: 'TABLE', comment: 'Product catalog' },
      { table_name: 'transactions', table_type: 'TABLE', comment: 'Financial transactions' }
    ];
    res.json(mockTables);
  } catch (error) {
    console.error('Error fetching tables:', error);
    res.status(500).json({ error: error.message });
  }
});

// Get table details
app.get('/api/table/:catalog/:schema/:table', async (req, res) => {
  try {
    const { catalog, schema, table } = req.params;
    // TODO: Integrate with Databricks SQL API
    const mockColumns = [
      { column_name: 'id', data_type: 'BIGINT', is_nullable: 'NO', comment: 'ID único' },
      { column_name: 'name', data_type: 'STRING', is_nullable: 'YES', comment: 'Nome do registro' },
      { column_name: 'email', data_type: 'STRING', is_nullable: 'YES', comment: 'Email de contato' },
      { column_name: 'created_at', data_type: 'TIMESTAMP', is_nullable: 'NO', comment: 'Data de criação' },
      { column_name: 'updated_at', data_type: 'TIMESTAMP', is_nullable: 'YES', comment: 'Data de atualização' }
    ];
    res.json({ columns: mockColumns });
  } catch (error) {
    console.error('Error fetching table details:', error);
    res.status(500).json({ error: error.message });
  }
});

// Search
app.get('/api/search', async (req, res) => {
  try {
    const { q } = req.query;
    // TODO: Integrate with Databricks SQL API
    const mockResults = [
      { table_catalog: 'main', table_schema: 'default', table_name: 'customers', comment: 'Customer data' },
      { table_catalog: 'main', table_schema: 'bronze', table_name: 'customer_raw', comment: 'Raw customer data' },
      { table_catalog: 'main', table_schema: 'gold', table_name: 'customer_360', comment: 'Customer 360 view' }
    ].filter(t => t.table_name.toLowerCase().includes(q.toLowerCase()));
    
    res.json(mockResults);
  } catch (error) {
    console.error('Error searching:', error);
    res.status(500).json({ error: error.message });
  }
});

app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
  console.log(`📊 Data Catalog API: http://localhost:${PORT}`);
});
