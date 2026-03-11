# Teste Local - Passo a Passo

## 1. Instalar Dependências Python

```bash
pip install -r requirements.txt
```

## 2. Configurar Variáveis de Ambiente

Crie o arquivo `.env` na raiz do projeto:

```bash
# Copiar template
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais Databricks:

```env
DATABRICKS_SERVER_HOSTNAME=seu-workspace.cloud.databricks.com
DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/seu-warehouse-id
DATABRICKS_TOKEN=seu-token-aqui
```

### Como obter as credenciais:

**DATABRICKS_SERVER_HOSTNAME:**

- Acesse seu workspace Databricks
- A URL é algo como: `https://adb-123456789.azuredatabricks.net`
- Use apenas: `adb-123456789.azuredatabricks.net`

**DATABRICKS_HTTP_PATH:**

- Vá em SQL → Warehouses
- Clique no seu warehouse
- Vá em "Connection Details"
- Copie o "HTTP Path": `/sql/1.0/warehouses/abc123def456`

**DATABRICKS_TOKEN:**

- Clique no seu perfil (canto superior direito)
- Settings → Developer → Access Tokens
- Generate New Token
- Copie o token gerado

## 3. Buildar o Frontend

```bash
cd frontend
npm install
npm run build
cd ..
```

Isso vai criar a pasta `frontend/build/` com os arquivos estáticos do React.

## 4. Rodar a Aplicação

```bash
python app.py
```

Você deve ver:

```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## 5. Testar no Navegador

Abra: **http://localhost:8000**

Você deve ver:

- ✅ Interface React com sidebar azul
- ✅ Dashboard com KPI cards
- ✅ Dados do Unity Catalog (se credenciais corretas)

## 6. Testar as APIs

### Health Check

```bash
curl http://localhost:8000/api/health
```

Resposta esperada:

```json
{
  "status": "healthy",
  "timestamp": "2024-03-10T...",
  "databricks_connected": true
}
```

### Inventory

```bash
curl http://localhost:8000/api/inventory
```

Deve retornar lista de tabelas do Unity Catalog.

### Documentação Interativa

Abra: **http://localhost:8000/docs**

Você verá a documentação Swagger com todas as APIs.

## Troubleshooting

### Erro: "Module not found: fastapi"

```bash
pip install -r requirements.txt
```

### Erro: "Connection failed"

Verifique o `.env`:

- Hostname está correto?
- HTTP Path está correto?
- Token é válido?
- SQL Warehouse está ativo?

### Erro: "Frontend not built"

```bash
cd frontend
npm install
npm run build
cd ..
python app.py
```

### Erro: "No tables found"

Verifique permissões no Unity Catalog:

- USE CATALOG
- USE SCHEMA
- SELECT

## Checklist de Teste

- [ ] Dependências Python instaladas
- [ ] `.env` configurado com credenciais
- [ ] Frontend buildado (`frontend/build/` existe)
- [ ] Servidor inicia sem erros
- [ ] http://localhost:8000 mostra interface React
- [ ] http://localhost:8000/api/health retorna "healthy"
- [ ] http://localhost:8000/api/inventory retorna dados
- [ ] Dashboard mostra KPIs e tabelas

## Próximo Passo

Se tudo funcionar localmente, você está pronto para fazer deploy no Databricks Apps!

Ver: [SETUP.md](SETUP.md) para instruções de deploy.
