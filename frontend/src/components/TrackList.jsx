import React from 'react'
import './TrackList.css'

function TrackList({ tracks }) {
  const getStateColor = (state) => {
    switch (state) {
      case 'CONFIRMED': return 'status-confirmed'
      case 'TENTATIVE': return 'status-tentative'
      case 'COASTING': return 'status-coasting'
      default: return ''
    }
  }

  const calculateSpeed = (velocity) => {
    if (!velocity || velocity.length < 3) return 0
    return Math.sqrt(velocity[0]**2 + velocity[1]**2 + velocity[2]**2)
  }

  return (
    <div className="card track-list">
      <div className="card-header">
        <div className="card-title">
          <span>📍</span>
          Active Tracks
        </div>
        <div className="card-badge">{tracks.length}</div>
      </div>
      
      <div className="table-container">
        {tracks.length === 0 ? (
          <div className="no-data">No active tracks</div>
        ) : (
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Status</th>
                <th>Sensor</th>
                <th>Speed (m/s)</th>
                <th>Detections</th>
              </tr>
            </thead>
            <tbody>
              {tracks.map(track => (
                <tr key={track.track_id} className="slide-in">
                  <td>
                    <strong>{track.track_id}</strong>
                  </td>
                  <td>
                    <span className={`status-indicator ${getStateColor(track.track_state)}`}></span>
                    {track.track_state}
                  </td>
                  <td>{track.sensor_id}</td>
                  <td>{calculateSpeed(track.velocity).toFixed(1)}</td>
                  <td>{track.num_detections}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default TrackList
