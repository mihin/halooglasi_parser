# Docker Deployment Guide

## Overview

This guide shows how to deploy the HaloOglasi Parser in Docker containers using environment variables for configuration.

## Docker Setup

### 1. Create Dockerfile

```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY scripts/ ./scripts/

# Create data and logs directories
RUN mkdir -p data logs

# Set environment variables (defaults)
ENV TELEGRAM_BOT_TOKEN=""
ENV TELEGRAM_CHAT_ID=""

# Run the scheduler by default
CMD ["python", "scripts/scheduler.py"]
```

### 2. Create docker-compose.yml

```yaml
version: '3.8'

services:
  halooglasi-parser:
    build: .
    container_name: halooglasi-monitor
    restart: unless-stopped
    environment:
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - TELEGRAM_CHAT_ID=${TELEGRAM_CHAT_ID}
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    healthcheck:
      test: ["CMD", "python", "-c", "import sys; sys.path.append('src'); from halooglasi_parser.config_loader import config_loader; exit(0 if config_loader.validate_telegram_config() else 1)"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### 3. Create .env file

```bash
# Copy this to .env and update with your values
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

## Deployment Commands

### Build and Run
```bash
# Build the image
docker-compose build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### One-time Search
```bash
# Run a single search instead of the scheduler
docker-compose run --rm halooglasi-parser python scripts/run_search.py
```

### Configuration Testing
```bash
# Test environment variable configuration
docker-compose run --rm halooglasi-parser python scripts/test_env_config.py
```

## Kubernetes Deployment

### 1. Create Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: halooglasi-credentials
type: Opaque
stringData:
  TELEGRAM_BOT_TOKEN: "your_bot_token_here"
  TELEGRAM_CHAT_ID: "your_chat_id_here"
```

### 2. Create Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: halooglasi-parser
spec:
  replicas: 1
  selector:
    matchLabels:
      app: halooglasi-parser
  template:
    metadata:
      labels:
        app: halooglasi-parser
    spec:
      containers:
      - name: halooglasi-parser
        image: halooglasi-parser:latest
        envFrom:
        - secretRef:
            name: halooglasi-credentials
        volumeMounts:
        - name: data-storage
          mountPath: /app/data
        - name: logs-storage
          mountPath: /app/logs
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
      volumes:
      - name: data-storage
        persistentVolumeClaim:
          claimName: halooglasi-data
      - name: logs-storage
        persistentVolumeClaim:
          claimName: halooglasi-logs
```

### 3. Create PersistentVolumeClaims

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: halooglasi-data
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: halooglasi-logs
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

## Cloud Deployment Examples

### AWS ECS Task Definition

```json
{
  "family": "halooglasi-parser",
  "taskRoleArn": "arn:aws:iam::account:role/ecsTaskRole",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "halooglasi-parser",
      "image": "your-account.dkr.ecr.region.amazonaws.com/halooglasi-parser:latest",
      "memory": 512,
      "cpu": 256,
      "essential": true,
      "environment": [
        {
          "name": "TELEGRAM_BOT_TOKEN",
          "valueFrom": "arn:aws:secretsmanager:region:account:secret:halooglasi/telegram-token"
        },
        {
          "name": "TELEGRAM_CHAT_ID", 
          "valueFrom": "arn:aws:secretsmanager:region:account:secret:halooglasi/chat-id"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/halooglasi-parser",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### Railway Deployment

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway add --service postgres  # Optional: if you add database features later

# Set environment variables
railway variables set TELEGRAM_BOT_TOKEN="your_token"
railway variables set TELEGRAM_CHAT_ID="your_chat_id"

# Deploy
railway up
```

### Heroku Deployment

```bash
# Create Heroku app
heroku create halooglasi-parser-app

# Set environment variables
heroku config:set TELEGRAM_BOT_TOKEN="your_token"
heroku config:set TELEGRAM_CHAT_ID="your_chat_id"

# Deploy
git push heroku main

# Scale to 1 worker (not web)
heroku ps:scale web=0 worker=1
```

## Environment Variable Security

### Best Practices

1. **Never hardcode secrets** in Docker images
2. **Use secret management** for production
3. **Rotate credentials** regularly
4. **Limit secret access** to necessary services only
5. **Monitor secret usage** and access logs

### Secret Management Options

- **Docker Swarm**: Docker secrets
- **Kubernetes**: Secrets and ConfigMaps
- **AWS**: Secrets Manager / Parameter Store
- **Azure**: Key Vault
- **GCP**: Secret Manager
- **HashiCorp**: Vault

## Monitoring and Troubleshooting

### Health Checks
```bash
# Check configuration
docker exec container_name python scripts/test_env_config.py

# View logs
docker logs container_name

# Check if Telegram is working
docker exec container_name python -c "
import sys; sys.path.append('src')
from halooglasi_parser.config_loader import config_loader
print('Valid:', config_loader.validate_telegram_config())
"
```

### Common Issues

1. **Environment variables not set**: Check container environment
2. **Volume permissions**: Ensure data/logs directories are writable
3. **Network connectivity**: Verify container can reach external APIs
4. **Resource limits**: Monitor CPU/memory usage

This setup provides a production-ready containerized deployment with secure credential management! 