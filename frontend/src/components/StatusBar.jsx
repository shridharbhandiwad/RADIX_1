import React from 'react'
import './StatusBar.css'

function StatusBar({ status }) {
  if (!status) return null

  const formatUptime = (seconds) => {
    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    const secs = Math.floor(seconds % 60)
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }

  return (
    <div className="status-bar">
      <div className="status-item">
        <div className="status-label">Uptime</div>
        <div className="status-value">{formatUptime(status.uptime_seconds)}</div>
      </div>
      
      <div className="status-item">
        <div className="status-label">Active Radars</div>
        <div className="status-value highlight">{status.active_radars}</div>
      </div>
      
      <div className="status-item">
        <div className="status-label">Total Detections</div>
        <div className="status-value">{status.total_detections.toLocaleString()}</div>
      </div>
      
      <div className="status-item">
        <div className="status-label">Active Tracks</div>
        <div className="status-value highlight">{status.active_tracks}</div>
      </div>
      
      <div className="status-item">
        <div className="status-label">Data Rate</div>
        <div className="status-value">{status.data_rate_hz.toFixed(1)} Hz</div>
      </div>
    </div>
  )
}

export default StatusBar
