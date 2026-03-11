# Databricks Apps Deployment Guide

## ✅ Databricks Apps SUPORTA npm!

Segundo a [documentação oficial](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/deploy), o Databricks Apps detecta automaticamente se você tem um projeto Node.js e executa o build.

## 🔄 Como Funciona o Deploy

### Se `package.json` existe na raiz do projeto:

1. ✅ `npm install` - Instala dependências Node
2. ✅ `pip install -r requirements.txt` - Instala dependências Python (se existir)
3. ✅ `npm run build` - Builda o frontend (se o script existir no package.json)
4. ✅ Executa o comando especificado em `app.yaml`, ou `npm run start` se não especificado

### Se `package.json` NÃO existe:

1. ✅ `pip install -r requirements.txt` - Instala dependências Python
2. ✅ Executa o comando em `app.yaml`, ou `python app.py` por padrão

## 📦 Nossa Estrutura

Nosso projeto tem:

- ✅ `package.json` na raiz? **NÃO** (está em `frontend/package.json`)
- ✅ `requirements.txt` na raiz? **SIM**
- ✅ `app.yaml` na raiz? **SIM**

## 🎯 Solução: Duas Opções

### Opção 1: Mover package.json para raiz (Recomendado para Databricks)

```bash
# Mover package.json para raiz
mv frontend/package.json .

# Atualizar scripts no package.json
{
  "scripts": {
    "build": "cd frontend && npm run build",
    "start": "python app.py"
  }
}
```

**Vantagem**: Databricks detecta automaticamente e roda `npm run build`

### Opção 2: Build manual antes do deploy (Atual)

```bash
# Build frontend localmente
cd frontend
npm install
npm run build
cd ..

# Deploy
databricks bundle deploy -t dev
```

**Vantagem**: Controle total do processo

## 📝 Arquivos de Configuração

### app.yaml (Já criado)

```yaml
# Comando para iniciar a aplicação
command: ["python", "app.py"]

# Variáveis de ambiente
env:
  - name: PORT
    value: "8000"
  - name: DATABRICKS_SERVER_HOSTNAME
    value: "{{secrets/databricks/server_hostname}}"
  - name: DATABRICKS_HTTP_PATH
    value: "{{secrets/databricks/http_path}}"
  - name: DATABRICKS_TOKEN
    value: "{{secrets/databricks/token}}"
```

### databricks.yml (Simplificado)

```yaml
bundle:
  name: data-governance-portal

resources:
  apps:
    governance_portal:
      name: data-governance-portal
      description: "Enterprise Data Governance Portal"

targets:
  dev:
    mode: development
  prod:
    mode: production
```

## 🚀 Processo de Deploy

### 1. Configurar Secrets no Databricks

```bash
# Criar scope de secrets
databricks secrets create-scope databricks

# Adicionar secrets
databricks secrets put-secret databricks server_hostname
databricks secrets put-secret databricks http_path
databricks secrets put-secret databricks token
```

### 2. Build Frontend (se não moveu package.json)

```bash
cd frontend
npm install
npm run build
cd ..
```

### 3. Validar Bundle

```bash
databricks bundle validate
```

### 4. Deploy

```bash
# Deploy dev
databricks bundle deploy -t dev

# Deploy prod
databricks bundle deploy -t prod
```

### 5. Verificar Logs

```bash
databricks apps logs data-governance-portal
```

## 📊 O que Acontece no Deploy

1. **Upload dos arquivos** para Databricks workspace
2. **Detecção de dependências**:
   - Se `package.json` na raiz: roda `npm install` e `npm run build`
   - Sempre roda `pip install -r requirements.txt`
3. **Execução do comando** definido em `app.yaml`
4. **Container inicia** e serve a aplicação

## 🎯 Estrutura Esperada no Databricks

```
/Workspace/apps/data-governance-portal/
├── app.py                    # Entry point
├── app.yaml                  # Runtime config
├── backend/
│   └── main.py              # API routes
├── frontend/
│   ├── build/               # React build (já buildado)
│   │   ├── index.html
│   │   └── static/
│   └── package.json
├── requirements.txt         # Python deps
└── databricks.yml          # Bundle config
```

## ✅ Checklist de Deploy

- [ ] Frontend buildado (`frontend/build/` existe)
- [ ] Secrets configurados no Databricks
- [ ] `databricks bundle validate` passa
- [ ] SQL Warehouse ativo
- [ ] Permissões configuradas
- [ ] Deploy executado
- [ ] Logs verificados
- [ ] App acessível

## 🐛 Troubleshooting

### "npm: command not found"

Databricks Apps tem Node.js instalado. Se ver esse erro, verifique se `package.json` está na raiz.

### "Frontend not built"

Build o frontend antes do deploy:

```bash
cd frontend && npm run build && cd ..
```

### "Connection failed"

Verifique se os secrets estão configurados corretamente:

```bash
databricks secrets list-secrets databricks
```

### "App not available"

Verifique os logs:

```bash
databricks apps logs data-governance-portal --level debug
```

## 📚 Referências

- [Databricks Apps Deploy Documentation](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/deploy)
- [Node.js Tutorial](https://docs.databricks.com/aws/dev-tools/databricks-apps/tutorial-node)
- [app.yaml Configuration](https://docs.databricks.com/gcp/en/dev-tools/databricks-apps/app-runtime)
- [System Environment](https://docs.databricks.com/gcp/en/dev-tools/databricks-apps/system-env)

## 🎉 Resumo

**SIM, Databricks Apps suporta npm!**

Para nosso projeto:

1. Build frontend localmente: `cd frontend && npm run build`
2. Deploy: `databricks bundle deploy -t dev`
3. Databricks instala Python deps e roda `python app.py`
4. App serve frontend buildado + API

Simples e funcional! 🚀
