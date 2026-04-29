"""
Alert and notification service
"""
import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta
from app.config import settings

logger = logging.getLogger(__name__)


class AlertService:
    """Manages alert rules and notifications"""
    
    def __init__(self):
        self.alert_cooldown = settings.alert_cooldown_seconds
        self.last_alerts = {}  # Track last alert time per rule
    
    def should_trigger_alert(self, rule_name: str) -> bool:
        """
        Check if alert should be triggered based on cooldown
        
        Args:
            rule_name: Alert rule name
        
        Returns:
            True if alert can be triggered
        """
        last_alert_time = self.last_alerts.get(rule_name)
        
        if last_alert_time is None:
            return True
        
        time_diff = datetime.utcnow() - last_alert_time
        if time_diff.total_seconds() >= self.alert_cooldown:
            return True
        
        return False
    
    def record_alert(self, rule_name: str):
        """Record alert trigger time"""
        self.last_alerts[rule_name] = datetime.utcnow()
        logger.debug(f"✓ Alert {rule_name} recorded at {datetime.utcnow()}")
    
    def trigger_alert(self, alert_data: Dict[str, Any]):
        """
        Trigger alert and send notifications
        
        Args:
            alert_data: Alert information
        """
        rule_name = alert_data.get("rule_name")
        
        if not self.should_trigger_alert(rule_name):
            logger.debug(f"⊘ Alert {rule_name} still in cooldown")
            return
        
        channels = alert_data.get("notification_channels", [])
        
        for channel in channels:
            try:
                if channel == "email":
                    self._send_email_alert(alert_data)
                elif channel == "slack":
                    self._send_slack_alert(alert_data)
                elif channel == "webhook":
                    self._send_webhook_alert(alert_data)
                elif channel == "sms":
                    self._send_sms_alert(alert_data)
            except Exception as e:
                logger.error(f"✗ Failed to send {channel} alert: {e}")
        
        self.record_alert(rule_name)
        logger.info(f"✓ Alert triggered: {rule_name}")
    
    @staticmethod
    def _send_email_alert(alert_data: Dict[str, Any]):
        """Send email notification"""
        # TODO: Implement email sending
        logger.info(f"📧 Email alert: {alert_data.get('rule_name')}")
    
    @staticmethod
    def _send_slack_alert(alert_data: Dict[str, Any]):
        """Send Slack notification"""
        # TODO: Implement Slack webhook
        logger.info(f"💬 Slack alert: {alert_data.get('rule_name')}")
    
    @staticmethod
    def _send_webhook_alert(alert_data: Dict[str, Any]):
        """Send webhook notification"""
        # TODO: Implement webhook POST
        logger.info(f"🔗 Webhook alert: {alert_data.get('rule_name')}")
    
    @staticmethod
    def _send_sms_alert(alert_data: Dict[str, Any]):
        """Send SMS notification"""
        # TODO: Implement SMS sending
        logger.info(f"📱 SMS alert: {alert_data.get('rule_name')}")
    
    def create_alert_from_event(
        self,
        event_type: str,
        severity: str,
        event_id: str
    ) -> Dict[str, Any]:
        """
        Create alert from detected event
        
        Args:
            event_type: Type of event
            severity: Event severity
            event_id: Event ID
        
        Returns:
            Alert data
        """
        rule_name = f"{event_type}_{severity}"
        
        alert = {
            "rule_name": rule_name,
            "alert_type": event_type,
            "triggered_by": "event_detection",
            "trigger_value": event_id,
            "notification_channels": self._get_notification_channels(severity),
            "severity": severity,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return alert
    
    @staticmethod
    def _get_notification_channels(severity: str) -> List[str]:
        """Get notification channels based on severity"""
        channels_map = {
            "low": ["email"],
            "medium": ["email", "slack"],
            "high": ["email", "slack", "webhook"],
            "critical": ["email", "slack", "webhook", "sms"]
        }
        
        return channels_map.get(severity, ["email"])


# Global instance
alert_service = None


def get_alert_service() -> AlertService:
    """Get or initialize alert service"""
    global alert_service
    if alert_service is None:
        alert_service = AlertService()
    return alert_service
