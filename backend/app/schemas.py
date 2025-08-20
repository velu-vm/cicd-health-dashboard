from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict, Any
from datetime import datetime

# Pipeline schemas
class PipelineBase(BaseModel):
    name: str
    provider: str
    repository: str
    branch: str = "main"

class PipelineCreate(PipelineBase):
    pass

class PipelineUpdate(BaseModel):
    name: Optional[str] = None
    branch: Optional[str] = None

class Pipeline(PipelineBase):
    id: int
    status: str
    last_build_number: Optional[int] = None
    last_build_url: Optional[str] = None
    last_build_time: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Build schemas
class BuildBase(BaseModel):
    build_number: int
    status: str
    commit_hash: Optional[str] = None
    commit_message: Optional[str] = None
    author: Optional[str] = None
    build_url: Optional[str] = None

class BuildCreate(BuildBase):
    pipeline_id: int
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None

class BuildUpdate(BaseModel):
    status: Optional[str] = None
    end_time: Optional[datetime] = None
    duration: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None

class Build(BuildBase):
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
class WebhookPayload(BaseModel):
    provider: str
    event_type: str
    payload: Dict[str, Any]
