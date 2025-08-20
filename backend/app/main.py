from fastapi import FastAPI, Depends, HTTPException, status, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import os
from datetime import datetime, timedelta
from typing import Optional, List
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from collections import defaultdict
import time

from .db import init_db, get_db
from .models import Provider, Build, Alert, Settings, Metrics
from .schemas import (
    MetricsSummary, BuildListResponse, Build as BuildSchema,
    GitHubWebhookPayload, JenkinsWebhookPayload,
    AlertTestRequest, AlertTestResponse, SeedRequest, SeedResponse,
    HealthResponse
)
from .alerts import alert_service

# In-memory rate limiter store
_rate_limits = defaultdict(list)  # ip -> [timestamps]
RATE_LIMIT_WINDOW_SECONDS = 60
RATE_LIMIT_MAX_REQUESTS = 60

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    pass

app = FastAPI(
    title="CI/CD Health Dashboard API",
    description="API for monitoring CI/CD pipeline health using GitHub Actions and Jenkins",
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

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "ok": True,
        "timestamp": datetime.now(),
        "version": "1.0.0",
        "database": "connected"
    }

@app.get("/api/metrics/summary", response_model=MetricsSummary)
async def get_metrics_summary(session: AsyncSession = Depends(get_db)):
    """Get dashboard summary metrics for the last 7 days"""
    try:
        # Calculate time window: last 7 days from now
        now = datetime.now()
        seven_days_ago = now - timedelta(days=7)
        
        # Get builds in the time window
        builds_query = select(Build).where(
            and_(
                Build.started_at >= seven_days_ago,
                Build.status.in_(["success", "failed", "running", "queued"])
            )
        )
        result = await session.execute(builds_query)
        builds = result.scalars().all()
        
        if not builds:
            return MetricsSummary(
                window_days=7,
                success_rate=0.0,
                failure_rate=0.0,
                avg_build_time_seconds=0.0,
                last_build_status="unknown",
                last_updated=now
            )
        
        # Calculate metrics
        total_builds = len(builds)
        successful_builds = len([b for b in builds if b.status == "success"])
        failed_builds = len([b for b in builds if b.status == "failed"])
        
        success_rate = successful_builds / total_builds if total_builds > 0 else 0.0
        failure_rate = failed_builds / total_builds if total_builds > 0 else 0.0
        
        # Calculate average build time (only for completed builds)
        completed_builds = [b for b in builds if b.duration_seconds is not None]
        avg_build_time = sum(b.duration_seconds for b in completed_builds) / len(completed_builds) if completed_builds else 0.0
        
        # Get last build status
        last_build = max(builds, key=lambda b: b.started_at if b.started_at else datetime.min)
        last_build_status = last_build.status
        
        return MetricsSummary(
            window_days=7,
            success_rate=success_rate,
            failure_rate=failure_rate,
            avg_build_time_seconds=avg_build_time,
            last_build_status=last_build_status,
            last_updated=now
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to calculate metrics: {str(e)}"
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
        
        # Convert to response schemas
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
                "started_at": build.started_at,
                "finished_at": build.finished_at,
                "duration_seconds": build.duration_seconds,
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
    """Get details of a specific build"""
    try:
        result = await session.execute(select(Build).where(Build.id == build_id))
        build = result.scalar_one_or_none()
        
        if not build:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Build with ID {build_id} not found"
            )
        
        build_data = {
            "id": build.id,
            "external_id": build.external_id,
            "status": build.status,
            "branch": build.branch,
            "commit_sha": build.commit_sha,
            "triggered_by": build.triggered_by,
            "url": build.url,
            "started_at": build.started_at,
            "finished_at": build.finished_at,
            "duration_seconds": build.duration_seconds,
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
        # Extract build information from webhook
        workflow_run = payload.workflow_run
        workflow = payload.workflow
        repository = payload.repository
        sender = payload.sender
        
        # Get or create provider
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
        external_id = str(workflow_run.id)
        result = await session.execute(
            select(Build).where(
                and_(
                    Build.external_id == external_id,
                    Build.provider_id == provider.id
                )
            )
        )
        build = result.scalar_one_or_none()
        
        if not build:
            build = Build(
                external_id=external_id,
                provider_id=provider.id,
                status=workflow_run.status,
                branch=workflow_run.head_branch,
                commit_sha=workflow_run.head_commit.id if workflow_run.head_commit else None,
                triggered_by=sender.login if sender else None,
                url=workflow_run.html_url,
                started_at=workflow_run.run_started_at,
                finished_at=workflow_run.updated_at,
                raw_payload=payload.dict()
            )
            session.add(build)
        else:
            # Update existing build
            build.status = workflow_run.status
            build.finished_at = workflow_run.updated_at
            build.raw_payload = payload.dict()
        
        await session.commit()
        
        # Send alert if build failed
        if workflow_run.conclusion == "failure":
            await alert_service.send_build_failure_alert(
                session=session,
                build=build,
                alert_type="email"
            )
        
        return {"status": "success", "build_id": build.id}
        
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
        # Extract build information from webhook
        name = payload.name
        url = payload.url
        build_info = payload.build
        
        # Get or create provider
        provider_name = f"jenkins-{name}"
        result = await session.execute(
            select(Provider).where(Provider.name == provider_name)
        )
        provider = result.scalar_one_or_none()
        
        if not provider:
            provider = Provider(
                name=provider_name,
                kind="jenkins",
                config_json={"name": name, "url": url}
            )
            session.add(provider)
            await session.commit()
            await session.refresh(provider)
        
        # Create or update build
        external_id = str(build_info.get("number", build_info.get("id", "unknown")))
        result = await session.execute(
            select(Build).where(
                and_(
                    Build.external_id == external_id,
                    Build.provider_id == provider.id
                )
            )
        )
        build = result.scalar_one_or_none()
        
        if not build:
            build = Build(
                external_id=external_id,
                provider_id=provider.id,
                status=build_info.get("status", "unknown"),
                branch=build_info.get("branch", "main"),
                commit_sha=build_info.get("commit", None),
                triggered_by=build_info.get("user", None),
                url=build_info.get("url", url),
                started_at=datetime.fromtimestamp(payload.timestamp / 1000) if payload.timestamp else None,
                raw_payload=payload.dict()
            )
            session.add(build)
        else:
            # Update existing build
            build.status = build_info.get("status", build.status)
            build.raw_payload = payload.dict()
        
        await session.commit()
        
        # Send alert if build failed
        if build_info.get("status") == "FAILURE":
            await alert_service.send_build_failure_alert(
                session=session,
                build=build,
                alert_type="email"
            )
        
        return {"status": "success", "build_id": build.id}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process webhook: {str(e)}"
        )

@app.post("/api/alert/test", response_model=AlertTestResponse)
async def test_alert(
    request: AlertTestRequest,
    session: AsyncSession = Depends(get_db)
):
    """Test alert delivery"""
    try:
        result = await alert_service.test_alert(
            session=session,
            alert_type=request.alert_type,
            message=request.message,
            severity=request.severity
        )
        
        return AlertTestResponse(**result)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to test alert: {str(e)}"
        )

@app.post("/api/seed", response_model=SeedResponse)
async def seed_database(
    request: SeedRequest,
    session: AsyncSession = Depends(get_db)
):
    """Seed database with sample data"""
    try:
        # Create sample providers
        github_provider = Provider(
            name="github-sample",
            kind="github_actions",
            config_json={"repository": "sample/repo"}
        )
        session.add(github_provider)
        
        jenkins_provider = Provider(
            name="jenkins-sample",
            kind="jenkins",
            config_json={"name": "Sample Pipeline", "url": "http://jenkins.example.com"}
        )
        session.add(jenkins_provider)
        
        await session.commit()
        await session.refresh(github_provider)
        await session.refresh(jenkins_provider)
        
        # Create sample builds
        sample_builds = [
            {
                "external_id": "123456789",
                "provider_id": github_provider.id,
                "status": "success",
                "branch": "main",
                "commit_sha": "abc123def456",
                "triggered_by": "john_doe",
                "url": "https://github.com/sample/repo/actions/runs/123456789",
                "started_at": datetime.now() - timedelta(hours=2),
                "finished_at": datetime.now() - timedelta(hours=1, minutes=55),
                "duration_seconds": 300
            },
            {
                "external_id": "123456790",
                "provider_id": github_provider.id,
                "status": "failed",
                "branch": "feature/new-feature",
                "commit_sha": "def456ghi789",
                "triggered_by": "jane_smith",
                "url": "https://github.com/sample/repo/actions/runs/123456790",
                "started_at": datetime.now() - timedelta(hours=4),
                "finished_at": datetime.now() - timedelta(hours=3, minutes=50),
                "duration_seconds": 600
            },
            {
                "external_id": "123456791",
                "provider_id": jenkins_provider.id,
                "status": "success",
                "branch": "develop",
                "commit_sha": "ghi789jkl012",
                "triggered_by": "build_bot",
                "url": "http://jenkins.example.com/job/Sample%20Pipeline/123456791/",
                "started_at": datetime.now() - timedelta(hours=6),
                "finished_at": datetime.now() - timedelta(hours=5, minutes=45),
                "duration_seconds": 900
            }
        ]
        
        for build_data in sample_builds:
            build = Build(**build_data)
            session.add(build)
        
        await session.commit()
        
        return SeedResponse(
            success=True,
            message="Database seeded successfully with sample data",
            builds_created=len(sample_builds),
            providers_created=2
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to seed database: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
