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
    GitHubWebhookPayload,
    AlertTestRequest, AlertTestResponse, SeedRequest, SeedResponse
)
from .deps import get_pagination_params, verify_write_key
from .alerts import send_alert, send_build_failure_alert
from .providers.github_actions import GitHubActionsProvider

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    pass

app = FastAPI(
    title="CI/CD Health Dashboard API",
    description="API for monitoring CI/CD pipeline health using GitHub Actions",
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

# Initialize GitHub Actions provider
github_provider = GitHubActionsProvider()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"ok": True}

@app.get("/api/metrics/summary", response_model=MetricsSummary)
async def get_metrics_summary(session: AsyncSession = Depends(get_db)):
    """Get dashboard summary metrics for the last 7 days"""
    try:
        # Calculate time window: last 7 days from now
        now = datetime.now()
        seven_days_ago = now - timedelta(days=7)
        
        # Get builds started in the last 7 days
        result = await session.execute(
            select(func.count(Build.id)).where(Build.started_at >= seven_days_ago)
        )
        builds_in_window = result.scalar() or 0
        
        # Get completed builds (success + failed) in the last 7 days
        result = await session.execute(
            select(func.count(Build.id)).where(
                and_(
                    Build.started_at >= seven_days_ago,
                    Build.status.in_(["success", "failed"]),
                    Build.finished_at.isnot(None)
                )
            )
        )
        completed_builds = result.scalar() or 0
        
        # Get successful builds in the last 7 days
        result = await session.execute(
            select(func.count(Build.id)).where(
                and_(
                    Build.started_at >= seven_days_ago,
                    Build.status == "success",
                    Build.finished_at.isnot(None)
                )
            )
        )
        successful_builds = result.scalar() or 0
        
        # Get failed builds in the last 7 days
        result = await session.execute(
            select(func.count(Build.id)).where(
                and_(
                    Build.started_at >= seven_days_ago,
                    Build.status == "failed",
                    Build.finished_at.isnot(None)
                )
            )
        )
        failed_builds = result.scalar() or 0
        
        # Calculate success and failure rates
        success_rate = 0.0
        failure_rate = 0.0
        if completed_builds > 0:
            success_rate = successful_builds / completed_builds
            failure_rate = failed_builds / completed_builds
        
        # Get average build time for completed builds in the last 7 days
        result = await session.execute(
            select(func.avg(Build.duration_seconds)).where(
                and_(
                    Build.started_at >= seven_days_ago,
                    Build.status.in_(["success", "failed"]),
                    Build.finished_at.isnot(None),
                    Build.duration_seconds.isnot(None)
                )
            )
        )
        avg_build_time_seconds = result.scalar()
        
        # Get last build status (most recently started build)
        result = await session.execute(
            select(Build.status).order_by(Build.started_at.desc()).limit(1)
        )
        last_build_status = result.scalar()
        
        return MetricsSummary(
            window_days=7,
            success_rate=success_rate,
            failure_rate=failure_rate,
            avg_build_time_seconds=avg_build_time_seconds,
            last_build_status=last_build_status,
            last_updated=now.isoformat()
        )
        
    except Exception as e:
        # Return default values if database query fails
        return MetricsSummary(
            window_days=7,
            success_rate=0.0,
            failure_rate=0.0,
            avg_build_time_seconds=None,
            last_build_status=None,
            last_updated=datetime.now().isoformat()
        )

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
        # Parse the webhook payload using the provider
        parsed_data = github_provider.parse_workflow_run(payload.dict())
        
        # Get or create provider
        repository = payload.repository
        provider_name = f"github-{repository.full_name}"
        result = await session.execute(
            select(Provider).where(Provider.name == provider_name)
        )
        provider = result.scalar_one_or_none()
        
        if not provider:
            provider = Provider(
                name=provider_name,
                kind="github_actions",
                config_json={"repository": repository.full_name}
            )
            session.add(provider)
            await session.commit()
            await session.refresh(provider)
        
        # Create or update build
        external_id = parsed_data["external_id"]
        result = await session.execute(
            select(Build).where(
                and_(Build.provider_id == provider.id, Build.external_id == external_id)
            )
        )
        build = result.scalar_one_or_none()
        
        if build:
            # Update existing build
            build.status = parsed_data["status"]
            build.duration_seconds = parsed_data["duration_seconds"]
            build.started_at = parsed_data["started_at"]
            build.finished_at = parsed_data["finished_at"]
            build.raw_payload = parsed_data["raw_payload"]
            
            # Check if this is a newly failed build that needs alerting
            if (build.status == "failed" and 
                build.finished_at and 
                not build.finished_at == build.started_at):  # Ensure it's actually finished
                
                # Get settings for alerting
                settings_result = await session.execute(
                    select(Settings).where(Settings.id == 1)
                )
                settings = settings_result.scalar_one_or_none()
                
                if settings and settings.alert_email:
                    # Prepare build data for alert
                    build_data = {
                        "id": build.id,
                        "external_id": build.external_id,
                        "status": build.status,
                        "branch": build.branch,
                        "duration_seconds": build.duration_seconds,
                        "url": build.url,
                        "provider_name": provider.name
                    }
                    
                    # Send alert (non-blocking)
                    await send_build_failure_alert(
                        build_data,
                        {"alert_email": settings.alert_email},
                        session
                    )
        else:
            # Create new build
            build = Build(
                provider_id=provider.id,
                external_id=external_id,
                status=parsed_data["status"],
                duration_seconds=parsed_data["duration_seconds"],
                branch=parsed_data["branch"],
                commit_sha=parsed_data["commit_sha"],
                triggered_by=parsed_data["triggered_by"],
                started_at=parsed_data["started_at"],
                finished_at=parsed_data["finished_at"],
                url=parsed_data["url"],
                raw_payload=parsed_data["raw_payload"]
            )
            session.add(build)
            await session.commit()
            await session.refresh(build)
            
            # Check if this is a failed build that needs alerting
            if (build.status == "failed" and 
                build.finished_at and 
                not build.finished_at == build.started_at):
                
                # Get settings for alerting
                settings_result = await session.execute(
                    select(Settings).where(Settings.id == 1)
                )
                settings = settings_result.scalar_one_or_none()
                
                if settings and settings.alert_email:
                    # Prepare build data for alert
                    build_data = {
                        "id": build.id,
                        "external_id": build.external_id,
                        "status": build.status,
                        "branch": build.branch,
                        "duration_seconds": build.duration_seconds,
                        "url": build.url,
                        "provider_name": provider.name
                    }
                    
                    # Send alert (non-blocking)
                    await send_build_failure_alert(
                        build_data,
                        {"alert_email": settings.alert_email},
                        session
                    )
        
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
        
        if not settings.alert_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Alert email not configured"
            )
        
        # Get SMTP configuration from environment
        smtp_host = os.getenv("SMTP_HOST")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        smtp_username = os.getenv("SMTP_USERNAME")
        smtp_password = os.getenv("SMTP_PASSWORD")
        
        if not all([smtp_host, smtp_username, smtp_password]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="SMTP configuration incomplete"
            )
        
        # Send test email
        smtp_config = {
            "host": smtp_host,
            "port": smtp_port,
            "username": smtp_username,
            "password": smtp_password
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
