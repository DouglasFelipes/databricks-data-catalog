# Data Governance Portal

Enterprise data governance portal for Databricks Unity Catalog with React frontend and FastAPI backend.

## Quick Start

### Local Development

**Option 1: Using the script (recommended)**

```bash
# 1. Configure environment
cp .env.example .env
# Edit .env with your Databricks credentials

# 2. Run (installs deps and builds frontend automatically)
./run_local.sh
```

**Option 2: Manual steps**

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with your Databricks credentials

# 3. Build frontend
cd frontend
npm install
npm run build
cd ..

# 4. Run application
python app.py
```

Access: http://localhost:8000

See [LOCAL_TEST.md](LOCAL_TEST.md) for detailed testing guide.

### Deploy to Databricks Apps

1. **Configure secrets in Databricks:**

```bash
# Create secret scope
databricks secrets create-scope databricks

# Add secrets (you'll be prompted to enter values)
databricks secrets put-secret databricks server_hostname
# Enter: your-workspace.cloud.databricks.com

databricks secrets put-secret databricks http_path
# Enter: /sql/1.0/warehouses/your-warehouse-id

databricks secrets put-secret databricks token
# Enter: your-personal-access-token
```

2. **Verify secrets:**

```bash
databricks secrets list-secrets databricks
```

3. **Deploy:**

```bash
databricks bundle validate
databricks bundle deploy -t dev
```

Databricks will automatically:

- Run `npm install` and `npm run build` (builds frontend)
- Run `pip install -r requirements.txt` (installs Python deps)
- Load secrets and set as environment variables
- Run `python app.py` (starts the app)

4. **Check logs:**

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

For Databricks Apps, configure via secrets in `databricks.yml`.

## Tech Stack

- **Frontend**: React 18, Fluent UI design
- **Backend**: FastAPI, Databricks SQL Connector
- **Data**: Unity Catalog (system.information_schema)
- **Deploy**: Databricks Apps
