import React from 'react'
import './Header.css'

function Header({ connected }) {
  return (
    <header className="header">
      <div className="header-content">
        <div className="logo-section">
          <div className="logo">RADIX</div>
          <div className="subtitle">Radar Data Integration & eXtraction Framework</div>
        </div>
        
        <div className="header-right">
          <div className={`connection-status ${connected ? 'connected' : 'disconnected'}`}>
            <span className="status-dot"></span>
            <span>{connected ? 'Connected' : 'Disconnected'}</span>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
