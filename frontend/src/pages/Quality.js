import React, { useState, useEffect } from 'react';
import { Stack, Text, Spinner, MessageBar, MessageBarType, mergeStyleSets } from '@fluentui/react';
import axios from 'axios';
import TableList from '../components/TableList';

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

const Quality = () => {
  const [loading, setLoading] = useState(true);
  const [inventory, setInventory] = useState(null);

  useEffect(() => {
    fetchInventory();
  }, []);

  const fetchInventory = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE}/api/inventory`);
      setInventory(response.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <Spinner label="Loading quality metrics..." size={3} />;
  }

  const undocumentedTables = inventory?.table_list?.filter(t => t.missing_description) || [];

  return (
    <Stack tokens={{ childrenGap: 24 }}>
      <div>
        <Text variant="xxLarge" styles={{ root: { fontWeight: '600', marginBottom: '8px' } }}>
          Quality Insights
        </Text>
        <Text variant="medium" styles={{ root: { color: '#605e5c' } }}>
          Monitor and improve data quality and governance
        </Text>
      </div>

      <div className={styles.card}>
        <Text variant="xLarge" styles={{ root: { marginBottom: '16px', fontWeight: '600' } }}>
          ⚠️ Tables Requiring Documentation
        </Text>
        {undocumentedTables.length > 0 ? (
          <>
            <TableList tables={undocumentedTables} />
            <MessageBar messageBarType={MessageBarType.warning} styles={{ root: { marginTop: '16px' } }}>
              {undocumentedTables.length} tables ({Math.round(undocumentedTables.length / inventory.total_table * 100)}%) require documentation to improve governance.
            </MessageBar>
          </>
        ) : (
          <MessageBar messageBarType={MessageBarType.success}>
            ✅ All tables are properly documented!
          </MessageBar>
        )}
      </div>
    </Stack>
  );
};

export default Quality;
