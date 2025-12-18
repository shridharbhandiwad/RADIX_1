"""
Unified data schemas for RADIX
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class RadarType(str, Enum):
    """Supported radar types"""
    FMCW = "FMCW"
    PULSE_DOPPLER = "PULSE_DOPPLER"
    AESA = "AESA"
    ISAR = "ISAR"
    CW = "CW"


class TrackState(str, Enum):
    """Target track state"""
    TENTATIVE = "TENTATIVE"
    CONFIRMED = "CONFIRMED"
    COASTING = "COASTING"
    LOST = "LOST"


class RadarConfig(BaseModel):
    """Radar configuration"""
    id: str
    type: RadarType
    location: List[float] = Field(..., min_length=3, max_length=3)
    frequency_ghz: float
    enabled: bool = True
    metadata: Dict[str, Any] = Field(default_factory=dict)


class RawRadarDetection(BaseModel):
    """Raw radar detection before normalization"""
    timestamp: datetime
    sensor_id: str
    raw_data: Dict[str, Any]
    format_type: str


class NormalizedRadarData(BaseModel):
    """Unified normalized radar data schema"""
    timestamp: datetime
    sensor_id: str
    target_id: Optional[int] = None
    range_m: float
    azimuth_deg: float
    elevation_deg: Optional[float] = None
    doppler_mps: float
    snr_db: float
    rcs_dbsm: Optional[float] = None
    track_state: Optional[TrackState] = None
    position_enu: Optional[List[float]] = None  # East-North-Up coordinates
    velocity_enu: Optional[List[float]] = None
    raw_iq_ref: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        json_schema_extra = {
            "example": {
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
        }


class TargetTrack(BaseModel):
    """Processed target track"""
    track_id: int
    sensor_id: str
    first_seen: datetime
    last_updated: datetime
    state_vector: List[float]  # [x, y, z, vx, vy, vz]
    covariance: Optional[List[List[float]]] = None
    track_state: TrackState
    detections: List[NormalizedRadarData] = Field(default_factory=list)
    classification: Optional[str] = None
    confidence: Optional[float] = None


class MLDataset(BaseModel):
    """ML-ready dataset configuration"""
    dataset_id: str
    name: str
    description: str
    created_at: datetime
    sensor_ids: List[str]
    start_time: datetime
    end_time: datetime
    num_samples: int
    format: str  # 'sequence', 'graph', 'image', 'tabular'
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SystemStatus(BaseModel):
    """System status information"""
    uptime_seconds: float
    active_radars: int
    total_detections: int
    active_tracks: int
    data_rate_hz: float
    timestamp: datetime
