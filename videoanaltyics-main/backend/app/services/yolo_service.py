"""
YOLOv8 object detection service
"""
import logging
from typing import List, Tuple, Dict, Any
import cv2
import numpy as np
from ultralytics import YOLO
from app.config import settings

logger = logging.getLogger(__name__)


class YOLOv8Service:
    """YOLOv8 inference engine for object detection"""
    
    def __init__(self):
        self.model = None
        self.device = settings.yolo_device
        self.confidence_threshold = settings.yolo_confidence_threshold
        self.model_size = settings.yolo_model_size
        self._initialize_model()
    
    def _initialize_model(self):
        """Load YOLOv8 model"""
        try:
            model_name = f"yolov8{self.model_size}.pt"
            self.model = YOLO(model_name)
            self.model.to(self.device)
            logger.info(f"✓ YOLOv8 model {model_name} loaded on {self.device}")
        except Exception as e:
            logger.error(f"✗ Failed to load YOLOv8 model: {e}")
            raise
    
    def detect(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """
        Run inference on a frame
        
        Args:
            frame: Input image frame
        
        Returns:
            List of detections with bounding boxes, classes, and confidence
        """
        try:
            results = self.model(frame, conf=self.confidence_threshold, verbose=False)
            
            detections = []
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    conf = box.conf[0].item()
                    cls_id = int(box.cls[0])
                    class_name = self.model.names[cls_id]
                    
                    detection = {
                        "class_name": class_name,
                        "confidence": conf,
                        "bbox": {
                            "x": int(x1),
                            "y": int(y1),
                            "x2": int(x2),
                            "y2": int(y2),
                            "width": int(x2 - x1),
                            "height": int(y2 - y1)
                        },
                        "cls_id": cls_id
                    }
                    detections.append(detection)
            
            return detections
        
        except Exception as e:
            logger.error(f"✗ Inference failed: {e}")
            return []
    
    def detect_with_tracking(self, frame: np.ndarray, persist: bool = True) -> List[Dict[str, Any]]:
        """
        Run inference with object tracking
        
        Args:
            frame: Input image frame
            persist: Enable object tracking across frames
        
        Returns:
            List of detections with tracking IDs
        """
        try:
            results = self.model(frame, conf=self.confidence_threshold, persist=persist, verbose=False)
            
            detections = []
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    conf = box.conf[0].item()
                    cls_id = int(box.cls[0])
                    track_id = int(box.id[0]) if box.id is not None else None
                    class_name = self.model.names[cls_id]
                    
                    detection = {
                        "class_name": class_name,
                        "confidence": conf,
                        "tracking_id": track_id,
                        "bbox": {
                            "x": int(x1),
                            "y": int(y1),
                            "x2": int(x2),
                            "y2": int(y2),
                            "width": int(x2 - x1),
                            "height": int(y2 - y1)
                        },
                        "cls_id": cls_id
                    }
                    detections.append(detection)
            
            return detections
        
        except Exception as e:
            logger.error(f"✗ Tracking inference failed: {e}")
            return []
    
    def annotate_frame(self, frame: np.ndarray, detections: List[Dict[str, Any]]) -> np.ndarray:
        """
        Draw bounding boxes and labels on frame
        
        Args:
            frame: Input image frame
            detections: List of detections
        
        Returns:
            Annotated frame with bounding boxes
        """
        annotated = frame.copy()
        
        for detection in detections:
            bbox = detection["bbox"]
            x, y, x2, y2 = bbox["x"], bbox["y"], bbox["x2"], bbox["y2"]
            class_name = detection["class_name"]
            confidence = detection["confidence"]
            
            # Draw bounding box
            color = (0, 255, 0) if confidence > 0.8 else (255, 165, 0)
            cv2.rectangle(annotated, (x, y), (x2, y2), color, 2)
            
            # Draw label
            label = f"{class_name} {confidence:.2f}"
            cv2.putText(
                annotated, label, (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2
            )
        
        return annotated
    
    def blur_faces(self, frame: np.ndarray, detections: List[Dict[str, Any]]) -> np.ndarray:
        """
        Blur faces in frame for privacy
        
        Args:
            frame: Input image frame
            detections: List of detections
        
        Returns:
            Frame with blurred faces
        """
        blurred = frame.copy()
        blur_strength = settings.blur_strength
        
        for detection in detections:
            if detection["class_name"].lower() == "person":
                bbox = detection["bbox"]
                x, y, x2, y2 = bbox["x"], bbox["y"], bbox["x2"], bbox["y2"]
                
                # Blur the region
                roi = blurred[y:y2, x:x2]
                blur_size = max(blur_strength, blur_strength + 1)
                roi_blurred = cv2.blur(roi, (blur_size, blur_size))
                blurred[y:y2, x:x2] = roi_blurred
        
        return blurred


# Global instance
yolo_service = None


def get_yolo_service() -> YOLOv8Service:
    """Get or initialize YOLOv8 service"""
    global yolo_service
    if yolo_service is None:
        yolo_service = YOLOv8Service()
    return yolo_service
