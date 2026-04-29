# API Reference

## Authentication

Currently, the API supports basic requests. For production, implement JWT authentication.

## Base URL

```
http://localhost:8000/api/v1
```

## Response Format

All responses are JSON with the following format:

```json
{
  "data": {},
  "status": "success",
  "timestamp": "2026-04-17T12:00:00Z"
}
```

## Cameras

### List Cameras

```
GET /cameras
```

**Query Parameters:**
- `skip`: Number of records to skip (default: 0)
- `limit`: Number of records to return (default: 10)

**Response:**
```json
[
  {
    "id": "uuid",
    "name": "Main Entrance",
    "source_url": "rtsp://camera-ip/stream",
    "location": "Building A, Floor 1",
    "resolution": {"width": 1920, "height": 1080},
    "fps": 30,
    "is_active": true,
    "created_at": "2026-04-17T12:00:00Z"
  }
]
```

### Create Camera

```
POST /cameras
Content-Type: application/json

{
  "name": "Main Entrance",
  "source_url": "rtsp://192.168.1.100:554/stream",
  "location": "Building A, Floor 1",
  "resolution": {"width": 1920, "height": 1080},
  "fps": 30
}
```

### Get Camera Details

```
GET /cameras/{camera_id}
```

### Update Camera

```
PUT /cameras/{camera_id}
Content-Type: application/json

{
  "name": "Main Entrance Updated",
  "location": "Building A, Floor 2"
}
```

### Delete Camera

```
DELETE /cameras/{camera_id}
```

### Start Stream

```
POST /cameras/{camera_id}/start-stream
```

### Stop Stream

```
POST /cameras/{camera_id}/stop-stream
```

## Events

### Search Events

```
GET /events?event_type=crowd_detected&severity=high&status=open&skip=0&limit=50
```

**Query Parameters:**
- `camera_id`: Filter by camera (optional)
- `event_type`: crowd_detected, vehicle_detected, intrusion_detected (optional)
- `severity`: low, medium, high, critical (optional)
- `status`: open, acknowledged, resolved (optional)
- `skip`: Number of records to skip (default: 0)
- `limit`: Number of records to return (default: 50)

### Create Event

```
POST /events
Content-Type: application/json

{
  "camera_id": "uuid",
  "event_type": "crowd_detected",
  "severity": "high",
  "description": "15 people detected",
  "confidence": 0.87
}
```

### Get Event Details

```
GET /events/{event_id}
```

### Acknowledge Event

```
POST /events/{event_id}/acknowledge
```

### Resolve Event

```
POST /events/{event_id}/resolve
```

### Get Event Snapshot

```
GET /events/{event_id}/snapshot
```

## Alerts

### List Alerts

```
GET /alerts?status=active&skip=0&limit=50
```

**Query Parameters:**
- `status`: active, acknowledged, resolved (optional)
- `skip`: Number of records to skip (default: 0)
- `limit`: Number of records to return (default: 50)

### Create Alert Rule

```
POST /alerts
Content-Type: application/json

{
  "rule_name": "High Crowd Alert",
  "alert_type": "crowd_detected",
  "notification_channels": ["email", "slack"],
  "severity": "high"
}
```

### Delete Alert Rule

```
DELETE /alerts/{alert_id}
```

### Test Alert

```
POST /alerts/{alert_id}/test
```

### Acknowledge Alert

```
POST /alerts/{alert_id}/acknowledge
```

## Streaming

### Start Stream Processing

```
POST /stream/start
Content-Type: application/json

{
  "camera_id": "uuid",
  "stream_quality": "medium"
}
```

**Quality Options:** low, medium, high

### Stop Stream Processing

```
POST /stream/stop
Content-Type: application/json

{
  "stream_id": "stream-uuid"
}
```

### Get Stream Status

```
GET /stream/status/{stream_id}
```

**Response:**
```json
{
  "stream_id": "stream-uuid",
  "status": "active",
  "frames_processed": 1500,
  "fps": 30,
  "uptime_seconds": 3600,
  "total_detections": 150
}
```

### WebSocket Live Feed

```
WS /stream/live/{camera_id}
```

**Connection:**
```javascript
const ws = new WebSocket('ws://localhost:8000/api/v1/stream/live/camera-uuid');

ws.onmessage = (event) => {
  const frame = JSON.parse(event.data);
  // Handle frame data
};

ws.send(JSON.stringify({
  type: 'quality_change',
  quality: 'high'
}));
```

## System

### Health Check

```
GET /system/health
```

**Response:**
```json
{
  "status": "healthy",
  "components": {
    "api": "ok",
    "database": "ok",
    "kafka": "ok",
    "redis": "ok",
    "yolo": "ok"
  },
  "timestamp": "2026-04-17T12:00:00Z"
}
```

### System Statistics

```
GET /system/stats
```

**Response:**
```json
{
  "total_cameras": 4,
  "active_cameras": 3,
  "uptime_seconds": 86400,
  "total_frames_processed": 1000000,
  "avg_inference_time_ms": 45.5,
  "total_detections": 5000,
  "detection_stats": {
    "detections_by_class": {
      "person": 3000,
      "car": 1500,
      "bicycle": 500
    }
  }
}
```

### System Info

```
GET /system/info
```

### API Version

```
GET /system/version
```

### Prometheus Metrics

```
GET /system/metrics
```

Returns Prometheus format metrics.

## Error Handling

### Error Response Format

```json
{
  "status": "error",
  "code": 400,
  "message": "Invalid request parameters",
  "timestamp": "2026-04-17T12:00:00Z"
}
```

### Common Error Codes

- `400`: Bad Request - Invalid parameters
- `401`: Unauthorized - Missing authentication
- `403`: Forbidden - Insufficient permissions
- `404`: Not Found - Resource not found
- `500`: Internal Server Error - Server error

## Rate Limiting

Currently disabled. For production, implement:
- 1000 requests per minute per IP
- 100 concurrent WebSocket connections per server

## Pagination

Use `skip` and `limit` parameters for pagination:

```
GET /events?skip=0&limit=50    # First page
GET /events?skip=50&limit=50   # Second page
GET /events?skip=100&limit=50  # Third page
```

## Filtering

Apply multiple filters with query parameters:

```
GET /events?camera_id=uuid&event_type=crowd_detected&severity=high&status=open
```

## Sorting

Supported sorting (to be implemented):

```
GET /events?sort_by=created_at&sort_order=desc
```

## Authentication (Future)

Add JWT token to Authorization header:

```
Authorization: Bearer <token>
```

## Rate Limiting (Future)

Check these headers in responses:

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1703088000
```
