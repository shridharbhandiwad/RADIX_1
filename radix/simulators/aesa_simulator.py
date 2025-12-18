"""
AESA (Active Electronically Scanned Array) Radar Simulator
"""
import numpy as np
from datetime import datetime
from typing import Dict, Any, Optional
from .base import RadarSimulator, Target


class AESARadarSimulator(RadarSimulator):
    """
    AESA radar simulator
    Used in advanced defense systems with electronic beam steering
    """
    
    def __init__(self, config):
        super().__init__(config)
        self.frequency_ghz = config.metadata.get("frequency_ghz", 35)
        self.elements = config.metadata.get("elements", 1024)
        self.beam_width_deg = config.metadata.get("beam_width_deg", 2.0)
        
        # AESA-specific parameters
        self.wavelength_m = 3e8 / (self.frequency_ghz * 1e9)
        self.element_spacing = self.wavelength_m / 2
        
        # Beam steering parameters
        self.scan_azimuth_range = (-60, 60)  # degrees
        self.scan_elevation_range = (-45, 45)  # degrees
        
        # Current beam pointing
        self.beam_azimuth = 0
        self.beam_elevation = 0
        
    def steer_beam(self, azimuth: float, elevation: float):
        """Electronically steer the beam"""
        self.beam_azimuth = np.clip(azimuth, *self.scan_azimuth_range)
        self.beam_elevation = np.clip(elevation, *self.scan_elevation_range)
    
    def calculate_beam_gain(self, target_az: float, target_el: float) -> float:
        """Calculate antenna gain based on beam pointing and target angle"""
        # Angular difference from beam center
        az_diff = abs(target_az - self.beam_azimuth)
        el_diff = abs(target_el - self.beam_elevation)
        
        # Gaussian beam pattern
        gain_db = -12 * ((az_diff / self.beam_width_deg) ** 2 + 
                         (el_diff / self.beam_width_deg) ** 2)
        
        return max(gain_db, -40)  # Minimum gain limit
    
    def generate_detection(self, target: Target, timestamp: datetime) -> Optional[Dict[str, Any]]:
        """Generate AESA-specific detection"""
        range_m, azimuth_deg, elevation_deg = target.get_range_azimuth_elevation(self.radar_pos)
        doppler_mps = target.get_doppler(self.radar_pos)
        
        # Calculate beam gain
        beam_gain_db = self.calculate_beam_gain(azimuth_deg, elevation_deg)
        
        # Enhanced SNR calculation with beam gain
        snr_db = self.calculate_snr(range_m, target.rcs) + beam_gain_db
        
        # AESA has better angle accuracy
        range_m += np.random.normal(0, self.range_noise_std * 0.5)
        azimuth_deg += np.random.normal(0, self.angle_noise_std * 0.3)
        elevation_deg += np.random.normal(0, self.angle_noise_std * 0.3)
        doppler_mps += np.random.normal(0, self.doppler_noise_std * 0.5)
        
        # AESA can measure additional parameters
        phase_noise_deg = np.random.normal(0, 5)
        
        detection = {
            "target_id": target.target_id,
            "range_m": max(0, range_m),
            "azimuth_deg": azimuth_deg % 360,
            "elevation_deg": np.clip(elevation_deg, -90, 90),
            "doppler_mps": doppler_mps,
            "snr_db": snr_db,
            "rcs_dbsm": target.rcs,
            "beam_azimuth_deg": self.beam_azimuth,
            "beam_elevation_deg": self.beam_elevation,
            "beam_gain_db": beam_gain_db,
            "num_elements": self.elements,
            "phase_noise_deg": phase_noise_deg,
            "angle_accuracy_deg": self.angle_noise_std * 0.3,
            "is_false_alarm": False
        }
        
        # Update beam steering (simple scan pattern)
        self.beam_azimuth += 5
        if self.beam_azimuth > self.scan_azimuth_range[1]:
            self.beam_azimuth = self.scan_azimuth_range[0]
        
        return detection
