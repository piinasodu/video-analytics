"""
Video processing service (Node.js)
Main entry point for streaming video frames to the backend
"""

# This is a TypeScript/JavaScript service that will:
# 1. Capture video frames from RTSP/HTTP streams
# 2. Send frames to the FastAPI backend for inference
# 3. Receive detection results and send to Kafka
# 4. Handle WebSocket connections for live video feed

# Installation:
# npm install

# Configuration via environment variables:
# VIDEO_SOURCES - Comma-separated RTSP URLs
# BACKEND_URL - FastAPI backend URL
# KAFKA_BROKERS - Kafka broker addresses
# FRAME_RATE - Frames per second to capture
# FRAME_SKIP - Skip frames for reduced processing
# MAX_FRAMES - Maximum frames to buffer

# Usage:
# npm start
