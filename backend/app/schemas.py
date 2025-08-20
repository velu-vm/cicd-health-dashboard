from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# Pipeline schemas
class PipelineBase(BaseModel):
    name: str
    repository: str
    owner: str
    branch: str = "main"
    workflow_file: Optional[str] = None

class PipelineCreate(PipelineBase):
    pass

class PipelineUpdate(BaseModel):
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
class WorkflowRunBase(BaseModel):
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
    metadata: Optional[Dict[str, Any]] = None

class WorkflowRunUpdate(BaseModel):
    status: Optional[str] = None
    conclusion: Optional[str] = None
    end_time: Optional[datetime] = None
    duration: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None

class WorkflowRun(WorkflowRunBase):
    id: int
    pipeline_id: int
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Alert schemas
class AlertBase(BaseModel):
    type: str
    message: str
    severity: str = "medium"

class AlertCreate(AlertBase):
    pipeline_id: int

class AlertUpdate(BaseModel):
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
class HealthCheck(BaseModel):
    ok: bool
    timestamp: datetime
    version: str

# Summary metrics schemas
class MetricsSummary(BaseModel):
    window_days: int = 7
    success_rate: float = 0.0
    failure_rate: float = 0.0
    avg_build_time_seconds: Optional[float] = None  # in seconds
    last_build_status: Optional[str] = None
    last_updated: str = ""  # ISO8601 timestamp

# Build schemas
class BuildBase(BaseModel):
    external_id: str
    status: str
    branch: str = "main"
    commit_sha: Optional[str] = None
    triggered_by: Optional[str] = None
    url: Optional[str] = None

class BuildCreate(BuildBase):
    provider_id: int
    duration_seconds: Optional[int] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    raw_payload: Optional[Dict[str, Any]] = None

class BuildUpdate(BaseModel):
    status: Optional[str] = None
    duration_seconds: Optional[int] = None
    finished_at: Optional[datetime] = None
    raw_payload: Optional[Dict[str, Any]] = None

class Build(BuildBase):
    id: int
    provider_id: int
    duration_seconds: Optional[int] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    raw_payload: Optional[Dict[str, Any]] = None
    created_at: datetime
    
    # Provider info
    provider_name: Optional[str] = None
    provider_kind: Optional[str] = None

    class Config:
        from_attributes = True

# Build list response with pagination
class BuildListResponse(BaseModel):
    builds: List[Build]
    total: int
    limit: int
    offset: int
    has_more: bool

# Webhook schemas
class GitHubWebhookPayload(BaseModel):
    workflow_run: Dict[str, Any]
    workflow: Dict[str, Any]
    repository: Dict[str, Any]
    sender: Dict[str, Any]

# Alert test schemas
class AlertTestRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    severity: str = Field(default="info", regex="^(info|warning|error)$")

class AlertTestResponse(BaseModel):
    success: bool
    message: str
    channel: str = "email"

# Seed data schemas
class SeedRequest(BaseModel):
    providers: Optional[List[Dict[str, Any]]] = None
    builds: Optional[List[Dict[str, Any]]] = None

class SeedResponse(BaseModel):
    success: bool
    message: str
    providers_created: int = 0
    builds_created: int = 0

# Error response schema
class ErrorResponse(BaseModel):
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.now)
