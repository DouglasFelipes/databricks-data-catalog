import React from 'react';

function Quality({ inventory }) {
  if (!inventory) return <div>Loading...</div>;

  const undocumented = inventory.table_list.filter(t => t.missing_description);

  return (
    <div className="quality">
      <header className="page-header">
        <h1>Data Quality</h1>
        <p>Monitor documentation quality</p>
      </header>

      <div className="card">
        <h3>📊 Quality Metrics</h3>
        <div className="metrics">
          <div className="metric">
            <span className="metric-value">{inventory.documentation_score}%</span>
            <span className="metric-label">Documentation Score</span>
          </div>
          <div className="metric">
            <span className="metric-value">{inventory.total_table - inventory.missing_description_count}</span>
            <span className="metric-label">Documented Tables</span>
          </div>
          <div className="metric">
            <span className="metric-value">{inventory.missing_description_count}</span>
            <span className="metric-label">Undocumented Tables</span>
          </div>
        </div>
      </div>

      <div className="card">
        <h3>⚠️ Tables Requiring Documentation</h3>
        <table>
          <thead>
            <tr>
              <th>Catalog</th>
              <th>Schema</th>
              <th>Table</th>
              <th>Priority</th>
            </tr>
          </thead>
          <tbody>
            {undocumented.slice(0, 50).map((table, idx) => (
              <tr key={idx}>
                <td>{table.catalog}</td>
                <td>{table.schema}</td>
                <td>{table.table_name}</td>
                <td>🔴 High</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Quality;
