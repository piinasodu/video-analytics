"""
Services module initialization
"""
from app.services.yolo_service import get_yolo_service
from app.services.kafka_service import get_kafka_service
from app.services.event_service import get_event_detection_service
from app.services.alert_service import get_alert_service

__all__ = [
    "get_yolo_service",
    "get_kafka_service",
    "get_event_detection_service",
    "get_alert_service",
]
