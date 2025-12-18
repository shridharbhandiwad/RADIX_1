import React, { useMemo } from 'react'
import Plot from 'react-plotly.js'
import './RadarDisplay.css'

function RadarDisplay({ detections, tracks, radars }) {
  const plotData = useMemo(() => {
    const traces = []
    
    // Radar positions
    if (radars && radars.length > 0) {
      traces.push({
        x: radars.map(r => r.location[0]),
        y: radars.map(r => r.location[1]),
        z: radars.map(r => r.location[2]),
        mode: 'markers+text',
        type: 'scatter3d',
        name: 'Radars',
        text: radars.map(r => r.id),
        textposition: 'top center',
        marker: {
          size: 12,
          color: '#00d4ff',
          symbol: 'diamond',
          line: {
            color: '#ffffff',
            width: 2
          }
        }
      })
    }
    
    // Detections by radar
    const detectionsByRadar = {}
    detections.forEach(det => {
      if (det.position_enu) {
        if (!detectionsByRadar[det.sensor_id]) {
          detectionsByRadar[det.sensor_id] = []
        }
        detectionsByRadar[det.sensor_id].push(det)
      }
    })
    
    const colors = {
      'RADAR_A': '#ff6b6b',
      'RADAR_B': '#4ecdc4',
      'RADAR_C': '#95e1d3'
    }
    
    Object.entries(detectionsByRadar).forEach(([sensorId, dets]) => {
      traces.push({
        x: dets.map(d => d.position_enu[0]),
        y: dets.map(d => d.position_enu[1]),
        z: dets.map(d => d.position_enu[2]),
        mode: 'markers',
        type: 'scatter3d',
        name: sensorId,
        marker: {
          size: 4,
          color: colors[sensorId] || '#ffffff',
          opacity: 0.6
        },
        hovertemplate: 
          '<b>%{text}</b><br>' +
          'Range: %{customdata[0]:.1f} m<br>' +
          'SNR: %{customdata[1]:.1f} dB<br>' +
          '<extra></extra>',
        text: dets.map(d => `Target ${d.target_id || '?'}`),
        customdata: dets.map(d => [d.range_m, d.snr_db])
      })
    })
    
    // Tracks
    if (tracks && tracks.length > 0) {
      tracks.forEach(track => {
        if (track.position) {
          // Track position
          traces.push({
            x: [track.position[0]],
            y: [track.position[1]],
            z: [track.position[2]],
            mode: 'markers+text',
            type: 'scatter3d',
            name: `Track ${track.track_id}`,
            text: [`T${track.track_id}`],
            textposition: 'top center',
            marker: {
              size: 8,
              color: '#00ff88',
              symbol: 'circle',
              line: {
                color: '#ffffff',
                width: 1
              }
            },
            showlegend: false
          })
          
          // Velocity vector
          const scale = 50
          traces.push({
            x: [track.position[0], track.position[0] + track.velocity[0] * scale],
            y: [track.position[1], track.position[1] + track.velocity[1] * scale],
            z: [track.position[2], track.position[2] + track.velocity[2] * scale],
            mode: 'lines',
            type: 'scatter3d',
            line: {
              color: '#00ff88',
              width: 3
            },
            showlegend: false
          })
        }
      })
    }
    
    return traces
  }, [detections, tracks, radars])

  const layout = {
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    font: {
      color: '#e0e0e0'
    },
    scene: {
      xaxis: {
        title: 'East (m)',
        gridcolor: '#3b4575',
        zerolinecolor: '#3b4575',
        color: '#8899aa'
      },
      yaxis: {
        title: 'North (m)',
        gridcolor: '#3b4575',
        zerolinecolor: '#3b4575',
        color: '#8899aa'
      },
      zaxis: {
        title: 'Up (m)',
        gridcolor: '#3b4575',
        zerolinecolor: '#3b4575',
        color: '#8899aa'
      },
      bgcolor: 'rgba(10, 14, 39, 0.5)',
      camera: {
        eye: { x: 1.5, y: 1.5, z: 1.2 }
      }
    },
    margin: { l: 0, r: 0, t: 0, b: 0 },
    legend: {
      bgcolor: 'rgba(26, 31, 58, 0.8)',
      bordercolor: '#3b4575',
      borderwidth: 1
    },
    hovermode: 'closest'
  }

  return (
    <div className="card radar-display">
      <div className="card-header">
        <div className="card-title">
          <span>🎯</span>
          3D Radar View
        </div>
        <div className="card-badge">
          {detections.length} Detections | {tracks.length} Tracks
        </div>
      </div>
      
      <div className="radar-plot">
        <Plot
          data={plotData}
          layout={layout}
          config={{
            displayModeBar: true,
            displaylogo: false,
            modeBarButtonsToRemove: ['toImage']
          }}
          style={{ width: '100%', height: '500px' }}
        />
      </div>
    </div>
  )
}

export default RadarDisplay
