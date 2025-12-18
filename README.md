# RADIX - Radar Data Integration & eXtraction Framework

<div align="center">

![RADIX Banner](https://img.shields.io/badge/RADIX-v1.0.0-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-teal?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/React-18.2-61DAFB?style=for-the-badge&logo=react)

**The data backbone for radar-driven AI systems**

</div>

---

## 🎯 Overview

RADIX is a **vendor-agnostic data infrastructure framework** designed to ingest, normalize, and extract intelligence-ready datasets from heterogeneous radar systems and sensor feeds, enabling direct downstream use in machine learning and AI model training.

### Key Features

- 🔌 **Multi-Radar Integration** - Support for FMCW, Pulse-Doppler, AESA, and custom radar types
- 🔄 **Real-Time Processing** - Live data streaming with WebSocket support
- 📊 **Unified Data Model** - Standardized schema across all radar types
- 🤖 **ML-Ready Datasets** - Export in formats ready for training (sequences, graphs, tabular)
- 🎨 **Professional GUI** - Real-time 3D visualization and monitoring
- 🧪 **Comprehensive Testing** - Full test coverage for all components
- 🚀 **Production Ready** - Scalable architecture with FastAPI backend

---

## 🏗️ Architecture

```
Radar / Sensor Inputs
(FMCW | PD | AESA | EO | RF)
        ↓
┌────────────────────────┐
│   RADIX Ingestion      │
│  (Adapters / Drivers)  │
└──────────┬─────────────┘
           ↓
┌────────────────────────┐
│ Time & Space Alignment │
│ (Sync, Calibration)    │
└──────────┬─────────────┘
           ↓
┌────────────────────────┐
│ Data Normalization     │
│ (Unified Schema)       │
└──────────┬─────────────┘
           ↓
┌────────────────────────┐
│ Feature Extraction     │
│ (Tracks, ISAR, μDop)   │
└──────────┬─────────────┘
           ↓
┌────────────────────────┐
│ ML-Ready Dataset Layer │
│ (Train | Val | Test)   │
└────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Node.js 16+ (for frontend)
- pip and npm

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd workspace
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Install frontend dependencies**
```bash
cd frontend
npm install
cd ..
```

### Running RADIX

#### Option 1: Run Backend and Frontend Separately

**Terminal 1 - Start Backend:**
```bash
python -m uvicorn radix.api.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Start Frontend:**
```bash
cd frontend
npm run dev
```

#### Option 2: Quick Start Script

Create a `start.sh` script:
```bash
#!/bin/bash

# Start backend in background
python -m uvicorn radix.api.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Start frontend
cd frontend
npm run dev &
FRONTEND_PID=$!

echo "RADIX is running!"
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "Access the application at: http://localhost:3000"
echo "API documentation at: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
wait
```

Make it executable and run:
```bash
chmod +x start.sh
./start.sh
```

### Access the Application

- **Web Interface**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **WebSocket Endpoint**: ws://localhost:8000/ws

---

## 📊 Features in Detail

### 1. Radar Simulators

RADIX includes high-fidelity simulators for multiple radar types:

#### FMCW (Frequency Modulated Continuous Wave)
- Automotive radar simulation
- 77 GHz frequency band
- Range and velocity measurement
- Beat frequency calculation

#### Pulse-Doppler
- Air defense applications
- Doppler processing
- Range/velocity ambiguity handling
- PRF optimization

#### AESA (Active Electronically Scanned Array)
- Electronic beam steering
- Multi-target tracking
- High angle accuracy
- Beam gain calculation

### 2. Data Normalization

All radar data is normalized to a unified schema:

```json
{
  "timestamp": "2025-12-18T10:30:00Z",
  "sensor_id": "RADAR_A",
  "target_id": 128,
  "range_m": 3450.0,
  "azimuth_deg": 23.4,
  "elevation_deg": 5.2,
  "doppler_mps": -12.6,
  "snr_db": 18.2,
  "track_state": "CONFIRMED",
  "position_enu": [2000, 3000, 100],
  "velocity_enu": [-10, -5, 0]
}
```

### 3. Multi-Target Tracking

- **Nearest-neighbor association**
- **Track state management** (Tentative → Confirmed → Coasting → Lost)
- **Configurable parameters**
- **Track history management**

### 4. ML Dataset Export

Export data in multiple formats:

#### Tabular Format
- CSV/Parquet export
- One row per detection
- All features included

#### Sequence Format
- Time-series data
- Perfect for LSTM/Transformer models
- Sliding window support

#### Graph Format
- Node-edge representation
- Spatial relationships
- Ideal for GNN models

### 5. Real-Time Visualization

The GUI provides:
- **3D Radar View** - Interactive 3D scatter plot showing detections and tracks
- **Status Dashboard** - Real-time system metrics
- **Track List** - Active target tracks with states
- **Detection Table** - Recent detections from all radars
- **Performance Charts** - Data rate and track count over time

---

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=radix --cov-report=html

# Run specific test file
pytest tests/test_simulators.py

# Run with verbose output
pytest -v
```

Test coverage includes:
- ✅ Radar simulators
- ✅ Data normalizer
- ✅ Target tracker
- ✅ Feature extractor
- ✅ API endpoints

---

## 📚 API Reference

### REST Endpoints

#### `GET /api/status`
Get system status and metrics

**Response:**
```json
{
  "uptime_seconds": 3600.5,
  "active_radars": 3,
  "total_detections": 15234,
  "active_tracks": 8,
  "data_rate_hz": 125.3,
  "timestamp": "2025-12-18T10:30:00Z"
}
```

#### `GET /api/radars`
Get configured radar systems

#### `GET /api/tracks`
Get active target tracks

#### `GET /api/detections?limit=100`
Get recent detections

#### `POST /api/datasets/create`
Create new ML dataset

**Parameters:**
- `name`: Dataset name
- `description`: Dataset description
- `format`: "tabular", "sequence", or "graph"

#### `GET /api/datasets/{dataset_id}/export?format=csv`
Export dataset in specified format

### WebSocket Interface

Connect to `ws://localhost:8000/ws` for real-time updates.

**Message Format:**
```json
{
  "type": "update",
  "timestamp": "2025-12-18T10:30:00Z",
  "detections": [...],
  "tracks": [...],
  "system_status": {...}
}
```

---

## 🛠️ Configuration

Edit `config.yaml` to customize RADIX:

```yaml
simulation:
  update_interval: 0.1  # seconds
  num_targets: 10
  max_range: 10000  # meters
  max_speed: 300    # m/s

radars:
  - id: "RADAR_A"
    type: "FMCW"
    location: [0, 0, 10]
    frequency_ghz: 77
    enabled: true
```

---

## 🔧 Development

### Project Structure

```
workspace/
├── radix/
│   ├── api/           # FastAPI backend
│   ├── core/          # Core processing engine
│   ├── models/        # Data schemas
│   └── simulators/    # Radar simulators
├── frontend/
│   └── src/
│       ├── components/  # React components
│       └── App.jsx      # Main application
├── tests/             # Comprehensive tests
├── requirements.txt   # Python dependencies
└── README.md
```

### Adding a New Radar Type

1. Create simulator in `radix/simulators/`
2. Inherit from `RadarSimulator` base class
3. Implement `generate_detection()` method
4. Add normalization in `radix/core/normalizer.py`
5. Update `RadarType` enum in schemas

---

## 🎯 Use Cases

### 1. Training Target vs Clutter Classifiers
```python
from radix.core.extractor import DataExtractor

extractor = DataExtractor()
df = extractor.extract_tabular_dataset(detections)
# Use df for training ML models
```

### 2. Multi-Radar Track Fusion
```python
from radix.core.tracker import SimpleTracker

tracker = SimpleTracker()
tracks = tracker.update(detections_from_all_radars)
```

### 3. Dataset Generation for Deep Learning
```python
# Sequence data for LSTM
sequence_df = extractor.extract_sequence_dataset(tracks, window_size=10)

# Graph data for GNN
graph_data = extractor.extract_graph_dataset(tracks)
```

---

## 📈 Performance

- **Data Rate**: 100-200 Hz typical
- **Latency**: < 100ms end-to-end
- **Tracks**: 50+ simultaneous targets
- **Radars**: 3+ simultaneous radar systems

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit a pull request

---

## 📄 License

This project is provided for educational and research purposes.

---

## 🙏 Acknowledgments

RADIX was designed to address real-world challenges in radar data integration for defense and automotive applications. The framework prioritizes:

- **Interoperability** - Work with any radar vendor
- **Reproducibility** - Dataset versioning and provenance
- **Scalability** - Production-ready architecture
- **Usability** - Professional GUI and comprehensive API

---

## 📞 Support

For questions, issues, or feature requests:

- Open an issue on GitHub
- Check the API documentation at `/docs`
- Review the test suite for usage examples

---

<div align="center">

**RADIX - From heterogeneous radars to ML-ready intelligence**

Built with ❤️ using Python, FastAPI, and React

</div>
