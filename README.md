# Enterprise Data Governance Portal

Professional React + FastAPI application for Databricks Unity Catalog governance.

## 🏗️ Architecture

- **Frontend**: React 18 with Fluent UI design system
- **Backend**: FastAPI + Databricks SQL Connector
- **Data Source**: Unity Catalog (system.information_schema)
- **Deployment**: Databricks Apps

## 🚀 Quick Start

### Option 1: Automated Setup

```bash
./start.sh
```

### Option 2: Manual Setup

1. **Configure Environment**

```bash
cp .env.example .env
# Edit .env with your Databricks credentials
```

2. **Install Dependencies**

```bash
# Backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
npm run build
cd ..
```

3. **Run Application**

```bash
# Option A: Using script
./run_local.sh

# Option B: Direct
python3 app.py
```

4. **Access Application**

- Frontend: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/api/health

## 📦 Deploy to Databricks Apps

```bash
# Validate configuration
databricks bundle validate

# Deploy to development
databricks bundle deploy -t dev

# Deploy to production
databricks bundle deploy -t prod
```

See [DEPLOY.md](DEPLOY.md) for detailed deployment instructions.

## 🔌 API Endpoints

- `GET /api/health` - Health check and connection status
- `GET /api/inventory` - Get all tables with quality metrics
- `GET /api/lineage/{catalog}/{schema}/{table}` - Get table column metadata

## ✨ Features

- ✅ Real-time Unity Catalog metadata
- ✅ Documentation quality scoring
- ✅ Interactive table and column explorer
- ✅ Quality insights dashboard
- ✅ Fluent UI design system
- ✅ Responsive layout

## 📁 Project Structure

```
.
├── app.py                 # Main FastAPI application
├── backend/
│   └── main.py           # API routes and business logic
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   └── App.js        # Main React app
│   └── package.json
├── databricks.yml        # Databricks Apps configuration
├── requirements.txt      # Python dependencies
├── validate.py          # Setup validation script
└── start.sh             # Quick start script
```

## 🔧 Development

Run frontend and backend separately for hot reload:

```bash
# Terminal 1 - Backend (port 8000)
python backend/main.py

# Terminal 2 - Frontend (port 3000)
cd frontend
npm start
```

## 📝 Environment Variables

Required in `.env`:

- `DATABRICKS_SERVER_HOSTNAME` - Your workspace URL
- `DATABRICKS_HTTP_PATH` - SQL Warehouse HTTP path
- `DATABRICKS_TOKEN` - Personal access token

## 📚 Documentation

- [QUICKSTART.md](QUICKSTART.md) - Get started in 5 minutes
- [ARCHITECTURE.md](ARCHITECTURE.md) - Technical architecture details
- [DEPLOY.md](DEPLOY.md) - Complete deployment guide
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues and solutions
- [CHECKLIST.md](CHECKLIST.md) - Pre-deployment checklist
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Project overview
- [DIAGRAM.txt](DIAGRAM.txt) - Visual architecture diagram

## 🐛 Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions to common issues.
