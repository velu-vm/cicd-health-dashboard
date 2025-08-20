# CI/CD Health Dashboard

A comprehensive monitoring and visualization platform for CI/CD pipeline health using GitHub Actions. Built with FastAPI, React, and modern DevOps practices.

## Features

- **📊 Real-time Monitoring**: GitHub Actions webhook processing with instant updates
- **📈 Metrics Dashboard**: Success rates, build times, and pipeline health visualization
- **🔔 Email Alert System**: Automatic alerts for failed builds with debouncing
- **🔄 Background Polling**: Worker service for continuous monitoring
- **📱 Responsive UI**: Modern React frontend with Tailwind CSS
- **🔒 API Security**: Write operations protected with API keys
- **🐳 Docker Ready**: Complete containerization for development and production
- **📊 SQLite First**: Local development with SQLite, production-ready for PostgreSQL

## Quick Start

### Prerequisites

- **Backend**: Python 3.9+, SQLite
- **Frontend**: Node.js 18+, npm
- **Docker**: Docker and Docker Compose (optional)

### Option 1: Docker (Recommended)

1. **Clone and navigate**
   ```bash
   git clone <repository-url>
   cd cicd-health-dashboard
   ```

2. **Start development environment**
   ```bash
   cd ops
   make dev-up
   ```

3. **Seed the database**
   ```bash
   make seed
   ```

4. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Option 2: Manual Setup

1. **Backend Setup**
   ```bash
   cd backend
   pip install -e .
   python init_db.py
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **Worker Setup** (Optional)
   ```bash
   cd worker
   pip install -r requirements.txt
   python run_scheduler.py
   ```

## Verification

After starting the services, verify that everything is working correctly using the verification script:

```bash
# Make sure the backend is running first
./scripts/verify.sh
```

The verification script tests:
- ✅ **Health Check**: `GET /health` endpoint responsiveness
- ✅ **Database Seeding**: `POST /api/seed` with API key authentication
- ✅ **Metrics Summary**: `GET /api/metrics/summary` data format
- ✅ **Builds List**: `GET /api/builds?limit=5` pagination

**Expected Output:**
```
🔍 CI/CD Health Dashboard API Verification
==========================================
API Base URL: http://localhost:8000
API Key: dev-write-key-change-in-production

1️⃣  Testing Health Check Endpoint...
   GET http://localhost:8000/health
✅ PASS: Health check endpoint is responding correctly

2️⃣  Testing Database Seeding...
   POST http://localhost:8000/api/seed
✅ PASS: Database seeding completed successfully

3️⃣  Testing Metrics Summary Endpoint...
   GET http://localhost:8000/api/metrics/summary
✅ PASS: Metrics summary endpoint is responding correctly

4️⃣  Testing Builds List Endpoint...
   GET http://localhost:8000/api/builds?limit=5
✅ PASS: Builds list endpoint is responding correctly

🎉 All API verification tests PASSED!
```

**Troubleshooting:**
- Ensure the backend is running on port 8000
- Check that the API key is correct
- Verify database initialization completed successfully
- Install `jq` for formatted JSON output: `brew install jq` (macOS) or `apt-get install jq` (Ubuntu)

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │     Worker      │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   (Polling)     │
│   Port 5173     │    │   Port 8000     │    │   Background    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       ▼                       │
         │              ┌─────────────────┐              │
         │              │   Database      │              │
         │              │   (SQLite)      │              │
         │              └─────────────────┘              │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   GitHub        │    │   Email         │    │   Metrics       │
│   Actions       │    │   Alerts        │    │   Dashboard     │
│   Webhooks      │    │   (SMTP)        │    │   (Real-time)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## API Endpoints

### Public Endpoints
- `GET /health` - Health check
- `GET /api/metrics/summary` - Dashboard metrics
- `GET /api/builds` - List builds with pagination
- `GET /api/builds/{id}` - Build details
- `POST /api/webhook/github-actions` - GitHub Actions webhook

### Protected Endpoints (Require X-API-KEY header)
- `POST /api/alert/test` - Test email alert delivery
- `POST /api/seed` - Seed database with sample data

### Default API Key
For development: `dev-write-key-change-in-production`

## Environment Configuration

### Backend Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `sqlite+aiosqlite:///./data.db` |
| `API_HOST` | API server host | `0.0.0.0` |
| `API_PORT` | API server port | `8000` |
| `DEBUG` | Enable debug mode | `false` |
| `ALERTS_ENABLED` | Enable/disable email alerts | `true` |
| `SMTP_HOST` | SMTP server hostname | Required |
| `SMTP_PORT` | SMTP server port | `587` |
| `SMTP_USERNAME` | SMTP username/email | Required |
| `SMTP_PASSWORD` | SMTP password or app password | Required |

### Frontend Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_BASE` | Backend API base URL | `http://localhost:8000` |

### Worker Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `ENABLE_GH` | Enable GitHub Actions polling | `true` |
| `GITHUB_TOKEN` | GitHub personal access token | Required |
| `GITHUB_REPOS` | Comma-separated repository list | Required |
| `WORKER_POLL_INTERVAL` | Polling interval in seconds | `60` |
| `DASHBOARD_API_KEY` | API key for backend access | Required |

## Development

### Available Make Commands

```bash
cd ops

# Development
make dev-up          # Start development environment
make dev-down        # Stop development environment
make dev-logs        # View development logs
make restart         # Restart development services

# Production
make prod-up         # Start production environment
make prod-down       # Stop production environment
make prod-logs       # View production logs
make build           # Build all Docker images

# Database & API
make seed            # Seed database with sample data
make alert-test      # Test email alert system

# Utilities
make clean           # Clean up containers and volumes
make status          # Show service status
make help            # Show all available commands
```

### Code Organization

```
├── backend/                 # FastAPI backend
│   ├── app/                # Application code
│   │   ├── main.py         # FastAPI app and routes
│   │   ├── models.py       # SQLAlchemy models
│   │   ├── schemas.py      # Pydantic schemas
│   │   ├── alerts.py       # Email alert system
│   │   └── providers/      # CI/CD provider integrations
│   ├── tests/              # Test suite
│   └── pyproject.toml      # Python dependencies
├── frontend/               # React frontend
│   ├── src/                # Source code
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # Page components
│   │   └── services/       # API communication
│   └── package.json        # Node.js dependencies
├── worker/                 # Background polling service
│   ├── poller.py           # CI/CD provider polling
│   ├── scheduler.py        # Task scheduling
│   └── requirements.txt    # Python dependencies
├── ops/                    # Operations and deployment
│   ├── docker/             # Docker configurations
│   ├── compose.dev.yml     # Development environment
│   ├── compose.prod.yml    # Production environment
│   └── Makefile            # Operations commands
└── scripts/                # Utility scripts
    └── verify.sh           # API verification script
```

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

### API Verification
```bash
./scripts/verify.sh
```

## Deployment

### Development
```bash
cd ops
make dev-up
```

### Production
```bash
cd ops
make build
make prod-up
```

### Environment Configuration
1. Copy environment examples:
   ```bash
   cp ops/.env.example ops/.env
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env
   ```

2. Configure production values:
   - SMTP settings for email alerts
   - GitHub token for repository access
   - Secure API keys
   - Database connection strings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the verification script
6. Submit a pull request

## Troubleshooting

### Common Issues

**Backend won't start:**
- Check Python version (3.9+)
- Verify dependencies are installed
- Check port 8000 is available

**Frontend won't build:**
- Ensure Node.js 18+ is installed
- Clear node_modules and reinstall
- Check Tailwind CSS configuration

**Database errors:**
- Run `python init_db.py` to initialize
- Check file permissions for SQLite
- Verify DATABASE_URL configuration

**API verification fails:**
- Ensure backend is running on port 8000
- Check API key configuration
- Verify database is seeded

### Getting Help

- Check the logs: `make dev-logs` or `make prod-logs`
- Verify API endpoints: `./scripts/verify.sh`
- Review environment configuration
- Check service status: `make status`

## License

MIT License - see LICENSE file for details.

---

Built with ❤️ using FastAPI, React, and modern DevOps practices.
