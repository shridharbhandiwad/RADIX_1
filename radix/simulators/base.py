"""
Base classes for radar simulation
"""
import numpy as np
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Any, Optional
from ..models.schemas import RadarConfig, RawRadarDetection, TrackState


class Target:
    """Simulated target with kinematic state"""
    
    def __init__(self, target_id: int, position: np.ndarray, velocity: np.ndarray, rcs: float = 10.0):
        self.target_id = target_id
        self.position = np.array(position, dtype=np.float64)  # [x, y, z] in meters
        self.velocity = np.array(velocity, dtype=np.float64)  # [vx, vy, vz] in m/s
        self.rcs = rcs  # Radar cross-section in dBsm
        self.track_state = TrackState.TENTATIVE
        self.detection_count = 0
    
    def update(self, dt: float):
        """Update target position"""
        self.position += self.velocity * dt
        
        # Simple boundary checking - bounce off walls
        for i in range(3):
            if abs(self.position[i]) > 10000:
                self.velocity[i] *= -1
                self.position[i] = np.clip(self.position[i], -10000, 10000)
    
    def get_range_azimuth_elevation(self, radar_pos: np.ndarray) -> tuple:
        """Calculate range, azimuth, elevation from radar"""
        rel_pos = self.position - radar_pos
        range_m = np.linalg.norm(rel_pos)
        
        # Azimuth (degrees from North, clockwise)
        azimuth_deg = np.degrees(np.arctan2(rel_pos[0], rel_pos[1]))
        if azimuth_deg < 0:
            azimuth_deg += 360
        
        # Elevation (degrees from horizontal)
        elevation_deg = np.degrees(np.arcsin(rel_pos[2] / (range_m + 1e-9)))
        
        return range_m, azimuth_deg, elevation_deg
    
    def get_doppler(self, radar_pos: np.ndarray) -> float:
        """Calculate radial velocity (Doppler)"""
        rel_pos = self.position - radar_pos
        range_m = np.linalg.norm(rel_pos)
        if range_m < 1e-9:
            return 0.0
        
        # Project velocity onto line-of-sight
        los_unit = rel_pos / range_m
        doppler_mps = np.dot(self.velocity, los_unit)
        return doppler_mps


class RadarSimulator(ABC):
    """Abstract base class for radar simulators"""
    
    def __init__(self, config: RadarConfig):
        self.config = config
        self.radar_pos = np.array(config.location)
        self.targets: List[Target] = []
        self.detection_probability = 0.95
        self.false_alarm_rate = 0.01
        self.range_noise_std = 5.0  # meters
        self.angle_noise_std = 0.5  # degrees
        self.doppler_noise_std = 0.5  # m/s
    
    def add_target(self, target: Target):
        """Add target to simulation"""
        self.targets.append(target)
    
    def update_targets(self, dt: float):
        """Update all target positions"""
        for target in self.targets:
            target.update(dt)
    
    def calculate_snr(self, range_m: float, rcs: float) -> float:
        """Calculate SNR based on radar equation (simplified)"""
        # Simplified radar equation
        base_snr = 30.0  # dB at reference range
        range_loss = 40 * np.log10(range_m / 1000.0)  # 1/R^4 loss
        rcs_gain = rcs
        
        snr_db = base_snr - range_loss + rcs_gain
        snr_db += np.random.normal(0, 2.0)  # Add noise
        
        return max(snr_db, -10.0)
    
    def should_detect(self, snr_db: float) -> bool:
        """Determine if target should be detected based on SNR"""
        # Detection probability based on SNR
        if snr_db > 13:  # High SNR
            prob = self.detection_probability
        elif snr_db > 5:  # Medium SNR
            prob = 0.7
        elif snr_db > 0:  # Low SNR
            prob = 0.3
        else:
            prob = 0.1
        
        return np.random.random() < prob
    
    @abstractmethod
    def generate_detection(self, target: Target, timestamp: datetime) -> Optional[Dict[str, Any]]:
        """Generate radar-specific detection data"""
        pass
    
    def simulate_frame(self, timestamp: datetime) -> List[RawRadarDetection]:
        """Simulate one radar frame"""
        detections = []
        
        # Real target detections
        for target in self.targets:
            range_m, azimuth_deg, elevation_deg = target.get_range_azimuth_elevation(self.radar_pos)
            
            # Check if in radar coverage
            if range_m > 50 and range_m < 10000:  # Min and max range
                snr_db = self.calculate_snr(range_m, target.rcs)
                
                if self.should_detect(snr_db):
                    detection_data = self.generate_detection(target, timestamp)
                    if detection_data:
                        detections.append(RawRadarDetection(
                            timestamp=timestamp,
                            sensor_id=self.config.id,
                            raw_data=detection_data,
                            format_type=self.config.type.value
                        ))
        
        # False alarms
        num_false_alarms = np.random.poisson(self.false_alarm_rate * 100)
        for _ in range(num_false_alarms):
            false_alarm = self.generate_false_alarm(timestamp)
            if false_alarm:
                detections.append(false_alarm)
        
        return detections
    
    def generate_false_alarm(self, timestamp: datetime) -> Optional[RawRadarDetection]:
        """Generate false alarm detection"""
        range_m = np.random.uniform(100, 10000)
        azimuth_deg = np.random.uniform(0, 360)
        elevation_deg = np.random.uniform(-10, 45)
        
        return RawRadarDetection(
            timestamp=timestamp,
            sensor_id=self.config.id,
            raw_data={
                "range_m": range_m,
                "azimuth_deg": azimuth_deg,
                "elevation_deg": elevation_deg,
                "doppler_mps": np.random.uniform(-50, 50),
                "snr_db": np.random.uniform(0, 8),
                "is_false_alarm": True
            },
            format_type=self.config.type.value
        )
