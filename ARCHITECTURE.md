# RADIX Architecture Documentation

## System Overview

RADIX is designed as a modular, scalable framework for radar data processing and ML dataset generation. The architecture follows a pipeline pattern with clear separation of concerns.

## Core Components

### 1. Radar Simulators (`radix/simulators/`)

#### Base Simulator
- **Location**: `radix/simulators/base.py`
- **Purpose**: Abstract base class for all radar simulators
- **Key Classes**:
  - `Target`: Represents a simulated target with position, velocity, and RCS
  - `RadarSimulator`: Base class with common functionality

#### Specific Simulators
- **FMCW**: `fmcw_simulator.py` - Automotive radar simulation
- **Pulse-Doppler**: `pulse_doppler_simulator.py` - Airborne radar simulation
- **AESA**: `aesa_simulator.py` - Phased array radar simulation

**Key Features**:
- Physics-based target motion
- Realistic detection probability based on SNR
- False alarm generation
- Radar-specific measurements (beat frequency, PRF, beam steering)

### 2. Data Normalization (`radix/core/normalizer.py`)

**Purpose**: Convert heterogeneous radar data to unified schema

**Process**:
1. Receive raw radar detection
2. Identify radar type
3. Apply type-specific normalization
4. Convert to ENU (East-North-Up) coordinates
5. Calculate position and velocity vectors
6. Preserve radar-specific metadata

**Output**: `NormalizedRadarData` - unified format for all downstream processing

### 3. Multi-Target Tracking (`radix/core/tracker.py`)

**Algorithm**: Nearest-neighbor data association

**Track States**:
```
TENTATIVE → CONFIRMED → COASTING → LOST
```

**Features**:
- Automatic track initialization
- Track state management
- Configurable association distance
- Coast time management
- Track history pruning

**Future Enhancements**:
- Kalman filtering for state estimation
- JPDA (Joint Probabilistic Data Association)
- MHT (Multiple Hypothesis Tracking)

### 4. Feature Extraction (`radix/core/extractor.py`)

**Purpose**: Generate ML-ready datasets from processed radar data

**Export Formats**:

#### Tabular Format
- One row per detection
- All features as columns
- Suitable for: Random Forest, XGBoost, SVM

#### Sequence Format
- Time-series windows
- Track-wise segmentation
- Suitable for: LSTM, GRU, Transformers

#### Graph Format
- Nodes: Target tracks
- Edges: Spatial relationships
- Suitable for: GCN, GAT, GNN

**Statistical Features**:
- Position statistics (mean, std)
- Velocity statistics
- Track characteristics
- Time-series metrics

### 5. API Layer (`radix/api/main.py`)

**Framework**: FastAPI

**Endpoints**:
- REST API for configuration and data access
- WebSocket for real-time streaming
- Dataset creation and export

**Key Features**:
- Asynchronous request handling
- CORS support for web clients
- Automatic API documentation
- WebSocket connection management

### 6. Frontend (`frontend/src/`)

**Framework**: React 18 with Vite

**Components**:
- `Header`: System status and branding
- `StatusBar`: Real-time metrics
- `RadarDisplay`: 3D visualization with Plotly
- `TrackList`: Active target tracks
- `DetectionTable`: Recent detections
- `DataRateChart`: Performance metrics with Recharts

**Real-Time Updates**:
- WebSocket connection to backend
- Automatic reconnection
- Efficient state management

## Data Flow

```
1. Simulation Loop (100ms interval)
   ↓
2. Multiple Radar Simulators
   └─> Generate raw detections
       ↓
3. Data Normalizer
   └─> Convert to unified schema
       ↓
4. Target Tracker
   └─> Associate detections to tracks
       ↓
5. WebSocket Broadcast
   └─> Send to connected clients
       ↓
6. Frontend Visualization
   └─> Update 3D view and tables
```

## State Management

### Backend State (`RADIXState`)
```python
class RADIXState:
    simulators: Dict[str, RadarSimulator]
    normalizer: DataNormalizer
    tracker: SimpleTracker
    extractor: DataExtractor
    all_detections: List[NormalizedRadarData]
    active_websockets: List[WebSocket]
    simulation_running: bool
```

### Frontend State
- `systemStatus`: System metrics
- `detections`: Recent detections
- `tracks`: Active tracks
- `radars`: Radar configurations
- `dataRateHistory`: Performance history
- `connected`: WebSocket connection status

## Concurrency Model

### Backend
- **Async Event Loop**: FastAPI with uvicorn
- **Simulation Loop**: Separate async task
- **WebSocket Broadcasting**: Non-blocking sends
- **Database**: SQLite with async support (aiosqlite)

### Frontend
- **Single-threaded**: React event loop
- **WebSocket Handler**: Async message processing
- **State Updates**: Immutable updates with hooks

## Scalability Considerations

### Current Design (Single Node)
- ✅ Suitable for development and testing
- ✅ 10 targets, 3 radars, 100-200 Hz
- ✅ Real-time visualization

### Production Scale-Out
1. **Message Queue**: Add Redis/RabbitMQ for radar data ingestion
2. **Processing Workers**: Multiple tracker instances
3. **Time-Series Database**: TimescaleDB for historical data
4. **Load Balancer**: Distribute WebSocket connections
5. **Microservices**: Separate ingestion, tracking, and serving

## Security Considerations

### Current Implementation
- CORS enabled for development
- No authentication (suitable for internal networks)
- WebSocket open to all

### Production Hardening
1. **Authentication**: JWT tokens for API access
2. **Authorization**: Role-based access control
3. **Encryption**: TLS/SSL for all connections
4. **Rate Limiting**: Prevent API abuse
5. **Input Validation**: Strict schema validation

## Testing Strategy

### Unit Tests
- Individual component testing
- Mock external dependencies
- 80%+ code coverage

### Integration Tests
- API endpoint testing
- WebSocket communication
- End-to-end data flow

### Performance Tests
- Load testing with multiple targets
- Latency measurements
- Memory profiling

## Configuration Management

### Static Configuration (`config.yaml`)
- Simulation parameters
- Radar configurations
- ML export settings

### Runtime Configuration
- API parameters
- WebSocket connections
- Dynamic radar enable/disable

## Error Handling

### Backend
- Try-catch blocks around critical sections
- Logging for debugging
- Graceful degradation (remove failed radars)

### Frontend
- Error boundaries for React components
- WebSocket reconnection logic
- User-friendly error messages

## Monitoring and Observability

### Metrics Exposed
- System uptime
- Data rate (Hz)
- Active tracks count
- Total detections
- Processing latency

### Future Enhancements
- Prometheus metrics export
- Grafana dashboards
- Distributed tracing
- Log aggregation

## Extension Points

### Adding New Radar Types
1. Implement `RadarSimulator` subclass
2. Add normalization logic
3. Update schemas
4. Add tests

### Adding New Export Formats
1. Implement extraction method in `DataExtractor`
2. Add API endpoint
3. Update frontend

### Custom Tracking Algorithms
1. Implement tracker interface
2. Swap in `RADIXState`
3. Maintain API compatibility

## Dependencies

### Backend
- **FastAPI**: Web framework
- **NumPy**: Numerical computing
- **Pandas**: Data manipulation
- **SQLAlchemy**: Database ORM
- **Pydantic**: Data validation

### Frontend
- **React**: UI framework
- **Plotly**: 3D visualization
- **Recharts**: 2D charts
- **Vite**: Build tool

## Deployment

### Development
```bash
# Backend
uvicorn radix.api.main:app --reload

# Frontend
npm run dev
```

### Production
```bash
# Backend with multiple workers
uvicorn radix.api.main:app --workers 4 --host 0.0.0.0

# Frontend (build and serve)
npm run build
serve -s build
```

### Docker (Future)
```dockerfile
# Multi-stage build
FROM python:3.11-slim AS backend
FROM node:18-alpine AS frontend
# ... combine in final image
```

## Performance Optimization

### Current Optimizations
- Batch normalization
- Detection history pruning (keep last 1000)
- WebSocket message throttling
- Efficient numpy operations

### Future Optimizations
- C++ extensions for critical paths
- GPU acceleration for ML features
- Cython compilation
- Database indexing
- Connection pooling

## Conclusion

RADIX's architecture is designed for:
- **Modularity**: Easy to extend and modify
- **Scalability**: Clear path from development to production
- **Maintainability**: Clean separation of concerns
- **Performance**: Optimized for real-time processing
- **Testability**: Comprehensive test coverage

The framework provides a solid foundation for building radar-based AI systems while remaining flexible enough to adapt to specific use cases and requirements.
