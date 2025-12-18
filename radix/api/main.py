"""
FastAPI main application for RADIX
"""
import asyncio
import json
from datetime import datetime
from typing import List, Dict, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import numpy as np

from ..models.schemas import (
    RadarConfig, RadarType, NormalizedRadarData, 
    TargetTrack, SystemStatus, MLDataset
)
from ..simulators.base import Target
from ..simulators.fmcw_simulator import FMCWRadarSimulator
from ..simulators.pulse_doppler_simulator import PulseDopplerRadarSimulator
from ..simulators.aesa_simulator import AESARadarSimulator
from ..core.normalizer import DataNormalizer
from ..core.tracker import SimpleTracker
from ..core.extractor import DataExtractor


app = FastAPI(
    title="RADIX API",
    description="Radar Data Integration & eXtraction Framework",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global state
class RADIXState:
    def __init__(self):
        self.simulators: Dict[str, Any] = {}
        self.normalizer = DataNormalizer()
        self.tracker = SimpleTracker()
        self.extractor = DataExtractor()
        self.all_detections: List[NormalizedRadarData] = []
        self.active_websockets: List[WebSocket] = []
        self.simulation_running = False
        self.start_time = datetime.utcnow()
        self.total_detections = 0
        self.data_rate_hz = 0.0


state = RADIXState()


def create_radar_simulator(config: RadarConfig):
    """Factory for creating radar simulators"""
    if config.type == RadarType.FMCW:
        return FMCWRadarSimulator(config)
    elif config.type == RadarType.PULSE_DOPPLER:
        return PulseDopplerRadarSimulator(config)
    elif config.type == RadarType.AESA:
        return AESARadarSimulator(config)
    else:
        raise ValueError(f"Unsupported radar type: {config.type}")


def initialize_simulation():
    """Initialize radar simulators and targets"""
    # Create radar configurations
    radar_configs = [
        RadarConfig(
            id="RADAR_A",
            type=RadarType.FMCW,
            location=[0, 0, 10],
            frequency_ghz=77,
            metadata={"frequency_ghz": 77, "bandwidth_mhz": 4000}
        ),
        RadarConfig(
            id="RADAR_B",
            type=RadarType.PULSE_DOPPLER,
            location=[1000, 1000, 15],
            frequency_ghz=10,
            metadata={"frequency_ghz": 10, "prf_hz": 10000}
        ),
        RadarConfig(
            id="RADAR_C",
            type=RadarType.AESA,
            location=[2000, -1000, 20],
            frequency_ghz=35,
            metadata={"frequency_ghz": 35, "elements": 1024}
        ),
    ]
    
    # Create simulators
    for config in radar_configs:
        simulator = create_radar_simulator(config)
        state.simulators[config.id] = simulator
    
    # Create simulated targets
    np.random.seed(42)
    for i in range(10):
        # Random position
        position = np.array([
            np.random.uniform(-5000, 5000),  # x
            np.random.uniform(1000, 8000),   # y (forward)
            np.random.uniform(50, 500)       # z (altitude)
        ])
        
        # Random velocity
        velocity = np.array([
            np.random.uniform(-50, 50),      # vx
            np.random.uniform(-30, 30),      # vy
            np.random.uniform(-5, 5)         # vz
        ])
        
        # Random RCS
        rcs = np.random.uniform(0, 20)
        
        target = Target(i, position, velocity, rcs)
        
        # Add target to all simulators
        for simulator in state.simulators.values():
            simulator.add_target(target)


async def simulation_loop():
    """Main simulation loop"""
    dt = 0.1  # 100ms update interval
    frame_count = 0
    last_rate_update = datetime.utcnow()
    detections_since_last = 0
    
    while state.simulation_running:
        current_time = datetime.utcnow()
        
        # Update all targets
        for simulator in state.simulators.values():
            simulator.update_targets(dt)
        
        # Generate detections from all radars
        all_raw_detections = []
        for simulator in state.simulators.values():
            raw_detections = simulator.simulate_frame(current_time)
            all_raw_detections.extend(raw_detections)
        
        # Normalize detections
        normalized_detections = state.normalizer.batch_normalize(all_raw_detections)
        state.all_detections.extend(normalized_detections)
        state.total_detections += len(normalized_detections)
        detections_since_last += len(normalized_detections)
        
        # Keep only recent detections in memory (last 1000)
        if len(state.all_detections) > 1000:
            state.all_detections = state.all_detections[-1000:]
        
        # Update tracks
        if normalized_detections:
            tracks = state.tracker.update(normalized_detections)
        else:
            tracks = list(state.tracker.tracks.values())
        
        # Calculate data rate
        time_diff = (current_time - last_rate_update).total_seconds()
        if time_diff >= 1.0:
            state.data_rate_hz = detections_since_last / time_diff
            detections_since_last = 0
            last_rate_update = current_time
        
        # Broadcast to WebSocket clients
        if state.active_websockets:
            message = {
                "type": "update",
                "timestamp": current_time.isoformat(),
                "detections": [
                    {
                        "sensor_id": d.sensor_id,
                        "target_id": d.target_id,
                        "range_m": round(d.range_m, 2),
                        "azimuth_deg": round(d.azimuth_deg, 2),
                        "elevation_deg": round(d.elevation_deg or 0, 2),
                        "doppler_mps": round(d.doppler_mps, 2),
                        "snr_db": round(d.snr_db, 2),
                        "position_enu": [round(p, 2) for p in d.position_enu] if d.position_enu else None,
                        "track_state": d.track_state.value if d.track_state else None
                    }
                    for d in normalized_detections[:50]  # Limit to 50 per frame
                ],
                "tracks": [
                    {
                        "track_id": t.track_id,
                        "sensor_id": t.sensor_id,
                        "position": [round(t.state_vector[i], 2) for i in range(3)],
                        "velocity": [round(t.state_vector[i], 2) for i in range(3, 6)],
                        "track_state": t.track_state.value,
                        "num_detections": len(t.detections)
                    }
                    for t in tracks
                ],
                "system_status": {
                    "uptime_seconds": (current_time - state.start_time).total_seconds(),
                    "active_radars": len(state.simulators),
                    "total_detections": state.total_detections,
                    "active_tracks": len(state.tracker.get_active_tracks()),
                    "data_rate_hz": round(state.data_rate_hz, 2)
                }
            }
            
            # Send to all connected clients
            disconnected = []
            for ws in state.active_websockets:
                try:
                    await ws.send_json(message)
                except:
                    disconnected.append(ws)
            
            # Remove disconnected clients
            for ws in disconnected:
                state.active_websockets.remove(ws)
        
        frame_count += 1
        await asyncio.sleep(dt)


@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    initialize_simulation()
    state.simulation_running = True
    # Start simulation loop
    asyncio.create_task(simulation_loop())


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    state.simulation_running = False


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "RADIX",
        "version": "1.0.0",
        "description": "Radar Data Integration & eXtraction Framework"
    }


@app.get("/api/status", response_model=SystemStatus)
async def get_status():
    """Get system status"""
    current_time = datetime.utcnow()
    return SystemStatus(
        uptime_seconds=(current_time - state.start_time).total_seconds(),
        active_radars=len(state.simulators),
        total_detections=state.total_detections,
        active_tracks=len(state.tracker.get_active_tracks()),
        data_rate_hz=state.data_rate_hz,
        timestamp=current_time
    )


@app.get("/api/radars")
async def get_radars():
    """Get configured radars"""
    return [
        {
            "id": sim.config.id,
            "type": sim.config.type.value,
            "location": sim.config.location,
            "enabled": sim.config.enabled
        }
        for sim in state.simulators.values()
    ]


@app.get("/api/tracks")
async def get_tracks():
    """Get active tracks"""
    tracks = state.tracker.get_active_tracks()
    return [
        {
            "track_id": t.track_id,
            "sensor_id": t.sensor_id,
            "position": t.state_vector[:3],
            "velocity": t.state_vector[3:6],
            "track_state": t.track_state.value,
            "first_seen": t.first_seen.isoformat(),
            "last_updated": t.last_updated.isoformat(),
            "num_detections": len(t.detections)
        }
        for t in tracks
    ]


@app.get("/api/detections")
async def get_recent_detections(limit: int = 100):
    """Get recent detections"""
    recent = state.all_detections[-limit:]
    return [
        {
            "timestamp": d.timestamp.isoformat(),
            "sensor_id": d.sensor_id,
            "target_id": d.target_id,
            "range_m": d.range_m,
            "azimuth_deg": d.azimuth_deg,
            "elevation_deg": d.elevation_deg,
            "doppler_mps": d.doppler_mps,
            "snr_db": d.snr_db,
            "position_enu": d.position_enu
        }
        for d in recent
    ]


@app.get("/api/datasets")
async def get_datasets():
    """Get available ML datasets"""
    return list(state.extractor.datasets.values())


@app.post("/api/datasets/create")
async def create_dataset(name: str, description: str, format: str = "tabular"):
    """Create new ML dataset"""
    tracks = list(state.tracker.tracks.values())
    dataset = state.extractor.create_ml_dataset(
        name=name,
        description=description,
        detections=state.all_detections,
        tracks=tracks,
        format=format
    )
    return dataset


@app.get("/api/datasets/{dataset_id}/export")
async def export_dataset(dataset_id: str, format: str = "csv"):
    """Export dataset in specified format"""
    if dataset_id not in state.extractor.datasets:
        return JSONResponse(status_code=404, content={"error": "Dataset not found"})
    
    tracks = list(state.tracker.tracks.values())
    
    if format == "tabular":
        df = state.extractor.extract_tabular_dataset(state.all_detections)
        return JSONResponse(content=df.to_dict(orient="records"))
    elif format == "sequence":
        df = state.extractor.extract_sequence_dataset(tracks)
        return JSONResponse(content=df.to_dict(orient="records"))
    elif format == "graph":
        graph_data = state.extractor.extract_graph_dataset(tracks)
        return JSONResponse(content={
            "nodes": graph_data["nodes"].to_dict(orient="records"),
            "adjacency": graph_data["adjacency"].tolist()
        })
    else:
        return JSONResponse(status_code=400, content={"error": "Invalid format"})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time data streaming"""
    await websocket.accept()
    state.active_websockets.append(websocket)
    
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        state.active_websockets.remove(websocket)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
