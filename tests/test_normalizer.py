"""
Tests for data normalizer
"""
import pytest
from datetime import datetime

from radix.models.schemas import RawRadarDetection, RadarType
from radix.core.normalizer import DataNormalizer


class TestDataNormalizer:
    """Test DataNormalizer"""
    
    def test_normalizer_creation(self):
        normalizer = DataNormalizer()
        assert normalizer is not None
        assert len(normalizer.normalizers) > 0
    
    def test_fmcw_normalization(self):
        normalizer = DataNormalizer()
        
        raw = RawRadarDetection(
            timestamp=datetime.utcnow(),
            sensor_id="RADAR_A",
            raw_data={
                "target_id": 1,
                "range_m": 1000.0,
                "azimuth_deg": 45.0,
                "elevation_deg": 10.0,
                "doppler_mps": -15.0,
                "snr_db": 20.0,
                "rcs_dbsm": 10.0,
                "is_false_alarm": False
            },
            format_type="FMCW"
        )
        
        normalized = normalizer.normalize(raw)
        
        assert normalized is not None
        assert normalized.sensor_id == "RADAR_A"
        assert normalized.target_id == 1
        assert normalized.range_m == 1000.0
        assert normalized.azimuth_deg == 45.0
        assert normalized.elevation_deg == 10.0
        assert normalized.doppler_mps == -15.0
        assert normalized.snr_db == 20.0
        assert normalized.position_enu is not None
        assert len(normalized.position_enu) == 3
        assert normalized.velocity_enu is not None
        assert len(normalized.velocity_enu) == 3
    
    def test_pulse_doppler_normalization(self):
        normalizer = DataNormalizer()
        
        raw = RawRadarDetection(
            timestamp=datetime.utcnow(),
            sensor_id="RADAR_B",
            raw_data={
                "target_id": 2,
                "range_m": 5000.0,
                "azimuth_deg": 180.0,
                "elevation_deg": 5.0,
                "doppler_mps": 25.0,
                "doppler_freq_hz": 1000.0,
                "snr_db": 15.0,
                "rcs_dbsm": 15.0,
                "prf_hz": 10000,
                "is_false_alarm": False
            },
            format_type="PULSE_DOPPLER"
        )
        
        normalized = normalizer.normalize(raw)
        
        assert normalized is not None
        assert normalized.sensor_id == "RADAR_B"
        assert normalized.target_id == 2
        assert normalized.metadata.get("doppler_freq_hz") == 1000.0
        assert normalized.metadata.get("prf_hz") == 10000
    
    def test_aesa_normalization(self):
        normalizer = DataNormalizer()
        
        raw = RawRadarDetection(
            timestamp=datetime.utcnow(),
            sensor_id="RADAR_C",
            raw_data={
                "target_id": 3,
                "range_m": 8000.0,
                "azimuth_deg": 270.0,
                "elevation_deg": 15.0,
                "doppler_mps": -30.0,
                "snr_db": 25.0,
                "rcs_dbsm": 20.0,
                "beam_azimuth_deg": 265.0,
                "beam_elevation_deg": 12.0,
                "beam_gain_db": -2.0,
                "num_elements": 1024,
                "is_false_alarm": False
            },
            format_type="AESA"
        )
        
        normalized = normalizer.normalize(raw)
        
        assert normalized is not None
        assert normalized.sensor_id == "RADAR_C"
        assert normalized.target_id == 3
        assert normalized.metadata.get("beam_azimuth_deg") == 265.0
        assert normalized.metadata.get("num_elements") == 1024
    
    def test_batch_normalization(self):
        normalizer = DataNormalizer()
        
        raw_detections = [
            RawRadarDetection(
                timestamp=datetime.utcnow(),
                sensor_id=f"RADAR_{i}",
                raw_data={
                    "target_id": i,
                    "range_m": 1000.0 + i * 100,
                    "azimuth_deg": 45.0 * i,
                    "elevation_deg": 10.0,
                    "doppler_mps": -15.0,
                    "snr_db": 20.0,
                    "is_false_alarm": False
                },
                format_type="FMCW"
            )
            for i in range(5)
        ]
        
        normalized = normalizer.batch_normalize(raw_detections)
        
        assert len(normalized) == 5
        for i, det in enumerate(normalized):
            assert det.target_id == i
            assert det.range_m == 1000.0 + i * 100
    
    def test_invalid_detection(self):
        normalizer = DataNormalizer()
        
        # Missing required fields
        raw = RawRadarDetection(
            timestamp=datetime.utcnow(),
            sensor_id="RADAR_X",
            raw_data={},
            format_type="UNKNOWN"
        )
        
        # Should use generic normalization
        normalized = normalizer.normalize(raw)
        assert normalized is not None
        assert normalized.sensor_id == "RADAR_X"
