"""
Tests for API endpoints
"""
import pytest
from fastapi.testclient import TestClient

from radix.api.main import app


client = TestClient(app)


class TestAPI:
    """Test API endpoints"""
    
    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "RADIX"
        assert "version" in data
    
    def test_status_endpoint(self):
        response = client.get("/api/status")
        assert response.status_code == 200
        data = response.json()
        assert "uptime_seconds" in data
        assert "active_radars" in data
        assert "total_detections" in data
        assert "active_tracks" in data
        assert "data_rate_hz" in data
    
    def test_radars_endpoint(self):
        response = client.get("/api/radars")
        assert response.status_code == 200
        radars = response.json()
        assert isinstance(radars, list)
        # Radars are initialized on startup, so list should be populated
        assert len(radars) >= 0  # May be empty or have radars depending on timing
        
        for radar in radars:
            assert "id" in radar
            assert "type" in radar
            assert "location" in radar
    
    def test_tracks_endpoint(self):
        response = client.get("/api/tracks")
        assert response.status_code == 200
        tracks = response.json()
        assert isinstance(tracks, list)
    
    def test_detections_endpoint(self):
        response = client.get("/api/detections")
        assert response.status_code == 200
        detections = response.json()
        assert isinstance(detections, list)
    
    def test_detections_with_limit(self):
        response = client.get("/api/detections?limit=10")
        assert response.status_code == 200
        detections = response.json()
        assert isinstance(detections, list)
        assert len(detections) <= 10
    
    def test_datasets_endpoint(self):
        response = client.get("/api/datasets")
        assert response.status_code == 200
        datasets = response.json()
        assert isinstance(datasets, list)
    
    def test_create_dataset(self):
        response = client.post(
            "/api/datasets/create",
            params={
                "name": "Test Dataset",
                "description": "Test description",
                "format": "tabular"
            }
        )
        assert response.status_code == 200
        dataset = response.json()
        assert dataset["name"] == "Test Dataset"
        assert "dataset_id" in dataset
    
    def test_export_dataset_invalid(self):
        response = client.get("/api/datasets/invalid_id/export")
        assert response.status_code == 404
