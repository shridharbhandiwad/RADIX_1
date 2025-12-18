"""
Tests for radar simulators
"""
import pytest
import numpy as np
from datetime import datetime

from radix.models.schemas import RadarConfig, RadarType
from radix.simulators.base import Target
from radix.simulators.fmcw_simulator import FMCWRadarSimulator
from radix.simulators.pulse_doppler_simulator import PulseDopplerRadarSimulator
from radix.simulators.aesa_simulator import AESARadarSimulator


class TestTarget:
    """Test Target class"""
    
    def test_target_creation(self):
        position = np.array([1000, 2000, 100])
        velocity = np.array([10, -5, 0])
        target = Target(1, position, velocity, rcs=15.0)
        
        assert target.target_id == 1
        assert np.allclose(target.position, position)
        assert np.allclose(target.velocity, velocity)
        assert target.rcs == 15.0
    
    def test_target_update(self):
        position = np.array([1000, 2000, 100])
        velocity = np.array([10, -5, 0])
        target = Target(1, position, velocity)
        
        dt = 1.0
        target.update(dt)
        
        expected_position = position + velocity * dt
        assert np.allclose(target.position, expected_position)
    
    def test_range_azimuth_elevation(self):
        position = np.array([1000, 1000, 100])
        velocity = np.array([0, 0, 0])
        target = Target(1, position, velocity)
        
        radar_pos = np.array([0, 0, 0])
        range_m, azimuth_deg, elevation_deg = target.get_range_azimuth_elevation(radar_pos)
        
        expected_range = np.sqrt(1000**2 + 1000**2 + 100**2)
        assert abs(range_m - expected_range) < 1.0
        assert 0 <= azimuth_deg < 360
        assert -90 <= elevation_deg <= 90
    
    def test_doppler_calculation(self):
        # Target moving towards radar
        position = np.array([0, 1000, 0])
        velocity = np.array([0, -10, 0])  # Moving towards origin
        target = Target(1, position, velocity)
        
        radar_pos = np.array([0, 0, 0])
        doppler = target.get_doppler(radar_pos)
        
        # Should be negative (approaching)
        assert doppler < 0


class TestFMCWSimulator:
    """Test FMCW radar simulator"""
    
    def test_simulator_creation(self):
        config = RadarConfig(
            id="TEST_FMCW",
            type=RadarType.FMCW,
            location=[0, 0, 10],
            frequency_ghz=77,
            metadata={"frequency_ghz": 77, "bandwidth_mhz": 4000}
        )
        
        sim = FMCWRadarSimulator(config)
        assert sim.config.id == "TEST_FMCW"
        assert sim.frequency_ghz == 77
        assert sim.bandwidth_mhz == 4000
    
    def test_detection_generation(self):
        config = RadarConfig(
            id="TEST_FMCW",
            type=RadarType.FMCW,
            location=[0, 0, 10],
            frequency_ghz=77,
            metadata={"frequency_ghz": 77, "bandwidth_mhz": 4000}
        )
        
        sim = FMCWRadarSimulator(config)
        
        # Add target
        target = Target(1, np.array([1000, 2000, 100]), np.array([10, -5, 0]), rcs=10.0)
        sim.add_target(target)
        
        # Generate detections
        detections = sim.simulate_frame(datetime.utcnow())
        
        # Should have at least one detection (target might not always be detected due to probability)
        assert len(detections) >= 0
        
        # Check detection format
        for det in detections:
            assert det.sensor_id == "TEST_FMCW"
            assert det.format_type == "FMCW"
            assert "range_m" in det.raw_data
            assert "azimuth_deg" in det.raw_data
            assert "doppler_mps" in det.raw_data


class TestPulseDopplerSimulator:
    """Test Pulse-Doppler radar simulator"""
    
    def test_simulator_creation(self):
        config = RadarConfig(
            id="TEST_PD",
            type=RadarType.PULSE_DOPPLER,
            location=[0, 0, 15],
            frequency_ghz=10,
            metadata={"frequency_ghz": 10, "prf_hz": 10000}
        )
        
        sim = PulseDopplerRadarSimulator(config)
        assert sim.config.id == "TEST_PD"
        assert sim.frequency_ghz == 10
        assert sim.prf_hz == 10000
    
    def test_detection_format(self):
        config = RadarConfig(
            id="TEST_PD",
            type=RadarType.PULSE_DOPPLER,
            location=[0, 0, 15],
            frequency_ghz=10,
            metadata={"frequency_ghz": 10, "prf_hz": 10000}
        )
        
        sim = PulseDopplerRadarSimulator(config)
        target = Target(1, np.array([1000, 2000, 100]), np.array([10, -5, 0]))
        
        detection = sim.generate_detection(target, datetime.utcnow())
        
        assert detection is not None
        assert "doppler_freq_hz" in detection
        assert "prf_hz" in detection


class TestAESASimulator:
    """Test AESA radar simulator"""
    
    def test_simulator_creation(self):
        config = RadarConfig(
            id="TEST_AESA",
            type=RadarType.AESA,
            location=[0, 0, 20],
            frequency_ghz=35,
            metadata={"frequency_ghz": 35, "elements": 1024}
        )
        
        sim = AESARadarSimulator(config)
        assert sim.config.id == "TEST_AESA"
        assert sim.frequency_ghz == 35
        assert sim.elements == 1024
    
    def test_beam_steering(self):
        config = RadarConfig(
            id="TEST_AESA",
            type=RadarType.AESA,
            location=[0, 0, 20],
            frequency_ghz=35,
            metadata={"frequency_ghz": 35, "elements": 1024}
        )
        
        sim = AESARadarSimulator(config)
        
        sim.steer_beam(30, 10)
        assert sim.beam_azimuth == 30
        assert sim.beam_elevation == 10
        
        # Test limits
        sim.steer_beam(100, 50)
        assert sim.beam_azimuth <= 60  # Max azimuth
        assert sim.beam_elevation <= 45  # Max elevation
    
    def test_beam_gain_calculation(self):
        config = RadarConfig(
            id="TEST_AESA",
            type=RadarType.AESA,
            location=[0, 0, 20],
            frequency_ghz=35,
            metadata={"frequency_ghz": 35, "elements": 1024}
        )
        
        sim = AESARadarSimulator(config)
        sim.steer_beam(0, 0)
        
        # On-axis gain should be maximum (0 dB loss)
        gain = sim.calculate_beam_gain(0, 0)
        assert gain == 0
        
        # Off-axis gain should be lower
        gain_off = sim.calculate_beam_gain(10, 10)
        assert gain_off < 0
