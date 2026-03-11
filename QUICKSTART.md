# Quick Start Guide

## 🚀 5 Minutos para Rodar Local

### 1. Clone e Configure

```bash
# Copiar template de ambiente
cp .env.example .env

# Editar com suas credenciais Databricks
nano .env  # ou vim, code, etc.
```

### 2. Rodar Aplicação

```bash
# Opção A: Script automático
./start.sh

# Opção B: Modo desenvolvimento (hot reload)
./dev.sh
```

### 3. Acessar

- **Produção**: http://localhost:8000
- **Desenvolvimento**: http://localhost:3000

## 📦 Deploy no Databricks (2 Minutos)

### 1. Build Frontend

```bash
cd frontend
npm install
npm run build
cd ..
```

### 2. Validar

```bash
python validate.py
```

### 3. Deploy

```bash
databricks bundle deploy -t dev
```

## 🔧 Comandos Úteis

### Desenvolvimento

```bash
# Rodar backend apenas
python backend/main.py

# Rodar frontend apenas
cd frontend && npm start

# Validar setup
python validate.py

# Ver estrutura do projeto
tree -L 2 -I 'node_modules|__pycache__|.git'
```

### Deploy

```bash
# Validar bundle
databricks bundle validate

# Deploy dev
databricks bundle deploy -t dev

# Deploy prod
databricks bundle deploy -t prod

# Ver logs
databricks apps logs data-governance-portal

# Listar apps
databricks apps list
```

### Troubleshooting

```bash
# Reinstalar dependências Python
pip install -r requirements.txt --force-reinstall

# Limpar e rebuildar frontend
cd frontend
rm -rf node_modules build
npm install
npm run build
cd ..

# Testar conexão Databricks
python -c "from databricks import sql; print('OK')"

# Ver variáveis de ambiente
cat .env
```

## 📝 Checklist Rápido

Antes de deploy:

- [ ] `.env` configurado
- [ ] `python validate.py` passou
- [ ] `frontend/build/` existe
- [ ] App roda local sem erros
- [ ] SQL Warehouse está ativo

## 🆘 Problemas Comuns

### "App Not Available"

```bash
# Verificar se frontend foi buildado
ls frontend/build/

# Se não existir
cd frontend && npm run build && cd ..
```

### "Connection Failed"

```bash
# Verificar variáveis
cat .env

# Testar conexão
python validate.py
```

### "No tables found"

```bash
# Verificar permissões no Unity Catalog
# Você precisa de: USE CATALOG, USE SCHEMA, SELECT
```

## 📚 Documentação Completa

- [README.md](README.md) - Visão geral
- [ARCHITECTURE.md](ARCHITECTURE.md) - Arquitetura detalhada
- [DEPLOY.md](DEPLOY.md) - Guia de deploy completo
- [CHECKLIST.md](CHECKLIST.md) - Checklist de deploy
