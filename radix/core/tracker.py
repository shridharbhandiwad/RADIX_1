"""
Multi-target tracking and data association
"""
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from ..models.schemas import NormalizedRadarData, TargetTrack, TrackState


class SimpleTracker:
    """
    Simple nearest-neighbor tracker for demonstration
    In production, use Kalman filters, JPDA, or MHT
    """
    
    def __init__(self, max_association_distance: float = 100.0, max_coast_time: float = 5.0):
        self.tracks: Dict[int, TargetTrack] = {}
        self.next_track_id = 1
        self.max_association_distance = max_association_distance
        self.max_coast_time = max_coast_time
    
    def update(self, detections: List[NormalizedRadarData]) -> List[TargetTrack]:
        """Update tracks with new detections"""
        current_time = detections[0].timestamp if detections else datetime.utcnow()
        
        # Match detections to existing tracks
        unassociated_detections = list(detections)
        updated_tracks = set()
        
        for track_id, track in list(self.tracks.items()):
            best_detection = None
            best_distance = self.max_association_distance
            
            for detection in unassociated_detections:
                if detection.position_enu and track.state_vector:
                    # Calculate distance
                    det_pos = np.array(detection.position_enu[:3])
                    track_pos = np.array(track.state_vector[:3])
                    distance = np.linalg.norm(det_pos - track_pos)
                    
                    if distance < best_distance:
                        best_distance = distance
                        best_detection = detection
            
            if best_detection:
                # Update track
                self._update_track(track, best_detection, current_time)
                unassociated_detections.remove(best_detection)
                updated_tracks.add(track_id)
            else:
                # Coast track
                time_since_update = (current_time - track.last_updated).total_seconds()
                if time_since_update < self.max_coast_time:
                    track.track_state = TrackState.COASTING
                else:
                    track.track_state = TrackState.LOST
        
        # Create new tracks for unassociated detections
        for detection in unassociated_detections:
            if detection.position_enu and detection.velocity_enu:
                self._create_track(detection, current_time)
        
        # Remove lost tracks
        self.tracks = {
            tid: track for tid, track in self.tracks.items()
            if track.track_state != TrackState.LOST
        }
        
        return list(self.tracks.values())
    
    def _create_track(self, detection: NormalizedRadarData, current_time: datetime):
        """Create new track from detection"""
        state_vector = detection.position_enu + detection.velocity_enu
        
        track = TargetTrack(
            track_id=self.next_track_id,
            sensor_id=detection.sensor_id,
            first_seen=current_time,
            last_updated=current_time,
            state_vector=state_vector,
            track_state=TrackState.TENTATIVE,
            detections=[detection]
        )
        
        self.tracks[self.next_track_id] = track
        self.next_track_id += 1
    
    def _update_track(self, track: TargetTrack, detection: NormalizedRadarData, current_time: datetime):
        """Update existing track with new detection"""
        # Simple update (in production, use Kalman filter)
        if detection.position_enu and detection.velocity_enu:
            track.state_vector = detection.position_enu + detection.velocity_enu
        
        track.last_updated = current_time
        track.detections.append(detection)
        
        # Update track state based on number of detections
        if len(track.detections) >= 3:
            track.track_state = TrackState.CONFIRMED
        else:
            track.track_state = TrackState.TENTATIVE
        
        # Keep only recent detections
        if len(track.detections) > 50:
            track.detections = track.detections[-50:]
    
    def get_active_tracks(self) -> List[TargetTrack]:
        """Get all active (confirmed or coasting) tracks"""
        return [
            track for track in self.tracks.values()
            if track.track_state in [TrackState.CONFIRMED, TrackState.COASTING]
        ]
    
    def get_track_by_id(self, track_id: int) -> Optional[TargetTrack]:
        """Get specific track by ID"""
        return self.tracks.get(track_id)
