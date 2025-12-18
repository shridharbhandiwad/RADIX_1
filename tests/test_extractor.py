"""
Tests for data extractor
"""
import pytest
import pandas as pd
from datetime import datetime

from radix.models.schemas import NormalizedRadarData, TargetTrack, TrackState
from radix.core.extractor import DataExtractor


class TestDataExtractor:
    """Test DataExtractor"""
    
    def test_extractor_creation(self):
        extractor = DataExtractor()
        assert extractor is not None
        assert len(extractor.datasets) == 0
    
    def test_tabular_extraction(self):
        extractor = DataExtractor()
        
        detections = [
            NormalizedRadarData(
                timestamp=datetime.utcnow(),
                sensor_id="RADAR_A",
                target_id=i,
                range_m=1000.0 + i * 100,
                azimuth_deg=45.0,
                doppler_mps=-10.0,
                snr_db=20.0,
                position_enu=[707.0, 707.0, 100.0],
                velocity_enu=[-7.0, -7.0, 0.0]
            )
            for i in range(10)
        ]
        
        df = extractor.extract_tabular_dataset(detections)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 10
        assert 'range_m' in df.columns
        assert 'azimuth_deg' in df.columns
        assert 'snr_db' in df.columns
    
    def test_sequence_extraction(self):
        extractor = DataExtractor()
        
        # Create track with detections
        detections = [
            NormalizedRadarData(
                timestamp=datetime.utcnow(),
                sensor_id="RADAR_A",
                target_id=1,
                range_m=1000.0 + i * 10,
                azimuth_deg=45.0,
                doppler_mps=-10.0,
                snr_db=20.0,
                position_enu=[707.0 + i, 707.0 + i, 100.0],
                velocity_enu=[-7.0, -7.0, 0.0]
            )
            for i in range(20)
        ]
        
        track = TargetTrack(
            track_id=1,
            sensor_id="RADAR_A",
            first_seen=datetime.utcnow(),
            last_updated=datetime.utcnow(),
            state_vector=[707.0, 707.0, 100.0, -7.0, -7.0, 0.0],
            track_state=TrackState.CONFIRMED,
            detections=detections
        )
        
        df = extractor.extract_sequence_dataset([track], window_size=10)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert 'track_id' in df.columns
        assert 'x' in df.columns
        assert 'vx' in df.columns
    
    def test_graph_extraction(self):
        extractor = DataExtractor()
        
        # Create multiple tracks
        tracks = [
            TargetTrack(
                track_id=i,
                sensor_id="RADAR_A",
                first_seen=datetime.utcnow(),
                last_updated=datetime.utcnow(),
                state_vector=[i * 100, i * 100, 100.0, -7.0, -7.0, 0.0],
                track_state=TrackState.CONFIRMED,
                detections=[]
            )
            for i in range(5)
        ]
        
        graph_data = extractor.extract_graph_dataset(tracks)
        
        assert 'nodes' in graph_data
        assert 'adjacency' in graph_data
        assert 'edge_index' in graph_data
        assert isinstance(graph_data['nodes'], pd.DataFrame)
        assert len(graph_data['nodes']) == 5
    
    def test_time_series_features(self):
        extractor = DataExtractor()
        
        detections = [
            NormalizedRadarData(
                timestamp=datetime.utcnow(),
                sensor_id="RADAR_A",
                target_id=1,
                range_m=1000.0 + i * 10,
                azimuth_deg=45.0,
                doppler_mps=-10.0,
                snr_db=20.0,
                position_enu=[707.0 + i, 707.0 + i, 100.0],
                velocity_enu=[-7.0, -7.0, 0.0]
            )
            for i in range(10)
        ]
        
        track = TargetTrack(
            track_id=1,
            sensor_id="RADAR_A",
            first_seen=datetime.utcnow(),
            last_updated=datetime.utcnow(),
            state_vector=[707.0, 707.0, 100.0, -7.0, -7.0, 0.0],
            track_state=TrackState.CONFIRMED,
            detections=detections
        )
        
        features = extractor.extract_time_series_features(track)
        
        assert len(features) > 0
        assert 'pos_mean_x' in features
        assert 'vel_mean' in features
        assert 'track_length' in features
    
    def test_ml_dataset_creation(self):
        extractor = DataExtractor()
        
        detections = [
            NormalizedRadarData(
                timestamp=datetime.utcnow(),
                sensor_id="RADAR_A",
                target_id=1,
                range_m=1000.0,
                azimuth_deg=45.0,
                doppler_mps=-10.0,
                snr_db=20.0,
                position_enu=[707.0, 707.0, 100.0],
                velocity_enu=[-7.0, -7.0, 0.0]
            )
        ]
        
        dataset = extractor.create_ml_dataset(
            name="Test Dataset",
            description="Test description",
            detections=detections,
            tracks=[],
            format="tabular"
        )
        
        assert dataset is not None
        assert dataset.name == "Test Dataset"
        assert dataset.num_samples == 1
        assert dataset.format == "tabular"
        assert dataset.dataset_id in extractor.datasets
