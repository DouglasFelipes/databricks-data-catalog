# Data Governance Portal

Enterprise data governance portal for Databricks Unity Catalog with React frontend and FastAPI backend.

## Quick Start

### Local Development

```bash
# Install Python dependencies
pip install -r requirements.txt

# Build frontend
cd frontend
npm install
npm run build
cd ..

# Run application
python app.py
```

Access: http://localhost:8000

### Deploy to Databricks Apps

**Important**: Databricks Apps will automatically build the frontend during deployment because we have `package.json` in the root.

1. **Configure secrets in Databricks:**

```bash
databricks secrets create-scope databricks
databricks secrets put-secret databricks server_hostname
databricks secrets put-secret databricks http_path
databricks secrets put-secret databricks token
```

2. **Deploy:**

```bash
databricks bundle validate
databricks bundle deploy -t dev
```

The deployment process will:

- Run `npm install` (installs frontend dependencies)
- Run `npm run build` (builds React app to `frontend/build/`)
- Run `pip install -r requirements.txt` (installs Python dependencies)
- Run `python app.py` (starts the application)

3. **Check logs:**

```bash
databricks apps logs data-governance-portal
```

## Project Structure

```
.
├── app.py                 # Main FastAPI application
├── app.yaml              # Databricks Apps runtime config
├── backend/
│   └── main.py          # API routes
├── frontend/
│   ├── src/             # React source
│   └── build/           # React production build
├── databricks.yml       # Databricks bundle config
└── requirements.txt     # Python dependencies
```

## API Endpoints

- `GET /` - Frontend or API info
- `GET /api/health` - Health check
- `GET /api/inventory` - Unity Catalog tables
- `GET /api/lineage/{catalog}/{schema}/{table}` - Table columns
- `GET /docs` - API documentation

## Environment Variables

Required in `.env` for local development:

```
DATABRICKS_SERVER_HOSTNAME=your-workspace.cloud.databricks.com
DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/your-warehouse-id
DATABRICKS_TOKEN=your-token
```

For Databricks Apps, configure via secrets in `app.yaml`.

## Tech Stack

- **Frontend**: React 18, Fluent UI design
- **Backend**: FastAPI, Databricks SQL Connector
- **Data**: Unity Catalog (system.information_schema)
- **Deploy**: Databricks Apps
