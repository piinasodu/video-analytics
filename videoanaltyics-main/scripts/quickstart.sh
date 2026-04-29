#!/bin/bash

# Quick start script for Video Analytics Platform

set -e

echo "🚀 Video Analytics Platform - Quick Start"
echo "=========================================="

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed"
    exit 1
fi

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed"
    exit 1
fi

# Create environment file if doesn't exist
if [ ! -f backend/.env ]; then
    echo "📝 Creating .env file from template..."
    cp backend/.env.example backend/.env
fi

# Create necessary directories
mkdir -p data/{postgres,redis,prometheus}

# Start services
echo "🐳 Starting Docker services..."
docker-compose up -d

echo "⏳ Waiting for services to be healthy..."
sleep 10

# Check services
echo "✅ Checking services..."
docker-compose ps

echo ""
echo "✨ Video Analytics Platform is running!"
echo ""
echo "📚 Access points:"
echo "   API: http://localhost:8000/api/v1"
echo "   API Docs: http://localhost:8000/api/v1/docs"
echo "   Dashboard: http://localhost:3000"
echo "   Grafana: http://localhost:3001 (admin/admin)"
echo "   Prometheus: http://localhost:9090"
echo ""
echo "📝 Useful commands:"
echo "   View logs: docker-compose logs -f backend"
echo "   Stop services: docker-compose down"
echo "   Reset data: docker-compose down -v"
echo ""
echo "🎯 Next steps:"
echo "   1. Open http://localhost:3000 in your browser"
echo "   2. Add a camera via the API"
echo "   3. Start a stream to see detections"
echo ""
