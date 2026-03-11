# Final Setup Guide

## ✅ O que já está pronto

1. ✅ Código limpo e funcional (React + FastAPI)
2. ✅ Frontend buildado (`frontend/build/`)
3. ✅ Rotas configuradas corretamente
4. ✅ Documentação completa
5. ✅ Scripts de automação
6. ✅ GitHub atualizado

## 🚀 Como rodar AGORA

### Passo 1: Instalar Dependências Python

```bash
pip3 install -r requirements.txt
```

Ou se preferir usar um ambiente virtual:

```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

### Passo 2: Configurar Databricks (Opcional para teste)

```bash
cp .env.example .env
# Editar .env com suas credenciais Databricks
```

Se não tiver credenciais Databricks agora, pode pular este passo. A aplicação vai rodar, mas as APIs de dados não vão funcionar.

### Passo 3: Rodar Aplicação

```bash
python3 app.py
```

Ou com o script:

```bash
./run_local.sh
```

### Passo 4: Acessar

Abra no navegador:

- **Frontend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

## 🎯 O que você deve ver

### Se o frontend está buildado (está!)

Você verá a interface React com:

- Sidebar azul com navegação
- Dashboard com KPI cards
- Páginas: Dashboard, Explorer, Quality

### Se não conectou ao Databricks

- Frontend vai carregar normalmente
- Mas vai mostrar "Loading..." ou erro ao buscar dados
- Isso é normal! Precisa configurar `.env` com credenciais

### Se conectou ao Databricks

- Tudo funciona!
- Dashboard mostra métricas reais
- Explorer lista tabelas do Unity Catalog
- Quality mostra score de documentação

## 🐛 Troubleshooting

### "Module not found: fastapi"

```bash
pip3 install -r requirements.txt
```

### "Frontend not built"

O frontend JÁ ESTÁ buildado! Se ver essa mensagem, reinicie o servidor:

```bash
# Parar o servidor (Ctrl+C)
# Iniciar novamente
python3 app.py
```

### "Connection failed" nas APIs

Normal se não configurou `.env`. Para testar sem Databricks:

```bash
# Apenas ver se o servidor sobe
python3 app.py

# Acessar
curl http://localhost:8000/
curl http://localhost:8000/api/health
```

## 📦 Deploy no Databricks Apps

Quando estiver pronto para deploy:

```bash
# 1. Validar
databricks bundle validate

# 2. Deploy dev
databricks bundle deploy -t dev

# 3. Ver logs
databricks apps logs data-governance-portal
```

## ✨ Resumo

**Status Atual**: ✅ Tudo pronto para rodar

**Falta apenas**:

1. Instalar dependências Python: `pip3 install -r requirements.txt`
2. Rodar: `python3 app.py`
3. Acessar: http://localhost:8000

**Opcional** (para ver dados reais):

- Configurar `.env` com credenciais Databricks
- Ter SQL Warehouse ativo
- Ter permissões no Unity Catalog

## 🎉 Próximos Passos

1. **Agora**: Rodar local para ver a interface
2. **Depois**: Configurar Databricks para ver dados reais
3. **Por último**: Deploy no Databricks Apps

Qualquer dúvida, veja:

- [QUICKSTART.md](QUICKSTART.md)
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- [TEST_LOCALLY.md](TEST_LOCALLY.md)
