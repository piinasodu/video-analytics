"""
Configuration settings for Video Analytics Platform
"""
import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application
    app_name: str = "Real-Time Video Analytics Platform"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = "production"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_prefix: str = "/api/v1"

    # Database
    database_url: str = "postgresql://videoadmin:videopass123@localhost:5432/videodb"
    db_echo: bool = False
    db_pool_size: int = 20

    # Redis
    redis_url: str = "redis://localhost:6379"
    redis_cache_ttl: int = 3600

    # Kafka
    kafka_brokers: str = "localhost:9092"
    kafka_topic_detections: str = "video_detections"
    kafka_topic_events: str = "video_events"
    kafka_topic_alerts: str = "video_alerts"
    kafka_consumer_group: str = "video_analytics"
    kafka_batch_size: int = 100

    # YOLOv8 Configuration
    yolo_model_size: str = "m"  # nano, small, medium, large, xlarge
    yolo_confidence_threshold: float = 0.5
    yolo_device: str = "cpu"  # cpu, cuda:0, etc.
    yolo_inference_timeout: int = 5

    # Video Processing
    video_input_source: str = "rtsp"  # rtsp, http, file
    video_frame_skip: int = 2
    video_buffer_size: int = 30
    video_max_width: int = 1280
    video_max_height: int = 720
    video_output_fps: int = 15

    # Alerting
    alert_enabled: bool = True
    alert_cooldown_seconds: int = 30
    alert_confidence_threshold: float = 0.6

    # Detection Zones
    enable_intrusion_detection: bool = True
    enable_crowd_detection: bool = True
    crowd_threshold: int = 10

    # Privacy
    enable_face_blur: bool = True
    blur_strength: int = 50

    # Logging
    log_level: str = "INFO"

    # Monitoring
    enable_metrics: bool = True
    metrics_port: int = 9090

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
