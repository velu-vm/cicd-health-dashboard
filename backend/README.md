# CI/CD Health Dashboard - Backend

FastAPI backend service for the CI/CD Health Dashboard.

## Features

- RESTful API for pipeline monitoring
- Support for GitHub Actions and Jenkins
- Real-time webhook processing
- Async database operations with SQLAlchemy
- Comprehensive testing suite
- Docker containerization

## Quick Start

### Prerequisites

- Python 3.9+
- PostgreSQL
- Redis (optional, for caching)

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

3. **Set up environment variables**
   ```bash
   cp ../../.env.example .env
   # Edit .env with your configuration
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
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://user:password@localhost:5432/cicd_dashboard` |
| `API_HOST` | API server host | `0.0.0.0` |
| `API_PORT` | API server port | `8000` |
| `DEBUG` | Enable debug mode | `false` |
| `GITHUB_TOKEN` | GitHub API token | - |
| `JENKINS_URL` | Jenkins server URL | - |
| `JENKINS_USERNAME` | Jenkins username | - |
| `JENKINS_API_TOKEN` | Jenkins API token | - |

## API Endpoints

### Health Check
- `GET /health` - Health check endpoint

### Alerts
- `GET /api/v1/alerts` - List all alerts
- `GET /api/v1/alerts/{alert_id}` - Get specific alert
- `POST /api/v1/alerts` - Create new alert
- `PUT /api/v1/alerts/{alert_id}` - Update alert
- `DELETE /api/v1/alerts/{alert_id}` - Delete alert

### Documentation
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /openapi.json` - OpenAPI schema

## Development

### Running Tests
```bash
pytest
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

### Linting
```bash
flake8 .
```

## Docker

Build and run with Docker:

```bash
# Build image
docker build -f ../../ops/docker/backend.Dockerfile -t cicd-dashboard-backend .

# Run container
docker run -p 8000:8000 cicd-dashboard-backend
```

## Architecture

The backend follows a clean architecture pattern:

- **Models**: SQLAlchemy ORM models for database entities
- **Schemas**: Pydantic models for API validation
- **Providers**: External service integrations (GitHub Actions, Jenkins)
- **Dependencies**: FastAPI dependency injection utilities
- **Utils**: Common utility functions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the test suite
6. Submit a pull request
