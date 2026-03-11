"""
Enterprise Data Governance Portal
Lead Product Designer & Senior Full Stack Developer
Fluent UI Design System + Real Databricks Unity Catalog Integration
"""

import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
from typing import Dict, List, Optional

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Enterprise Data Governance Portal",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# FLUENT UI DESIGN SYSTEM - CSS
# ============================================================================

def inject_fluent_css():
    """Inject Microsoft Fluent Design System CSS"""
    st.markdown("""
    <style>
        /* Import Segoe UI Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
        }
        
        /* Main App Background - Fluent Neutral */
        .stApp {
            background-color: #F3F2F1;
        }
        
        /* Sidebar - Side Navigation Rail */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0078D4 0%, #106EBE 100%);
            padding: 0;
        }
        
        [data-testid="stSidebar"] > div:first-child {
            padding: 2rem 1rem;
        }
        
        /* Sidebar Logo Area */
        [data-testid="stSidebar"] .sidebar-logo {
            background: rgba(255, 255, 255, 0.1);
            padding: 1.5rem;
            border-radius: 8px;
            margin-bottom: 2rem;
            text-align: center;
            backdrop-filter: blur(10px);
        }
        
        /* Sidebar Navigation Items */
        [data-testid="stSidebar"] .stRadio > label {
            color: white !important;
            font-size: 0.95rem;
            font-weight: 600;
            margin-bottom: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        [data-testid="stSidebar"] [role="radiogroup"] label {
            background: rgba(255, 255, 255, 0.08);
            padding: 1rem 1.25rem;
            border-radius: 8px;
            margin: 0.5rem 0;
            color: white !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            backdrop-filter: blur(10px);
            border-left: 4px solid transparent;
        }
        
        [data-testid="stSidebar"] [role="radiogroup"] label:hover {
            background: rgba(255, 255, 255, 0.15);
            transform: translateX(4px);
            border-left-color: rgba(255, 255, 255, 0.5);
        }
        
        [data-testid="stSidebar"] [role="radiogroup"] label[data-checked="true"] {
            background: white;
            color: #0078D4 !important;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            border-left-color: #0078D4;
        }
        
        /* Top Command Bar */
        .command-bar {
            background: #FFFFFF;
            padding: 1rem 2rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .command-bar h1 {
            color: #0078D4;
            font-size: 1.75rem;
            font-weight: 600;
            margin: 0;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        
        .command-bar-subtitle {
            color: #605E5C;
            font-size: 0.9rem;
            margin-top: 0.25rem;
        }
        
        /* Canvas Cards - Fluent Container */
        .fluent-card {
            background: #FFFFFF;
            border-radius: 8px;
            padding: 1.5rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
            margin-bottom: 1.5rem;
            border: 1px solid #EDEBE9;
            transition: all 0.3s ease;
        }
        
        .fluent-card:hover {
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
            transform: translateY(-2px);
        }
        
        .fluent-card h3 {
            color: #323130;
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        /* KPI Metrics Cards */
        .kpi-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        
        .kpi-card {
            background: #FFFFFF;
            border-radius: 8px;
            padding: 1.5rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
            border: 1px solid #EDEBE9;
            position: relative;
            overflow: hidden;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .kpi-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #0078D4, #50E6FF);
        }
        
        .kpi-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(0, 120, 212, 0.15);
        }
        
        .kpi-icon {
            font-size: 2rem;
            margin-bottom: 0.75rem;
            display: block;
        }
        
        .kpi-value {
            font-size: 2.5rem;
            font-weight: 700;
            color: #0078D4;
            line-height: 1;
            margin-bottom: 0.5rem;
        }
        
        .kpi-label {
            font-size: 0.85rem;
            color: #605E5C;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .kpi-trend {
            font-size: 0.8rem;
            margin-top: 0.5rem;
            font-weight: 500;
        }
        
        .trend-positive {
            color: #107C10;
        }
        
        .trend-negative {
            color: #D13438;
        }
        
        /* Badges - Fluent Style */
        .badge {
            display: inline-block;
            padding: 0.35rem 0.75rem;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
            margin: 0 0.25rem;
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
        
        .badge-neutral {
            background: #F3F2F1;
            color: #605E5C;
        }
        
        /* Loading Shimmer Effect */
        .shimmer {
            background: linear-gradient(90deg, #F3F2F1 25%, #E1DFDD 50%, #F3F2F1 75%);
            background-size: 200% 100%;
            animation: shimmer 1.5s infinite;
            border-radius: 8px;
            height: 100px;
        }
        
        @keyframes shimmer {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }
        
        /* Streamlit Tabs - Fluent Style */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
            background: #FFFFFF;
            padding: 0.75rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
            border: 1px solid #EDEBE9;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 0.75rem 1.5rem;
            border-radius: 6px;
            font-weight: 500;
            color: #605E5C;
            transition: all 0.2s ease;
            border: none;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background: #F3F2F1;
            color: #0078D4;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #0078D4 0%, #50E6FF 100%);
            color: white !important;
            box-shadow: 0 2px 8px rgba(0, 120, 212, 0.3);
        }
        
        /* DataFrames - Fluent Table Style */
        .dataframe {
            border: none !important;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
        }
        
        .dataframe thead tr th {
            background: #F3F2F1 !important;
            color: #323130 !important;
            font-weight: 600;
            padding: 1rem !important;
            text-align: left;
            border-bottom: 2px solid #EDEBE9 !important;
        }
        
        .dataframe tbody tr {
            transition: background 0.2s ease;
        }
        
        .dataframe tbody tr:hover {
            background: #F3F2F1 !important;
        }
        
        .dataframe tbody tr td {
            padding: 0.875rem 1rem !important;
            border-bottom: 1px solid #EDEBE9 !important;
        }
        
        /* Selectbox - Fluent Style */
        .stSelectbox > div > div {
            border-radius: 6px;
            border: 2px solid #EDEBE9;
            background: #FFFFFF;
            transition: all 0.2s ease;
        }
        
        .stSelectbox > div > div:hover {
            border-color: #0078D4;
        }
        
        /* Text Input - Fluent Style */
        .stTextInput > div > div > input {
            border-radius: 6px;
            border: 2px solid #EDEBE9;
            padding: 0.75rem 1rem;
            transition: all 0.2s ease;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #0078D4;
            box-shadow: 0 0 0 4px rgba(0, 120, 212, 0.1);
        }
        
        /* Metrics - Fluent Style */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            font-weight: 700;
            color: #0078D4;
        }
        
        [data-testid="stMetricLabel"] {
            font-size: 0.85rem;
            color: #605E5C;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        /* Hide Streamlit Branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Animations */
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .fluent-card, .kpi-card {
            animation: fadeIn 0.5s ease-out;
        }
    </style>
    """, unsafe_allow_html=True)

inject_fluent_css()

# ============================================================================
# DATA LAYER - REAL DATABRICKS UNITY CATALOG INTEGRATION
# ============================================================================

@st.cache_data(ttl=600)  # 10 minutes cache
def get_catalog_metadata() -> Dict:
    """
    Fetch metadata from Unity Catalog using system.information_schema
    Returns: Dictionary with catalogs, schemas, tables metadata
    """
    try:
        # Query all tables from information_schema
        query = """
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
        ORDER BY table_catalog, table_schema, table_name
        """
        
        df = st.connection("sql").query(query)
        
        return {
            'tables': df,
            'total_tables': len(df),
            'tables_without_desc': df['missing_description'].sum(),
            'catalogs': df['catalog'].unique().tolist(),
            'schemas': df.groupby('catalog')['schema'].unique().to_dict()
        }
    except Exception as e:
        st.error(f"Error connecting to Unity Catalog: {str(e)}")
        return {
            'tables': pd.DataFrame(),
            'total_tables': 0,
            'tables_without_desc': 0,
            'catalogs': [],
            'schemas': {}
        }

@st.cache_data(ttl=600)
def get_table_columns(catalog: str, schema: str, table: str) -> pd.DataFrame:
    """
    Fetch column metadata for a specific table
    """
    try:
        query = f"""
        SELECT 
            column_name as column_name,
            data_type as type,
            is_nullable as nullable,
            comment as description,
            ordinal_position as position
        FROM system.information_schema.columns
        WHERE table_catalog = '{catalog}'
        AND table_schema = '{schema}'
        AND table_name = '{table}'
        ORDER BY ordinal_position
        """
        
        return st.connection("sql").query(query)
    except Exception as e:
        st.error(f"Error fetching columns: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=600)
def get_data_quality_metrics() -> Dict:
    """
    Calculate data quality metrics
    """
    try:
        metadata = get_catalog_metadata()
        df = metadata['tables']
        
        if df.empty:
            return {
                'documentation_score': 0,
                'total_tables': 0,
                'documented_tables': 0,
                'undocumented_tables': 0
            }
        
        documented = len(df[df['missing_description'] == 0])
        total = len(df)
        
        return {
            'documentation_score': round((documented / total * 100), 1) if total > 0 else 0,
            'total_tables': total,
            'documented_tables': documented,
            'undocumented_tables': total - documented
        }
    except Exception as e:
        st.error(f"Error calculating metrics: {str(e)}")
        return {
            'documentation_score': 0,
            'total_tables': 0,
            'documented_tables': 0,
            'undocumented_tables': 0
        }

# ============================================================================
# UI COMPONENTS - MODULAR FUNCTIONS
# ============================================================================

def render_command_bar(title: str, subtitle: str):
    """Render Top Command Bar"""
    st.markdown(f"""
    <div class="command-bar">
        <div>
            <h1>🎯 {title}</h1>
            <div class="command-bar-subtitle">{subtitle}</div>
        </div>
        <div style="color: #605E5C; font-size: 0.85rem;">
            Last updated: {datetime.now().strftime("%H:%M:%S")}
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_kpi_cards(metadata: Dict, quality_metrics: Dict):
    """Render KPI Metrics Cards"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <span class="kpi-icon">📚</span>
            <div class="kpi-value">{metadata['total_tables']}</div>
            <div class="kpi-label">Total Tables</div>
            <div class="kpi-trend trend-positive">↑ Active</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <span class="kpi-icon">⚠️</span>
            <div class="kpi-value">{metadata['tables_without_desc']}</div>
            <div class="kpi-label">Missing Description</div>
            <div class="kpi-trend trend-negative">Requires Attention</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <span class="kpi-icon">📊</span>
            <div class="kpi-value">{quality_metrics['documentation_score']}%</div>
            <div class="kpi-label">Documentation Score</div>
            <div class="kpi-trend {'trend-positive' if quality_metrics['documentation_score'] > 70 else 'trend-negative'}">
                {'↑ Good' if quality_metrics['documentation_score'] > 70 else '↓ Needs Improvement'}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <span class="kpi-icon">🗂️</span>
            <div class="kpi-value">{len(metadata['catalogs'])}</div>
            <div class="kpi-label">Active Catalogs</div>
            <div class="kpi-trend trend-positive">↑ Monitored</div>
        </div>
        """, unsafe_allow_html=True)

def render_overview_tab(metadata: Dict):
    """Render Overview Tab Content"""
    df = metadata['tables']
    
    if df.empty:
        st.warning("No tables found in Unity Catalog. Please check your connection.")
        return
    
    # Tables by Catalog
    st.markdown('<div class="fluent-card"><h3>📁 Tables by Catalog</h3></div>', unsafe_allow_html=True)
    
    catalog_counts = df.groupby('catalog').size().reset_index(name='count')
    catalog_counts.columns = ['Catalog', 'Table Count']
    st.dataframe(catalog_counts, use_container_width=True, hide_index=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Recent Tables (Top 10)
    st.markdown('<div class="fluent-card"><h3>📊 All Tables</h3></div>', unsafe_allow_html=True)
    
    # Add badges for missing descriptions
    display_df = df[['catalog', 'schema', 'table_name', 'type', 'description']].copy()
    display_df.columns = ['Catalog', 'Schema', 'Table', 'Type', 'Description']
    
    # Add status column
    display_df['Status'] = display_df['Description'].apply(
        lambda x: '🟢 Documented' if pd.notna(x) and x != '' else '🟡 Missing Description'
    )
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)

def render_schema_explorer_tab(metadata: Dict):
    """Render Schema Explorer Tab"""
    st.markdown('<div class="fluent-card"><h3>🔍 Schema Explorer</h3></div>', unsafe_allow_html=True)
    
    if not metadata['catalogs']:
        st.warning("No catalogs available")
        return
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_catalog = st.selectbox(
            "📁 Select Catalog",
            options=metadata['catalogs'],
            key="catalog_select"
        )
    
    with col2:
        if selected_catalog:
            schemas = metadata['schemas'].get(selected_catalog, [])
            selected_schema = st.selectbox(
                "📂 Select Schema",
                options=schemas,
                key="schema_select"
            )
        else:
            selected_schema = None
            st.selectbox("📂 Select Schema", options=[], disabled=True)
    
    with col3:
        if selected_catalog and selected_schema:
            df = metadata['tables']
            tables = df[(df['catalog'] == selected_catalog) & (df['schema'] == selected_schema)]['table_name'].tolist()
            selected_table = st.selectbox(
                "📄 Select Table",
                options=tables,
                key="table_select"
            )
        else:
            selected_table = None
            st.selectbox("📄 Select Table", options=[], disabled=True)
    
    # Display table details
    if selected_catalog and selected_schema and selected_table:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Table info
        df = metadata['tables']
        table_info = df[(df['catalog'] == selected_catalog) & 
                       (df['schema'] == selected_schema) & 
                       (df['table_name'] == selected_table)].iloc[0]
        
        st.markdown(f"""
        <div class="fluent-card">
            <h3>📊 {selected_catalog}.{selected_schema}.{selected_table}</h3>
            <p>
                <span class="badge badge-info">{table_info['type']}</span>
                <span class="badge {'badge-success' if table_info['missing_description'] == 0 else 'badge-warning'}">
                    {'✓ Documented' if table_info['missing_description'] == 0 else '⚠ Missing Description'}
                </span>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Fetch and display columns
        with st.spinner("Loading columns..."):
            columns_df = get_table_columns(selected_catalog, selected_schema, selected_table)
            
            if not columns_df.empty:
                st.markdown('<div class="fluent-card"><h3>📋 Columns</h3></div>', unsafe_allow_html=True)
                
                # Format columns display
                display_cols = columns_df[['column_name', 'type', 'nullable', 'description']].copy()
                display_cols.columns = ['Column Name', 'Data Type', 'Nullable', 'Description']
                display_cols['Nullable'] = display_cols['Nullable'].apply(lambda x: '✅' if x == 'YES' else '❌')
                display_cols['Description'] = display_cols['Description'].fillna('-')
                
                st.dataframe(display_cols, use_container_width=True, hide_index=True)
            else:
                st.info("No column information available")

def render_data_quality_tab(metadata: Dict, quality_metrics: Dict):
    """Render Data Quality Tab"""
    st.markdown('<div class="fluent-card"><h3>🎯 Data Quality Overview</h3></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Documentation Score",
            f"{quality_metrics['documentation_score']}%",
            delta=None
        )
    
    with col2:
        st.metric(
            "Documented Tables",
            quality_metrics['documented_tables'],
            delta=None
        )
    
    with col3:
        st.metric(
            "Undocumented Tables",
            quality_metrics['undocumented_tables'],
            delta=None
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tables without description
    st.markdown('<div class="fluent-card"><h3>⚠️ Tables Requiring Documentation</h3></div>', unsafe_allow_html=True)
    
    df = metadata['tables']
    undocumented = df[df['missing_description'] == 1][['catalog', 'schema', 'table_name', 'type']].copy()
    
    if not undocumented.empty:
        undocumented.columns = ['Catalog', 'Schema', 'Table', 'Type']
        undocumented['Priority'] = '🔴 High'
        st.dataframe(undocumented, use_container_width=True, hide_index=True)
        
        st.warning(f"⚠️ {len(undocumented)} tables ({round(len(undocumented)/len(df)*100, 1)}%) require documentation to improve governance.")
    else:
        st.success("✅ All tables are properly documented!")

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main Application Entry Point"""
    
    # Sidebar Navigation
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-logo">
            <h2 style="color: white; margin: 0;">🎯</h2>
            <h3 style="color: white; margin: 0.5rem 0 0 0; font-size: 1.1rem;">Data Governance</h3>
            <p style="color: rgba(255,255,255,0.8); font-size: 0.8rem; margin: 0.25rem 0 0 0;">Enterprise Portal</p>
        </div>
        """, unsafe_allow_html=True)
        
        page = st.radio(
            "Navigation",
            ["🏠 Dashboard", "🔍 Data Discovery", "📊 Quality Insights"],
            label_visibility="collapsed"
        )
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="color: rgba(255,255,255,0.7); font-size: 0.75rem; text-align: center; padding: 1rem;">
            <p>Powered by Unity Catalog</p>
            <p>v1.0.0</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Load data with loading shimmer
    with st.spinner(""):
        metadata = get_catalog_metadata()
        quality_metrics = get_data_quality_metrics()
    
    # Dashboard Page
    if page == "🏠 Dashboard":
        render_command_bar(
            "Enterprise Data Governance Portal",
            "Comprehensive view of your Unity Catalog data assets"
        )
        
        render_kpi_cards(metadata, quality_metrics)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Tabs
        tab1, tab2, tab3 = st.tabs(["📊 Overview", "🔍 Schema Explorer", "🎯 Data Quality"])
        
        with tab1:
            render_overview_tab(metadata)
        
        with tab2:
            render_schema_explorer_tab(metadata)
        
        with tab3:
            render_data_quality_tab(metadata, quality_metrics)
    
    # Data Discovery Page
    elif page == "🔍 Data Discovery":
        render_command_bar(
            "Data Discovery",
            "Explore and discover data assets across Unity Catalog"
        )
        
        render_schema_explorer_tab(metadata)
    
    # Quality Insights Page
    elif page == "📊 Quality Insights":
        render_command_bar(
            "Quality Insights",
            "Monitor and improve data quality and governance"
        )
        
        render_kpi_cards(metadata, quality_metrics)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        render_data_quality_tab(metadata, quality_metrics)

if __name__ == "__main__":
    main()
