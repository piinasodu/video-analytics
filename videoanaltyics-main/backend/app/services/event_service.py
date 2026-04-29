"""
Event detection and analysis service
"""
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from app.config import settings
from app.schemas import EventCreate

logger = logging.getLogger(__name__)


class EventDetectionService:
    """Detects high-level events from raw detections"""
    
    def __init__(self):
        self.frame_history = {}
        self.crowd_threshold = settings.crowd_threshold
        self.enable_crowd_detection = settings.enable_crowd_detection
        self.enable_intrusion_detection = settings.enable_intrusion_detection
    
    def detect_crowd(
        self,
        camera_id: str,
        detections: List[Dict[str, Any]]
    ) -> Optional[EventCreate]:
        """
        Detect crowd events based on detection count
        
        Args:
            camera_id: Camera identifier
            detections: List of detections
        
        Returns:
            EventCreate object if crowd detected, None otherwise
        """
        if not self.enable_crowd_detection:
            return None
        
        person_count = sum(1 for d in detections if d["class_name"].lower() == "person")
        
        if person_count >= self.crowd_threshold:
            avg_confidence = (
                sum(d["confidence"] for d in detections) / len(detections)
                if detections else 0
            )
            
            event = EventCreate(
                camera_id=camera_id,
                event_type="crowd_detected",
                severity="high" if person_count > self.crowd_threshold * 2 else "medium",
                description=f"Crowd detected: {person_count} people",
                confidence=avg_confidence,
                metadata={
                    "person_count": person_count,
                    "detection_count": len(detections)
                }
            )
            
            logger.info(f"✓ Crowd event detected: {person_count} people")
            return event
        
        return None
    
    def detect_intrusion(
        self,
        camera_id: str,
        detections: List[Dict[str, Any]],
        intrusion_zones: Optional[Dict[str, Any]]
    ) -> Optional[EventCreate]:
        """
        Detect intrusion into restricted zones
        
        Args:
            camera_id: Camera identifier
            detections: List of detections
            intrusion_zones: Zones marked as restricted
        
        Returns:
            EventCreate object if intrusion detected, None otherwise
        """
        if not self.enable_intrusion_detection or not intrusion_zones:
            return None
        
        # Check if any detection is in intrusion zone
        intrusions = []
        for detection in detections:
            if detection["class_name"].lower() in ["person", "car"]:
                bbox = detection["bbox"]
                center_x = (bbox["x"] + bbox["x2"]) / 2
                center_y = (bbox["y"] + bbox["y2"]) / 2
                
                # Simple point-in-polygon check (simplified for demo)
                for zone in intrusion_zones.get("zones", []):
                    if self._point_in_zone(center_x, center_y, zone):
                        intrusions.append(detection)
        
        if intrusions:
            event = EventCreate(
                camera_id=camera_id,
                event_type="intrusion_detected",
                severity="critical",
                description=f"Intrusion detected: {len(intrusions)} objects in restricted zone",
                confidence=sum(d["confidence"] for d in intrusions) / len(intrusions),
                metadata={
                    "intrusion_count": len(intrusions),
                    "detected_classes": list(set(d["class_name"] for d in intrusions))
                }
            )
            
            logger.warning(f"⚠ Intrusion detected: {len(intrusions)} objects")
            return event
        
        return None
    
    def detect_loitering(
        self,
        camera_id: str,
        detections: List[Dict[str, Any]]
    ) -> Optional[EventCreate]:
        """
        Detect loitering behavior (same person in same area for extended time)
        
        Args:
            camera_id: Camera identifier
            detections: List of detections
        
        Returns:
            EventCreate object if loitering detected, None otherwise
        """
        # Track people by tracking_id
        person_detections = [d for d in detections if d["class_name"].lower() == "person"]
        
        if not person_detections:
            return None
        
        # This would require tracking people across frames
        # For now, return None
        return None
    
    def detect_vehicle_event(
        self,
        camera_id: str,
        detections: List[Dict[str, Any]]
    ) -> Optional[EventCreate]:
        """
        Detect vehicle-related events
        
        Args:
            camera_id: Camera identifier
            detections: List of detections
        
        Returns:
            EventCreate object if vehicle event detected, None otherwise
        """
        vehicle_count = sum(
            1 for d in detections 
            if d["class_name"].lower() in ["car", "truck", "bus", "motorbike"]
        )
        
        if vehicle_count > 0:
            event = EventCreate(
                camera_id=camera_id,
                event_type="vehicle_detected",
                severity="low",
                description=f"Vehicle detected: {vehicle_count} vehicles",
                confidence=sum(
                    d["confidence"] for d in detections 
                    if d["class_name"].lower() in ["car", "truck", "bus", "motorbike"]
                ) / vehicle_count,
                metadata={
                    "vehicle_count": vehicle_count,
                    "vehicle_types": list(set(
                        d["class_name"] for d in detections 
                        if d["class_name"].lower() in ["car", "truck", "bus", "motorbike"]
                    ))
                }
            )
            
            return event
        
        return None
    
    @staticmethod
    def _point_in_zone(x: float, y: float, zone: Dict[str, Any]) -> bool:
        """
        Check if point is in zone (simplified rectangle check)
        
        Args:
            x: X coordinate
            y: Y coordinate
            zone: Zone definition with x1, y1, x2, y2
        
        Returns:
            True if point is in zone
        """
        x1, y1 = zone.get("x1", 0), zone.get("y1", 0)
        x2, y2 = zone.get("x2", 1920), zone.get("y2", 1080)
        
        return x1 <= x <= x2 and y1 <= y <= y2


# Global instance
event_detection_service = None


def get_event_detection_service() -> EventDetectionService:
    """Get or initialize event detection service"""
    global event_detection_service
    if event_detection_service is None:
        event_detection_service = EventDetectionService()
    return event_detection_service
