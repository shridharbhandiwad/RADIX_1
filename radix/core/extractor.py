"""
ML-ready dataset extraction
"""
import numpy as np
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any, Optional
from ..models.schemas import NormalizedRadarData, TargetTrack, MLDataset


class DataExtractor:
    """Extracts ML-ready datasets from normalized radar data"""
    
    def __init__(self):
        self.datasets: Dict[str, MLDataset] = {}
    
    def extract_sequence_dataset(
        self,
        tracks: List[TargetTrack],
        window_size: int = 10,
        stride: int = 1
    ) -> pd.DataFrame:
        """
        Extract sequence dataset for LSTM/Transformer models
        Format: [track_id, timestamp, x, y, z, vx, vy, vz, features...]
        """
        sequences = []
        
        for track in tracks:
            if len(track.detections) < window_size:
                continue
            
            for i in range(0, len(track.detections) - window_size + 1, stride):
                window = track.detections[i:i + window_size]
                
                for det in window:
                    if det.position_enu and det.velocity_enu:
                        sequences.append({
                            'track_id': track.track_id,
                            'sensor_id': det.sensor_id,
                            'timestamp': det.timestamp,
                            'x': det.position_enu[0],
                            'y': det.position_enu[1],
                            'z': det.position_enu[2],
                            'vx': det.velocity_enu[0],
                            'vy': det.velocity_enu[1],
                            'vz': det.velocity_enu[2],
                            'range_m': det.range_m,
                            'azimuth_deg': det.azimuth_deg,
                            'elevation_deg': det.elevation_deg or 0,
                            'doppler_mps': det.doppler_mps,
                            'snr_db': det.snr_db,
                            'rcs_dbsm': det.rcs_dbsm or 0,
                            'track_state': track.track_state.value
                        })
        
        return pd.DataFrame(sequences)
    
    def extract_tabular_dataset(
        self,
        detections: List[NormalizedRadarData]
    ) -> pd.DataFrame:
        """
        Extract tabular dataset for classical ML models
        Format: One row per detection with all features
        """
        rows = []
        
        for det in detections:
            row = {
                'timestamp': det.timestamp,
                'sensor_id': det.sensor_id,
                'target_id': det.target_id or -1,
                'range_m': det.range_m,
                'azimuth_deg': det.azimuth_deg,
                'elevation_deg': det.elevation_deg or 0,
                'doppler_mps': det.doppler_mps,
                'snr_db': det.snr_db,
                'rcs_dbsm': det.rcs_dbsm or 0,
            }
            
            if det.position_enu:
                row['x'] = det.position_enu[0]
                row['y'] = det.position_enu[1]
                row['z'] = det.position_enu[2]
            
            if det.velocity_enu:
                row['vx'] = det.velocity_enu[0]
                row['vy'] = det.velocity_enu[1]
                row['vz'] = det.velocity_enu[2]
            
            rows.append(row)
        
        return pd.DataFrame(rows)
    
    def extract_graph_dataset(
        self,
        tracks: List[TargetTrack],
        time_window: float = 1.0
    ) -> Dict[str, Any]:
        """
        Extract graph dataset for GNN models
        Format: Nodes (tracks) and edges (spatial relationships)
        """
        # Build adjacency matrix based on spatial proximity
        n_tracks = len(tracks)
        adjacency = np.zeros((n_tracks, n_tracks))
        node_features = []
        
        for i, track_i in enumerate(tracks):
            if track_i.state_vector:
                pos_i = np.array(track_i.state_vector[:3])
                
                # Node features
                node_features.append({
                    'track_id': track_i.track_id,
                    'x': track_i.state_vector[0],
                    'y': track_i.state_vector[1],
                    'z': track_i.state_vector[2],
                    'vx': track_i.state_vector[3],
                    'vy': track_i.state_vector[4],
                    'vz': track_i.state_vector[5],
                    'num_detections': len(track_i.detections),
                    'track_state': track_i.track_state.value
                })
                
                # Edges based on proximity
                for j, track_j in enumerate(tracks):
                    if i != j and track_j.state_vector:
                        pos_j = np.array(track_j.state_vector[:3])
                        distance = np.linalg.norm(pos_i - pos_j)
                        
                        # Connect if within 1km
                        if distance < 1000:
                            adjacency[i, j] = 1.0 / (distance + 1)  # Weight by inverse distance
        
        return {
            'nodes': pd.DataFrame(node_features),
            'adjacency': adjacency,
            'edge_index': np.array(np.where(adjacency > 0))
        }
    
    def extract_time_series_features(
        self,
        track: TargetTrack
    ) -> Dict[str, float]:
        """Extract statistical features from track time series"""
        if len(track.detections) < 2:
            return {}
        
        # Extract position and velocity time series
        positions = np.array([d.position_enu for d in track.detections if d.position_enu])
        velocities = np.array([d.velocity_enu for d in track.detections if d.velocity_enu])
        
        if len(positions) == 0:
            return {}
        
        features = {
            # Position statistics
            'pos_mean_x': np.mean(positions[:, 0]),
            'pos_mean_y': np.mean(positions[:, 1]),
            'pos_mean_z': np.mean(positions[:, 2]),
            'pos_std_x': np.std(positions[:, 0]),
            'pos_std_y': np.std(positions[:, 1]),
            'pos_std_z': np.std(positions[:, 2]),
            
            # Velocity statistics
            'vel_mean': np.mean(np.linalg.norm(velocities, axis=1)) if len(velocities) > 0 else 0,
            'vel_std': np.std(np.linalg.norm(velocities, axis=1)) if len(velocities) > 0 else 0,
            
            # Track characteristics
            'track_length': len(track.detections),
            'track_duration': (track.last_updated - track.first_seen).total_seconds(),
        }
        
        return features
    
    def create_ml_dataset(
        self,
        name: str,
        description: str,
        detections: List[NormalizedRadarData],
        tracks: List[TargetTrack],
        format: str = "tabular"
    ) -> MLDataset:
        """Create and register an ML dataset"""
        sensor_ids = list(set(d.sensor_id for d in detections))
        timestamps = [d.timestamp for d in detections]
        
        dataset = MLDataset(
            dataset_id=f"dataset_{len(self.datasets)}",
            name=name,
            description=description,
            created_at=datetime.utcnow(),
            sensor_ids=sensor_ids,
            start_time=min(timestamps) if timestamps else datetime.utcnow(),
            end_time=max(timestamps) if timestamps else datetime.utcnow(),
            num_samples=len(detections),
            format=format,
            metadata={
                'num_tracks': len(tracks),
                'num_sensors': len(sensor_ids)
            }
        )
        
        self.datasets[dataset.dataset_id] = dataset
        return dataset
