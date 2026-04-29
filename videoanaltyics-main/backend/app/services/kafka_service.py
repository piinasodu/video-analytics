"""
Kafka streaming service for video analytics events
"""
import json
import logging
from typing import Dict, Any, Callable, Optional
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
from app.config import settings
import threading

logger = logging.getLogger(__name__)


class KafkaService:
    """Kafka producer and consumer for video analytics"""
    
    def __init__(self):
        self.brokers = settings.kafka_brokers.split(",")
        self.producer = None
        self.consumers = {}
        self._initialize_producer()
    
    def _initialize_producer(self):
        """Initialize Kafka producer"""
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=self.brokers,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                acks="all",
                retries=3,
                compression_type="snappy"
            )
            logger.info(f"✓ Kafka producer initialized with brokers: {self.brokers}")
        except Exception as e:
            logger.error(f"✗ Kafka producer initialization failed: {e}")
    
    def send_detection(self, detection: Dict[str, Any]):
        """
        Send detection event to Kafka
        
        Args:
            detection: Detection data
        """
        try:
            future = self.producer.send(
                settings.kafka_topic_detections,
                value=detection
            )
            future.get(timeout=1)
            logger.debug(f"✓ Detection sent to Kafka: {detection.get('camera_id')}")
        except Exception as e:
            logger.error(f"✗ Failed to send detection to Kafka: {e}")
    
    def send_event(self, event: Dict[str, Any]):
        """
        Send event to Kafka
        
        Args:
            event: Event data
        """
        try:
            future = self.producer.send(
                settings.kafka_topic_events,
                value=event
            )
            future.get(timeout=1)
            logger.debug(f"✓ Event sent to Kafka: {event.get('event_type')}")
        except Exception as e:
            logger.error(f"✗ Failed to send event to Kafka: {e}")
    
    def send_alert(self, alert: Dict[str, Any]):
        """
        Send alert to Kafka
        
        Args:
            alert: Alert data
        """
        try:
            future = self.producer.send(
                settings.kafka_topic_alerts,
                value=alert
            )
            future.get(timeout=1)
            logger.debug(f"✓ Alert sent to Kafka: {alert.get('rule_name')}")
        except Exception as e:
            logger.error(f"✗ Failed to send alert to Kafka: {e}")
    
    def consume_events(
        self,
        topic: str,
        callback: Callable[[Dict[str, Any]], None],
        group_id: Optional[str] = None
    ):
        """
        Consume events from Kafka topic
        
        Args:
            topic: Topic to consume from
            callback: Callback function for each message
            group_id: Consumer group ID
        """
        try:
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers=self.brokers,
                group_id=group_id or settings.kafka_consumer_group,
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                auto_offset_reset="earliest",
                enable_auto_commit=True
            )
            
            logger.info(f"✓ Kafka consumer initialized for topic: {topic}")
            
            # Run consumer in separate thread
            def consumer_loop():
                try:
                    for message in consumer:
                        callback(message.value)
                except Exception as e:
                    logger.error(f"✗ Consumer error: {e}")
                finally:
                    consumer.close()
            
            thread = threading.Thread(target=consumer_loop, daemon=True)
            thread.start()
            
            self.consumers[topic] = consumer
        
        except Exception as e:
            logger.error(f"✗ Failed to initialize consumer for {topic}: {e}")
    
    def close(self):
        """Close producer and consumers"""
        if self.producer:
            self.producer.close()
        for consumer in self.consumers.values():
            consumer.close()
        logger.info("✓ Kafka service closed")


# Global instance
kafka_service = None


def get_kafka_service() -> KafkaService:
    """Get or initialize Kafka service"""
    global kafka_service
    if kafka_service is None:
        kafka_service = KafkaService()
    return kafka_service
