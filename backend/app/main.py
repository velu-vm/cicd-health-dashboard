from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import os
import sqlite3
from datetime import datetime, timedelta
from typing import Optional, List
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from .db import init_db, get_db
from .models import Provider, Build, Alert, Settings
from .schemas import (
    MetricsSummary, BuildListResponse, Build as BuildSchema,
    GitHubWebhookPayload, JenkinsWebhookPayload,
    AlertTestRequest, AlertTestResponse, SeedRequest, SeedResponse
)
from .deps import get_pagination_params, verify_write_key
from .alerts import send_alert

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    pass

app = FastAPI(
    title="CI/CD Health Dashboard API",
    description="API for monitoring CI/CD pipeline health",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"ok": True}

@app.get("/api/metrics/summary", response_model=MetricsSummary)
async def get_metrics_summary(session: AsyncSession = Depends(get_db)):
    """Get dashboard summary metrics"""
    try:
        # Get total builds
        result = await session.execute(select(func.count(Build.id)))
        total_builds = result.scalar() or 0
        
        # Get builds from last 7 days
        seven_days_ago = datetime.now() - timedelta(days=7)
        result = await session.execute(
            select(func.count(Build.id)).where(Build.created_at >= seven_days_ago)
        )
        builds_last_7d = result.scalar() or 0
        
        # Get failed builds from last 7 days
        result = await session.execute(
            select(func.count(Build.id)).where(
                and_(Build.created_at >= seven_days_ago, Build.status == "failed")
            )
        )
        failed_builds_last_7d = result.scalar() or 0
        
        # Calculate success rate
        success_rate = 0.0
        if builds_last_7d > 0:
            success_rate = (builds_last_7d - failed_builds_last_7d) / builds_last_7d
        
        # Get average build time for completed builds
        result = await session.execute(
            select(func.avg(Build.duration_seconds)).where(
                and_(Build.status.in_(["success", "failed"]), Build.duration_seconds.isnot(None))
            )
        )
        avg_build_time = result.scalar()
        
        # Get last build status
        result = await session.execute(
            select(Build.status).order_by(Build.created_at.desc()).limit(1)
        )
        last_build_status = result.scalar()
        
        return MetricsSummary(
            total_builds=total_builds,
            success_rate=success_rate,
            failure_rate=1.0 - success_rate,
            avg_build_time=avg_build_time,
            last_build_status=last_build_status,
            builds_last_7d=builds_last_7d,
            failed_builds_last_7d=failed_builds_last_7d
        )
        
    except Exception as e:
        # Return default values if database query fails
        return MetricsSummary()

@app.get("/api/builds", response_model=BuildListResponse)
async def get_builds(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    status: Optional[str] = None,
    provider: Optional[str] = None,
    session: AsyncSession = Depends(get_db)
):
    """Get list of builds with pagination and filters"""
    try:
        # Build query
        query = select(Build)
        
        if status:
            query = query.where(Build.status == status)
        if provider:
            query = query.join(Provider).where(Provider.kind == provider)
        
        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        result = await session.execute(count_query)
        total = result.scalar() or 0
        
        # Get paginated results
        query = query.offset(offset).limit(limit)
        result = await session.execute(query)
        builds = result.scalars().all()
        
        # Convert to response models
        build_schemas = []
        for build in builds:
            build_data = {
                "id": build.id,
                "external_id": build.external_id,
                "status": build.status,
                "branch": build.branch,
                "commit_sha": build.commit_sha,
                "triggered_by": build.triggered_by,
                "url": build.url,
                "provider_id": build.provider_id,
                "duration_seconds": build.duration_seconds,
                "started_at": build.started_at,
                "finished_at": build.finished_at,
                "raw_payload": build.raw_payload,
                "created_at": build.created_at,
                "provider_name": build.provider.name if build.provider else None,
                "provider_kind": build.provider.kind if build.provider else None
            }
            build_schemas.append(BuildSchema(**build_data))
        
        return BuildListResponse(
            builds=build_schemas,
            total=total,
            limit=limit,
            offset=offset,
            has_more=offset + limit < total
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch builds: {str(e)}"
        )

@app.get("/api/builds/{build_id}", response_model=BuildSchema)
async def get_build(build_id: int, session: AsyncSession = Depends(get_db)):
    """Get detailed build information"""
    try:
        result = await session.execute(
            select(Build).where(Build.id == build_id)
        )
        build = result.scalar_one_or_none()
        
        if not build:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Build not found"
            )
        
        build_data = {
            "id": build.id,
            "external_id": build.external_id,
            "status": build.status,
            "branch": build.branch,
            "commit_sha": build.commit_sha,
            "triggered_by": build.triggered_by,
            "url": build.url,
            "provider_id": build.provider_id,
            "duration_seconds": build.duration_seconds,
            "started_at": build.started_at,
            "finished_at": build.finished_at,
            "raw_payload": build.raw_payload,
            "created_at": build.created_at,
            "provider_name": build.provider.name if build.provider else None,
            "provider_kind": build.provider.kind if build.provider else None
        }
        
        return BuildSchema(**build_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch build: {str(e)}"
        )

@app.post("/api/webhook/github-actions")
async def github_webhook(
    payload: GitHubWebhookPayload,
    session: AsyncSession = Depends(get_db)
):
    """Handle GitHub Actions webhook"""
    try:
        # Extract workflow run data
        workflow_run = payload.workflow_run
        repository = payload.repository
        
        # Get or create provider
        provider_name = f"github-{repository['full_name']}"
        result = await session.execute(
            select(Provider).where(Provider.name == provider_name)
        )
        provider = result.scalar_one_or_none()
        
        if not provider:
            provider = Provider(
                name=provider_name,
                kind="github_actions",
                config_json={"repository": repository['full_name']}
            )
            session.add(provider)
            await session.commit()
            await session.refresh(provider)
        
        # Create or update build
        external_id = str(workflow_run['id'])
        result = await session.execute(
            select(Build).where(
                and_(Build.provider_id == provider.id, Build.external_id == external_id)
            )
        )
        build = result.scalar_one_or_none()
        
        if build:
            # Update existing build
            build.status = workflow_run['conclusion'] or workflow_run['status']
            build.duration_seconds = None
            if workflow_run.get('run_started_at') and workflow_run.get('updated_at'):
                start_time = datetime.fromisoformat(workflow_run['run_started_at'].replace('Z', '+00:00'))
                end_time = datetime.fromisoformat(workflow_run['updated_at'].replace('Z', '+00:00'))
                build.started_at = start_time
                build.finished_at = end_time
                build.duration_seconds = int((end_time - start_time).total_seconds())
            build.raw_payload = payload.dict()
        else:
            # Create new build
            build = Build(
                provider_id=provider.id,
                external_id=external_id,
                status=workflow_run['conclusion'] or workflow_run['status'],
                branch=workflow_run.get('head_branch', 'main'),
                commit_sha=workflow_run.get('head_sha'),
                triggered_by=workflow_run.get('actor', {}).get('login'),
                url=workflow_run.get('html_url'),
                raw_payload=payload.dict()
            )
            session.add(build)
        
        await session.commit()
        return {"status": "processed"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process webhook: {str(e)}"
        )

@app.post("/api/webhook/jenkins")
async def jenkins_webhook(
    payload: JenkinsWebhookPayload,
    session: AsyncSession = Depends(get_db)
):
    """Handle Jenkins webhook"""
    try:
        # Get or create provider
        provider_name = f"jenkins-{payload.name}"
        result = await session.execute(
            select(Provider).where(Provider.name == provider_name)
        )
        provider = result.scalar_one_or_none()
        
        if not provider:
            provider = Provider(
                name=provider_name,
                kind="jenkins",
                config_json={"url": payload.url}
            )
            session.add(provider)
            await session.commit()
            await session.refresh(provider)
        
        # Create or update build
        build_data = payload.build
        external_id = str(build_data.get('number', build_data.get('id')))
        
        result = await session.execute(
            select(Build).where(
                and_(Build.provider_id == provider.id, Build.external_id == external_id)
            )
        )
        build = result.scalar_one_or_none()
        
        if build:
            # Update existing build
            build.status = build_data.get('result', 'unknown')
            build.raw_payload = payload.dict()
        else:
            # Create new build
            build = Build(
                provider_id=provider.id,
                external_id=external_id,
                status=build_data.get('result', 'unknown'),
                url=build_data.get('url'),
                raw_payload=payload.dict()
            )
            session.add(build)
        
        await session.commit()
        return {"status": "processed"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process webhook: {str(e)}"
        )

@app.post("/api/alert/test", response_model=AlertTestResponse)
async def test_alert(
    request: AlertTestRequest,
    session: AsyncSession = Depends(get_db),
    _: bool = Depends(verify_write_key)
):
    """Test alert delivery"""
    try:
        # Get settings
        result = await session.execute(select(Settings).where(Settings.id == 1))
        settings = result.scalar_one_or_none()
        
        if not settings:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Settings not configured"
            )
        
        if not settings.alert_email or not all([settings.smtp_host, settings.smtp_port, settings.smtp_username, settings.smtp_password]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email configuration not complete"
            )
        
        # Send test email
        smtp_config = {
            "host": settings.smtp_host,
            "port": settings.smtp_port,
            "username": settings.smtp_username,
            "password": settings.smtp_password
        }
        
        success = await send_alert(
            request.message,
            smtp_config,
            settings.alert_email
        )
        
        return AlertTestResponse(
            success=success,
            message=f"Alert sent via email to {settings.alert_email}",
            channel="email"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send test alert: {str(e)}"
        )

@app.post("/api/seed", response_model=SeedResponse)
async def seed_database(
    request: SeedRequest,
    session: AsyncSession = Depends(get_db),
    _: bool = Depends(verify_write_key)
):
    """Seed database with sample data"""
    try:
        providers_created = 0
        builds_created = 0
        
        # Create providers if specified
        if request.providers:
            for provider_data in request.providers:
                provider = Provider(**provider_data)
                session.add(provider)
                providers_created += 1
        
        # Create builds if specified
        if request.builds:
            for build_data in request.builds:
                build = Build(**build_data)
                session.add(build)
                builds_created += 1
        
        await session.commit()
        
        return SeedResponse(
            success=True,
            message=f"Database seeded successfully",
            providers_created=providers_created,
            builds_created=builds_created
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to seed database: {str(e)}"
        )

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "CI/CD Health Dashboard API",
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=os.getenv("DEBUG", "false").lower() == "true"
    )
