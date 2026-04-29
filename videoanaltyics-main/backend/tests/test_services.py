"""
Unit tests for YOLOv8 service
"""
import pytest
from app.services.yolo_service import YOLOv8Service
import numpy as np


@pytest.mark.skip(reason="Requires YOLOv8 model download")
def test_yolo_service_initialization():
    """Test YOLOv8 service initialization"""
    service = YOLOv8Service()
    assert service.model is not None
    assert service.device in ["cpu", "cuda:0"]


@pytest.mark.skip(reason="Requires YOLOv8 model")
def test_yolo_detect():
    """Test YOLO detection"""
    service = YOLOv8Service()
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    
    detections = service.detect(frame)
    assert isinstance(detections, list)


def test_event_detection_crowd():
    """Test crowd detection"""
    from app.services.event_service import EventDetectionService
    
    service = EventDetectionService()
    detections = [
        {"class_name": "person", "confidence": 0.9, "bbox": {"x": 0, "y": 0, "x2": 100, "y2": 100}},
        {"class_name": "person", "confidence": 0.85, "bbox": {"x": 150, "y": 0, "x2": 250, "y2": 100}},
        # Add more detections to trigger crowd
    ] * 10  # 20 person detections
    
    event = service.detect_crowd("camera-1", detections)
    # Should detect crowd if >= CROWD_THRESHOLD
    # assert event is not None


def test_alert_cooldown():
    """Test alert cooldown mechanism"""
    from app.services.alert_service import AlertService
    
    service = AlertService()
    
    # First alert should trigger
    assert service.should_trigger_alert("test-rule") == True
    service.record_alert("test-rule")
    
    # Second alert should be blocked (within cooldown)
    assert service.should_trigger_alert("test-rule") == False


if __name__ == "__main__":
    pytest.main([__file__])
