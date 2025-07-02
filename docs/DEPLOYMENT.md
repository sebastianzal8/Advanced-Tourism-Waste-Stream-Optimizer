# Deployment Guide

## Prerequisites
- Docker and Docker Compose installed
- Git installed
- Access to a cloud provider (AWS, Azure, GCP)

## Local Development Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd "Advanced Tourism Waste Stream Optimizer"
```

### 2. Environment Setup
Create a `.env` file in the root directory:
```bash
# Database
DATABASE_URL=postgresql://admin:password123@localhost:5432/tourism_waste_optimizer

# API
SECRET_KEY=your-secret-key-here
DEBUG=True

# Frontend
REACT_APP_API_URL=http://localhost:8000
```

### 3. Start Services with Docker Compose
```bash
docker-compose up -d
```

This will start:
- PostgreSQL database on port 5432
- Backend API on port 8000
- Frontend application on port 3000
- Redis cache on port 6379

### 4. Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Production Deployment

### Option 1: Docker Compose on Server
1. Set up a server with Docker and Docker Compose
2. Configure environment variables for production
3. Run `docker-compose -f docker-compose.prod.yml up -d`

### Option 2: Kubernetes Deployment
1. Create Kubernetes manifests in the `k8s/` directory
2. Apply the manifests to your cluster
3. Configure ingress and load balancer

### Option 3: Cloud Platform Deployment
- **AWS**: Use ECS/EKS with Application Load Balancer
- **Azure**: Use Azure Container Instances or AKS
- **GCP**: Use Cloud Run or GKE

## Environment Variables

### Backend
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key
- `DEBUG`: Enable/disable debug mode
- `REDIS_URL`: Redis connection string
- `CORS_ORIGINS`: Allowed CORS origins

### Frontend
- `REACT_APP_API_URL`: Backend API URL
- `REACT_APP_ENVIRONMENT`: Environment name

## Monitoring and Logging
- Use Prometheus for metrics collection
- Use Grafana for visualization
- Configure log aggregation with ELK stack

## Security Considerations
- Use HTTPS in production
- Implement proper authentication and authorization
- Regular security updates
- Database encryption at rest
- Network security groups/firewall rules 