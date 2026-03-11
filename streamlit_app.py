import streamlit as st
import os
import pandas as pd
from datetime import datetime

# Tentar importar databricks-sql-connector
try:
    from databricks import sql
    DATABRICKS_AVAILABLE = True
except ImportError:
    DATABRICKS_AVAILABLE = False

# Configuração da página
st.set_page_config(
    page_title="Data Catalog",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado - Design moderno Microsoft Fluent
st.markdown("""
<style>
    /* Importar fonte Segoe UI */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Background principal */
    .stApp {
        background: linear-gradient(135deg, #F3F2F1 0%, #E1DFDD 100%);
    }
    
    /* Sidebar moderna */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0078D4 0%, #106EBE 100%);
        padding: 2rem 1rem;
    }
    
    [data-testid="stSidebar"] .stRadio > label {
        color: white !important;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    [data-testid="stSidebar"] [role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.1);
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        color: white !important;
        transition: all 0.3s ease;
        cursor: pointer;
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stSidebar"] [role="radiogroup"] label:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateX(5px);
    }
    
    [data-testid="stSidebar"] [role="radiogroup"] label[data-checked="true"] {
        background: white;
        color: #0078D4 !important;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Header principal */
    .main-header {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        margin-bottom: 2rem;
        border-left: 6px solid #0078D4;
    }
    
    .main-header h1 {
        color: #0078D4;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .main-header p {
        color: #605E5C;
        font-size: 1rem;
        margin: 0.5rem 0 0 0;
    }
    
    /* Cards KPI modernos */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .kpi-card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #0078D4, #00BCF2);
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0, 120, 212, 0.2);
    }
    
    .kpi-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .kpi-value {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #0078D4 0%, #00BCF2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0.5rem 0;
    }
    
    .kpi-label {
        font-size: 0.95rem;
        color: #605E5C;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .kpi-trend {
        font-size: 0.85rem;
        color: #107C10;
        margin-top: 0.5rem;
        font-weight: 600;
    }
    
    /* Card de conteúdo */
    .content-card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        margin: 1rem 0;
    }
    
    .content-card h3 {
        color: #0078D4;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Search bar moderna */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #E1DFDD;
        padding: 1rem 1.5rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        background: white;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #0078D4;
        box-shadow: 0 0 0 4px rgba(0, 120, 212, 0.1);
    }
    
    /* Selectbox moderna */
    .stSelectbox > div > div {
        border-radius: 12px;
        border: 2px solid #E1DFDD;
        background: white;
    }
    
    /* Tabelas modernas */
    .dataframe {
        border: none !important;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }
    
    .dataframe thead tr th {
        background: linear-gradient(135deg, #0078D4 0%, #106EBE 100%);
        color: white !important;
        font-weight: 600;
        padding: 1rem;
        text-align: left;
    }
    
    .dataframe tbody tr:hover {
        background: #F3F2F1;
    }
    
    /* Tabs modernas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: white;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0078D4 0%, #00BCF2 100%);
        color: white;
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.2rem;
    }
    
    .badge-success {
        background: #DFF6DD;
        color: #107C10;
    }
    
    .badge-warning {
        background: #FFF4CE;
        color: #F7630C;
    }
    
    .badge-danger {
        background: #FDE7E9;
        color: #D13438;
    }
    
    .badge-info {
        background: #E6F3FF;
        color: #0078D4;
    }
    
    /* Animações */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .content-card, .kpi-card {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Esconder elementos do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation com ícones
st.sidebar.markdown("# 🎯 Data Catalog")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navegação",
    ["🏠 Home", "🔍 Explorer", "🔎 Search", "🛡️ Governance"],
    label_visibility="collapsed"
)

# Função para conectar ao Databricks (mock para desenvolvimento)
def get_sample_data():
    """Retorna dados de exemplo para desenvolvimento"""
    return {
        "catalogs": ["main", "samples", "analytics"],
        "schemas": {
            "main": ["default", "bronze", "silver", "gold"],
            "samples": ["nyctaxi", "tpch"],
            "analytics": ["marketing", "sales", "finance"]
        },
        "tables": {
            "default": ["customers", "orders", "products", "transactions"],
            "bronze": ["raw_events", "raw_logs"],
            "silver": ["cleaned_events", "processed_logs"],
            "gold": ["customer_360", "sales_metrics"]
        }
    }

def get_kpis():
    """Retorna KPIs de exemplo"""
    return {
        "total_tables": 247,
        "tables_without_desc": 89,
        "data_volume": "12.4 TB",
        "pii_columns": 156,
        "last_updated": datetime.now().strftime("%d/%m/%Y %H:%M")
    }

# HOME PAGE
if page == "🏠 Home":
    st.markdown("""
    <div class="main-header">
        <h1>📊 Dashboard</h1>
        <p>Visão geral do seu catálogo de dados no Unity Catalog</p>
    </div>
    """, unsafe_allow_html=True)
    
    kpis = get_kpis()
    
    # KPIs em grid
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">📚</div>
            <div class="kpi-value">{kpis['total_tables']}</div>
            <div class="kpi-label">Total de Tabelas</div>
            <div class="kpi-trend">↑ 12% este mês</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">⚠️</div>
            <div class="kpi-value">{kpis['tables_without_desc']}</div>
            <div class="kpi-label">Sem Descrição</div>
            <div class="kpi-trend" style="color: #D13438;">↓ Requer atenção</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">💾</div>
            <div class="kpi-value">{kpis['data_volume']}</div>
            <div class="kpi-label">Volume de Dados</div>
            <div class="kpi-trend">↑ 2.3 TB este mês</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">🔒</div>
            <div class="kpi-value">{kpis['pii_columns']}</div>
            <div class="kpi-label">Colunas PII</div>
            <div class="kpi-trend">Monitoradas</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Gráficos e informações adicionais
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="content-card">
            <h3>📈 Tabelas Mais Acessadas</h3>
        </div>
        """, unsafe_allow_html=True)
        
        df_top = pd.DataFrame({
            "Tabela": ["customer_360", "sales_metrics", "product_catalog", "user_events", "transactions"],
            "Acessos": [1250, 980, 756, 654, 543],
            "Status": ["🟢 Ativo", "🟢 Ativo", "🟢 Ativo", "🟡 Alerta", "🟢 Ativo"]
        })
        st.dataframe(df_top, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("""
        <div class="content-card">
            <h3>🎯 Qualidade dos Dados</h3>
        </div>
        """, unsafe_allow_html=True)
        
        df_quality = pd.DataFrame({
            "Métrica": ["Documentação", "Freshness", "Completude", "Consistência"],
            "Score": ["64%", "92%", "88%", "95%"],
            "Tendência": ["↓", "↑", "↑", "→"]
        })
        st.dataframe(df_quality, use_container_width=True, hide_index=True)

# EXPLORER PAGE
elif page == "🔍 Explorer":
    st.markdown("""
    <div class="main-header">
        <h1>🔍 Explorer</h1>
        <p>Navegue pela hierarquia Catalog → Schema → Table</p>
    </div>
    """, unsafe_allow_html=True)
    
    data = get_sample_data()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        catalog = st.selectbox("📁 Catalog", ["Selecione..."] + data["catalogs"])
    
    with col2:
        if catalog and catalog != "Selecione...":
            schemas = data["schemas"].get(catalog, [])
            schema = st.selectbox("📂 Schema", ["Selecione..."] + schemas)
        else:
            schema = st.selectbox("📂 Schema", ["Selecione..."])
    
    with col3:
        if schema and schema != "Selecione...":
            tables = data["tables"].get(schema, [])
            table = st.selectbox("📄 Table", ["Selecione..."] + tables)
        else:
            table = st.selectbox("📄 Table", ["Selecione..."])
    
    if catalog != "Selecione..." and schema != "Selecione..." and table != "Selecione...":
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="content-card">
            <h3>📊 {catalog}.{schema}.{table}</h3>
            <p style="color: #605E5C; margin-top: 0.5rem;">
                <span class="badge badge-success">Ativo</span>
                <span class="badge badge-info">Produção</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Colunas", "📊 Estatísticas", "🔗 Lineage", "📝 Metadados"])
        
        with tab1:
            df_columns = pd.DataFrame({
                "Coluna": ["id", "customer_name", "email", "phone", "created_at"],
                "Tipo": ["BIGINT", "STRING", "STRING", "STRING", "TIMESTAMP"],
                "Nullable": ["❌", "✅", "✅", "✅", "❌"],
                "PII": ["❌", "✅", "✅", "✅", "❌"],
                "Descrição": ["ID único", "Nome do cliente", "Email de contato", "Telefone", "Data de criação"]
            })
            st.dataframe(df_columns, use_container_width=True, hide_index=True)
        
        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total de Linhas", "1,234,567", "+5.2%")
                st.metric("Tamanho", "45.2 GB", "+2.1 GB")
            with col2:
                st.metric("Última Atualização", "2 horas atrás")
                st.metric("Partições", "365")
        
        with tab3:
            st.info("🔗 Visualização de lineage em desenvolvimento")
        
        with tab4:
            st.markdown("""
            **Owner:** Data Engineering Team  
            **Tags:** customer, production, pii  
            **Criado em:** 15/01/2024  
            **Última modificação:** Hoje às 14:30
            """)

# SEARCH PAGE
elif page == "🔎 Search":
    st.markdown("""
    <div class="main-header">
        <h1>🔎 Search</h1>
        <p>Busca global em tabelas, colunas e descrições</p>
    </div>
    """, unsafe_allow_html=True)
    
    search_query = st.text_input(
        "🔍",
        placeholder="Digite para buscar tabelas, colunas, descrições...",
        label_visibility="collapsed"
    )
    
    if search_query:
        st.markdown(f"""
        <div class="content-card">
            <h3>🎯 Resultados para "{search_query}"</h3>
        </div>
        """, unsafe_allow_html=True)
        
        df_results = pd.DataFrame({
            "Tipo": ["📄 Tabela", "📄 Tabela", "📋 Coluna", "📋 Coluna"],
            "Nome": ["customer_data", "customer_360", "customer_name", "customer_id"],
            "Localização": ["main.bronze", "main.gold", "main.silver.users", "main.bronze.raw"],
            "Relevância": ["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐⭐"]
        })
        st.dataframe(df_results, use_container_width=True, hide_index=True)
    else:
        st.markdown("""
        <div class="content-card">
            <h3>💡 Dicas de Busca</h3>
            <ul style="color: #605E5C; line-height: 2;">
                <li>Use palavras-chave para encontrar tabelas e colunas</li>
                <li>Busque por nomes de schemas ou catalogs</li>
                <li>Procure por descrições e metadados</li>
                <li>Filtre por tags e owners</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# GOVERNANCE PAGE
elif page == "🛡️ Governance":
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ Governance</h1>
        <p>Monitoramento de PII e qualidade da documentação</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔒 Colunas Sensíveis (PII)", "📝 Documentação Faltante"])
    
    with tab1:
        st.markdown("""
        <div class="content-card">
            <h3>🔒 Colunas com Dados Sensíveis Identificadas</h3>
        </div>
        """, unsafe_allow_html=True)
        
        df_pii = pd.DataFrame({
            "Tabela": ["customers", "users", "orders", "employees", "contacts"],
            "Coluna": ["email", "phone", "credit_card", "ssn", "address"],
            "Tipo PII": ["Email", "Telefone", "Cartão", "SSN", "Endereço"],
            "Risco": ["🟡 Médio", "🟡 Médio", "🔴 Alto", "🔴 Alto", "🟡 Médio"],
            "Ação": ["Mascarar", "Mascarar", "Criptografar", "Criptografar", "Mascarar"]
        })
        st.dataframe(df_pii, use_container_width=True, hide_index=True)
        
        st.markdown("""
        <div style="margin-top: 1rem;">
            <span class="badge badge-danger">🔴 Alto Risco: 45 colunas</span>
            <span class="badge badge-warning">🟡 Médio Risco: 89 colunas</span>
            <span class="badge badge-success">🟢 Baixo Risco: 22 colunas</span>
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        <div class="content-card">
            <h3>📝 Tabelas e Colunas sem Documentação</h3>
        </div>
        """, unsafe_allow_html=True)
        
        df_missing = pd.DataFrame({
            "Tabela": ["raw_events", "temp_data", "staging_users", "legacy_orders", "test_table"],
            "Schema": ["bronze", "bronze", "silver", "gold", "dev"],
            "Colunas sem Desc.": [12, 8, 15, 6, 20],
            "Última Atualização": ["3 dias", "1 semana", "2 dias", "1 mês", "6 meses"],
            "Prioridade": ["🔴 Alta", "🟡 Média", "🔴 Alta", "🟡 Média", "🟢 Baixa"]
        })
        st.dataframe(df_missing, use_container_width=True, hide_index=True)
        
        st.warning("⚠️ 89 tabelas (36%) estão sem descrição adequada. Recomenda-se documentar para melhorar a governança.")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: #605E5C; font-size: 0.85rem; padding: 2rem;">
    Data Catalog v1.0 | Powered by Databricks Unity Catalog | Última atualização: {}
</div>
""".format(datetime.now().strftime("%d/%m/%Y %H:%M")), unsafe_allow_html=True)
