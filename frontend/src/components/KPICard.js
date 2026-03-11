import React from 'react';

function KPICard({ icon, value, label, trend }) {
  return (
    <div className="kpi-card">
      <span className="kpi-icon">{icon}</span>
      <div className="kpi-value">{value}</div>
      <div className="kpi-label">{label}</div>
      {trend && <div className="kpi-trend">{trend}</div>}
    </div>
  );
}

export default KPICard;
