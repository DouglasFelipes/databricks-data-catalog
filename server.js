const express = require('express');
const cors = require('cors');
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 8000;

app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Databricks SQL Connection
let dbsql;
try {
  dbsql = require('@databricks/sql');
} catch (e) {
  console.log('Databricks SQL not available, using mock data');
}

// Helper function to get Databricks connection
async function getDatabricksConnection() {
  if (!dbsql) return null;
  
  const client = dbsql.DBSQLClient.getInstance({
    host: process.env.DATABRICKS_HOST || process.env.DATABRICKS_SERVER_HOSTNAME,
    path: process.env.DATABRICKS_HTTP_PATH,
    token: process.env.DATABRICKS_TOKEN,
  });
  
  return await client.connect();
}

// API Routes
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', message: 'Data Catalog API is running' });
});

// Get KPIs
app.get('/api/kpis', async (req, res) => {
  try {
    const connection = await getDatabricksConnection();
    
    if (!connection) {
      return res.json({
        totalTables: 247,
        tablesWithoutDescription: 89,
        dataVolume: '12.4 TB',
        piiColumns: 156,
        lastUpdated: new Date().toISOString()
      });
    }
    
    const session = await connection.openSession();
    
    // Total tables
    const totalQuery = await session.executeStatement(
      'SELECT COUNT(*) as total FROM system.information_schema.tables'
    );
    const totalResult = await totalQuery.fetchAll();
    const totalTables = totalResult[0]?.total || 0;
    
    // Tables without description
    const noDescQuery = await session.executeStatement(
      `SELECT COUNT(*) as total FROM system.information_schema.tables 
       WHERE comment IS NULL OR comment = ''`
    );
    const noDescResult = await noDescQuery.fetchAll();
    const tablesWithoutDescription = noDescResult[0]?.total || 0;
    
    await session.close();
    await connection.close();
    
    res.json({
      totalTables,
      tablesWithoutDescription,
      dataVolume: 'N/A',
      piiColumns: 0,
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
    const connection = await getDatabricksConnection();
    
    if (!connection) {
      return res.json(['main', 'samples', 'analytics']);
    }
    
    const session = await connection.openSession();
    const query = await session.executeStatement('SHOW CATALOGS');
    const result = await query.fetchAll();
    
    await session.close();
    await connection.close();
    
    const catalogs = result.map(row => row.catalog);
    res.json(catalogs);
  } catch (error) {
    console.error('Error fetching catalogs:', error);
    res.status(500).json({ error: error.message });
  }
});

// Get schemas
app.get('/api/schemas/:catalog', async (req, res) => {
  try {
    const { catalog } = req.params;
    const connection = await getDatabricksConnection();
    
    if (!connection) {
      return res.json(['default', 'bronze', 'silver', 'gold']);
    }
    
    const session = await connection.openSession();
    const query = await session.executeStatement(`SHOW SCHEMAS IN ${catalog}`);
    const result = await query.fetchAll();
    
    await session.close();
    await connection.close();
    
    const schemas = result.map(row => row.databaseName);
    res.json(schemas);
  } catch (error) {
    console.error('Error fetching schemas:', error);
    res.status(500).json({ error: error.message });
  }
});

// Get tables
app.get('/api/tables/:catalog/:schema', async (req, res) => {
  try {
    const { catalog, schema } = req.params;
    const connection = await getDatabricksConnection();
    
    if (!connection) {
      return res.json(['customers', 'orders', 'products', 'transactions']);
    }
    
    const session = await connection.openSession();
    const query = await session.executeStatement(
      `SELECT * FROM system.information_schema.tables 
       WHERE table_catalog = '${catalog}' AND table_schema = '${schema}'`
    );
    const result = await query.fetchAll();
    
    await session.close();
    await connection.close();
    
    res.json(result);
  } catch (error) {
    console.error('Error fetching tables:', error);
    res.status(500).json({ error: error.message });
  }
});

// Get table details
app.get('/api/table/:catalog/:schema/:table', async (req, res) => {
  try {
    const { catalog, schema, table } = req.params;
    const connection = await getDatabricksConnection();
    
    if (!connection) {
      return res.json({
        columns: [
          { name: 'id', type: 'BIGINT', nullable: false, comment: 'ID único' },
          { name: 'name', type: 'STRING', nullable: true, comment: 'Nome' }
        ]
      });
    }
    
    const session = await connection.openSession();
    const query = await session.executeStatement(
      `SELECT * FROM system.information_schema.columns 
       WHERE table_catalog = '${catalog}' 
       AND table_schema = '${schema}' 
       AND table_name = '${table}'`
    );
    const columns = await query.fetchAll();
    
    await session.close();
    await connection.close();
    
    res.json({ columns });
  } catch (error) {
    console.error('Error fetching table details:', error);
    res.status(500).json({ error: error.message });
  }
});

// Search
app.get('/api/search', async (req, res) => {
  try {
    const { q } = req.query;
    const connection = await getDatabricksConnection();
    
    if (!connection) {
      return res.json([
        { type: 'table', name: 'customers', location: 'main.default', relevance: 5 }
      ]);
    }
    
    const session = await connection.openSession();
    const query = await session.executeStatement(
      `SELECT table_catalog, table_schema, table_name, comment 
       FROM system.information_schema.tables 
       WHERE LOWER(table_name) LIKE LOWER('%${q}%') 
       OR LOWER(comment) LIKE LOWER('%${q}%')
       LIMIT 50`
    );
    const result = await query.fetchAll();
    
    await session.close();
    await connection.close();
    
    res.json(result);
  } catch (error) {
    console.error('Error searching:', error);
    res.status(500).json({ error: error.message });
  }
});

app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
  console.log(`📊 Data Catalog API: http://localhost:${PORT}`);
});
