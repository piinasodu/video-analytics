# Architecture Overview

## System Components

### 1. Video Sources
- RTSP streams from CCTV cameras
- HTTP video feeds
- Local video files

### 2. Video Processor (Node.js)
**Responsibilities:**
- Frame extraction from video sources
- Frame buffering (configurable buffer size)
- Format conversion and normalization
- Connection pooling for multiple sources

**Key Features:**
- Handles connection failures and reconnection
- Configurable frame skip for reduced processing load
- Maintains frame timestamps for tracking

### 3. FastAPI Backend
**Responsibilities:**
- REST API for CRUD operations
- WebSocket connections for live streaming
- Database operations
- Kafka integration
- System monitoring

**Architecture:**
```
FastAPI App
├── Routes
│   ├── /cameras - Camera management
│   ├── /events - Event querying
│   ├── /alerts - Alert management
│   ├── /stream - Stream operations
│   └── /system - System info
├── Services
│   ├── YOLOv8Service - Model inference
│   ├── KafkaService - Event streaming
│   ├── EventDetectionService - Event logic
│   └── AlertService - Alert management
├── Models
│   ├── Camera
│   ├── Detection
│   ├── Event
│   ├── Alert
│   └── EventLog
└── Database
    └── PostgreSQL
```

### 4. YOLOv8 Inference
**Model Sizes:**
- nano: ~3M parameters, fastest
- small: ~11M parameters
- medium: ~25M parameters (default)
- large: ~53M parameters
- xlarge: ~87M parameters, most accurate

**Inference Pipeline:**
1. Frame normalization
2. Model inference
3. Post-processing (NMS)
4. Class mapping
5. Confidence filtering

### 5. Event Processing
**Event Types:**
- `crowd_detected`: >= CROWD_THRESHOLD people
- `vehicle_detected`: Car, truck, bus, motorbike
- `intrusion_detected`: Object in restricted zone
- `loitering`: Same person in same area for extended time

**Processing Flow:**
```
Detection → Event Detection Service → Event Creation → Alert Check
                                           ↓
                                    Kafka Publishing
```

### 6. Kafka Streaming
**Topics:**
- `video_detections`: Real-time detections (high frequency)
- `video_events`: Business logic events (medium frequency)
- `video_alerts`: Alert triggers (low frequency)

**Consumer Groups:**
- Event detection service
- Alert notification service
- Analytics pipeline

### 7. Database Schema
**Key Tables:**
```sql
cameras
├── id (UUID, primary key)
├── name (string)
├── source_url (string)
├── detection_zones (JSON array)
├── intrusion_zones (JSON array)
└── last_heartbeat (timestamp)

detections
├── id (UUID, primary key)
├── camera_id (foreign key)
├── class_name (string)
├── confidence (float)
├── bounding_box (JSON)
├── tracking_id (integer)
└── frame_number (integer)

events
├── id (UUID, primary key)
├── camera_id (foreign key)
├── event_type (string)
├── severity (enum)
├── status (enum: open, acknowledged, resolved)
└── detection_count (integer)

alerts
├── id (UUID, primary key)
├── rule_name (string)
├── alert_type (string)
├── notification_channels (JSON array)
└── status (enum)
```

### 8. React Frontend
**Features:**
- Real-time camera grid
- Event filtering and search
- Alert management dashboard
- System statistics
- WebSocket live video feed

**Components:**
```
App
├── Navigation
├── Tabs
│   ├── Cameras (CameraGrid)
│   ├── Events (EventsList)
│   ├── Alerts (AlertsPanel)
│   └── Statistics (StatsCards)
└── API Integration
    └── Axios for REST
    └── WebSocket for live data
```

## Data Flow

### Detection Pipeline
```
Video Source
    ↓
Video Processor (Frame Extraction)
    ↓
YOLOv8 Inference
    ↓
Kafka: video_detections
    ↓
Backend: Detection Storage
```

### Event Processing
```
Detection Stream
    ↓
Event Detection Service
    ├─→ Crowd Detection
    ├─→ Intrusion Detection
    └─→ Vehicle Detection
    ↓
Kafka: video_events
    ↓
Backend: Event Storage
    ↓
Alert Check
    ↓
Kafka: video_alerts
    ↓
Notification Service
```

## Scaling Strategy

### Horizontal Scaling
```
Load Balancer
├── Backend Instance 1
├── Backend Instance 2
└── Backend Instance N

Video Processor Cluster
├── Processor 1 (cameras 1-5)
├── Processor 2 (cameras 6-10)
└── Processor N
```

### Kafka Partitioning
- Partition by camera_id for better locality
- Enables parallel event processing
- Consumer groups for scalability

### Database Scaling
- Read replicas for analytics queries
- Connection pooling (SQLAlchemy)
- Index optimization

### Caching Strategy
- Redis for real-time camera status
- Query result caching
- Session management

## Performance Considerations

### Inference Optimization
- Model size selection based on GPU capability
- Batch inference for multiple streams
- GPU sharing with container orchestration
- Inference timeout to prevent hangs

### Network Optimization
- WebSocket for real-time updates (avoid polling)
- Frame compression for bandwidth reduction
- CDN for static assets
- Connection pooling

### Storage Optimization
- Retention policies (configurable)
- Snapshot compression
- Archive old events to object storage
- Database indices on frequently queried columns

## Security Considerations

### Authentication & Authorization
- API key per camera source
- JWT tokens for API access
- Role-based access control

### Data Privacy
- Face blur capability
- GDPR-compliant data retention
- Encrypted connections (TLS/SSL)
- Audit logging

### System Security
- Network isolation with VPC
- Secrets management (environment variables)
- Regular security updates
- Monitoring and alerting

## Monitoring & Observability

### Metrics
- Frame processing rate (fps)
- Inference latency (ms)
- Detection rate (objects/frame)
- Event rate (events/hour)
- Alert rate (alerts/hour)
- System resource usage

### Logging
- Application logs (structured JSON)
- Access logs
- Error tracking
- Audit trail

### Visualization
- Grafana dashboards
- Real-time metrics
- Historical trends
- Alert history

## Deployment Architecture

### Development (Docker Compose)
```
docker-compose
├── PostgreSQL
├── Redis
├── Kafka/Zookeeper
├── Backend
├── Frontend
└── Video Processor
```

### Production (Kubernetes)
```
Kubernetes Cluster
├── Namespace: video-analytics
├── Services
│   ├── PostgreSQL StatefulSet
│   ├── Redis Deployment
│   ├── Kafka StatefulSet
│   ├── Backend Deployment (replicas: 3)
│   ├── Frontend Deployment
│   └── Video Processor DaemonSet
├── Ingress Controller
├── ConfigMaps & Secrets
└── Persistent Volumes
```

## Disaster Recovery

### Backup Strategy
- Database daily snapshots
- Kafka topic retention policies
- Configuration version control

### Redundancy
- Multi-replica Kafka topics
- Database replication
- Horizontal scaling for stateless services

### Recovery RTO/RPO
- RTO: < 15 minutes (with Kubernetes)
- RPO: < 1 hour (database backups)
