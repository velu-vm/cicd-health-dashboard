from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Any
from datetime import datetime

# Base configuration for all models
class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

# Pipeline schemas
class PipelineBase(BaseSchema):
    name: str
    repository: str
    owner: str
    branch: str = "main"
    workflow_file: Optional[str] = None

class PipelineCreate(PipelineBase):
    pass

class PipelineUpdate(BaseSchema):
    name: Optional[str] = None
    branch: Optional[str] = None
    workflow_file: Optional[str] = None

class Pipeline(PipelineBase):
    id: int
    provider: str = "github_actions"
    status: str
    last_run_number: Optional[int] = None
    last_run_url: Optional[str] = None
    last_run_time: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Workflow Run schemas
class WorkflowRunBase(BaseSchema):
    run_number: int
    run_id: str
    status: str
    conclusion: Optional[str] = None
    commit_hash: Optional[str] = None
    commit_message: Optional[str] = None
    author: Optional[str] = None
    run_url: Optional[str] = None
    workflow_name: Optional[str] = None
    trigger: Optional[str] = None

class WorkflowRunCreate(WorkflowRunBase):
    pipeline_id: int
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration: Optional[int] = None
    metadata: Optional[Any] = None

class WorkflowRunUpdate(BaseSchema):
    status: Optional[str] = None
    conclusion: Optional[str] = None
    end_time: Optional[datetime] = None
    duration: Optional[int] = None
    metadata: Optional[Any] = None

class WorkflowRun(WorkflowRunBase):
    id: int
    pipeline_id: int
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration: Optional[int] = None
    metadata: Optional[Any] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Alert schemas
class AlertBase(BaseSchema):
    type: str
    message: str
    severity: str = "medium"

class AlertCreate(AlertBase):
    pipeline_id: int

class AlertUpdate(BaseSchema):
    is_active: Optional[bool] = None
    resolved_at: Optional[datetime] = None

class Alert(AlertBase):
    id: int
    pipeline_id: int
    is_active: bool
    created_at: datetime
    resolved_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Health check schema
class HealthCheck(BaseSchema):
    ok: bool
    timestamp: datetime
    version: str

# Summary metrics schemas
class MetricsSummary(BaseSchema):
    window_days: int = 7
    success_rate: float = 0.0
    failure_rate: float = 0.0
    avg_build_time_seconds: Optional[float] = None  # in seconds
    last_build_status: Optional[str] = None
    last_updated: str = ""  # ISO8601 timestamp

# Build schemas
class BuildBase(BaseSchema):
    external_id: str
    status: str
    branch: str = "main"
    commit_sha: Optional[str] = None
    triggered_by: Optional[str] = None
    url: Optional[str] = None
    provider_id: int
    duration_seconds: Optional[int] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    raw_payload: Any

class BuildCreate(BuildBase):
    pass

class BuildUpdate(BaseSchema):
    external_id: Optional[str] = None
    status: Optional[str] = None
    branch: Optional[str] = None
    commit_sha: Optional[str] = None
    triggered_by: Optional[str] = None
    url: Optional[str] = None
    provider_id: Optional[int] = None
    duration_seconds: Optional[int] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    raw_payload: Optional[Any] = None

class Build(BuildBase):
    id: int
    created_at: datetime
    provider_name: Optional[str] = None
    provider_kind: Optional[str] = None

# Build list response with pagination
class BuildListResponse(BaseSchema):
    builds: List[Build]
    total: int
    limit: int
    offset: int
    has_more: bool

# Webhook schemas
class GitHubWebhookPayload(BaseSchema):
    workflow_run: dict
    workflow: dict
    repository: dict
    sender: dict

# Alert test schemas
class AlertTestRequest(BaseSchema):
    message: str = Field(..., min_length=1, max_length=1000)
    severity: str = Field(default="info", pattern="^(info|warning|error)$")

class AlertTestResponse(BaseSchema):
    success: bool
    message: str
    channel: str = "email"

# Seed data schemas
class SeedRequest(BaseSchema):
    providers: Optional[List[dict]] = None
    builds: Optional[List[dict]] = None

class SeedResponse(BaseSchema):
    success: bool
    message: str
    providers_created: int = 0
    builds_created: int = 0

# Error response schema
class ErrorResponse(BaseSchema):
    detail: str
