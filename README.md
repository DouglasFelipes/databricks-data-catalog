# Data Catalog - Databricks

Catálogo de Dados Profissional para Databricks com design Microsoft Fluent.

## Arquitetura

- **Backend**: Node.js + Express (API e gerenciamento)
- **Frontend**: Streamlit (visualização de dados)
- **Deploy**: Databricks Asset Bundles (DABs)

## Funcionalidades

- **Home**: Dashboard com KPIs principais
- **Explorer**: Navegação Catalog > Schema > Table
- **Search**: Busca global de tabelas e colunas
- **Governance**: Identificação de PII e documentação faltante

## Instalação

### 1. Instalar dependências Node.js

```bash
npm install
```

### 2. Instalar dependências Python

```bash
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente

```bash
cp .env.example .env
# Edite o arquivo .env com suas credenciais Databricks
```

## Executar Localmente

### Iniciar servidor Express

```bash
npm start
```

### Iniciar Streamlit

```bash
streamlit run streamlit_app.py
```

## Deploy no Databricks

### 1. Instalar Databricks CLI

```bash
pip install databricks-cli
```

### 2. Configurar autenticação

```bash
databricks configure --token
```

### 3. Deploy com DABs

```bash
databricks bundle deploy -t dev
```

### 4. Executar aplicação

```bash
databricks bundle run data_catalog -t dev
```

## Design System

- **Cor de fundo**: #F3F2F1
- **Cor primária**: #0078D4
- **Estilo**: Microsoft Fluent Design
- **Componentes**: Cards com bordas arredondadas, sombras suaves

## Estrutura do Projeto

```
.
├── server.js              # Servidor Express
├── streamlit_app.py       # Aplicação Streamlit
├── databricks.yml         # Configuração DABs
├── package.json           # Dependências Node.js
├── requirements.txt       # Dependências Python
└── README.md             # Documentação
```

## Próximos Passos

1. Conectar ao Unity Catalog via `system.information_schema`
2. Implementar queries para KPIs
3. Adicionar lógica de detecção de PII
4. Implementar busca full-text
5. Adicionar cache para performance
