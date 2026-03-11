# Deploy Checklist

Use este checklist antes de fazer deploy no Databricks Apps.

## ✅ Pré-Deploy

- [ ] Arquivo `.env` criado e configurado
- [ ] SQL Warehouse ativo no Databricks
- [ ] Token com permissões corretas (USE CATALOG, USE SCHEMA, SELECT)
- [ ] Databricks CLI instalado e configurado
- [ ] Python 3.8+ instalado
- [ ] Node.js 16+ instalado

## ✅ Build

- [ ] Dependências Python instaladas: `pip install -r requirements.txt`
- [ ] Dependências Node instaladas: `cd frontend && npm install`
- [ ] Frontend buildado: `npm run build` (deve criar `frontend/build/`)
- [ ] Validação passou: `python validate.py`

## ✅ Teste Local

- [ ] Aplicação roda localmente: `python app.py`
- [ ] Frontend carrega em http://localhost:8000
- [ ] API responde em http://localhost:8000/api/health
- [ ] Dados do Unity Catalog aparecem no dashboard
- [ ] Navegação entre páginas funciona
- [ ] Explorer mostra colunas ao clicar em tabela

## ✅ Deploy

- [ ] Bundle validado: `databricks bundle validate`
- [ ] Deploy em dev: `databricks bundle deploy -t dev`
- [ ] App acessível no Databricks workspace
- [ ] Logs sem erros: `databricks apps logs data-governance-portal`
- [ ] Funcionalidades testadas no ambiente dev

## ✅ Produção

- [ ] Testes completos em dev
- [ ] Variáveis de ambiente de prod configuradas
- [ ] Deploy em prod: `databricks bundle deploy -t prod`
- [ ] Permissões configuradas para usuários finais
- [ ] Documentação atualizada
- [ ] Equipe notificada

## 🚨 Rollback

Se algo der errado:

```bash
# Ver versões anteriores
databricks apps list-versions data-governance-portal

# Fazer rollback
databricks apps rollback data-governance-portal --version <version-id>
```

## 📊 Monitoramento

Após deploy, monitorar:

- [ ] Logs de erro: `databricks apps logs data-governance-portal --level error`
- [ ] Performance de queries
- [ ] Uso de recursos
- [ ] Feedback dos usuários
