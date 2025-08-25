# 🚀 CI/CD Health Dashboard

A comprehensive dashboard for monitoring CI/CD pipeline health with real-time email notifications, webhook processing, and automated alerting.

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Environment Setup](#-environment-setup)
- [GitHub Actions Configuration](#-github-actions-configuration)
- [Email Notifications](#-email-notifications)
- [API Endpoints](#-api-endpoints)
- [Evaluation Guide](#-evaluation-guide)
- [Troubleshooting](#-troubleshooting)

## ✨ Features

- **Real-time Pipeline Monitoring** - Track CI/CD pipeline status in real-time
- **Automated Email Alerts** - Get notified instantly for pipeline success/failure
- **Webhook Integration** - Receive updates from GitHub Actions automatically
- **Modern Dashboard UI** - Clean, responsive interface for monitoring
- **Multi-Provider Support** - GitHub Actions, GitLab CI, Jenkins, and more
- **Database Persistence** - SQLite database for build history and metrics
- **RESTful API** - Full API for integration and automation

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────────────────────────────┐    ┌─────────────────┐
│   GitHub        │    │           Backend Server                │    │   Email         │
│   Actions       │───▶│         (FastAPI + Frontend)           │───▶│   Notifications │
│   (Webhooks)    │    │         Port: 8000                     │    │   (SMTP)        │
└─────────────────┘    │  ┌─────────────┐  ┌─────────────────┐ │    └─────────────────┘
                       │  │  Frontend   │  │   REST API      │ │
                       │  │  Dashboard  │  │   Endpoints     │ │
                       │  │  (HTML/JS)  │  │   (/api/*)      │ │
                       │  └─────────────┘  └─────────────────┘ │
                       └─────────────────────────────────────────┘
```

**Note**: The backend FastAPI server serves both the frontend dashboard and provides REST API endpoints on the same port (8000).

### Frontend & Backend Details
- **Frontend**: Single-page dashboard served by backend at `http://localhost:8000`
- **Backend**: FastAPI server that serves both frontend and API at `http://localhost:8000`
- **Port**: Single port 8000 serves everything
- **Database**: SQLite database with async SQLAlchemy
- **Real-time Updates**: Auto-refresh every 15 seconds
- **Architecture**: Backend serves frontend HTML + provides REST API endpoints

## 📋 Prerequisites

- **Python 3.11+** - Backend runtime
- **Git** - Version control
- **GitHub Account** - For repository and secrets
- **Gmail Account** - For SMTP email notifications (with App Password)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/velu-vm/cicd-health-dashboard.git
cd cicd-health-dashboard
```

### 2. Run Setup Script
```bash
./setup.sh
```

This script will:
- ✅ Set up Python virtual environment
- ✅ Install all dependencies
- ✅ Create configuration files
- ✅ Start the dashboard server
- ✅ Test all functionality

### 3. Access the Dashboard
- **Frontend Dashboard**: http://localhost:8000
- **Backend API**: http://localhost:8000/api
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Builds Endpoint**: http://localhost:8000/api/builds
- **Metrics Endpoint**: http://localhost:8000/api/metrics/summary

## ⚙️ Environment Setup

### 1. Create Environment File
The setup script will create a `.env` file automatically, or you can create it manually:

```bash
# Database Configuration
DATABASE_URL=sqlite+aiosqlite:///./data.db
DEBUG=true

# Server Configuration
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=["http://localhost:8080", "http://localhost:3000"]

# Security Configuration
SECRET_KEY=your-secret-key-here
WRITE_KEY=your-write-key-here
GITHUB_WEBHOOK_SECRET=your-github-webhook-secret

# Email Configuration
ALERTS_ENABLED=true
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-gmail-app-password
SMTP_FROM_EMAIL=noreply@cicd-dashboard.com
SMTP_FROM_NAME=CI/CD Dashboard

# Monitoring Configuration
METRICS_ENABLED=true
HEALTH_CHECK_INTERVAL=30
RATE_LIMIT_MAX_REQUESTS=100
RATE_LIMIT_WINDOW_SECONDS=60
```

### 2. Gmail App Password Setup
For email notifications to work:

1. **Enable 2-Factor Authentication** on your Google account
2. **Generate App Password**:
   - Go to Google Account → Security → App passwords
   - Select "Mail" and generate password
   - Use this 16-character password in `SMTP_PASSWORD`

## 🔧 GitHub Actions Configuration

### 1. Required Secrets
Add these secrets in your GitHub repository (Settings → Secrets and variables → Actions):

```bash
# SMTP Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-gmail-app-password
SMTP_FROM_EMAIL=noreply@cicd-dashboard.com
SMTP_FROM_NAME=CI/CD Dashboard

# Email Recipients
ALERT_DEFAULT_RECIPIENT=your-email@gmail.com
ALERT_TEST_RECIPIENT=your-email@gmail.com

# Dashboard Configuration (Optional - for webhooks)
DASHBOARD_WEBHOOK_URL=https://your-public-url.com
DASHBOARD_WRITE_KEY=your-write-key

# Docker Configuration (Optional)
DOCKERUSER=your-docker-username
DOCKERPASS=your-docker-password
```

### 2. Workflow Features
The GitHub Actions workflow automatically:

- ✅ **Sends email notifications** for pipeline start/success/failure
- ✅ **Builds Docker images** (if Docker secrets configured)
- ✅ **Deploys to production** (if Docker secrets configured)
- ✅ **Sends webhooks** to dashboard (if webhook URL configured)

## 📧 Email Notifications

### Automatic Email Triggers
- 🚀 **Pipeline Started** - When CI/CD workflow begins
- ✅ **Pipeline Success** - When all tests pass
- ❌ **Pipeline Failure** - When tests fail
- 🐳 **Build Success/Failure** - Docker build status
- 🚀 **Deployment Success/Failure** - Production deployment status

### Email Content
Each email includes:
- Repository name and branch
- Commit SHA and author
- Pipeline URL for detailed logs
- Status-specific information
- Professional formatting

## 🌐 Quick Access Links

### Local Development URLs
- **Main Dashboard**: http://localhost:8000 (Frontend + Backend)
- **API Endpoints**: http://localhost:8000/api/* (Backend API)
- **Interactive API Docs**: http://localhost:8000/docs (Backend Documentation)
- **Health Status**: http://localhost:8000/health (Backend Health Check)

### Key API Endpoints
- **Builds List**: http://localhost:8000/api/builds
- **Metrics Summary**: http://localhost:8000/api/metrics/summary
- **Test Alert**: http://localhost:8000/api/alert/test
- **Webhook Receiver**: http://localhost:8000/api/webhook/github-actions

## 🔌 API Endpoints

### Core Endpoints
- `GET /health` - Health check and system status
- `GET /` - Dashboard frontend
- `GET /api/docs` - Interactive API documentation

### Build Management
- `GET /api/builds` - List all builds
- `POST /api/seed` - Seed database with sample data
- `GET /api/metrics/summary` - Pipeline metrics and statistics

### Webhook Processing
- `POST /api/webhook/github-actions` - GitHub Actions webhook receiver

### Alert System
- `POST /api/alert/test` - Test email alert system

## 🧪 Testing the Application

### Quick Test Commands
```bash
# Test Frontend Dashboard
curl http://localhost:8000

# Test Backend Health
curl http://localhost:8000/health

# Test API Endpoints
curl http://localhost:8000/api/builds
curl http://localhost:8000/api/metrics/summary

# Test Email Alert System
curl -X POST "http://localhost:8000/api/alert/test" \
  -H "Content-Type: application/json" \
  -d '{"message": "Test alert", "severity": "info"}'
```

## 📊 Evaluation Guide

### 1. Setup Verification
```bash
# Run the setup script
./setup.sh

# Verify all components are working
curl http://localhost:8000/health
```

**Expected Results:**
- ✅ Virtual environment created and activated
- ✅ All dependencies installed successfully
- ✅ Server starts without errors
- ✅ Health check returns `{"ok": true}`

### 2. Email System Testing
```bash
# Test email functionality
curl -X POST "http://localhost:8000/api/alert/test" \
  -H "Content-Type: application/json" \
  -d '{"message": "Test alert", "severity": "info"}'
```

**Expected Results:**
- ✅ Email sent successfully
- ✅ Response: `{"success": true, "message": "Alert test completed successfully"}`

### 3. Webhook Processing
```bash
# Test webhook processing
curl -X POST "http://localhost:8000/api/webhook/github-actions" \
  -H "Authorization: Bearer YOUR_WRITE_KEY" \
  -H "Content-Type: application/json" \
  -d '{"workflow_run": {"id": "test123", "conclusion": "success"}}'
```

**Expected Results:**
- ✅ Webhook processed successfully
- ✅ Build created in database
- ✅ Email notification triggered

### 4. GitHub Actions Integration
1. **Make a git push** to trigger the workflow
2. **Check GitHub Actions tab** for workflow execution
3. **Verify email notifications** are received
4. **Check dashboard** for real-time updates

**Expected Results:**
- ✅ Pipeline runs successfully
- ✅ Email notifications sent automatically
- ✅ Dashboard shows pipeline status

### 5. Dashboard Functionality
- **Access dashboard**: http://localhost:8000
- **Check build history**: View recent pipeline runs
- **Monitor metrics**: Success rates, build times, etc.
- **Real-time updates**: Auto-refresh every 15 seconds

## 🐛 Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Check what's using port 8000
lsof -i :8000

# Kill the process
kill $(lsof -ti :8000)
```

#### 2. Email Not Working
- ✅ Verify `ALERTS_ENABLED=true` in `.env`
- ✅ Check SMTP credentials are correct
- ✅ Ensure Gmail App Password is used (not regular password)
- ✅ Verify 2FA is enabled on Google account

#### 3. Dependencies Not Found
```bash
# Activate virtual environment
source .venv/bin/activate

# Reinstall dependencies
pip install -r backend/requirements.txt
pip install -r worker/requirements.txt
```

#### 4. Database Issues
```bash
# Remove existing database
rm -f data.db

# Restart server to recreate database
python run_server.py
```

### Debug Mode
Enable debug logging by setting `DEBUG=true` in `.env` file.

## 📁 Project Structure

```
cicd-health-dashboard/
├── .github/workflows/          # GitHub Actions workflows
├── backend/                    # FastAPI backend application
│   ├── app/                   # Main application code
│   ├── models.py              # Database models
│   ├── schemas.py             # Pydantic schemas
│   └── requirements.txt       # Python dependencies
├── frontend/                   # Dashboard frontend
│   ├── dashboard.js           # Main dashboard logic
│   ├── styles.css             # Dashboard styling
│   └── index.html             # Dashboard HTML
├── worker/                     # Background worker processes
├── setup.sh                    # Main setup script
├── deploy.sh                   # Production deployment script
├── .env                        # Environment configuration
└── README.md                   # This file
```

## 🚀 Production Deployment

### Using Docker
```bash
# Build and run with Docker
docker build -t cicd-dashboard .
docker run -p 8000:8000 cicd-dashboard
```

### Using deploy.sh
```bash
# Run production deployment
./deploy.sh
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
- Check the troubleshooting section above
- Review GitHub Actions logs
- Check server logs for error details
- Ensure all environment variables are set correctly

---

**🎯 Ready to monitor your CI/CD pipelines with real-time email notifications!**
