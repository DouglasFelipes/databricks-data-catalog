// API Base URL
const API_BASE = window.location.origin;

// State Management
const state = {
    currentPage: 'home',
    kpis: null,
    catalogs: [],
    selectedCatalog: null,
    selectedSchema: null,
    selectedTable: null
};

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
    setupNavigation();
    loadPage('home');
    fetchKPIs();
});

// Navigation Setup
function setupNavigation() {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const page = e.target.dataset.page;
            
            // Update active state
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            e.target.classList.add('active');
            
            // Load page
            loadPage(page);
        });
    });
}

// Load Page Content
function loadPage(page) {
    state.currentPage = page;
    const content = document.getElementById('content');
    
    switch(page) {
        case 'home':
            renderHomePage(content);
            break;
        case 'explorer':
            renderExplorerPage(content);
            break;
        case 'search':
            renderSearchPage(content);
            break;
        case 'governance':
            renderGovernancePage(content);
            break;
    }
}

// Fetch KPIs from API
async function fetchKPIs() {
    try {
        const response = await fetch(`${API_BASE}/api/kpis`);
        state.kpis = await response.json();
        if (state.currentPage === 'home') {
            renderHomePage(document.getElementById('content'));
        }
    } catch (error) {
        console.error('Error fetching KPIs:', error);
    }
}

// Render Home Page
function renderHomePage(container) {
    const kpis = state.kpis || {
        totalTables: '...',
        tablesWithoutDescription: '...',
        dataVolume: '...',
        piiColumns: '...'
    };
    
    container.innerHTML = `
        <div class="hero">
            <div class="hero-content">
                <h1>📊 Data Catalog</h1>
                <p>Explore, descubra e governe seus dados no Unity Catalog</p>
            </div>
        </div>
        
        <div class="kpi-grid">
            <div class="kpi-card">
                <span class="kpi-icon">📚</span>
                <div class="kpi-value">${kpis.totalTables}</div>
                <div class="kpi-label">Total de Tabelas</div>
                <div class="kpi-trend trend-up">↑ 12% este mês</div>
            </div>
            
            <div class="kpi-card">
                <span class="kpi-icon">⚠️</span>
                <div class="kpi-value">${kpis.tablesWithoutDescription}</div>
                <div class="kpi-label">Sem Descrição</div>
                <div class="kpi-trend trend-down">Requer atenção</div>
            </div>
            
            <div class="kpi-card">
                <span class="kpi-icon">💾</span>
                <div class="kpi-value">${kpis.dataVolume}</div>
                <div class="kpi-label">Volume de Dados</div>
                <div class="kpi-trend trend-up">↑ 2.3 TB este mês</div>
            </div>
            
            <div class="kpi-card">
                <span class="kpi-icon">🔒</span>
                <div class="kpi-value">${kpis.piiColumns}</div>
                <div class="kpi-label">Colunas PII</div>
                <div class="kpi-trend">Monitoradas</div>
            </div>
        </div>
        
        <div class="content-grid">
            <div class="content-card">
                <h2>📈 Tabelas Mais Acessadas</h2>
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Tabela</th>
                            <th>Acessos</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>customer_360</td>
                            <td>1,250</td>
                            <td><span class="badge badge-success">Ativo</span></td>
                        </tr>
                        <tr>
                            <td>sales_metrics</td>
                            <td>980</td>
                            <td><span class="badge badge-success">Ativo</span></td>
                        </tr>
                        <tr>
                            <td>product_catalog</td>
                            <td>756</td>
                            <td><span class="badge badge-success">Ativo</span></td>
                        </tr>
                        <tr>
                            <td>user_events</td>
                            <td>654</td>
                            <td><span class="badge badge-warning">Alerta</span></td>
                        </tr>
                        <tr>
                            <td>transactions</td>
                            <td>543</td>
                            <td><span class="badge badge-success">Ativo</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>
            
            <div class="content-card">
                <h2>🎯 Qualidade dos Dados</h2>
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Métrica</th>
                            <th>Score</th>
                            <th>Tendência</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Documentação</td>
                            <td>64%</td>
                            <td>↓</td>
                        </tr>
                        <tr>
                            <td>Freshness</td>
                            <td>92%</td>
                            <td>↑</td>
                        </tr>
                        <tr>
                            <td>Completude</td>
                            <td>88%</td>
                            <td>↑</td>
                        </tr>
                        <tr>
                            <td>Consistência</td>
                            <td>95%</td>
                            <td>→</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    `;
}

// Render Explorer Page
async function renderExplorerPage(container) {
    container.innerHTML = `
        <div class="hero">
            <div class="hero-content">
                <h1>🔍 Explorer</h1>
                <p>Navegue pela hierarquia Catalog → Schema → Table</p>
            </div>
        </div>
        
        <div class="select-group">
            <div class="select-wrapper">
                <label>📁 Catalog</label>
                <select id="catalog-select">
                    <option value="">Carregando...</option>
                </select>
            </div>
            <div class="select-wrapper">
                <label>📂 Schema</label>
                <select id="schema-select" disabled>
                    <option value="">Selecione um catalog</option>
                </select>
            </div>
            <div class="select-wrapper">
                <label>📄 Table</label>
                <select id="table-select" disabled>
                    <option value="">Selecione um schema</option>
                </select>
            </div>
        </div>
        
        <div id="table-details"></div>
    `;
    
    // Load catalogs
    await loadCatalogs();
    
    // Setup event listeners
    document.getElementById('catalog-select').addEventListener('change', handleCatalogChange);
    document.getElementById('schema-select').addEventListener('change', handleSchemaChange);
    document.getElementById('table-select').addEventListener('change', handleTableChange);
}

// Load Catalogs
async function loadCatalogs() {
    try {
        const response = await fetch(`${API_BASE}/api/catalogs`);
        state.catalogs = await response.json();
        
        const select = document.getElementById('catalog-select');
        select.innerHTML = '<option value="">Selecione...</option>' +
            state.catalogs.map(c => `<option value="${c}">${c}</option>`).join('');
    } catch (error) {
        console.error('Error loading catalogs:', error);
    }
}

// Handle Catalog Change
async function handleCatalogChange(e) {
    const catalog = e.target.value;
    state.selectedCatalog = catalog;
    
    const schemaSelect = document.getElementById('schema-select');
    const tableSelect = document.getElementById('table-select');
    
    if (!catalog) {
        schemaSelect.disabled = true;
        tableSelect.disabled = true;
        return;
    }
    
    schemaSelect.disabled = false;
    schemaSelect.innerHTML = '<option value="">Carregando...</option>';
    
    try {
        const response = await fetch(`${API_BASE}/api/schemas/${catalog}`);
        const schemas = await response.json();
        
        schemaSelect.innerHTML = '<option value="">Selecione...</option>' +
            schemas.map(s => `<option value="${s}">${s}</option>`).join('');
    } catch (error) {
        console.error('Error loading schemas:', error);
        schemaSelect.innerHTML = '<option value="">Erro ao carregar</option>';
    }
}

// Handle Schema Change
async function handleSchemaChange(e) {
    const schema = e.target.value;
    state.selectedSchema = schema;
    
    const tableSelect = document.getElementById('table-select');
    
    if (!schema) {
        tableSelect.disabled = true;
        return;
    }
    
    tableSelect.disabled = false;
    tableSelect.innerHTML = '<option value="">Carregando...</option>';
    
    try {
        const response = await fetch(`${API_BASE}/api/tables/${state.selectedCatalog}/${schema}`);
        const tables = await response.json();
        
        tableSelect.innerHTML = '<option value="">Selecione...</option>' +
            tables.map(t => `<option value="${t.table_name}">${t.table_name}</option>`).join('');
    } catch (error) {
        console.error('Error loading tables:', error);
        tableSelect.innerHTML = '<option value="">Erro ao carregar</option>';
    }
}

// Handle Table Change
async function handleTableChange(e) {
    const table = e.target.value;
    state.selectedTable = table;
    
    if (!table) return;
    
    const detailsContainer = document.getElementById('table-details');
    detailsContainer.innerHTML = '<div class="loading"><div class="spinner"></div><p>Carregando detalhes...</p></div>';
    
    try {
        const response = await fetch(`${API_BASE}/api/table/${state.selectedCatalog}/${state.selectedSchema}/${table}`);
        const data = await response.json();
        
        renderTableDetails(detailsContainer, data);
    } catch (error) {
        console.error('Error loading table details:', error);
        detailsContainer.innerHTML = '<div class="content-card"><p>Erro ao carregar detalhes da tabela.</p></div>';
    }
}

// Render Table Details
function renderTableDetails(container, data) {
    container.innerHTML = `
        <div class="content-card">
            <h2>📊 ${state.selectedCatalog}.${state.selectedSchema}.${state.selectedTable}</h2>
            <p>
                <span class="badge badge-success">Ativo</span>
                <span class="badge badge-info">Produção</span>
            </p>
            
            <div class="tabs">
                <button class="tab active" data-tab="columns">📋 Colunas</button>
                <button class="tab" data-tab="stats">📊 Estatísticas</button>
                <button class="tab" data-tab="metadata">📝 Metadados</button>
            </div>
            
            <div class="tab-content active" id="tab-columns">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Coluna</th>
                            <th>Tipo</th>
                            <th>Nullable</th>
                            <th>Descrição</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${data.columns.map(col => `
                            <tr>
                                <td>${col.column_name || col.name}</td>
                                <td>${col.data_type || col.type}</td>
                                <td>${col.is_nullable === 'YES' ? '✅' : '❌'}</td>
                                <td>${col.comment || col.comment || '-'}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
            
            <div class="tab-content" id="tab-stats">
                <p>Estatísticas da tabela em desenvolvimento...</p>
            </div>
            
            <div class="tab-content" id="tab-metadata">
                <p><strong>Owner:</strong> Data Engineering Team</p>
                <p><strong>Criado em:</strong> 15/01/2024</p>
                <p><strong>Última modificação:</strong> Hoje</p>
            </div>
        </div>
    `;
    
    // Setup tab switching
    container.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', (e) => {
            const tabName = e.target.dataset.tab;
            
            container.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            container.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            
            e.target.classList.add('active');
            container.querySelector(`#tab-${tabName}`).classList.add('active');
        });
    });
}

// Render Search Page
function renderSearchPage(container) {
    container.innerHTML = `
        <div class="hero">
            <div class="hero-content">
                <h1>🔎 Search</h1>
                <p>Busca global em tabelas, colunas e descrições</p>
            </div>
        </div>
        
        <div class="search-container">
            <div class="search-box">
                <input 
                    type="text" 
                    class="search-input" 
                    id="search-input"
                    placeholder="Digite para buscar tabelas, colunas, descrições..."
                >
                <span class="search-icon">🔍</span>
            </div>
        </div>
        
        <div id="search-results"></div>
    `;
    
    const searchInput = document.getElementById('search-input');
    let searchTimeout;
    
    searchInput.addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            performSearch(e.target.value);
        }, 500);
    });
}

// Perform Search
async function performSearch(query) {
    const resultsContainer = document.getElementById('search-results');
    
    if (!query) {
        resultsContainer.innerHTML = `
            <div class="content-card">
                <h2>💡 Dicas de Busca</h2>
                <ul style="color: var(--text-secondary); line-height: 2;">
                    <li>Use palavras-chave para encontrar tabelas e colunas</li>
                    <li>Busque por nomes de schemas ou catalogs</li>
                    <li>Procure por descrições e metadados</li>
                    <li>Filtre por tags e owners</li>
                </ul>
            </div>
        `;
        return;
    }
    
    resultsContainer.innerHTML = '<div class="loading"><div class="spinner"></div><p>Buscando...</p></div>';
    
    try {
        const response = await fetch(`${API_BASE}/api/search?q=${encodeURIComponent(query)}`);
        const results = await response.json();
        
        if (results.length === 0) {
            resultsContainer.innerHTML = `
                <div class="content-card">
                    <h2>Nenhum resultado encontrado</h2>
                    <p>Tente usar palavras-chave diferentes.</p>
                </div>
            `;
            return;
        }
        
        resultsContainer.innerHTML = `
            <div class="content-card">
                <h2>🎯 Resultados para "${query}"</h2>
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Tipo</th>
                            <th>Nome</th>
                            <th>Localização</th>
                            <th>Descrição</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${results.map(r => `
                            <tr>
                                <td>📄 Tabela</td>
                                <td>${r.table_name}</td>
                                <td>${r.table_catalog}.${r.table_schema}</td>
                                <td>${r.comment || '-'}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
    } catch (error) {
        console.error('Error searching:', error);
        resultsContainer.innerHTML = `
            <div class="content-card">
                <h2>Erro na busca</h2>
                <p>Não foi possível realizar a busca. Tente novamente.</p>
            </div>
        `;
    }
}

// Render Governance Page
function renderGovernancePage(container) {
    container.innerHTML = `
        <div class="hero">
            <div class="hero-content">
                <h1>🛡️ Governance</h1>
                <p>Monitoramento de PII e qualidade da documentação</p>
            </div>
        </div>
        
        <div class="tabs">
            <button class="tab active" data-tab="pii">🔒 Colunas Sensíveis (PII)</button>
            <button class="tab" data-tab="docs">📝 Documentação Faltante</button>
        </div>
        
        <div class="tab-content active" id="tab-pii">
            <div class="content-card">
                <h2>🔒 Colunas com Dados Sensíveis Identificadas</h2>
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Tabela</th>
                            <th>Coluna</th>
                            <th>Tipo PII</th>
                            <th>Risco</th>
                            <th>Ação</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>customers</td>
                            <td>email</td>
                            <td>Email</td>
                            <td><span class="badge badge-warning">Médio</span></td>
                            <td>Mascarar</td>
                        </tr>
                        <tr>
                            <td>users</td>
                            <td>phone</td>
                            <td>Telefone</td>
                            <td><span class="badge badge-warning">Médio</span></td>
                            <td>Mascarar</td>
                        </tr>
                        <tr>
                            <td>orders</td>
                            <td>credit_card</td>
                            <td>Cartão</td>
                            <td><span class="badge badge-danger">Alto</span></td>
                            <td>Criptografar</td>
                        </tr>
                        <tr>
                            <td>employees</td>
                            <td>ssn</td>
                            <td>SSN</td>
                            <td><span class="badge badge-danger">Alto</span></td>
                            <td>Criptografar</td>
                        </tr>
                        <tr>
                            <td>contacts</td>
                            <td>address</td>
                            <td>Endereço</td>
                            <td><span class="badge badge-warning">Médio</span></td>
                            <td>Mascarar</td>
                        </tr>
                    </tbody>
                </table>
                <p style="margin-top: 16px;">
                    <span class="badge badge-danger">Alto Risco: 45 colunas</span>
                    <span class="badge badge-warning">Médio Risco: 89 colunas</span>
                    <span class="badge badge-success">Baixo Risco: 22 colunas</span>
                </p>
            </div>
        </div>
        
        <div class="tab-content" id="tab-docs">
            <div class="content-card">
                <h2>📝 Tabelas e Colunas sem Documentação</h2>
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Tabela</th>
                            <th>Schema</th>
                            <th>Colunas sem Desc.</th>
                            <th>Última Atualização</th>
                            <th>Prioridade</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>raw_events</td>
                            <td>bronze</td>
                            <td>12</td>
                            <td>3 dias</td>
                            <td><span class="badge badge-danger">Alta</span></td>
                        </tr>
                        <tr>
                            <td>temp_data</td>
                            <td>bronze</td>
                            <td>8</td>
                            <td>1 semana</td>
                            <td><span class="badge badge-warning">Média</span></td>
                        </tr>
                        <tr>
                            <td>staging_users</td>
                            <td>silver</td>
                            <td>15</td>
                            <td>2 dias</td>
                            <td><span class="badge badge-danger">Alta</span></td>
                        </tr>
                        <tr>
                            <td>legacy_orders</td>
                            <td>gold</td>
                            <td>6</td>
                            <td>1 mês</td>
                            <td><span class="badge badge-warning">Média</span></td>
                        </tr>
                        <tr>
                            <td>test_table</td>
                            <td>dev</td>
                            <td>20</td>
                            <td>6 meses</td>
                            <td><span class="badge badge-success">Baixa</span></td>
                        </tr>
                    </tbody>
                </table>
                <p style="margin-top: 16px; color: var(--text-secondary);">
                    ⚠️ 89 tabelas (36%) estão sem descrição adequada. Recomenda-se documentar para melhorar a governança.
                </p>
            </div>
        </div>
    `;
    
    // Setup tab switching
    container.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', (e) => {
            const tabName = e.target.dataset.tab;
            
            container.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            container.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            
            e.target.classList.add('active');
            container.querySelector(`#tab-${tabName}`).classList.add('active');
        });
    });
}
