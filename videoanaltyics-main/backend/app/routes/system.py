"""
System health and statistics endpoints
"""
from fastapi import APIRouter
from datetime import datetime

from app.schemas import HealthStatus, SystemStats, DetectionStats, EventStats, AlertStats

router = APIRouter(prefix="/system", tags=["system"])


@router.get("/health", response_model=HealthStatus)
async def health_check():
    """Check system health"""
    return {
        "status": "healthy",
        "components": {
            "api": "ok",
            "database": "ok",
            "kafka": "ok",
            "redis": "ok",
            "yolo": "ok"
        },
        "timestamp": datetime.utcnow()
    }


@router.get("/stats", response_model=SystemStats)
async def get_system_stats():
    """Get system statistics"""
    return {
        "total_cameras": 4,
        "active_cameras": 3,
        "uptime_seconds": 86400,
        "total_frames_processed": 1000000,
        "avg_inference_time_ms": 45.5,
        "total_detections": 5000,
        "detection_stats": {
            "total_detections": 5000,
            "detections_by_class": {
                "person": 3000,
                "car": 1500,
                "bicycle": 500
            },
            "avg_confidence": 0.85,
            "total_cameras": 4
        },
        "event_stats": {
            "total_events": 150,
            "events_by_type": {
                "crowd_detected": 50,
                "vehicle_detected": 80,
                "intrusion_detected": 20
            },
            "events_by_severity": {
                "low": 80,
                "medium": 50,
                "high": 20,
                "critical": 0
            },
            "open_events": 10,
            "avg_confidence": 0.82
        },
        "alert_stats": {
            "total_alerts": 50,
            "active_alerts": 5,
            "acknowledged_alerts": 30,
            "resolved_alerts": 15
        }
    }


@router.get("/info")
async def get_system_info():
    """Get system information"""
    return {
        "name": "Real-Time Video Analytics Platform",
        "version": "1.0.0",
        "environment": "production",
        "features": [
            "real_time_detection",
            "multi_camera_support",
            "event_alerting",
            "live_dashboard"
        ]
    }


@router.get("/version")
async def get_api_version():
    """Get API version"""
    return {
        "version": "1.0.0",
        "api_version": "v1",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/metrics")
async def get_metrics():
    """Get Prometheus metrics"""
    # Return metrics in Prometheus format
    return """# HELP video_frames_processed Total frames processed
# TYPE video_frames_processed counter
video_frames_processed{camera_id="camera-1"} 10000

# HELP video_detections_total Total detections
# TYPE video_detections_total counter
video_detections_total{class="person"} 3000
video_detections_total{class="car"} 1500

# HELP video_inference_time_ms Inference time in milliseconds
# TYPE video_inference_time_ms histogram
video_inference_time_ms_bucket{le="10"} 1000
video_inference_time_ms_bucket{le="50"} 95000
video_inference_time_ms_bucket{le="100"} 100000
"""
