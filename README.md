# Data Catalog - Databricks

Catálogo de Dados Profissional para Databricks com design Microsoft Fluent e integração real com Unity Catalog.

## 🎨 Design

Interface moderna inspirada no site da Microsoft com:

- Design Microsoft Fluent
- JavaScript vanilla para performance máxima
- Responsivo e acessível
- Animações suaves e transições

## 🚀 Funcionalidades

- **Home**: Dashboard com KPIs em tempo real do Unity Catalog
- **Explorer**: Navegação hierárquica Catalog → Schema → Table
- **Search**: Busca global em tabelas e colunas
- **Governance**: Identificação de PII e documentação faltante

## 📦 Instalação

### 1. Instalar dependências

```bash
npm install
```

### 2. Configurar variáveis de ambiente

```bash
cp .env.example .env
# Edite o arquivo .env com suas credenciais Databricks
```

Variáveis necessárias:

```
DATABRICKS_HOST=dbc-xxxxx.cloud.databricks.com
DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/xxxxx
DATABRICKS_TOKEN=dapi...
PORT=8000
```

### 3. Executar localmente

```bash
npm start
```

Acesse: http://localhost:8000

## 🔧 Deploy no Databricks Apps

### Opção 1: Via Databricks CLI

```bash
# Instalar CLI
pip install databricks-cli

# Configurar
databricks configure --token

# Sync contínuo (deixe rodando)
databricks sync --watch . /Workspace/Users/seu-email/databricks-data-catalog

# Deploy (em outro terminal)
databricks apps deploy databricks-data-catalog
```

### Opção 2: Via Interface Web

1. No Databricks, vá em **Apps**
2. Selecione seu app **databricks-data-catalog**
3. Clique em **Deploy** ou **Redeploy**

## 🏗️ Arquitetura

```
├── server.js              # Backend Node.js/Express
├── public/
│   ├── index.html        # HTML principal
│   ├── app.js            # JavaScript frontend
│   └── styles.css        # CSS Microsoft Fluent
├── app.yaml              # Config Databricks Apps
└── package.json          # Dependências
```

## 🔌 API Endpoints

- `GET /api/health` - Status da API
- `GET /api/kpis` - KPIs do Unity Catalog
- `GET /api/catalogs` - Lista de catalogs
- `GET /api/schemas/:catalog` - Schemas de um catalog
- `GET /api/tables/:catalog/:schema` - Tabelas de um schema
- `GET /api/table/:catalog/:schema/:table` - Detalhes de uma tabela
- `GET /api/search?q=query` - Busca global

## 🎯 Integração com Unity Catalog

O app se conecta diretamente ao Unity Catalog via:

- `system.information_schema.tables` - Metadados de tabelas
- `system.information_schema.columns` - Metadados de colunas
- Databricks SQL Connector para Node.js

## 🔐 Autenticação

Suporta dois métodos:

1. **OAuth M2M** (automático no Databricks Apps)
2. **Personal Access Token** (para desenvolvimento local)

## 📊 Dados Reais

Todos os KPIs e dados são buscados em tempo real do Unity Catalog:

- Total de tabelas
- Tabelas sem descrição
- Estrutura de catalogs/schemas/tables
- Metadados de colunas

## 🎨 Customização

Para alterar cores e estilos, edite `public/styles.css`:

```css
:root {
  --primary: #0078d4;
  --secondary: #50e6ff;
  --background: #fafafa;
}
```

## 📝 Licença

MIT License

## 👥 Contribuindo

Pull requests são bem-vindos!
