# Architecture Overview

## Stack

### Frontend

- **Framework**: React 18
- **Design System**: Microsoft Fluent UI (custom CSS)
- **Build Tool**: Create React App
- **State Management**: React Hooks (useState, useEffect)
- **HTTP Client**: Fetch API

### Backend

- **Framework**: FastAPI
- **Database Connector**: databricks-sql-connector
- **Data Validation**: Pydantic
- **ASGI Server**: Uvicorn

### Data Source

- **Platform**: Databricks Unity Catalog
- **Schema**: system.information_schema
- **Tables Used**:
  - `system.information_schema.tables`
  - `system.information_schema.columns`

## Application Flow

```
User Browser
    ↓
React App (Port 3000 in dev, served by FastAPI in prod)
    ↓
FastAPI Backend (/api/*)
    ↓
Databricks SQL Connector
    ↓
Unity Catalog (system.information_schema)
```

## File Structure

```
.
├── app.py                      # Main entry point (FastAPI + React serving)
├── backend/
│   └── main.py                # API routes and business logic
├── frontend/
│   ├── public/
│   │   └── index.html         # HTML template
│   ├── src/
│   │   ├── components/        # Reusable components
│   │   │   ├── Layout.js      # App layout with sidebar
│   │   │   ├── KPICard.js     # Metric card component
│   │   │   └── TableList.js   # Table list component
│   │   ├── pages/             # Page components
│   │   │   ├── Dashboard.js   # Main dashboard
│   │   │   ├── Explorer.js    # Data explorer
│   │   │   └── Quality.js     # Quality insights
│   │   ├── App.js             # Main React component
│   │   ├── index.js           # React entry point
│   │   └── index.css          # Global styles
│   └── package.json           # Node dependencies
├── databricks.yml             # Databricks Apps config
├── requirements.txt           # Python dependencies
├── .env.example               # Environment template
└── README.md                  # Documentation
```

## API Endpoints

### Health Check

```
GET /api/health
Response: {
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00",
  "databricks_connected": true
}
```

### Inventory

```
GET /api/inventory
Response: {
  "total_table": 150,
  "missing_description_count": 45,
  "documentation_score": 70.0,
  "catalog_list": ["main", "dev"],
  "table_list": [...]
}
```

### Lineage

```
GET /api/lineage/{catalog}/{schema}/{table}
Response: {
  "catalog": "main",
  "schema": "default",
  "table": "users",
  "column_list": [...]
}
```

## Data Models

### TableMetadata

- catalog: str
- schema: str
- table_name: str
- table_type: str
- description: Optional[str]
- missing_description: bool

### ColumnMetadata

- column_name: str
- data_type: str
- is_nullable: str
- description: Optional[str]

## Security

- **Authentication**: Databricks Personal Access Token
- **Authorization**: Unity Catalog permissions (USE CATALOG, USE SCHEMA, SELECT)
- **CORS**: Enabled for development, should be restricted in production
- **Environment Variables**: Sensitive data stored in .env (not committed)

## Performance

- **Caching**: None (real-time data)
- **Pagination**: Frontend limits to 50 rows for display
- **Connection Pooling**: Handled by databricks-sql-connector
- **Build Optimization**: React production build with minification

## Deployment

### Development

- Frontend: npm start (port 3000)
- Backend: python backend/main.py (port 8001)
- Proxy: Frontend proxies /api/\* to backend

### Production (Databricks Apps)

- Frontend: Built and served as static files by FastAPI
- Backend: FastAPI serves both static files and API
- Port: 8000
- Environment: Variables injected by Databricks Apps

## Monitoring

- Health endpoint for uptime checks
- FastAPI automatic OpenAPI docs at /docs
- Databricks Apps logs via CLI: `databricks apps logs data-governance-portal`

## Future Enhancements

- [ ] Add authentication/authorization layer
- [ ] Implement caching for better performance
- [ ] Add data lineage visualization
- [ ] Export reports to PDF/Excel
- [ ] Add search and filtering
- [ ] Implement pagination on backend
- [ ] Add unit and integration tests
- [ ] Add CI/CD pipeline
