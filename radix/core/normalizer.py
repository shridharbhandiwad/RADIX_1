"""
Data normalization engine - converts heterogeneous radar data to unified schema
"""
import numpy as np
from datetime import datetime
from typing import List, Optional
from ..models.schemas import RawRadarDetection, NormalizedRadarData, RadarType, TrackState


class DataNormalizer:
    """Normalizes radar-specific data to unified RADIX schema"""
    
    def __init__(self):
        self.normalizers = {
            RadarType.FMCW: self._normalize_fmcw,
            RadarType.PULSE_DOPPLER: self._normalize_pulse_doppler,
            RadarType.AESA: self._normalize_aesa,
        }
    
    def normalize(self, raw_detection: RawRadarDetection) -> Optional[NormalizedRadarData]:
        """Normalize raw detection to unified format"""
        try:
            radar_type = RadarType(raw_detection.format_type)
            normalizer = self.normalizers.get(radar_type)
            
            if normalizer:
                return normalizer(raw_detection)
            else:
                return self._generic_normalize(raw_detection)
                
        except ValueError:
            # Unknown radar type, use generic normalization
            return self._generic_normalize(raw_detection)
        except Exception as e:
            print(f"Normalization error: {e}")
            return None
    
    def _normalize_fmcw(self, raw: RawRadarDetection) -> NormalizedRadarData:
        """Normalize FMCW radar data"""
        data = raw.raw_data
        
        # Convert to ENU coordinates
        range_m = data["range_m"]
        azimuth_rad = np.radians(data["azimuth_deg"])
        elevation_rad = np.radians(data["elevation_deg"])
        
        # Spherical to Cartesian (ENU)
        x = range_m * np.cos(elevation_rad) * np.sin(azimuth_rad)
        y = range_m * np.cos(elevation_rad) * np.cos(azimuth_rad)
        z = range_m * np.sin(elevation_rad)
        
        # Velocity vector (radial velocity only, approximate)
        doppler = data["doppler_mps"]
        vx = doppler * np.cos(elevation_rad) * np.sin(azimuth_rad)
        vy = doppler * np.cos(elevation_rad) * np.cos(azimuth_rad)
        vz = doppler * np.sin(elevation_rad)
        
        return NormalizedRadarData(
            timestamp=raw.timestamp,
            sensor_id=raw.sensor_id,
            target_id=data.get("target_id"),
            range_m=data["range_m"],
            azimuth_deg=data["azimuth_deg"],
            elevation_deg=data["elevation_deg"],
            doppler_mps=data["doppler_mps"],
            snr_db=data["snr_db"],
            rcs_dbsm=data.get("rcs_dbsm"),
            track_state=TrackState.TENTATIVE if not data.get("is_false_alarm") else None,
            position_enu=[float(x), float(y), float(z)],
            velocity_enu=[float(vx), float(vy), float(vz)],
            metadata={
                "beat_frequency_khz": data.get("beat_frequency_khz"),
                "range_resolution_m": data.get("range_resolution_m"),
                "radar_type": "FMCW"
            }
        )
    
    def _normalize_pulse_doppler(self, raw: RawRadarDetection) -> NormalizedRadarData:
        """Normalize Pulse-Doppler radar data"""
        data = raw.raw_data
        
        # Convert to ENU coordinates
        range_m = data["range_m"]
        azimuth_rad = np.radians(data["azimuth_deg"])
        elevation_rad = np.radians(data["elevation_deg"])
        
        x = range_m * np.cos(elevation_rad) * np.sin(azimuth_rad)
        y = range_m * np.cos(elevation_rad) * np.cos(azimuth_rad)
        z = range_m * np.sin(elevation_rad)
        
        doppler = data["doppler_mps"]
        vx = doppler * np.cos(elevation_rad) * np.sin(azimuth_rad)
        vy = doppler * np.cos(elevation_rad) * np.cos(azimuth_rad)
        vz = doppler * np.sin(elevation_rad)
        
        return NormalizedRadarData(
            timestamp=raw.timestamp,
            sensor_id=raw.sensor_id,
            target_id=data.get("target_id"),
            range_m=data["range_m"],
            azimuth_deg=data["azimuth_deg"],
            elevation_deg=data["elevation_deg"],
            doppler_mps=data["doppler_mps"],
            snr_db=data["snr_db"],
            rcs_dbsm=data.get("rcs_dbsm"),
            track_state=TrackState.TENTATIVE if not data.get("is_false_alarm") else None,
            position_enu=[float(x), float(y), float(z)],
            velocity_enu=[float(vx), float(vy), float(vz)],
            metadata={
                "doppler_freq_hz": data.get("doppler_freq_hz"),
                "prf_hz": data.get("prf_hz"),
                "velocity_folded": data.get("velocity_folded"),
                "range_ambiguity": data.get("range_ambiguity"),
                "radar_type": "PULSE_DOPPLER"
            }
        )
    
    def _normalize_aesa(self, raw: RawRadarDetection) -> NormalizedRadarData:
        """Normalize AESA radar data"""
        data = raw.raw_data
        
        # Convert to ENU coordinates
        range_m = data["range_m"]
        azimuth_rad = np.radians(data["azimuth_deg"])
        elevation_rad = np.radians(data["elevation_deg"])
        
        x = range_m * np.cos(elevation_rad) * np.sin(azimuth_rad)
        y = range_m * np.cos(elevation_rad) * np.cos(azimuth_rad)
        z = range_m * np.sin(elevation_rad)
        
        doppler = data["doppler_mps"]
        vx = doppler * np.cos(elevation_rad) * np.sin(azimuth_rad)
        vy = doppler * np.cos(elevation_rad) * np.cos(azimuth_rad)
        vz = doppler * np.sin(elevation_rad)
        
        return NormalizedRadarData(
            timestamp=raw.timestamp,
            sensor_id=raw.sensor_id,
            target_id=data.get("target_id"),
            range_m=data["range_m"],
            azimuth_deg=data["azimuth_deg"],
            elevation_deg=data["elevation_deg"],
            doppler_mps=data["doppler_mps"],
            snr_db=data["snr_db"],
            rcs_dbsm=data.get("rcs_dbsm"),
            track_state=TrackState.CONFIRMED if data["snr_db"] > 15 else TrackState.TENTATIVE,
            position_enu=[float(x), float(y), float(z)],
            velocity_enu=[float(vx), float(vy), float(vz)],
            metadata={
                "beam_azimuth_deg": data.get("beam_azimuth_deg"),
                "beam_elevation_deg": data.get("beam_elevation_deg"),
                "beam_gain_db": data.get("beam_gain_db"),
                "num_elements": data.get("num_elements"),
                "angle_accuracy_deg": data.get("angle_accuracy_deg"),
                "radar_type": "AESA"
            }
        )
    
    def _generic_normalize(self, raw: RawRadarDetection) -> NormalizedRadarData:
        """Generic normalization for unknown radar types"""
        data = raw.raw_data
        
        return NormalizedRadarData(
            timestamp=raw.timestamp,
            sensor_id=raw.sensor_id,
            target_id=data.get("target_id"),
            range_m=data.get("range_m", 0),
            azimuth_deg=data.get("azimuth_deg", 0),
            elevation_deg=data.get("elevation_deg", 0),
            doppler_mps=data.get("doppler_mps", 0),
            snr_db=data.get("snr_db", 0),
            rcs_dbsm=data.get("rcs_dbsm"),
            metadata={"radar_type": "UNKNOWN"}
        )
    
    def batch_normalize(self, raw_detections: List[RawRadarDetection]) -> List[NormalizedRadarData]:
        """Normalize a batch of detections"""
        normalized = []
        for raw in raw_detections:
            result = self.normalize(raw)
            if result:
                normalized.append(result)
        return normalized
