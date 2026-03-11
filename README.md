# Enterprise Data Governance Portal

**Lead Product Designer & Senior Full Stack Developer**  
Fluent UI Design System + Real Databricks Unity Catalog Integration

## 🎯 Overview

Enterprise-grade Data Governance Portal com design Microsoft Fluent UI e integração real com Databricks Unity Catalog. Desenvolvido seguindo as melhores práticas de UX/UI da Microsoft 365.

## ✨ Features

### Design System (Microsoft Fluent UI)

- **Side Navigation Rail** - Navegação lateral com gradiente azul Microsoft
- **Top Command Bar** - Barra de comandos superior para ações globais
- **Fluent Cards** - Containers com bordas de 8px e sombras sutis de 4px
- **Loading Shimmer** - Estados de carregamento elegantes
- **Micro-interações** - Transições suaves e hover effects
- **Tipografia Segoe UI** - Fonte oficial da Microsoft

### Paleta de Cores (Fluent Neutral)

- Background: `#F3F2F1`
- Canvas: `#FFFFFF`
- Primary: `#0078D4`
- Secondary: `#50E6FF`
- Text Primary: `#323130`
- Text Secondary: `#605E5C`

### Data Layer (Real Unity Catalog)

- ✅ **Zero Mock Data** - Apenas dados reais do Unity Catalog
- ✅ **st.connection("sql")** - Conexão nativa com Databricks
- ✅ **system.information_schema** - Metadados de tabelas e colunas
- ✅ **Cache com TTL 10min** - Otimização de DBU com `@st.cache_data(ttl=600)`
- ✅ **Normalização Singular** - Nomes de colunas e tabelas no singular

### Funcionalidades

#### 🏠 Dashboard

- KPIs em tempo real do Unity Catalog
- Total de tabelas, tabelas sem descrição, score de documentação
- Visão geral por catalog
- Tabs: Overview, Schema Explorer, Data Quality

#### 🔍 Data Discovery

- Navegação hierárquica: Catalog → Schema → Table
- Exploração de colunas com metadados completos
- Busca e filtros avançados

#### 📊 Quality Insights

- Score de documentação calculado em tempo real
- Identificação de tabelas sem descrição (Badge Amarelo ⚠️)
- Métricas de governança
- Priorização de ações

## 🚀 Deploy no Databricks Apps

### 1. Configurar Databricks CLI

```bash
pip install databricks-cli
databricks configure --token
```

### 2. Sync do código

```bash
databricks sync --watch . /Workspace/Users/seu-email/data-governance-portal
```

### 3. Deploy

```bash
databricks apps deploy enterprise-data-governance-portal
```

Ou via interface web:

1. Acesse **Apps** no Databricks
2. Selecione seu app
3. Clique em **Deploy**

## 📦 Estrutura do Projeto

```
.
├── app.py                 # Aplicação principal Streamlit
├── app.yaml              # Config Databricks Apps
├── databricks.yml        # Bundle config com permissões
├── requirements.txt      # Dependências Python
└── README.md            # Documentação
```

## 🔧 Arquitetura

### Modular Functions

- `inject_fluent_css()` - Injeta CSS do Fluent Design System
- `get_catalog_metadata()` - Busca metadados do Unity Catalog (cached)
- `get_table_columns()` - Busca colunas de uma tabela (cached)
- `get_data_quality_metrics()` - Calcula métricas de qualidade (cached)
- `render_command_bar()` - Renderiza barra de comandos
- `render_kpi_cards()` - Renderiza cards de KPIs
- `render_overview_tab()` - Tab de visão geral
- `render_schema_explorer_tab()` - Tab de exploração
- `render_data_quality_tab()` - Tab de qualidade

### Cache Strategy

- TTL: 10 minutos (`@st.cache_data(ttl=600)`)
- Otimiza consumo de DBU
- Refresh automático após expiração

### Queries SQL

```sql
-- Metadados de tabelas
SELECT
    table_catalog as catalog,
    table_schema as schema,
    table_name as table_name,
    table_type as type,
    comment as description,
    CASE
        WHEN comment IS NULL OR comment = '' THEN 1
        ELSE 0
    END as missing_description
FROM system.information_schema.tables

-- Colunas de uma tabela
SELECT
    column_name,
    data_type as type,
    is_nullable as nullable,
    comment as description,
    ordinal_position as position
FROM system.information_schema.columns
WHERE table_catalog = '{catalog}'
AND table_schema = '{schema}'
AND table_name = '{table}'
```

## 🎨 Design Guidelines

### Fluent UI Components

- **Cards**: 8px border-radius, 4px box-shadow
- **Hover Effects**: translateY(-4px), shadow elevation
- **Transitions**: cubic-bezier(0.4, 0, 0.2, 1)
- **Badges**: 12px border-radius, semantic colors
- **Loading**: Shimmer effect com gradiente animado

### Badges Semânticos

- 🟢 Success: `#DFF6DD` / `#107C10`
- 🟡 Warning: `#FFF4CE` / `#F7630C`
- 🔴 Danger: `#FDE7E9` / `#D13438`
- 🔵 Info: `#E6F3FF` / `#0078D4`

## 🔐 Permissões (databricks.yml)

```yaml
permissions:
  - level: CAN_MANAGE
    group_name: "data-engineers"
  - level: CAN_USE
    group_name: "data-analysts"
```

## 📊 KPIs Monitorados

1. **Total Tables** - Contagem total de tabelas no Unity Catalog
2. **Missing Description** - Tabelas sem documentação (COMMENT IS NULL)
3. **Documentation Score** - % de tabelas documentadas
4. **Active Catalogs** - Número de catalogs ativos

## 🎯 Governança

### Alertas Visuais

- ⚠️ Badge Amarelo para tabelas sem descrição
- 🔴 Prioridade Alta para tabelas críticas sem documentação
- 📊 Score de qualidade em tempo real

### Métricas de Qualidade

- Documentation Score (%)
- Documented vs Undocumented Tables
- Tables by Catalog
- Column-level metadata completeness

## 🚀 Performance

- Cache de 10 minutos reduz queries repetitivas
- Queries otimizadas no information_schema
- Lazy loading de colunas (apenas quando necessário)
- Shimmer loading para melhor UX

## 📝 Próximos Passos

- [ ] Integração com Data Lineage
- [ ] Detecção automática de PII
- [ ] Alertas e notificações
- [ ] Export de relatórios
- [ ] API REST para integração

## 👥 Contribuindo

Pull requests são bem-vindos! Para mudanças importantes, abra uma issue primeiro.

## 📄 Licença

MIT License

---

**Desenvolvido com ❤️ seguindo Microsoft Fluent Design System**
