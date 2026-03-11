# Deploy Guide - Databricks Apps

## Pré-requisitos

1. Databricks CLI instalado e configurado
2. SQL Warehouse ativo no workspace
3. Permissões no Unity Catalog

## Passo 1: Configurar Variáveis de Ambiente

Crie arquivo `.env` na raiz:

```bash
DATABRICKS_SERVER_HOSTNAME=seu-workspace.cloud.databricks.com
DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/seu-warehouse-id
DATABRICKS_TOKEN=seu-token-aqui
```

## Passo 2: Build do Frontend

```bash
cd frontend
npm install
npm run build
cd ..
```

## Passo 3: Testar Localmente

```bash
# Instalar dependências Python
pip install -r requirements.txt

# Rodar aplicação
python app.py
```

Acesse: http://localhost:8000

## Passo 4: Deploy no Databricks

```bash
# Validar bundle
databricks bundle validate

# Deploy em dev
databricks bundle deploy -t dev

# Deploy em prod
databricks bundle deploy -t prod
```

## Passo 5: Verificar Status

```bash
# Listar apps
databricks apps list

# Ver logs
databricks apps logs data-governance-portal
```

## Troubleshooting

### Erro: "App Not Available"

1. Verificar se o build do React foi feito: `frontend/build/` deve existir
2. Verificar variáveis de ambiente no Databricks
3. Verificar logs: `databricks apps logs data-governance-portal`

### Erro: "Connection Failed"

1. Verificar SQL Warehouse está ativo
2. Verificar token tem permissões corretas
3. Verificar DATABRICKS_HTTP_PATH está correto

### Erro: "No tables found"

1. Verificar permissões no Unity Catalog
2. Verificar query em `system.information_schema.tables`
3. Testar conexão manualmente com databricks-sql-connector
