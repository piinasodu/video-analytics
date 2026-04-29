"""
SQLAlchemy ORM models for video analytics
"""
from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import (
    Column, String, Integer, Float, DateTime, 
    Boolean, JSON, Index, ForeignKey, ARRAY, Text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Camera(Base):
    """Camera configuration and metadata"""
    __tablename__ = "cameras"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False, unique=True)
    source_url = Column(String(512), nullable=False)
    location = Column(String(255), nullable=True)
    enabled = Column(Boolean, default=True)
    fps = Column(Integer, default=30)
    resolution_width = Column(Integer, default=1920)
    resolution_height = Column(Integer, default=1080)
    
    # Detection zones (GeoJSON format)
    detection_zones = Column(JSON, nullable=True)
    intrusion_zones = Column(JSON, nullable=True)
    
    # Configuration
    brightness = Column(Integer, default=100)
    contrast = Column(Integer, default=100)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_heartbeat = Column(DateTime, nullable=True)
    
    # Relationships
    detections = relationship("Detection", back_populates="camera", cascade="all, delete-orphan")
    events = relationship("Event", back_populates="camera", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index("idx_camera_enabled_name", "enabled", "name"),
        Index("idx_camera_created_at", "created_at"),
    )


class Detection(Base):
    """Real-time object detections from YOLO"""
    __tablename__ = "detections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    camera_id = Column(UUID(as_uuid=True), ForeignKey("cameras.id"), nullable=False)
    
    # Detection details
    class_name = Column(String(100), nullable=False)  # person, car, bicycle, etc.
    confidence = Column(Float, nullable=False)
    
    # Bounding box (x, y, width, height)
    bbox_x = Column(Integer, nullable=False)
    bbox_y = Column(Integer, nullable=False)
    bbox_width = Column(Integer, nullable=False)
    bbox_height = Column(Integer, nullable=False)
    
    # Additional metadata
    tracking_id = Column(String(100), nullable=True)
    speed = Column(Float, nullable=True)
    direction = Column(String(50), nullable=True)
    
    # Inference details
    inference_time_ms = Column(Float, nullable=False)
    frame_number = Column(Integer, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    camera = relationship("Camera", back_populates="detections")
    
    __table_args__ = (
        Index("idx_detection_camera_created", "camera_id", "created_at"),
        Index("idx_detection_class_confidence", "class_name", "confidence"),
        Index("idx_detection_tracking_id", "tracking_id"),
    )


class Event(Base):
    """High-level events detected by analytics"""
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    camera_id = Column(UUID(as_uuid=True), ForeignKey("cameras.id"), nullable=False)
    
    # Event details
    event_type = Column(String(100), nullable=False)  # crowd, intrusion, loitering, etc.
    severity = Column(String(20), default="medium")  # low, medium, high, critical
    
    # Event data
    description = Column(Text, nullable=False)
    metadata = Column(JSON, nullable=True)
    
    # Snapshot
    snapshot_url = Column(String(512), nullable=True)
    annotated_frame_url = Column(String(512), nullable=True)
    
    # Confidence and statistics
    confidence = Column(Float, nullable=False)
    detection_count = Column(Integer, default=1)
    
    # Status
    status = Column(String(50), default="open")  # open, acknowledged, resolved
    acknowledged_at = Column(DateTime, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    camera = relationship("Camera", back_populates="events")
    alerts = relationship("Alert", back_populates="event", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index("idx_event_camera_created", "camera_id", "created_at"),
        Index("idx_event_type_severity", "event_type", "severity"),
        Index("idx_event_status", "status"),
    )


class Alert(Base):
    """Alert rules and alert instances"""
    __tablename__ = "alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=True)
    
    # Alert details
    rule_name = Column(String(255), nullable=False)
    alert_type = Column(String(100), nullable=False)
    
    # Trigger details
    triggered_by = Column(String(100), nullable=False)  # detection_class, event_type, etc.
    trigger_value = Column(String(255), nullable=True)
    
    # Status and acknowledgment
    status = Column(String(50), default="active")  # active, acknowledged, resolved
    acknowledged_by = Column(String(255), nullable=True)
    acknowledged_at = Column(DateTime, nullable=True)
    
    # Notification channels
    notification_channels = Column(ARRAY(String), default=["email"])  # email, sms, slack, webhook
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    event = relationship("Event", back_populates="alerts")
    
    __table_args__ = (
        Index("idx_alert_status_created", "status", "created_at"),
        Index("idx_alert_rule_name", "rule_name"),
    )


class EventLog(Base):
    """Audit log for all events"""
    __tablename__ = "event_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=False)
    
    # Log details
    action = Column(String(100), nullable=False)  # created, acknowledged, resolved
    performed_by = Column(String(255), nullable=False)
    details = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index("idx_event_log_event_id_created", "event_id", "created_at"),
    )
