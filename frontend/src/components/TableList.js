import React from 'react';
import {
  DetailsList,
  DetailsListLayoutMode,
  SelectionMode,
  mergeStyleSets
} from '@fluentui/react';

const styles = mergeStyleSets({
  detailsList: {
    selectors: {
      '.ms-DetailsHeader': {
        paddingTop: 0,
        borderBottom: '2px solid #edebe9'
      },
      '.ms-DetailsHeader-cell': {
        fontSize: '12px',
        fontWeight: '600',
        color: '#323130',
        background: '#faf9f8'
      },
      '.ms-DetailsRow': {
        borderBottom: '1px solid #edebe9',
        selectors: {
          ':hover': {
            background: '#f3f2f1'
          }
        }
      },
      '.ms-DetailsRow-cell': {
        fontSize: '14px',
        padding: '12px 8px'
      }
    }
  }
});

const TableList = ({ tables }) => {
  const columns = [
    {
      key: 'catalog',
      name: 'Catalog',
      fieldName: 'catalog',
      minWidth: 100,
      maxWidth: 150,
      isResizable: true
    },
    {
      key: 'schema',
      name: 'Schema',
      fieldName: 'schema',
      minWidth: 100,
      maxWidth: 150,
      isResizable: true
    },
    {
      key: 'table_name',
      name: 'Table',
      fieldName: 'table_name',
      minWidth: 150,
      maxWidth: 250,
      isResizable: true
    },
    {
      key: 'table_type',
      name: 'Type',
      fieldName: 'table_type',
      minWidth: 80,
      maxWidth: 100,
      isResizable: true
    },
    {
      key: 'description',
      name: 'Description',
      fieldName: 'description',
      minWidth: 200,
      isResizable: true,
      onRender: (item) => {
        return item.description || <span style={{ color: '#a19f9d' }}>-</span>;
      }
    },
    {
      key: 'status',
      name: 'Status',
      minWidth: 120,
      maxWidth: 150,
      onRender: (item) => {
        const badge = item.missing_description
          ? { text: '⚠ Missing Description', color: '#fff4ce', textColor: '#f7630c' }
          : { text: '✓ Documented', color: '#dff6dd', textColor: '#107c10' };
        
        return (
          <span
            style={{
              display: 'inline-block',
              padding: '4px 12px',
              borderRadius: '12px',
              fontSize: '12px',
              fontWeight: '600',
              background: badge.color,
              color: badge.textColor
            }}
          >
            {badge.text}
          </span>
        );
      }
    }
  ];

  return (
    <DetailsList
      items={tables}
      columns={columns}
      layoutMode={DetailsListLayoutMode.justified}
      selectionMode={SelectionMode.none}
      className={styles.detailsList}
      isHeaderVisible={true}
    />
  );
};

export default TableList;
