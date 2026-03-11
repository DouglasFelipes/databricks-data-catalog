# Test Locally - Quick Guide

## Teste Rápido (Sem Databricks)

Para testar se a estrutura está correta sem conectar ao Databricks:

```bash
# 1. Instalar dependências
pip install fastapi uvicorn python-dotenv pydantic

# 2. Testar imports
python3 test_app.py

# 3. Iniciar servidor (vai falhar ao conectar, mas mostra as rotas)
python3 app.py
```

## Teste Completo (Com Databricks)

```bash
# 1. Configurar .env
cp .env.example .env
# Editar .env com suas credenciais

# 2. Instalar todas as dependências
pip install -r requirements.txt

# 3. Validar setup
python3 validate.py

# 4. Iniciar aplicação
python3 app.py
```

## Testar Rotas da API

Com o servidor rodando (python3 app.py):

```bash
# Health check
curl http://localhost:8000/api/health

# Inventory (requer Databricks configurado)
curl http://localhost:8000/api/inventory

# Lineage (requer Databricks configurado)
curl http://localhost:8000/api/lineage/main/default/users
```

## Verificar Rotas Disponíveis

Acesse no navegador:

- http://localhost:8000/docs - Swagger UI (documentação interativa)
- http://localhost:8000/redoc - ReDoc (documentação alternativa)

## Estrutura de Rotas

```
GET  /                                      → Frontend ou mensagem
GET  /api/health                           → Health check
GET  /api/inventory                        → Lista de tabelas
GET  /api/lineage/{catalog}/{schema}/{table} → Colunas da tabela
```

## Troubleshooting

### Erro: "Module not found"

```bash
pip install -r requirements.txt
```

### Erro: "Connection failed"

```bash
# Verificar .env
cat .env

# Testar conexão
python3 validate.py
```

### Erro: "Not Found" nas rotas

```bash
# Verificar se as rotas estão registradas
python3 test_app.py
```
