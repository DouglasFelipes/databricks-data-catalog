# Documentation Index

Complete guide to the Data Governance Portal project.

## 🚀 Getting Started

Start here if you're new to the project:

1. **[QUICKSTART.md](QUICKSTART.md)** - Get up and running in 5 minutes
   - Local setup
   - Quick deploy
   - Common commands

2. **[README.md](README.md)** - Project overview
   - Features
   - Architecture summary
   - Installation guide

## 📖 Understanding the Project

Learn about the architecture and design:

3. **[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical deep dive
   - Stack details
   - Data flow
   - API endpoints
   - Security considerations

4. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - What was built
   - Files created
   - Files removed
   - Features implemented

5. **[DIAGRAM.txt](DIAGRAM.txt)** - Visual architecture
   - ASCII diagrams
   - Data flow visualization
   - Deployment flow

## 🚢 Deployment

Deploy to Databricks Apps:

6. **[DEPLOY.md](DEPLOY.md)** - Complete deployment guide
   - Prerequisites
   - Step-by-step instructions
   - Environment configuration
   - Troubleshooting basics

7. **[CHECKLIST.md](CHECKLIST.md)** - Pre-deployment checklist
   - Pre-deploy checks
   - Build verification
   - Local testing
   - Production deployment
   - Monitoring

## 🔧 Development

For developers working on the project:

8. **[Makefile](Makefile)** - Build automation
   - `make install` - Install dependencies
   - `make dev` - Development mode
   - `make build` - Build frontend
   - `make deploy-dev` - Deploy to dev

9. **Scripts**
   - `start.sh` - Production start script
   - `dev.sh` - Development mode script
   - `validate.py` - Setup validation

## 🐛 Troubleshooting

When things go wrong:

10. **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Comprehensive troubleshooting
    - App Not Available
    - Connection errors
    - Build failures
    - Performance issues
    - CORS problems
    - And more...

## 📁 Code Reference

### Backend (Python)

- `app.py` - Main entry point
- `backend/main.py` - API routes and business logic
- `requirements.txt` - Python dependencies

### Frontend (React)

- `frontend/src/App.js` - Main React application
- `frontend/src/components/` - Reusable components
  - `Layout.js` - App layout with sidebar
  - `KPICard.js` - Metric display cards
  - `TableList.js` - Table listing component
- `frontend/src/pages/` - Page components
  - `Dashboard.js` - Main dashboard
  - `Explorer.js` - Data explorer
  - `Quality.js` - Quality insights
- `frontend/package.json` - Node dependencies

### Configuration

- `databricks.yml` - Databricks Apps configuration
- `.env.example` - Environment variables template
- `.gitignore` - Git ignore rules

## 🎯 Quick Reference

### Common Tasks

| Task                     | Command                                       |
| ------------------------ | --------------------------------------------- |
| Install dependencies     | `make install`                                |
| Start development        | `make dev` or `./dev.sh`                      |
| Start production (local) | `make start` or `./start.sh`                  |
| Build frontend           | `cd frontend && npm run build`                |
| Validate setup           | `python validate.py`                          |
| Deploy to dev            | `make deploy-dev`                             |
| Deploy to prod           | `make deploy-prod`                            |
| View logs                | `databricks apps logs data-governance-portal` |

### API Endpoints

| Endpoint                                      | Description                 |
| --------------------------------------------- | --------------------------- |
| `GET /api/health`                             | Health check                |
| `GET /api/inventory`                          | Get all tables with metrics |
| `GET /api/lineage/{catalog}/{schema}/{table}` | Get table columns           |

### Environment Variables

| Variable                     | Description        |
| ---------------------------- | ------------------ |
| `DATABRICKS_SERVER_HOSTNAME` | Workspace URL      |
| `DATABRICKS_HTTP_PATH`       | SQL Warehouse path |
| `DATABRICKS_TOKEN`           | Access token       |

## 📊 Project Statistics

- **Backend**: 1 main file (app.py) + 1 API file (backend/main.py)
- **Frontend**: 9 React components/pages
- **Documentation**: 10 markdown files
- **Scripts**: 3 automation scripts
- **Total Lines**: ~2000+ lines of code
- **Languages**: Python, JavaScript, CSS, YAML, Shell

## 🎓 Learning Path

Recommended reading order:

1. Start: [QUICKSTART.md](QUICKSTART.md)
2. Understand: [README.md](README.md)
3. Deep dive: [ARCHITECTURE.md](ARCHITECTURE.md)
4. Deploy: [DEPLOY.md](DEPLOY.md) + [CHECKLIST.md](CHECKLIST.md)
5. Troubleshoot: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

## 🔗 External Resources

- [Databricks Apps Documentation](https://docs.databricks.com/en/dev-tools/databricks-apps/index.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Unity Catalog Documentation](https://docs.databricks.com/en/data-governance/unity-catalog/index.html)

## 📝 Notes

- All documentation is in Markdown format
- Code examples use bash for shell commands
- Python code follows PEP 8 style guide
- React code uses functional components with hooks
- CSS follows Fluent UI design system principles

---

**Last Updated**: Project creation date  
**Version**: 1.0.0  
**Status**: Production Ready ✅
