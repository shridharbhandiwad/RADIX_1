"""
FMCW (Frequency Modulated Continuous Wave) Radar Simulator
"""
import numpy as np
from datetime import datetime
from typing import Dict, Any, Optional
from .base import RadarSimulator, Target


class FMCWRadarSimulator(RadarSimulator):
    """
    FMCW radar simulator
    Common in automotive and short-range applications
    """
    
    def __init__(self, config):
        super().__init__(config)
        self.frequency_ghz = config.metadata.get("frequency_ghz", 77)
        self.bandwidth_mhz = config.metadata.get("bandwidth_mhz", 4000)
        self.chirp_time_us = config.metadata.get("chirp_time_us", 50)
        
        # FMCW-specific parameters
        self.range_resolution = 3e8 / (2 * self.bandwidth_mhz * 1e6)  # meters
        self.max_range = (3e8 * self.chirp_time_us * 1e-6) / 2
        
    def generate_detection(self, target: Target, timestamp: datetime) -> Optional[Dict[str, Any]]:
        """Generate FMCW-specific detection"""
        range_m, azimuth_deg, elevation_deg = target.get_range_azimuth_elevation(self.radar_pos)
        doppler_mps = target.get_doppler(self.radar_pos)
        snr_db = self.calculate_snr(range_m, target.rcs)
        
        # Add FMCW-specific noise
        range_m += np.random.normal(0, self.range_noise_std)
        azimuth_deg += np.random.normal(0, self.angle_noise_std)
        elevation_deg += np.random.normal(0, self.angle_noise_std)
        doppler_mps += np.random.normal(0, self.doppler_noise_std)
        
        # FMCW-specific measurements
        beat_frequency_khz = (2 * self.bandwidth_mhz * range_m) / (3e8 * self.chirp_time_us * 1e-6) / 1000
        
        detection = {
            "target_id": target.target_id,
            "range_m": max(0, range_m),
            "azimuth_deg": azimuth_deg % 360,
            "elevation_deg": np.clip(elevation_deg, -90, 90),
            "doppler_mps": doppler_mps,
            "snr_db": snr_db,
            "rcs_dbsm": target.rcs,
            "beat_frequency_khz": beat_frequency_khz,
            "chirp_time_us": self.chirp_time_us,
            "range_resolution_m": self.range_resolution,
            "is_false_alarm": False
        }
        
        return detection
