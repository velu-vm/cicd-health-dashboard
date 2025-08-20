# CI/CD Health Dashboard

A comprehensive dashboard for monitoring and visualizing the health of CI/CD pipelines across multiple providers including GitHub Actions and Jenkins.

## Features

- Real-time monitoring of CI/CD pipeline health
- Support for GitHub Actions and Jenkins
- Webhook integration for instant updates
- Historical data tracking and analytics
- Modern React frontend with Tailwind CSS
- FastAPI backend with async processing
- Background worker for polling and scheduling

## Quick Start

### Development

```bash
# Start all services
make dev

# Or start individually
docker-compose -f ops/compose.dev.yml up backend
docker-compose -f ops/compose.dev.yml up frontend
docker-compose -f ops/compose.dev.yml up worker
```

### Production

```bash
docker-compose -f ops/compose.prod.yml up -d
```

## Architecture

- **Backend**: FastAPI application with SQLAlchemy ORM
- **Frontend**: React + Vite + Tailwind CSS
- **Worker**: Background service for polling CI/CD providers
- **Database**: PostgreSQL with async support
- **Message Queue**: Redis for job processing

## License

MIT License - see LICENSE file for details.

Copyright (c) 2024 CI/CD Health Dashboard Contributors
