"""
Tests for tracker
"""
import pytest
from datetime import datetime, timedelta

from radix.models.schemas import NormalizedRadarData, TrackState
from radix.core.tracker import SimpleTracker


class TestSimpleTracker:
    """Test SimpleTracker"""
    
    def test_tracker_creation(self):
        tracker = SimpleTracker()
        assert tracker is not None
        assert len(tracker.tracks) == 0
        assert tracker.next_track_id == 1
    
    def test_track_creation(self):
        tracker = SimpleTracker()
        
        detection = NormalizedRadarData(
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
        
        tracks = tracker.update([detection])
        
        assert len(tracker.tracks) == 1
        assert len(tracks) == 1
        assert tracks[0].track_state == TrackState.TENTATIVE
    
    def test_track_confirmation(self):
        tracker = SimpleTracker()
        
        # Create multiple detections for same target
        base_time = datetime.utcnow()
        detections = []
        
        for i in range(5):
            det = NormalizedRadarData(
                timestamp=base_time + timedelta(seconds=i * 0.1),
                sensor_id="RADAR_A",
                target_id=1,
                range_m=1000.0 + i * 10,
                azimuth_deg=45.0,
                doppler_mps=-10.0,
                snr_db=20.0,
                position_enu=[707.0 + i * 1, 707.0 + i * 1, 100.0],
                velocity_enu=[-7.0, -7.0, 0.0]
            )
            detections.append(det)
        
        # Update tracker with detections one by one
        for det in detections:
            tracks = tracker.update([det])
        
        # Track should be confirmed after 3+ detections
        assert len(tracks) > 0
        assert tracks[0].track_state == TrackState.CONFIRMED
        assert len(tracks[0].detections) >= 3
    
    def test_multiple_tracks(self):
        tracker = SimpleTracker()
        
        # Create detections for two separate targets
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
            ),
            NormalizedRadarData(
                timestamp=datetime.utcnow(),
                sensor_id="RADAR_A",
                target_id=2,
                range_m=2000.0,
                azimuth_deg=90.0,
                doppler_mps=15.0,
                snr_db=18.0,
                position_enu=[2000.0, 0.0, 150.0],
                velocity_enu=[15.0, 0.0, 0.0]
            )
        ]
        
        tracks = tracker.update(detections)
        
        assert len(tracks) == 2
    
    def test_track_coasting(self):
        tracker = SimpleTracker(max_coast_time=1.0)
        
        # Create initial detection
        detection = NormalizedRadarData(
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
        
        # Create track
        tracker.update([detection])
        
        # Update without detections (should coast)
        tracks = tracker.update([])
        
        # Track should still exist but coasting
        assert len(tracks) > 0
    
    def test_get_active_tracks(self):
        tracker = SimpleTracker()
        
        # Create confirmed track
        for i in range(5):
            det = NormalizedRadarData(
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
            tracker.update([det])
        
        active_tracks = tracker.get_active_tracks()
        assert len(active_tracks) > 0
    
    def test_track_by_id(self):
        tracker = SimpleTracker()
        
        detection = NormalizedRadarData(
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
        
        tracker.update([detection])
        
        track = tracker.get_track_by_id(1)
        assert track is not None
        assert track.track_id == 1
        
        # Non-existent track
        track = tracker.get_track_by_id(999)
        assert track is None
