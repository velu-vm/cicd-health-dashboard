from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

# Enums
class BuildStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    RUNNING = "running"
    QUEUED = "queued"
    CANCELLED = "cancelled"
    UNKNOWN = "unknown"

class AlertType(str, Enum):
    EMAIL = "email"
    SLACK = "slack"
    WEBHOOK = "webhook"

class AlertSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

# Base Models
class ProviderBase(BaseModel):
    name: str = Field(..., description="Provider name")
    kind: str = Field(..., description="Provider type (github_actions, jenkins, etc.)")
    config_json: Optional[Dict[str, Any]] = Field(None, description="Provider configuration")
    is_active: bool = Field(True, description="Whether provider is active")

class ProviderCreate(ProviderBase):
    pass

class Provider(ProviderBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class BuildBase(BaseModel):
    external_id: str = Field(..., description="External build ID from provider")
    status: BuildStatus = Field(..., description="Build status")
    branch: Optional[str] = Field(None, description="Git branch")
    commit_sha: Optional[str] = Field(None, description="Git commit SHA")
    triggered_by: Optional[str] = Field(None, description="User who triggered the build")
    url: Optional[str] = Field(None, description="Build URL in provider")
    started_at: Optional[datetime] = Field(None, description="Build start time")
    finished_at: Optional[datetime] = Field(None, description="Build finish time")
    duration_seconds: Optional[float] = Field(None, description="Build duration in seconds")
    raw_payload: Optional[Dict[str, Any]] = Field(None, description="Raw webhook payload")

class BuildCreate(BuildBase):
    provider_id: int = Field(..., description="Provider ID")

class Build(BuildBase):
    id: int
    provider_id: int
    provider: Optional[Provider] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class BuildListResponse(BaseModel):
    builds: List[Build]
    total: int
    limit: int
    offset: int
    has_more: bool

class AlertBase(BaseModel):
    type: AlertType = Field(..., description="Alert type")
    name: str = Field(..., description="Alert name")
    config_json: Dict[str, Any] = Field(..., description="Alert configuration")
    is_active: bool = Field(True, description="Whether alert is active")

class AlertCreate(AlertBase):
    pass

class Alert(AlertBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class AlertHistoryBase(BaseModel):
    alert_id: int = Field(..., description="Alert ID")
    build_id: Optional[int] = Field(None, description="Build ID if alert is build-related")
    message: str = Field(..., description="Alert message")
    severity: AlertSeverity = Field(..., description="Alert severity")
    status: str = Field(..., description="Alert status (sent, failed, pending)")

class AlertHistoryCreate(AlertHistoryBase):
    pass

class AlertHistory(AlertHistoryBase):
    id: int
    error_message: Optional[str] = Field(None, description="Error message if alert failed")
    sent_at: datetime
    alert: Optional[Alert] = None
    build: Optional[Build] = None

    class Config:
        from_attributes = True

class SettingsBase(BaseModel):
    key: str = Field(..., description="Setting key")
    value: Optional[str] = Field(None, description="Setting value")
    description: Optional[str] = Field(None, description="Setting description")

class SettingsCreate(SettingsBase):
    pass

class Settings(SettingsBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class MetricsBase(BaseModel):
    metric_name: str = Field(..., description="Metric name")
    metric_value: float = Field(..., description="Metric value")
    metric_unit: Optional[str] = Field(None, description="Metric unit")
    window_start: datetime = Field(..., description="Metrics window start time")
    window_end: datetime = Field(..., description="Metrics window end time")

class MetricsCreate(MetricsBase):
    pass

class Metrics(MetricsBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Dashboard Models
class MetricsSummary(BaseModel):
    window_days: int = Field(..., description="Metrics window in days")
    success_rate: float = Field(..., description="Success rate (0.0 to 1.0)")
    failure_rate: float = Field(..., description="Failure rate (0.0 to 1.0)")
    avg_build_time_seconds: float = Field(..., description="Average build time in seconds")
    last_build_status: str = Field(..., description="Last build status")
    last_updated: datetime = Field(..., description="Last metrics update time")

# Webhook Models
class GitHubWebhookPayload(BaseModel):
    """GitHub Actions webhook payload"""
    workflow_run: Dict[str, Any]
    workflow: Dict[str, Any]
    repository: Dict[str, Any]
    sender: Dict[str, Any]

class JenkinsWebhookPayload(BaseModel):
    """Jenkins webhook payload"""
    name: str
    url: str
    build: Dict[str, Any]
    timestamp: Optional[int] = None

# Alert Models
class AlertTestRequest(BaseModel):
    message: str = Field(..., description="Test message")
    severity: AlertSeverity = Field(AlertSeverity.INFO, description="Alert severity")
    alert_type: AlertType = Field(..., description="Alert type to test")

class AlertTestResponse(BaseModel):
    success: bool
    message: str
    alert_id: Optional[int] = None
    error: Optional[str] = None

# Seed Models
class SeedRequest(BaseModel):
    """Request to seed database with sample data"""
    pass

class SeedResponse(BaseModel):
    """Response from seeding database"""
    success: bool
    message: str
    builds_created: int
    providers_created: int

# Health Check
class HealthResponse(BaseModel):
    ok: bool
    timestamp: datetime
    version: str = "1.0.0"
    database: str = "connected"
