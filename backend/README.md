# CI/CD Health Dashboard - Backend

FastAPI backend service for the CI/CD Health Dashboard with SQLite support and comprehensive CI/CD monitoring.

## Features

- **Real-time Monitoring**: GitHub Actions and Jenkins webhook processing
- **Metrics Dashboard**: Success rates, build times, and pipeline health
- **Alert System**: Slack and email notifications with error handling
- **SQLite First**: Local development with SQLite, production-ready for PostgreSQL
- **API Security**: Write operations protected with API keys
- **Comprehensive Testing**: Full test coverage for all endpoints

## Quick Start

### Prerequisites

- Python 3.9+
- SQLite (included with Python)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cicd-health-dashboard/backend
   ```

2. **Install dependencies**
   ```bash
   # Using uv (recommended)
   uv sync
   
   # Or using pip
   pip install -e .
   ```

3. **Initialize database**
   ```bash
   python init_db.py
   ```

4. **Run the application**
   ```bash
   # Development
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   
   # Or directly
   python -m app.main
   ```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `sqlite+aiosqlite:///./data.db` |
| `API_HOST` | API server host | `0.0.0.0` |
| `API_PORT` | API server port | `8000` |
| `DEBUG` | Enable debug mode | `false` |

## API Endpoints

### Public Endpoints
- `GET /health` - Health check
- `GET /api/metrics/summary` - Dashboard metrics
- `GET /api/builds` - List builds with pagination
- `GET /api/builds/{id}` - Build details
- `POST /api/webhook/github-actions` - GitHub Actions webhook
- `POST /api/webhook/jenkins` - Jenkins webhook

### Protected Endpoints (Require X-API-KEY header)
- `POST /api/alert/test` - Test alert delivery
- `POST /api/seed` - Seed database with sample data

### Default API Key
For development, the default API key is: `dev-write-key-change-in-production`

## Database Schema

### Core Tables
- **providers**: CI/CD provider configuration
- **builds**: Build/run information with status tracking
- **alerts**: Alert history and delivery status
- **settings**: Application configuration and API keys

### Indexes
- `idx_builds_status_started`: Performance for status queries
- `idx_builds_provider_finished`: Provider-specific queries
- `idx_builds_external_id`: External ID lookups

## Webhook Integration

### GitHub Actions
Accepts `workflow_run` events and automatically:
- Creates/updates providers
- Tracks workflow runs
- Calculates build duration
- Stores raw payload for debugging

### Jenkins
Accepts Jenkins webhook payloads and:
- Creates Jenkins providers
- Tracks build status
- Maintains build history

## Alert System

### Supported Channels
- **Slack**: Webhook-based notifications
- **Email**: SMTP-based delivery

### Error Handling
- Non-blocking: Alerts don't crash the pipeline
- Comprehensive logging
- Graceful degradation

## Development

### Running Tests
```bash
pytest
```

### Database Initialization
```bash
python init_db.py
```

### Code Formatting
```bash
black .
isort .
```

### Type Checking
```bash
mypy .
```

## Production Deployment

### Database Migration
The application is designed to work with both SQLite and PostgreSQL:

```python
# Development (SQLite)
DATABASE_URL=sqlite+aiosqlite:///./data.db

# Production (PostgreSQL)
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/dbname
```

### Environment Configuration
```bash
# Production settings
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/cicd_dashboard
DEBUG=false
API_WRITE_KEY=your-secure-production-key
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/xxx/yyy/zzz
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=alerts@company.com
SMTP_PASSWORD=app_password
```

## Architecture

The backend follows a clean, async-first architecture:

- **Models**: SQLAlchemy ORM with proper relationships
- **Schemas**: Pydantic validation and serialization
- **Dependencies**: FastAPI dependency injection
- **Alerts**: Non-blocking notification system
- **Webhooks**: Real-time CI/CD integration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the test suite
6. Submit a pull request
