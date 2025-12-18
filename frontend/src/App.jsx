import React, { useState, useEffect, useCallback } from 'react'
import Header from './components/Header'
import StatusBar from './components/StatusBar'
import RadarDisplay from './components/RadarDisplay'
import DetectionTable from './components/DetectionTable'
import TrackList from './components/TrackList'
import DataRateChart from './components/DataRateChart'
import './App.css'

function App() {
  const [systemStatus, setSystemStatus] = useState(null)
  const [detections, setDetections] = useState([])
  const [tracks, setTracks] = useState([])
  const [radars, setRadars] = useState([])
  const [dataRateHistory, setDataRateHistory] = useState([])
  const [connected, setConnected] = useState(false)

  // WebSocket connection
  useEffect(() => {
    const ws = new WebSocket(`ws://${window.location.hostname}:8000/ws`)
    
    ws.onopen = () => {
      console.log('WebSocket connected')
      setConnected(true)
    }
    
    ws.onmessage = (event) => {
      const message = JSON.parse(event.data)
      
      if (message.type === 'update') {
        setDetections(message.detections || [])
        setTracks(message.tracks || [])
        setSystemStatus(message.system_status)
        
        // Update data rate history
        if (message.system_status) {
          setDataRateHistory(prev => {
            const newHistory = [...prev, {
              time: new Date(message.timestamp),
              rate: message.system_status.data_rate_hz,
              tracks: message.system_status.active_tracks
            }]
            // Keep last 100 points
            return newHistory.slice(-100)
          })
        }
      }
    }
    
    ws.onerror = (error) => {
      console.error('WebSocket error:', error)
      setConnected(false)
    }
    
    ws.onclose = () => {
      console.log('WebSocket disconnected')
      setConnected(false)
    }
    
    // Heartbeat
    const heartbeat = setInterval(() => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.send('ping')
      }
    }, 5000)
    
    return () => {
      clearInterval(heartbeat)
      ws.close()
    }
  }, [])

  // Fetch radars
  useEffect(() => {
    fetch('/api/radars')
      .then(res => res.json())
      .then(data => setRadars(data))
      .catch(err => console.error('Error fetching radars:', err))
  }, [])

  return (
    <div className="app">
      <Header connected={connected} />
      <StatusBar status={systemStatus} />
      
      <div className="main-content">
        <div className="left-panel">
          <RadarDisplay 
            detections={detections} 
            tracks={tracks} 
            radars={radars}
          />
          <DataRateChart data={dataRateHistory} />
        </div>
        
        <div className="right-panel">
          <TrackList tracks={tracks} />
          <DetectionTable detections={detections} />
        </div>
      </div>
    </div>
  )
}

export default App
