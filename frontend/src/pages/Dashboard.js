import React from 'react';
import KPICard from '../components/KPICard';

function Dashboard({ inventory }) {
  if (!inventory) return <div>Loading...</div>;

  return (
    <div className="dashboard">
      <header className="page-header">
        <h1>Enterprise Data Governance Portal</h1>
        <p>Comprehensive view of your Unity Catalog data assets</p>
      </header>

      <div className="kpi-grid">
        <KPICard 
          icon="📚" 
          value={inventory.total_table} 
          label="Total Tables" 
          trend="↑ Active" 
        />
        <KPICard 
          icon="⚠️" 
          value={inventory.missing_description_count} 
          label="Missing Description" 
          trend="Requires Attention" 
        />
        <KPICard 
          icon="📊" 
          value={`${inventory.documentation_score}%`} 
          label="Documentation Score" 
          trend={inventory.documentation_score > 70 ? '↑ Good' : '↓ Needs Improvement'} 
        />
        <KPICard 
          icon="🗂️" 
          value={inventory.catalog_list.length} 
          label="Active Catalogs" 
          trend="↑ Monitored" 
        />
      </div>

      <div className="card">
        <h3>📁 Catalogs</h3>
        <ul>
          {inventory.catalog_list.map(catalog => (
            <li key={catalog}>{catalog}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default Dashboard;
