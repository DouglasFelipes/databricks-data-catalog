import React, { useState, useEffect } from 'react';
import Dashboard from './pages/Dashboard';
import Explorer from './pages/Explorer';
import Quality from './pages/Quality';
import Layout from './components/Layout';

function App() {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [inventory, setInventory] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchInventory();
  }, []);

  const fetchInventory = async () => {
    try {
      const response = await fetch('/api/inventory');
      const data = await response.json();
      setInventory(data);
    } catch (error) {
      console.error('Error fetching inventory:', error);
    } finally {
      setLoading(false);
    }
  };

  const renderPage = () => {
    if (loading) return <div className="loading">Loading...</div>;
    
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard inventory={inventory} />;
      case 'explorer':
        return <Explorer inventory={inventory} />;
      case 'quality':
        return <Quality inventory={inventory} />;
      default:
        return <Dashboard inventory={inventory} />;
    }
  };

  return (
    <Layout currentPage={currentPage} setCurrentPage={setCurrentPage}>
      {renderPage()}
    </Layout>
  );
}

export default App;
