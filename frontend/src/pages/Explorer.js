import React, { useState } from 'react';

function Explorer({ inventory }) {
  const [selectedTable, setSelectedTable] = useState(null);
  const [columns, setColumns] = useState([]);

  const fetchColumns = async (catalog, schema, table) => {
    try {
      const response = await fetch(`/api/lineage/${catalog}/${schema}/${table}`);
      const data = await response.json();
      setColumns(data.column_list);
      setSelectedTable({ catalog, schema, table });
    } catch (error) {
      console.error('Error fetching columns:', error);
    }
  };

  if (!inventory) return <div>Loading...</div>;

  return (
    <div className="explorer">
      <header className="page-header">
        <h1>Data Explorer</h1>
        <p>Explore tables and schemas</p>
      </header>

      <div className="card">
        <h3>📊 Tables</h3>
        <table>
          <thead>
            <tr>
              <th>Catalog</th>
              <th>Schema</th>
              <th>Table</th>
              <th>Type</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {inventory.table_list.slice(0, 50).map((table, idx) => (
              <tr key={idx}>
                <td>{table.catalog}</td>
                <td>{table.schema}</td>
                <td>{table.table_name}</td>
                <td>{table.table_type}</td>
                <td>
                  <button onClick={() => fetchColumns(table.catalog, table.schema, table.table_name)}>
                    View Columns
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {selectedTable && (
        <div className="card">
          <h3>📋 Columns: {selectedTable.catalog}.{selectedTable.schema}.{selectedTable.table}</h3>
          <table>
            <thead>
              <tr>
                <th>Column</th>
                <th>Type</th>
                <th>Nullable</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>
              {columns.map((col, idx) => (
                <tr key={idx}>
                  <td>{col.column_name}</td>
                  <td>{col.data_type}</td>
                  <td>{col.is_nullable}</td>
                  <td>{col.description || '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default Explorer;
