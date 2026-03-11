# Setup Guide

## Local Development

```bash
# 1. Install dependencies
pip install -r requirements.txt
cd frontend && npm install && npm run build && cd ..

# 2. Configure environment
cp .env.example .env
# Edit .env with your Databricks credentials

# 3. Run
python app.py
```

Access: http://localhost:8000

## Databricks Deploy

**Note**: With `package.json` in the root, Databricks Apps automatically:

- Runs `npm install` (installs frontend deps)
- Runs `npm run build` (builds React to `frontend/build/`)
- Runs `pip install -r requirements.txt`
- Runs `python app.py`

```bash
# 1. Configure secrets
databricks secrets create-scope databricks
databricks secrets put-secret databricks server_hostname
databricks secrets put-secret databricks http_path
databricks secrets put-secret databricks token

# 2. Deploy
databricks bundle validate
databricks bundle deploy -t dev

# 3. Check logs
databricks apps logs data-governance-portal
```

The frontend will be automatically built during deployment!
