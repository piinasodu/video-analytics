"""
Pydantic schemas for request/response validation
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field


# Camera Schemas
class CameraCreate(BaseModel):
    name: str
    source_url: str
    location: Optional[str] = None
    fps: int = 30
    resolution_width: int = 1920
    resolution_height: int = 1080


class CameraUpdate(BaseModel):
    name: Optional[str] = None
    enabled: Optional[bool] = None
    detection_zones: Optional[Dict[str, Any]] = None
    intrusion_zones: Optional[Dict[str, Any]] = None


class CameraSchema(BaseModel):
    id: UUID
    name: str
    location: Optional[str]
    enabled: bool
    fps: int
    resolution_width: int
    resolution_height: int
    last_heartbeat: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


# Detection Schemas
class DetectionCreate(BaseModel):
    camera_id: UUID
    class_name: str
    confidence: float
    bbox_x: int
    bbox_y: int
    bbox_width: int
    bbox_height: int
    inference_time_ms: float
    frame_number: int
    tracking_id: Optional[str] = None


class DetectionSchema(BaseModel):
    id: UUID
    camera_id: UUID
    class_name: str
    confidence: float
    bbox_x: int
    bbox_y: int
    bbox_width: int
    bbox_height: int
    tracking_id: Optional[str]
    inference_time_ms: float
    created_at: datetime
    
    class Config:
        from_attributes = True


# Event Schemas
class EventCreate(BaseModel):
    camera_id: UUID
    event_type: str
    severity: str = "medium"
    description: str
    confidence: float
    metadata: Optional[Dict[str, Any]] = None
    snapshot_url: Optional[str] = None


class EventUpdate(BaseModel):
    status: Optional[str] = None
    severity: Optional[str] = None
    description: Optional[str] = None


class EventSchema(BaseModel):
    id: UUID
    camera_id: UUID
    event_type: str
    severity: str
    description: str
    confidence: float
    detection_count: int
    status: str
    snapshot_url: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Alert Schemas
class AlertCreate(BaseModel):
    rule_name: str
    alert_type: str
    triggered_by: str
    trigger_value: Optional[str] = None
    notification_channels: List[str] = ["email"]


class AlertSchema(BaseModel):
    id: UUID
    rule_name: str
    alert_type: str
    status: str
    triggered_by: str
    notification_channels: List[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


# Statistics Schemas
class DetectionStats(BaseModel):
    total_detections: int
    detections_by_class: Dict[str, int]
    avg_confidence: float
    total_cameras: int


class EventStats(BaseModel):
    total_events: int
    events_by_type: Dict[str, int]
    events_by_severity: Dict[str, int]
    open_events: int
    avg_confidence: float


class AlertStats(BaseModel):
    total_alerts: int
    active_alerts: int
    acknowledged_alerts: int
    resolved_alerts: int


class SystemStats(BaseModel):
    total_cameras: int
    active_cameras: int
    uptime_seconds: int
    total_frames_processed: int
    avg_inference_time_ms: float
    total_detections: int
    detection_stats: DetectionStats
    event_stats: EventStats
    alert_stats: AlertStats


# Stream Response Schema
class StreamResponse(BaseModel):
    stream_id: str
    camera_id: UUID
    status: str
    frame_count: int
    current_fps: float
    uptime_seconds: int


# Health Check Schema
class HealthStatus(BaseModel):
    status: str
    components: Dict[str, str]
    timestamp: datetime
