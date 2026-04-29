# Real-Time Video Analytics Platform

A scalable, production-ready system that processes live video streams from CCTV cameras and performs real-time object detection, event analysis, and automated alerting.

## 🎯 Features

- **Real-Time Object Detection**: YOLOv8-based detection for people and vehicles with configurable confidence thresholds
- **Multi-Camera Support**: Process multiple video streams simultaneously with horizontal scaling
- **Event-Based Alerting**: Automatic alerts for crowd detection, intrusion, and vehicle events
- **Live Dashboard**: React-based real-time monitoring dashboard with WebSocket streaming
- **Kafka Streaming**: Event-driven architecture with Kafka for scalability
- **Privacy Features**: Built-in face blur capability for privacy compliance
- **Comprehensive Monitoring**: Prometheus metrics and Grafana visualization
- **Production Ready**: Docker and Kubernetes deployment configurations

## 🏗️ Architecture

### Components

1. **FastAPI Backend** (`backend/`)
   - REST API for camera management and event querying
   - WebSocket support for live streaming
   - Kafka producer/consumer integration
   - SQLAlchemy ORM with PostgreSQL

2. **Video Processor** (`video_processor/`)
   - Node.js service for video frame extraction
   - RTSP stream handling
   - Kafka integration for event publishing

3. **React Dashboard** (`frontend/`)
   - Real-time camera monitoring
   - Event visualization and filtering
   - Alert management
   - System statistics and metrics

4. **Infrastructure**
   - PostgreSQL: Persistent data storage
   - Redis: Caching and real-time state
   - Kafka: Event streaming pipeline
   - Prometheus: Metrics collection
   - Grafana: Visualization

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for frontend/video processor development)
- GPU support (optional, for faster inference)

### Using Docker Compose

```bash
# Clone the repository
git clone <repository>
cd video_analytics_platform

# Copy environment file
cp backend/.env.example backend/.env

# Build and start all services
docker-compose up -d

# Check service health
docker-compose ps

# View logs
docker-compose logs -f backend
```

### Access the Application

- **Dashboard**: http://localhost:3000
- **API Documentation**: http://localhost:8000/api/v1/docs
- **Grafana**: http://localhost:3001 (admin/admin)
- **Prometheus**: http://localhost:9090

## 📋 Configuration

### Backend Configuration (`.env`)

```env
# Database
DATABASE_URL=postgresql://analytics:password@localhost:5432/video_analytics

# Redis
REDIS_URL=redis://localhost:6379

# Kafka
KAFKA_BROKERS=localhost:9092

# YOLOv8
YOLO_MODEL_SIZE=m (nano, small, medium, large, xlarge)
YOLO_CONFIDENCE_THRESHOLD=0.5
YOLO_DEVICE=cpu (cpu, cuda:0)

# Event Detection
CROWD_THRESHOLD=10
ENABLE_INTRUSION_DETECTION=True

# Alerting
ALERT_COOLDOWN_SECONDS=30
```

## 📚 API Endpoints

### Cameras
- `GET /api/v1/cameras` - List all cameras
- `POST /api/v1/cameras` - Create new camera
- `GET /api/v1/cameras/{id}` - Get camera details
- `PUT /api/v1/cameras/{id}` - Update camera
- `DELETE /api/v1/cameras/{id}` - Delete camera

### Events
- `GET /api/v1/events` - Search events with filters
- `POST /api/v1/events` - Create event
- `POST /api/v1/events/{id}/acknowledge` - Acknowledge event
- `POST /api/v1/events/{id}/resolve` - Resolve event

### Alerts
- `GET /api/v1/alerts` - List alert rules
- `POST /api/v1/alerts` - Create alert rule
- `POST /api/v1/alerts/{id}/test` - Test alert

### Streaming
- `POST /api/v1/stream/start` - Start stream processing
- `POST /api/v1/stream/stop` - Stop stream processing
- `WS /api/v1/stream/live/{camera_id}` - WebSocket live feed

### System
- `GET /api/v1/system/health` - Health check
- `GET /api/v1/system/stats` - System statistics
- `GET /api/v1/system/metrics` - Prometheus metrics

## 🛠️ Development

### Local Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload
```

### Local Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

## 🔧 Customization

### Adding Detection Zones

Configure detection and intrusion zones per camera:

```json
{
  "detection_zones": [
    {"name": "entrance", "x1": 0, "y1": 0, "x2": 640, "y2": 480}
  ],
  "intrusion_zones": [
    {"name": "restricted", "x1": 200, "y1": 200, "x2": 400, "y2": 400}
  ]
}
```

### Custom Event Rules

Extend `EventDetectionService` to add custom event detection logic:

```python
def detect_custom_event(self, camera_id: str, detections: List[Dict]):
    # Your custom logic here
    pass
```

### Multi-Channel Alerts

Configure alerts for multiple channels:

```python
notification_channels = ["email", "slack", "webhook", "sms"]
```

## 📊 Monitoring

### Metrics

The system exposes Prometheus metrics on port 9090:

- `video_frames_processed` - Total frames processed
- `video_detections_total` - Total detections by class
- `video_inference_time_ms` - Inference time histogram
- `video_events_total` - Total events by type
- `kafka_messages_sent` - Kafka messages published

### Dashboards

Pre-configured Grafana dashboards for:

- System overview and performance
- Detection metrics by camera
- Event trends and patterns
- Alert timeline

## 🐛 Troubleshooting

### Backend Issues

```bash
# Check service health
curl http://localhost:8000/api/v1/system/health

# View logs
docker-compose logs backend

# Restart service
docker-compose restart backend
```

### Database Issues

```bash
# Connect to PostgreSQL
docker exec -it video-analytics-db psql -U analytics -d video_analytics

# Check database migrations
\dt

# Reset database
docker-compose down -v
docker-compose up -d
```

### Kafka Issues

```bash
# Check Kafka topics
docker exec -it video-analytics-kafka kafka-topics --list --bootstrap-server localhost:9092

# Consume messages
docker exec -it video-analytics-kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic video_detections
```

## 🚢 Deployment

### Docker Compose (Development)

```bash
docker-compose up -d
```

### Kubernetes (Production)

```bash
# Create namespace
kubectl create namespace video-analytics

# Deploy services
kubectl apply -f kubernetes/postgres.yaml -n video-analytics
kubectl apply -f kubernetes/redis.yaml -n video-analytics
kubectl apply -f kubernetes/kafka.yaml -n video-analytics
kubectl apply -f kubernetes/backend.yaml -n video-analytics
kubectl apply -f kubernetes/frontend.yaml -n video-analytics

# Check status
kubectl get pods -n video-analytics
```

## 📝 Project Structure

```
video_analytics_platform/
├── backend/
│   ├── app/
│   │   ├── models/          # SQLAlchemy ORM models
│   │   ├── schemas/         # Pydantic validation schemas
│   │   ├── services/        # Business logic services
│   │   ├── routes/          # API endpoints
│   │   ├── config.py        # Configuration management
│   │   └── main.py          # FastAPI application
│   ├── tests/               # Unit and integration tests
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile
├── video_processor/
│   ├── src/
│   │   ├── streams.js       # Stream processing
│   │   ├── kafka.js         # Kafka integration
│   │   └── server.js        # Express server
│   ├── package.json
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── App.tsx          # Main app component
│   │   └── main.tsx         # Entry point
│   ├── package.json
│   └── Dockerfile
├── kubernetes/              # K8s manifests
├── config/                  # Configuration files
├── docker-compose.yml       # Docker Compose config
└── README.md
```

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please follow the [contribution guidelines](CONTRIBUTING.md).

## 📞 Support

For issues, feature requests, or questions:
- Open an issue on GitHub
- Check existing documentation
- Review API documentation at http://localhost:8000/api/v1/docs

## 🎓 Learning Resources

- [YOLOv8 Documentation](https://docs.ultralytics.com/)
- [FastAPI Guide](https://fastapi.tiangolo.com/)
- [Kafka Documentation](https://kafka.apache.org/documentation/)
- [React Documentation](https://react.dev/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## 🔮 Future Roadmap

- [ ] WebRTC support for optimal video streaming
- [ ] Advanced analytics and reporting
- [ ] Multi-tenant support
- [ ] Custom model training interface
- [ ] Edge deployment with NVIDIA Jetson
- [ ] Mobile app for alerts and monitoring
- [ ] Advanced anomaly detection (temporal patterns)
- [ ] Integration with third-party systems (SIEM, ticketing)
