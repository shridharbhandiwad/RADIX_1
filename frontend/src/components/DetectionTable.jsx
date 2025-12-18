import React from 'react'
import './DetectionTable.css'

function DetectionTable({ detections }) {
  return (
    <div className="card detection-table">
      <div className="card-header">
        <div className="card-title">
          <span>🔍</span>
          Recent Detections
        </div>
        <div className="card-badge">{detections.length}</div>
      </div>
      
      <div className="table-container">
        {detections.length === 0 ? (
          <div className="no-data">No recent detections</div>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Sensor</th>
                <th>Target</th>
                <th>Range (m)</th>
                <th>Az (°)</th>
                <th>Doppler (m/s)</th>
                <th>SNR (dB)</th>
              </tr>
            </thead>
            <tbody>
              {detections.slice(0, 20).map((det, idx) => (
                <tr key={idx} className="slide-in">
                  <td>
                    <span className="sensor-badge">{det.sensor_id}</span>
                  </td>
                  <td>{det.target_id || '-'}</td>
                  <td>{det.range_m.toFixed(0)}</td>
                  <td>{det.azimuth_deg.toFixed(1)}</td>
                  <td>{det.doppler_mps.toFixed(1)}</td>
                  <td>
                    <span className={`snr-value ${det.snr_db > 15 ? 'high' : det.snr_db > 8 ? 'medium' : 'low'}`}>
                      {det.snr_db.toFixed(1)}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default DetectionTable
