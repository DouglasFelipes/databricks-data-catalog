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

```bash
# 1. Configure secrets
databricks secrets create-scope databricks
databricks secrets put-secret databricks server_hostname
databricks secrets put-secret databricks http_path
databricks secrets put-secret databricks token

# 2. Deploy
databricks bundle validate
databricks bundle deploy -t dev

# 3. Check
databricks apps logs data-governance-portal
```
