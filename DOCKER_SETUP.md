# 🐳 Docker Setup for CI/CD Health Dashboard

## 🚀 Quick Start

### 1. Build and Run with Docker Compose (Recommended)

```bash
# Clone the repository
git clone <your-repo-url>
cd cicd-health-dashboard-1

# Set environment variables
export WRITE_KEY="your-secret-key-here"
export SLACK_WEBHOOK_URL="your-slack-webhook-url"  # Optional
export SMTP_HOST="smtp.gmail.com"  # Optional
export SMTP_USERNAME="your-email@gmail.com"  # Optional
export SMTP_PASSWORD="your-app-password"  # Optional

# Start the dashboard
docker-compose up -d

# View logs
docker-compose logs -f
```

### 2. Build and Run with Docker (Manual)

```bash
# Build the image
docker build -t cicd-dashboard:latest .

# Run the container
docker run -d \
  --name cicd-dashboard \
  --restart unless-stopped \
  -p 8080:80 \
  -p 8000:8000 \
  -e WRITE_KEY="your-secret-key-here" \
  -e DEBUG=false \
  cicd-dashboard:latest

# Or use the deployment script
./deploy.sh
```

## 🌐 Access Points

- **Frontend Dashboard**: http://localhost:8080
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🔐 Security Configuration

### Environment Variables

Create a `.env` file or set environment variables:

```bash
# Required
WRITE_KEY=your-secret-key-here

# Optional - Alerts
ALERTS_ENABLED=true
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
SLACK_CHANNEL=#cicd-alerts

# Optional - Email Alerts
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=your-email@gmail.com
SMTP_FROM_NAME=CI/CD Dashboard
```

## 🔗 GitHub Actions Integration

### 1. Add Repository Secrets

In your GitHub repository, go to **Settings > Secrets and variables > Actions** and add:

- `DASHBOARD_WEBHOOK_URL`: `http://your-dashboard-ip:8000/api/webhook/github-actions`
- `DASHBOARD_WRITE_KEY`: Same as your `WRITE_KEY` environment variable

### 2. Use the Provided Workflow

Copy `.github/workflows/ci-cd.yml` to your repository. This workflow will:

- Send webhooks when tests start
- Send webhooks when builds complete (success/failure)
- Send webhooks when deployments complete (success/failure)

### 3. Customize the Workflow

Modify the workflow to match your actual CI/CD pipeline:

```yaml
# Example: Add your actual build steps
- name: Build application
  run: |
    npm install
    npm run build
    # Your actual build commands
```

## 🐳 Docker Commands

### Management Commands

```bash
# View running containers
docker ps

# View logs
docker logs -f cicd-dashboard

# Stop container
docker stop cicd-dashboard

# Remove container
docker rm cicd-dashboard

# Restart container
docker restart cicd-dashboard

# View container details
docker inspect cicd-dashboard
```

### Development Commands

```bash
# Run in development mode with volume mounts
docker run -d \
  --name cicd-dashboard-dev \
  -p 8080:80 \
  -p 8000:8000 \
  -v $(pwd)/backend:/app/backend \
  -v $(pwd)/frontend:/usr/share/nginx/html \
  -e DEBUG=true \
  -e WRITE_KEY="dev-key" \
  cicd-dashboard:latest

# Build with different tags
docker build -t cicd-dashboard:v1.0.0 .
docker build -t cicd-dashboard:latest .
```

## 🚀 Production Deployment

### 1. Use Docker Compose with Production Profile

```bash
# Start with PostgreSQL
docker-compose --profile production up -d

# Use production environment file
docker-compose --env-file env.production up -d
```

### 2. Production Considerations

- **Database**: Use PostgreSQL instead of SQLite
- **HTTPS**: Configure Nginx with SSL certificates
- **Monitoring**: Add health checks and logging
- **Backup**: Set up database backups
- **Scaling**: Use Docker Swarm or Kubernetes

### 3. Production Environment File

```bash
# Copy and configure production environment
cp env.production .env
# Edit .env with your production values
```

## 🔧 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Check what's using the port
   lsof -i :8080
   lsof -i :8000
   
   # Stop conflicting services
   sudo systemctl stop nginx  # if using nginx
   ```

2. **Container Won't Start**
   ```bash
   # Check logs
   docker logs cicd-dashboard
   
   # Check container status
   docker ps -a
   ```

3. **Webhook Authentication Failed**
   - Verify `WRITE_KEY` environment variable is set
   - Check GitHub Actions secrets are configured correctly
   - Ensure webhook URL is accessible from GitHub

4. **Database Issues**
   ```bash
   # Check database connection
   curl http://localhost:8000/health
   
   # View database logs
   docker logs cicd-dashboard | grep -i database
   ```

### Debug Mode

```bash
# Run with debug enabled
docker run -d \
  --name cicd-dashboard-debug \
  -p 8080:80 \
  -p 8000:8000 \
  -e DEBUG=true \
  -e WRITE_KEY="debug-key" \
  cicd-dashboard:latest

# View detailed logs
docker logs -f cicd-dashboard-debug
```

## 📊 Monitoring

### Health Checks

The dashboard includes built-in health checks:

```bash
# Check API health
curl http://localhost:8000/health

# Check container health
docker inspect cicd-dashboard | grep Health -A 10
```

### Metrics

Monitor dashboard performance:

```bash
# Get metrics summary
curl http://localhost:8000/api/metrics/summary

# Get recent builds
curl http://localhost:8000/api/builds
```

## 🎯 Next Steps

1. **Deploy the dashboard** using Docker
2. **Configure GitHub Actions** with the provided workflow
3. **Set up repository secrets** for authentication
4. **Test webhooks** by pushing to your repository
5. **Monitor real-time data** in the dashboard
6. **Configure alerts** for build failures
7. **Scale and optimize** for production use

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Nginx Documentation](https://nginx.org/en/docs/)
