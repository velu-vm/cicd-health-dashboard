from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .db import Base

class Pipeline(Base):
    __tablename__ = "pipelines"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    provider = Column(String(50), default="github_actions")  # Always github_actions
    repository = Column(String(255), nullable=False)
    owner = Column(String(255), nullable=False)  # GitHub owner/organization
    branch = Column(String(100), default="main")
    workflow_file = Column(String(255))  # .github/workflows/filename.yml
    status = Column(String(50), default="unknown")  # success, failed, running, unknown
    last_run_number = Column(Integer)
    last_run_url = Column(String(500))
    last_run_time = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    runs = relationship("WorkflowRun", back_populates="pipeline")

class WorkflowRun(Base):
    __tablename__ = "workflow_runs"
    
    id = Column(Integer, primary_key=True, index=True)
    pipeline_id = Column(Integer, ForeignKey("pipelines.id"))
    run_number = Column(Integer, nullable=False)
    run_id = Column(String(100), nullable=False)  # GitHub run ID
    status = Column(String(50), nullable=False)  # success, failure, cancelled, in_progress
    conclusion = Column(String(50))  # success, failure, cancelled, skipped
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    duration = Column(Integer)  # in seconds
    commit_hash = Column(String(100))
    commit_message = Column(Text)
    author = Column(String(255))
    run_url = Column(String(500))
    workflow_name = Column(String(255))
    trigger = Column(String(50))  # push, pull_request, manual, etc.
    metadata = Column(JSON)  # Additional GitHub-specific data
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    pipeline = relationship("Pipeline", back_populates="runs")

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    pipeline_id = Column(Integer, ForeignKey("pipelines.id"))
    type = Column(String(50), nullable=False)  # workflow_failed, workflow_slow, pipeline_down
    message = Column(Text, nullable=False)
    severity = Column(String(20), default="medium")  # low, medium, high, critical
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime(timezone=True))
    
    # Relationships
    pipeline = relationship("Pipeline")
