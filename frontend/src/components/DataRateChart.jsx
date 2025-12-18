import React from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import './DataRateChart.css'

function DataRateChart({ data }) {
  const chartData = data.map((item, index) => ({
    index,
    rate: item.rate,
    tracks: item.tracks
  }))

  return (
    <div className="card data-rate-chart">
      <div className="card-header">
        <div className="card-title">
          <span>📊</span>
          Performance Metrics
        </div>
      </div>
      
      <ResponsiveContainer width="100%" height={250}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#3b4575" />
          <XAxis 
            dataKey="index" 
            stroke="#8899aa"
            tick={{ fill: '#8899aa' }}
            label={{ value: 'Time', position: 'insideBottom', offset: -5, fill: '#8899aa' }}
          />
          <YAxis 
            yAxisId="left"
            stroke="#00d4ff"
            tick={{ fill: '#8899aa' }}
            label={{ value: 'Data Rate (Hz)', angle: -90, position: 'insideLeft', fill: '#8899aa' }}
          />
          <YAxis 
            yAxisId="right"
            orientation="right"
            stroke="#00ff88"
            tick={{ fill: '#8899aa' }}
            label={{ value: 'Active Tracks', angle: 90, position: 'insideRight', fill: '#8899aa' }}
          />
          <Tooltip 
            contentStyle={{ 
              background: 'rgba(26, 31, 58, 0.95)', 
              border: '1px solid #3b4575',
              borderRadius: '8px',
              color: '#e0e0e0'
            }}
          />
          <Legend />
          <Line 
            yAxisId="left"
            type="monotone" 
            dataKey="rate" 
            stroke="#00d4ff" 
            strokeWidth={2}
            dot={false}
            name="Data Rate (Hz)"
          />
          <Line 
            yAxisId="right"
            type="monotone" 
            dataKey="tracks" 
            stroke="#00ff88" 
            strokeWidth={2}
            dot={false}
            name="Active Tracks"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

export default DataRateChart
