import React, { useState, useEffect } from 'react';
import {
  Stack,
  Text,
  Spinner,
  MessageBar,
  MessageBarType,
  mergeStyleSets
} from '@fluentui/react';
import axios from 'axios';
import KPICard from '../components/KPICard';
import TableList from '../components/TableList';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const styles = mergeStyleSets({
  header: {
    marginBottom: '24px'
  },
  title: {
    fontSize: '28px',
    fontWeight: '600',
    color: '#323130',
    marginBottom: '8px'
  },
  subtitle: {
    fontSize: '14px',
    color: '#605e5c'
  },
  kpiContainer: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
    gap: '16px',
    marginBottom: '24px'
  },
  card: {
    background: '#ffffff',
    borderRadius: '8px',
    padding: '24px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.08)',
    border: '1px solid #edebe9'
  }
});

const Dashboard = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [inventory, setInventory] = useState(null);

  useEffect(() => {
    fetchInventory();
  }, []);

  const fetchInventory = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get(`${API_BASE}/api/inventory`);
      setInventory(response.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Stack horizontalAlign="center" verticalAlign="center" styles={{ root: { height: '100%' } }}>
        <Spinner label="Loading inventory..." size={3} />
      </Stack>
    );
  }

  if (error) {
    return (
      <MessageBar messageBarType={MessageBarType.error} isMultiline={false}>
        Error loading data: {error}
      </MessageBar>
    );
  }

  return (
    <Stack tokens={{ childrenGap: 24 }}>
      {/* Header */}
      <div className={styles.header}>
        <Text className={styles.title}>Dashboard</Text>
        <Text className={styles.subtitle}>
          Comprehensive view of your Unity Catalog data assets
        </Text>
      </div>

      {/* KPI Cards */}
      <div className={styles.kpiContainer}>
        <KPICard
          icon="📚"
          value={inventory?.total_table || 0}
          label="Total Tables"
          trend="Active"
          trendPositive={true}
        />
        <KPICard
          icon="⚠️"
          value={inventory?.missing_description_count || 0}
          label="Missing Description"
          trend="Requires Attention"
          trendPositive={false}
        />
        <KPICard
          icon="📊"
          value={`${inventory?.documentation_score || 0}%`}
          label="Documentation Score"
          trend={inventory?.documentation_score > 70 ? 'Good' : 'Needs Improvement'}
          trendPositive={inventory?.documentation_score > 70}
        />
        <KPICard
          icon="🗂️"
          value={inventory?.catalog_list?.length || 0}
          label="Active Catalogs"
          trend="Monitored"
          trendPositive={true}
        />
      </div>

      {/* Tables List */}
      <div className={styles.card}>
        <Text variant="xLarge" styles={{ root: { marginBottom: '16px', fontWeight: '600' } }}>
          📊 All Tables
        </Text>
        <TableList tables={inventory?.table_list || []} />
      </div>
    </Stack>
  );
};

export default Dashboard;
