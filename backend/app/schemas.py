from pydantic import BaseModel, HttpUrl
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

# Webhook schemas
class GitHubWebhookPayload(BaseModel):
    workflow_run: Dict[str, Any]
    workflow: Dict[str, Any]
    repository: Dict[str, Any]
    sender: Dict[str, Any]
