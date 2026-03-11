import streamlit as st
import os
import pandas as pd

# Tentar importar databricks-sql-connector
try:
    from databricks import sql
    DATABRICKS_AVAILABLE = True
except ImportError:
    DATABRICKS_AVAILABLE = False

# Configuração da página
st.set_page_config(
    page_title="Data Catalog",
    page_icon="📊",
    layout="wide"
)

# CSS customizado - Microsoft Fluent Design
st.markdown("""
<style>
    .stApp {
        background-color: #F3F2F1;
    }
    .main-header {
        color: #0078D4;
        font-size: 2.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .kpi-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: 700;
        color: #0078D4;
    }
    .kpi-label {
        font-size: 0.9rem;
        color: #605E5C;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("📊 Data Catalog")
page = st.sidebar.radio("Navegação", ["Home", "Explorer", "Search", "Governance"])

# Função para conectar ao Databricks
def get_databricks_connection():
    if not DATABRICKS_AVAILABLE:
        return None
    
    try:
        # Usar OAuth M2M se disponível (Databricks Apps)
        if os.getenv("DATABRICKS_CLIENT_ID") and os.getenv("DATABRICKS_CLIENT_SECRET"):
            connection = sql.connect(
                server_hostname=os.getenv("DATABRICKS_HOST"),
                http_path=os.getenv("DATABRICKS_HTTP_PATH", "/sql/1.0/warehouses/"),
                credentials_provider=lambda: (
                    os.getenv("DATABRICKS_CLIENT_ID"),
                    os.getenv("DATABRICKS_CLIENT_SECRET")
                )
            )
        else:
            # Fallback para token
            connection = sql.connect(
                server_hostname=os.getenv("DATABRICKS_SERVER_HOSTNAME"),
                http_path=os.getenv("DATABRICKS_HTTP_PATH"),
                access_token=os.getenv("DATABRICKS_TOKEN")
            )
        return connection
    except Exception as e:
        st.error(f"Erro ao conectar: {str(e)}")
        return None

# Função para buscar KPIs do Unity Catalog
def fetch_kpis():
    conn = get_databricks_connection()
    if not conn:
        return {"total_tables": 0, "tables_without_desc": 0, "data_volume": "0 TB"}
    
    try:
        cursor = conn.cursor()
        
        # Total de tabelas
        cursor.execute("SELECT COUNT(*) as total FROM system.information_schema.tables")
        total_tables = cursor.fetchone()[0]
        
        # Tabelas sem descrição
        cursor.execute("""
            SELECT COUNT(*) as total 
            FROM system.information_schema.tables 
            WHERE comment IS NULL OR comment = ''
        """)
        tables_without_desc = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        return {
            "total_tables": total_tables,
            "tables_without_desc": tables_without_desc,
            "data_volume": "N/A"
        }
    except Exception as e:
        st.warning(f"Não foi possível buscar KPIs: {str(e)}")
        return {"total_tables": 0, "tables_without_desc": 0, "data_volume": "0 TB"}

# HOME PAGE
if page == "Home":
    st.markdown('<div class="main-header">Dashboard</div>', unsafe_allow_html=True)
    
    # Buscar KPIs
    kpis = fetch_kpis()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{kpis['total_tables']}</div>
            <div class="kpi-label">Total de Tabelas</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{kpis['tables_without_desc']}</div>
            <div class="kpi-label">Tabelas sem Descrição</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{kpis['data_volume']}</div>
            <div class="kpi-label">Volume de Dados</div>
        </div>
        """, unsafe_allow_html=True)

# EXPLORER PAGE
elif page == "Explorer":
    st.markdown('<div class="main-header">Explorer</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        catalog = st.selectbox("Catalog", ["Selecione..."])
    
    with col2:
        schema = st.selectbox("Schema", ["Selecione..."])
    
    with col3:
        table = st.selectbox("Table", ["Selecione..."])
    
    if catalog and schema and table:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Detalhes da Tabela")
        st.markdown('</div>', unsafe_allow_html=True)

# SEARCH PAGE
elif page == "Search":
    st.markdown('<div class="main-header">Search</div>', unsafe_allow_html=True)
    
    search_query = st.text_input("🔍 Buscar tabelas, colunas ou descrições...", placeholder="Digite para buscar")
    
    if search_query:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write("Resultados da busca aparecerão aqui")
        st.markdown('</div>', unsafe_allow_html=True)

# GOVERNANCE PAGE
elif page == "Governance":
    st.markdown('<div class="main-header">Governance</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Colunas Sensíveis (PII)", "Documentação Faltante"])
    
    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write("Identificação de colunas com dados sensíveis")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write("Tabelas e colunas sem descrição")
        st.markdown('</div>', unsafe_allow_html=True)
