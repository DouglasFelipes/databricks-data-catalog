import React from 'react';

function TableList({ tables, onTableClick }) {
  return (
    <div className="table-list">
      <table>
        <thead>
          <tr>
            <th>Catalog</th>
            <th>Schema</th>
            <th>Table</th>
            <th>Type</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {tables.map((table, idx) => (
            <tr key={idx} onClick={() => onTableClick && onTableClick(table)}>
              <td>{table.catalog}</td>
              <td>{table.schema}</td>
              <td>{table.table_name}</td>
              <td>{table.table_type}</td>
              <td>
                {table.missing_description ? (
                  <span className="badge badge-warning">⚠ Missing Desc</span>
                ) : (
                  <span className="badge badge-success">✓ Documented</span>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default TableList;
