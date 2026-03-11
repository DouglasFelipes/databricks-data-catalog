# Enterprise Data Governance Portal

**Arquitetura Desacoplada: React + FastAPI + Unity Catalog**

## 🏗️ Arquitetura

### Backend (FastAPI)

- **Framework**: FastAPI com Pydantic para validação
- **Database**: Databricks SQL Connector para Unity Catalog
- **Endpoints**: RESTful API com documentação automática (Swagger)
- **Performance**: Queries otimizadas com cálculos SQL

### Frontend (React + Fluent UI)

- **Framework**: React 18 com Hooks
- **UI Library**: @fluentui/react (Microsoft Fluent Design System)
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **Design**: Idêntico ao Microsoft 365

### Data Layer

- **Source**: Unity Catalog via `system.information_schema`
- **Connector**: databricks-sql-connector (Python)
- **Queries**: SQL otimizado com cálculos no banco
- **Validation**: Tratamento de KeyError com validação SQL

## 📁 Estrutura do Projeto

```
.
├── backend/
│   └── main.py                 # FastAPI application
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── Layout.js       # LeftNav + CommandBar
│   │   │   ├── KPICard.js      # Metric cards
│   │   │   └── TableList.js    # Fluent DetailsList
│   │   ├── pages/
│   │   │   ├── Dashboard.js    # Home page
│   │   │   ├── Explorer.js     # Data discovery
│   │   │   └── Quality.js      # Quality insights
│   │   ├── App.js              # Main app with routing
│   │   └── index.js            # Entry point
│   └── package.json
├── databricks.yml              # Databricks Apps config
├── app.yaml                    # Deployment config
├── requirements.txt            # Python dependencies
└── README.md
```

## 🚀 API Endpoints

### Health Check

```
GET /api/health
Response: { status, timestamp, databricks_connected }
```

### Inventory

```
GET /api/inventory
Response: {
  total_table: int,
  missing_description_count: int,
  documentation_score: float,
  catalog_list: [string],
  table_list: [TableMetadata]
}
```

### Lineage

```
GET /api/lineage/{catalog}/{schema}/{table}
Response: {
  catalog: string,
  schema: string,
  table: string,
  column_list: [ColumnMetadata]
}
```

### Schema List

```
GET /api/catalog/{catalog}/schema
Response: { catalog, schema_list }
```

### Table List

```
GET /api/catalog/{catalog}/schema/{schema}/table
Response: { catalog, schema, table_list }
```

## 🎨 Design System (Fluent UI)

### Components

- **LeftNav**: Side navigation rail com gradiente azul
- **CommandBar**: Top bar para ações globais
- **DetailsList**: Tabelas com sorting e filtering
- **KPI Cards**: Métricas com hover effects
- **Badges**: Status indicators semânticos

### Paleta de Cores

- Primary: `#0078d4`
- Background: `#faf9f8`
- Surface: `#ffffff`
- Border: `#edebe9`
- Text Primary: `#323130`
- Text Secondary: `#605e5c`

### Nomenclatura (Singular)

- `/api/inventory` (não inventories)
- `/api/lineage` (não lineages)
- `table_list` (não tables)
- `column_list` (não columns)

## 🔧 Instalação e Deploy

### 1. Desenvolvimento Local

#### Backend

```bash
cd backend
pip install -r ../requirements.txt
uvicorn main:app --reload --port 8000
```

#### Frontend

```bash
cd frontend
npm install
npm start
```

### 2. Deploy no Databricks Apps

#### Configurar variáveis de ambiente

```bash
export DATABRICKS_HOST=your-workspace.cloud.databricks.com
export DATABRICKS_SERVER_HOSTNAME=your-workspace.cloud.databricks.com
export DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/your-warehouse-id
export DATABRICKS_TOKEN=your-token
```

#### Deploy via CLI

```bash
databricks apps deploy data-governance-portal
```

#### Deploy via Interface

1. Acesse **Apps** no Databricks
2. Crie novo app ou selecione existente
3. Configure source code path
4. Clique em **Deploy**

## 🐛 Correção de Erros

### KeyError: 'missing_description'

**Problema**: Coluna calculada não existe no DataFrame

**Solução**: Cálculo movido para SQL

```sql
CASE
    WHEN comment IS NULL OR TRIM(comment) = '' THEN true
    ELSE false
END as missing_description
```

### CORS Issues

**Solução**: Middleware configurado no FastAPI

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
```

## 📊 Queries SQL Otimizadas

### Inventory Query

```sql
SELECT
    table_catalog as catalog,
    table_schema as schema,
    table_name,
    table_type,
    comment as description,
    CASE
        WHEN comment IS NULL OR TRIM(comment) = '' THEN true
        ELSE false
    END as missing_description
FROM system.information_schema.tables
WHERE table_catalog NOT IN ('system', 'information_schema')
ORDER BY table_catalog, table_schema, table_name
```

### Column Lineage Query

```sql
SELECT
    column_name,
    data_type,
    is_nullable,
    comment as description,
    ordinal_position
FROM system.information_schema.columns
WHERE table_catalog = '{catalog}'
AND table_schema = '{schema}'
AND table_name = '{table}'
ORDER BY ordinal_position
```

## 🎯 Features

### Dashboard

- KPI cards com métricas em tempo real
- Total de tabelas, documentação, score
- Lista completa de tabelas com DetailsList
- Badges para status de documentação

### Explorer

- Navegação hierárquica: Catalog → Schema → Table
- Dropdowns em cascata
- Visualização de colunas com metadados
- Tipos de dados e nullable indicators

### Quality

- Tabelas sem documentação destacadas
- Score de qualidade calculado
- Alertas visuais (badges amarelos)
- Métricas de governança

## 🔐 Permissões (databricks.yml)

```yaml
permissions:
  - level: CAN_MANAGE
    group_name: "data-engineers"
  - level: CAN_USE
    group_name: "data-analysts"
```

## 📦 Dependências

### Python (requirements.txt)

- fastapi==0.104.1
- uvicorn[standard]==0.24.0
- databricks-sql-connector==3.0.0
- pydantic==2.5.0
- python-dotenv==1.0.0

### JavaScript (package.json)

- @fluentui/react: ^8.110.0
- @fluentui/react-icons: ^2.0.220
- react: ^18.2.0
- react-router-dom: ^6.20.0
- axios: ^1.6.0

## 🚀 Performance

- Queries otimizadas no SQL
- Cálculos no banco (não no Python)
- Validação de dados antes do processamento
- Lazy loading de colunas
- React memoization para componentes

## 📝 Próximos Passos

- [ ] Cache Redis para queries frequentes
- [ ] WebSocket para updates em tempo real
- [ ] Data Lineage visualization
- [ ] PII detection automática
- [ ] Export de relatórios (PDF/Excel)
- [ ] Alertas e notificações
- [ ] Audit log

## 👥 Contribuindo

Pull requests são bem-vindos! Para mudanças importantes, abra uma issue primeiro.

## 📄 Licença

MIT License

---

**Desenvolvido com ❤️ usando FastAPI + React + Fluent UI**
