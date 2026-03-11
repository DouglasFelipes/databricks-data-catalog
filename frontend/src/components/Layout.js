import React from 'react';

function Layout({ children, currentPage, setCurrentPage }) {
  return (
    <div className="app">
      <nav className="sidebar">
        <div className="sidebar-header">
          <h2>🎯 Data Governance</h2>
        </div>
        <ul className="nav-menu">
          <li className={currentPage === 'dashboard' ? 'active' : ''} onClick={() => setCurrentPage('dashboard')}>
            🏠 Dashboard
          </li>
          <li className={currentPage === 'explorer' ? 'active' : ''} onClick={() => setCurrentPage('explorer')}>
            🔍 Explorer
          </li>
          <li className={currentPage === 'quality' ? 'active' : ''} onClick={() => setCurrentPage('quality')}>
            📊 Quality
          </li>
        </ul>
      </nav>
      <main className="main-content">
        {children}
      </main>
    </div>
  );
}

export default Layout;
