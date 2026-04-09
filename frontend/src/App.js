import React from 'react';
import './App.css';
import Dashboard from './components/Dashboard';

function App() {
  return (
    <div className="app-container">
      <header className="app-header">
        <h1>🌐 IoT Monitoring Dashboard</h1>
        <div className="header-status">
          <span className="status-dot"></span>
          <span>System Online</span>
        </div>
      </header>
      <Dashboard />
    </div>
  );
}

export default App;
