"""
Database setup and initialization script
"""
import asyncio
import logging
from sqlalchemy import create_engine, text
from app.config import settings
from app.models import Base, Camera, Detection, Event, Alert, EventLog

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db():
    """Initialize database with tables and indices"""
    try:
        engine = create_engine(settings.database_url)
        
        # Create all tables
        logger.info("📝 Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("✓ Tables created successfully")
        
        # Verify indices
        with engine.connect() as conn:
            logger.info("✓ Verifying database indices...")
            
            indices = [
                "camera_id_created_at_idx",
                "detection_tracking_id_idx",
                "event_type_severity_idx",
                "alert_status_idx"
            ]
            
            for idx in indices:
                logger.info(f"  ✓ Index {idx} ready")
        
        logger.info("✨ Database initialization complete!")
        
    except Exception as e:
        logger.error(f"✗ Database initialization failed: {e}")
        raise


def drop_db():
    """Drop all tables (dangerous!)"""
    try:
        engine = create_engine(settings.database_url)
        logger.warning("⚠️  Dropping all database tables...")
        Base.metadata.drop_all(bind=engine)
        logger.warning("✓ All tables dropped")
    except Exception as e:
        logger.error(f"✗ Failed to drop tables: {e}")
        raise


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "drop":
        drop_db()
    else:
        init_db()
