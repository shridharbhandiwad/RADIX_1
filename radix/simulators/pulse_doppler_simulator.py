"""
Pulse-Doppler Radar Simulator
"""
import numpy as np
from datetime import datetime
from typing import Dict, Any, Optional
from .base import RadarSimulator, Target


class PulseDopplerRadarSimulator(RadarSimulator):
    """
    Pulse-Doppler radar simulator
    Common in airborne and air defense applications
    """
    
    def __init__(self, config):
        super().__init__(config)
        self.frequency_ghz = config.metadata.get("frequency_ghz", 10)
        self.prf_hz = config.metadata.get("prf_hz", 10000)  # Pulse Repetition Frequency
        self.pulse_width_us = config.metadata.get("pulse_width_us", 1.0)
        self.num_pulses = config.metadata.get("num_pulses", 128)
        
        # Pulse-Doppler specific parameters
        self.wavelength_m = 3e8 / (self.frequency_ghz * 1e9)
        self.max_unambiguous_range = (3e8 / (2 * self.prf_hz))
        self.max_unambiguous_velocity = (self.wavelength_m * self.prf_hz) / 4
        
    def generate_detection(self, target: Target, timestamp: datetime) -> Optional[Dict[str, Any]]:
        """Generate Pulse-Doppler specific detection"""
        range_m, azimuth_deg, elevation_deg = target.get_range_azimuth_elevation(self.radar_pos)
        doppler_mps = target.get_doppler(self.radar_pos)
        snr_db = self.calculate_snr(range_m, target.rcs)
        
        # Add noise
        range_m += np.random.normal(0, self.range_noise_std)
        azimuth_deg += np.random.normal(0, self.angle_noise_std)
        elevation_deg += np.random.normal(0, self.angle_noise_std * 1.5)
        doppler_mps += np.random.normal(0, self.doppler_noise_std)
        
        # Doppler frequency
        doppler_freq_hz = 2 * doppler_mps / self.wavelength_m
        
        # Check for range/velocity ambiguities
        range_ambiguity = int(range_m / self.max_unambiguous_range)
        velocity_folded = doppler_mps % (2 * self.max_unambiguous_velocity) - self.max_unambiguous_velocity
        
        detection = {
            "target_id": target.target_id,
            "range_m": max(0, range_m),
            "azimuth_deg": azimuth_deg % 360,
            "elevation_deg": np.clip(elevation_deg, -90, 90),
            "doppler_mps": doppler_mps,
            "doppler_freq_hz": doppler_freq_hz,
            "velocity_folded": velocity_folded,
            "snr_db": snr_db,
            "rcs_dbsm": target.rcs,
            "prf_hz": self.prf_hz,
            "pulse_width_us": self.pulse_width_us,
            "num_pulses": self.num_pulses,
            "range_ambiguity": range_ambiguity,
            "is_false_alarm": False
        }
        
        return detection
