import React, { useState, useEffect } from 'react';
import { Stack, Text, Dropdown, Spinner, MessageBar, MessageBarType, mergeStyleSets } from '@fluentui/react';
import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const styles = mergeStyleSets({
  card: {
    background: '#ffffff',
    borderRadius: '8px',
    padding: '24px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.08)',
    border: '1px solid #edebe9'
  }
});

const Explorer = () => {
  const [catalogs, setCatalogs] = useState([]);
  const [schemas, setSchemas] = useState([]);
  const [tables, setTables] = useState([]);
  const [columns, setColumns] = useState([]);
  
  const [selectedCatalog, setSelectedCatalog] = useState(null);
  const [selectedSchema, setSelectedSchema] = useState(null);
  const [selectedTable, setSelectedTable] = useState(null);
  
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchCatalogs();
  }, []);

  const fetchCatalogs = async () => {
    try {
      const response = await axios.get(`${API_BASE}/api/inventory`);
      setCatalogs(response.data.catalog_list.map(c => ({ key: c, text: c })));
    } catch (err) {
      console.error(err);
    }
  };

  const handleCatalogChange = async (event, option) => {
    setSelectedCatalog(option.key);
    setSelectedSchema(null);
    setSelectedTable(null);
    setSchemas([]);
    setTables([]);
    setColumns([]);
    
    try {
      const response = await axios.get(`${API_BASE}/api/catalog/${option.key}/schema`);
      setSchemas(response.data.schema_list.map(s => ({ key: s, text: s })));
    } catch (err) {
      console.error(err);
    }
  };

  const handleSchemaChange = async (event, option) => {
    setSelectedSchema(option.key);
    setSelectedTable(null);
    setTables([]);
    setColumns([]);
    
    try {
      const response = await axios.get(`${API_BASE}/api/catalog/${selectedCatalog}/schema/${option.key}/table`);
      setTables(response.data.table_list.map(t => ({ key: t.table_name, text: t.table_name })));
    } catch (err) {
      console.error(err);
    }
  };

  const handleTableChange = async (event, option) => {
    setSelectedTable(option.key);
    setLoading(true);
    
    try {
      const response = await axios.get(`${API_BASE}/api/lineage/${selectedCatalog}/${selectedSchema}/${option.key}`);
      setColumns(response.data.column_list);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Stack tokens={{ childrenGap: 24 }}>
      <div>
        <Text variant="xxLarge" styles={{ root: { fontWeight: '600', marginBottom: '8px' } }}>
          Explorer
        </Text>
        <Text variant="medium" styles={{ root: { color: '#605e5c' } }}>
          Navigate through Catalog → Schema → Table
        </Text>
      </div>

      <div className={styles.card}>
        <Stack horizontal tokens={{ childrenGap: 16 }}>
          <Dropdown
            placeholder="Select Catalog"
            label="📁 Catalog"
            options={catalogs}
            onChange={handleCatalogChange}
            styles={{ root: { width: 200 } }}
          />
          <Dropdown
            placeholder="Select Schema"
            label="📂 Schema"
            options={schemas}
            onChange={handleSchemaChange}
            disabled={!selectedCatalog}
            styles={{ root: { width: 200 } }}
          />
          <Dropdown
            placeholder="Select Table"
            label="📄 Table"
            options={tables}
            onChange={handleTableChange}
            disabled={!selectedSchema}
            styles={{ root: { width: 200 } }}
          />
        </Stack>
      </div>

      {loading && <Spinner label="Loading columns..." />}

      {columns.length > 0 && (
        <div className={styles.card}>
          <Text variant="xLarge" styles={{ root: { marginBottom: '16px', fontWeight: '600' } }}>
            📋 Columns
          </Text>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ borderBottom: '2px solid #edebe9', background: '#faf9f8' }}>
                <th style={{ padding: '12px', textAlign: 'left', fontWeight: '600' }}>Column</th>
                <th style={{ padding: '12px', textAlign: 'left', fontWeight: '600' }}>Type</th>
                <th style={{ padding: '12px', textAlign: 'left', fontWeight: '600' }}>Nullable</th>
                <th style={{ padding: '12px', textAlign: 'left', fontWeight: '600' }}>Description</th>
              </tr>
            </thead>
            <tbody>
              {columns.map((col, idx) => (
                <tr key={idx} style={{ borderBottom: '1px solid #edebe9' }}>
                  <td style={{ padding: '12px' }}>{col.column_name}</td>
                  <td style={{ padding: '12px' }}>{col.data_type}</td>
                  <td style={{ padding: '12px' }}>{col.is_nullable === 'YES' ? '✅' : '❌'}</td>
                  <td style={{ padding: '12px' }}>{col.description || '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </Stack>
  );
};

export default Explorer;
