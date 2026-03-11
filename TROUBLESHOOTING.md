# Troubleshooting Guide

## 🔴 Erro: "App Not Available" no Databricks Apps

### Causa

O container do app crashou durante a inicialização.

### Soluções

1. **Verificar se o frontend foi buildado**

```bash
ls frontend/build/
# Deve mostrar: index.html, static/, etc.
```

Se não existir:

```bash
cd frontend
npm install
npm run build
cd ..
```

2. **Verificar logs do Databricks**

```bash
databricks apps logs data-governance-portal
```

3. **Verificar variáveis de ambiente**

```bash
# No Databricks, as variáveis devem estar configuradas
# Verificar databricks.yml tem as variáveis corretas
```

4. **Testar localmente primeiro**

```bash
python app.py
# Deve iniciar sem erros
```

---

## 🔴 Erro: KeyError ou ImportError

### Causa

Dependências Python faltando ou versões incompatíveis.

### Soluções

1. **Reinstalar dependências**

```bash
pip install -r requirements.txt --force-reinstall
```

2. **Verificar versões**

```bash
pip list | grep -E "fastapi|uvicorn|databricks|pydantic"
```

3. **Usar ambiente virtual**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

---

## 🔴 Erro: "Connection Failed" ou "Database connection failed"

### Causa

Credenciais Databricks incorretas ou SQL Warehouse inativo.

### Soluções

1. **Verificar .env**

```bash
cat .env
# Verificar se as 3 variáveis estão preenchidas
```

2. **Verificar SQL Warehouse está ativo**

- Ir no Databricks workspace
- SQL → Warehouses
- Verificar se o warehouse está "Running"
- Se estiver "Stopped", clicar em "Start"

3. **Testar conexão manualmente**

```python
from databricks import sql
import os
from dotenv import load_dotenv

load_dotenv()

connection = sql.connect(
    server_hostname=os.getenv('DATABRICKS_SERVER_HOSTNAME'),
    http_path=os.getenv('DATABRICKS_HTTP_PATH'),
    access_token=os.getenv('DATABRICKS_TOKEN')
)

cursor = connection.cursor()
cursor.execute("SELECT 1")
print(cursor.fetchall())
cursor.close()
connection.close()
print("✅ Connection successful!")
```

4. **Verificar token tem permissões**

- Token precisa de: USE CATALOG, USE SCHEMA, SELECT
- Criar novo token se necessário

---

## 🔴 Erro: "No tables found" ou lista vazia

### Causa

Permissões insuficientes no Unity Catalog.

### Soluções

1. **Verificar permissões**

```sql
-- Rodar no SQL Editor do Databricks
SHOW CATALOGS;
SHOW SCHEMAS IN catalog_name;
SHOW TABLES IN catalog_name.schema_name;
```

2. **Testar query diretamente**

```sql
SELECT * FROM system.information_schema.tables LIMIT 10;
```

3. **Verificar filtros na query**

```python
# Em backend/main.py, a query filtra:
WHERE table_catalog NOT IN ('system', 'information_schema')
# Verificar se seus catálogos não estão sendo filtrados
```

---

## 🔴 Erro: "Module not found" no frontend

### Causa

Dependências Node não instaladas.

### Soluções

1. **Instalar dependências**

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

2. **Verificar versão do Node**

```bash
node --version
# Deve ser 16.x ou superior
```

3. **Limpar cache**

```bash
npm cache clean --force
npm install
```

---

## 🔴 Erro: "Port already in use"

### Causa

Porta 8000 ou 3000 já está sendo usada.

### Soluções

1. **Encontrar processo usando a porta**

```bash
# Linux/Mac
lsof -i :8000
lsof -i :3000

# Windows
netstat -ano | findstr :8000
```

2. **Matar processo**

```bash
# Linux/Mac
kill -9 <PID>

# Windows
taskkill /PID <PID> /F
```

3. **Usar porta diferente**

```bash
# Backend
uvicorn backend.main:app --port 8001

# Frontend
PORT=3001 npm start
```

---

## 🔴 Erro: "databricks bundle validate" falha

### Causa

Configuração incorreta no databricks.yml.

### Soluções

1. **Verificar sintaxe YAML**

```bash
# Usar validador online ou
python -c "import yaml; yaml.safe_load(open('databricks.yml'))"
```

2. **Verificar variáveis de ambiente**

```bash
echo $DATABRICKS_HOST
echo $DATABRICKS_HTTP_PATH
echo $DATABRICKS_TOKEN
```

3. **Verificar Databricks CLI configurado**

```bash
databricks auth login
databricks workspace list
```

---

## 🔴 Erro: CORS no frontend

### Causa

Frontend rodando em porta diferente do backend.

### Soluções

1. **Verificar proxy no package.json**

```json
{
  "proxy": "http://localhost:8000"
}
```

2. **Verificar CORS no backend**

```python
# Em backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em prod, especificar domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🔴 Erro: "React build não funciona"

### Causa

Erros de compilação no código React.

### Soluções

1. **Ver erros de build**

```bash
cd frontend
npm run build
# Ler mensagens de erro
```

2. **Verificar sintaxe JSX**

```bash
npm run build 2>&1 | grep -i error
```

3. **Limpar e rebuildar**

```bash
rm -rf build node_modules
npm install
npm run build
```

---

## 🔴 Performance lenta

### Causa

Muitas tabelas no Unity Catalog.

### Soluções

1. **Adicionar paginação no backend**

```python
@app.get("/api/inventory")
async def get_inventory(limit: int = 100, offset: int = 0):
    query = f"""
    SELECT * FROM system.information_schema.tables
    LIMIT {limit} OFFSET {offset}
    """
```

2. **Adicionar cache**

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_cached_inventory():
    # ...
```

3. **Filtrar por catalog**

```python
@app.get("/api/inventory")
async def get_inventory(catalog: str = None):
    where_clause = f"WHERE table_catalog = '{catalog}'" if catalog else ""
```

---

## 🔴 Erro: "validate.py" falha

### Causa

Algum componente não está configurado corretamente.

### Soluções

1. **Rodar com verbose**

```bash
python validate.py -v
```

2. **Verificar cada componente individualmente**

```bash
# Testar .env
cat .env

# Testar Python deps
pip list

# Testar frontend build
ls frontend/build/

# Testar conexão
python -c "from databricks import sql; print('OK')"
```

---

## 📞 Ainda com problemas?

1. Verificar logs completos:

```bash
databricks apps logs data-governance-portal --level debug
```

2. Testar cada componente isoladamente:

```bash
# Backend apenas
python backend/main.py

# Frontend apenas
cd frontend && npm start
```

3. Verificar documentação:

- [README.md](README.md)
- [ARCHITECTURE.md](ARCHITECTURE.md)
- [DEPLOY.md](DEPLOY.md)

4. Criar issue com:

- Mensagem de erro completa
- Output de `python validate.py`
- Output de `databricks apps logs`
- Versões: `python --version`, `node --version`
