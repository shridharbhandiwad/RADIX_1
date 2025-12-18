# RADIX Feature Showcase

## Visual Interface Overview

When you launch RADIX, you'll see a professional, military-grade radar monitoring interface with the following components:

### 1. Header Bar (Top)
```
┌─────────────────────────────────────────────────────────────────────┐
│ RADIX                                         [●] Connected         │
│ Radar Data Integration & eXtraction Framework                       │
└─────────────────────────────────────────────────────────────────────┘
```
- **Logo**: Gradient blue-green RADIX branding
- **Connection Status**: Live WebSocket connection indicator
- **Dark Theme**: Optimized for 24/7 monitoring

### 2. Status Dashboard (Below Header)
```
┌─────────────────────────────────────────────────────────────────────┐
│  Uptime      Active Radars   Total Detections   Active Tracks  Rate │
│  00:05:23         3              15,234             8         125 Hz│
└─────────────────────────────────────────────────────────────────────┘
```
- **Real-Time Metrics**: Updated 10 times per second
- **Color Coded**: Critical metrics highlighted in cyan
- **Monospace Font**: Easy to read numbers

### 3. Main Content Area

#### Left Panel - Visualization

**3D Radar Display**
```
┌─────────────────────────────────────────────────────────────────────┐
│ 🎯 3D Radar View                          50 Detections | 8 Tracks  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│                    ╱│╲                                                │
│                   ╱ │ ╲        ●●●  ← Detections (color by radar)    │
│                  ╱  │  ╲                                              │
│                 ╱   │   ╲      ⭘ → Track with velocity vector        │
│          North ╱    │    ╲                                            │
│               ╱     │     ╲    ◆ RADAR_A (red)                        │
│         ●●  ╱      ↑│      ╲   ◆ RADAR_B (teal)                       │
│            ╱       Up       ╲  ◆ RADAR_C (green)                      │
│           ╱                  ╲                                        │
│      ────┼────────────────────┼──── East                              │
│          ╲                    ╱                                        │
│           ╲       ⭘●         ╱                                         │
│            ╲                ╱                                          │
│             ╲●●            ╱                                           │
│              ╲            ╱                                            │
│               ╲          ╱                                             │
│                ╲        ╱                                              │
│                 ╲      ╱                                               │
│                  ╲    ╱                                                │
│                   ╲  ╱                                                 │
│                    ╲╱                                                  │
│                                                                        │
│  [Interactive: Click+Drag to Rotate, Scroll to Zoom]                 │
└────────────────────────────────────────────────────────────────────────┘
```

**Features:**
- **3D Scatter Plot**: Plotly.js powered interactive visualization
- **Radar Positions**: Diamond markers showing radar locations
- **Detections**: Color-coded dots by radar type
  - 🔴 Red: FMCW (RADAR_A)
  - 🟢 Teal: Pulse-Doppler (RADAR_B)  
  - 🟣 Green: AESA (RADAR_C)
- **Tracks**: Large circles with velocity vectors
- **Hover Info**: Mouse over any point for details
- **Controls**: Rotate, zoom, pan with mouse

**Performance Metrics Chart**
```
┌─────────────────────────────────────────────────────────────────────┐
│ 📊 Performance Metrics                                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Data Rate (Hz)                                    Active Tracks     │
│  200 ┤                                                          ┤ 10 │
│      ┤     ╱╲    ╱╲                                             ┤    │
│  150 ┤    ╱  ╲  ╱  ╲      ← Blue: Data Rate                     ┤ 8  │
│      ┤   ╱    ╲╱    ╲                                            ┤    │
│  100 ┤  ╱            ╲                                           ┤ 6  │
│      ┤ ╱              ╲___                                       ┤    │
│   50 ┤╱                   ╲___                                   ┤ 4  │
│      ┤                        ╲___   ← Green: Track Count       ┤    │
│    0 ┼─────────────────────────────────────────────────────────┼ 0  │
│      0        20        40        60        80       100              │
│                          Time (seconds)                               │
└────────────────────────────────────────────────────────────────────────┘
```

#### Right Panel - Data Tables

**Active Tracks**
```
┌─────────────────────────────────────────────────────────────────────┐
│ 📍 Active Tracks                                                  8  │
├────┬──────────┬─────────┬───────────┬─────────────────────────────────┤
│ ID │ Status   │ Sensor  │ Speed(m/s)│ Detections                      │
├────┼──────────┼─────────┼───────────┼─────────────────────────────────┤
│  1 │ ● CONFIRMED│RADAR_A │    45.2   │    25                          │
│  2 │ ● CONFIRMED│RADAR_B │    78.3   │    18                          │
│  3 │ ◐ TENTATIVE│RADAR_A │    12.5   │     2                          │
│  4 │ ● CONFIRMED│RADAR_C │   125.8   │    42                          │
│  5 │ ● CONFIRMED│RADAR_B │    95.1   │    31                          │
│  6 │ ◑ COASTING │RADAR_A │    55.7   │    15                          │
│  7 │ ● CONFIRMED│RADAR_C │   142.3   │    38                          │
│  8 │ ● CONFIRMED│RADAR_B │    88.9   │    22                          │
└────┴──────────┴─────────┴───────────┴─────────────────────────────────┘
```

**Status Indicators:**
- 🟢 Green: CONFIRMED track (3+ detections)
- 🟠 Orange: TENTATIVE track (1-2 detections)
- 🟡 Yellow: COASTING track (no recent detections)

**Recent Detections**
```
┌─────────────────────────────────────────────────────────────────────┐
│ 🔍 Recent Detections                                             50  │
├────────┬────────┬──────────┬─────────┬───────────┬──────────────────┤
│ Sensor │ Target │ Range(m) │  Az(°)  │Doppler(m/s)│  SNR(dB)        │
├────────┼────────┼──────────┼─────────┼───────────┼──────────────────┤
│RADAR_A │   12   │   3450   │  23.4   │  -12.6    │ 18.2 (high)     │
│RADAR_B │   45   │   8750   │  156.8  │   25.3    │ 15.7 (high)     │
│RADAR_A │    8   │   1200   │  89.2   │   -5.4    │ 22.1 (high)     │
│RADAR_C │   23   │   5600   │  245.1  │  -18.9    │  9.3 (medium)   │
│RADAR_B │   67   │   9200   │  12.5   │   31.7    │ 16.4 (high)     │
│RADAR_A │   34   │   2850   │  178.9  │    8.2    │  6.8 (medium)   │
│RADAR_C │   19   │   7100   │  301.4  │  -22.1    │ 19.8 (high)     │
└────────┴────────┴──────────┴─────────┴───────────┴──────────────────┘
```

**SNR Color Coding:**
- 🟢 Green: High SNR (>15 dB) - Reliable detection
- 🟠 Orange: Medium SNR (8-15 dB) - Acceptable
- 🔴 Red: Low SNR (<8 dB) - Uncertain

---

## Real-Time Features

### 1. Live Data Updates
- **Update Rate**: 10 Hz (every 100ms)
- **Smooth Animation**: No flickering or lag
- **Auto-Scrolling**: Tables automatically update
- **Connection Resilience**: Auto-reconnect on disconnect

### 2. Interactive Elements
- **3D Rotation**: Click and drag to rotate view
- **Zoom**: Scroll wheel to zoom in/out
- **Pan**: Right-click and drag to pan
- **Hover Details**: Mouse over for detailed information
- **Responsive**: Works on desktop, tablet, mobile

### 3. Visual Indicators
- **Pulse Animations**: Connection status pulses
- **Color Coding**: Intuitive status colors
- **Smooth Transitions**: Fade in/out effects
- **Loading States**: Clear feedback

---

## Data Flow Visualization

```
┌──────────────────────────────────────────────────────────────┐
│                    RADIX Data Pipeline                       │
└──────────────────────────────────────────────────────────────┘

1. Simulation (100ms tick)
   ├─ RADAR_A (FMCW)      → Generates detections
   ├─ RADAR_B (Pulse-Dop) → Generates detections  
   └─ RADAR_C (AESA)      → Generates detections
          ↓
2. Normalization
   └─ Convert to unified schema
   └─ ENU coordinate transformation
          ↓
3. Tracking
   └─ Associate detections to tracks
   └─ Update track states
          ↓
4. WebSocket Broadcast
   └─ Send to all connected clients
          ↓
5. Frontend Update
   ├─ Update 3D visualization
   ├─ Update track table
   ├─ Update detection table
   └─ Update performance charts
```

---

## API Interaction Examples

### Get System Status
```bash
curl http://localhost:8000/api/status

Response:
{
  "uptime_seconds": 323.5,
  "active_radars": 3,
  "total_detections": 15234,
  "active_tracks": 8,
  "data_rate_hz": 125.3,
  "timestamp": "2025-12-18T10:30:00Z"
}
```

### Get Active Tracks
```bash
curl http://localhost:8000/api/tracks

Response:
[
  {
    "track_id": 1,
    "sensor_id": "RADAR_A",
    "position": [2000.5, 3000.2, 100.0],
    "velocity": [-10.2, -5.1, 0.0],
    "track_state": "CONFIRMED",
    "num_detections": 25
  },
  ...
]
```

### WebSocket Connection
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Detections:', data.detections.length);
  console.log('Tracks:', data.tracks.length);
  console.log('Data Rate:', data.system_status.data_rate_hz);
};
```

---

## Dataset Export Examples

### Create Tabular Dataset
```python
import requests

response = requests.post(
    'http://localhost:8000/api/datasets/create',
    params={
        'name': 'Training Dataset',
        'description': 'Dataset for classifier training',
        'format': 'tabular'
    }
)

dataset = response.json()
print(f"Created dataset: {dataset['dataset_id']}")
```

### Export for ML Training
```python
import pandas as pd

# Export as CSV
response = requests.get(
    f'http://localhost:8000/api/datasets/{dataset_id}/export',
    params={'format': 'csv'}
)

df = pd.DataFrame(response.json())
print(df.head())

# Use for ML training
from sklearn.ensemble import RandomForestClassifier

X = df[['range_m', 'doppler_mps', 'snr_db']]
y = df['track_state']

model = RandomForestClassifier()
model.fit(X, y)
```

---

## Performance Characteristics

### Typical Operating Metrics
- **Detections/Second**: 100-200
- **Tracks**: Up to 50 simultaneous
- **Latency**: <100ms from detection to display
- **Memory Usage**: <500 MB
- **CPU Usage**: <10% on modern hardware
- **Network Bandwidth**: <1 Mbps

### Scalability
Current system handles:
- ✅ 10 targets
- ✅ 3 radars
- ✅ 100-200 Hz data rate
- ✅ Multiple WebSocket clients

For larger scale:
- Add Redis for message queue
- Use PostgreSQL for historical data
- Deploy multiple tracker instances
- Load balance WebSocket connections

---

## Color Scheme

### Primary Colors
- **Cyan** (#00d4ff): Primary accent, active elements
- **Green** (#00ff88): Success, confirmed tracks
- **Orange** (#ffa500): Warning, tentative tracks
- **Red** (#ff4444): Alert, low SNR
- **Yellow** (#ffff00): Attention, coasting tracks

### Background Colors
- **Dark Blue** (#0a0e27): Primary background
- **Navy** (#1a1f3a): Card backgrounds
- **Slate** (#3b4575): Borders and dividers

### Text Colors
- **White** (#e0e0e0): Primary text
- **Gray** (#8899aa): Secondary text
- **Cyan** (#00d4ff): Headings and labels

---

## Keyboard Shortcuts (Frontend)

- **R**: Reset 3D camera view
- **F**: Toggle fullscreen
- **S**: Take screenshot (browser default)
- **Ctrl+Shift+I**: Open browser DevTools
- **F5**: Refresh page

---

## Browser Compatibility

✅ **Fully Supported:**
- Chrome 90+
- Firefox 88+
- Edge 90+
- Safari 14+

⚠️ **Partial Support:**
- IE 11 (limited WebSocket support)
- Older mobile browsers

---

## Mobile/Tablet Experience

The interface is responsive and works on mobile devices:

- **Portrait Mode**: Stacked layout
- **Landscape Mode**: Side-by-side panels
- **Touch Controls**: Tap, pinch, swipe
- **Optimized**: Reduced data transfer on cellular

---

## Customization Options

### Change Update Rate
Edit `config.yaml`:
```yaml
simulation:
  update_interval: 0.05  # 20 Hz (faster)
  # or
  update_interval: 0.5   # 2 Hz (slower)
```

### Add More Targets
```yaml
simulation:
  num_targets: 20  # More targets
```

### Adjust Radar Parameters
```yaml
radars:
  - id: "RADAR_A"
    location: [100, 200, 50]  # Reposition
    enabled: false            # Disable
```

---

## Tips for Best Experience

1. **Use Chrome or Firefox**: Best WebGL performance
2. **High DPI Display**: Sharper visualization
3. **Dark Room**: Easier on eyes for long monitoring
4. **Multiple Monitors**: Spread out API docs + GUI
5. **Fast Network**: Reduce WebSocket latency

---

## Troubleshooting Display Issues

### 3D View Not Rendering
- Check browser WebGL support: https://get.webgl.org/
- Update graphics drivers
- Try different browser

### Choppy Animation
- Close other browser tabs
- Check CPU usage
- Reduce number of targets in config

### No Data Showing
- Check WebSocket connection (green indicator)
- Verify backend is running
- Check browser console for errors

---

<div align="center">

**Experience RADIX Today!**

Launch the application and see professional radar data integration in action.

```bash
./start.sh
```

Then visit: **http://localhost:3000**

</div>
