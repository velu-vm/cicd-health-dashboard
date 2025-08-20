from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, JSON, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .db import Base

class Provider(Base):
    __tablename__ = "providers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    kind = Column(String(50), nullable=False)  # github_actions, jenkins
    config_json = Column(JSON)  # Provider-specific configuration
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    builds = relationship("Build", back_populates="provider")

class Build(Base):
    __tablename__ = "builds"
    
    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey("providers.id"), nullable=False)
    external_id = Column(String(255), nullable=False)  # External build ID from provider
    status = Column(String(50), nullable=False)  # success, failed, running, queued
    duration_seconds = Column(Integer)  # Build duration in seconds
    branch = Column(String(100), default="main")
    commit_sha = Column(String(100))
    triggered_by = Column(String(255))  # User who triggered the build
    started_at = Column(DateTime(timezone=True))
    finished_at = Column(DateTime(timezone=True))
    url = Column(String(500))  # Build URL
    raw_payload = Column(JSON)  # Raw payload from provider
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    provider = relationship("Provider", back_populates="builds")
    alerts = relationship("Alert", back_populates="build")

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    build_id = Column(Integer, ForeignKey("builds.id"), nullable=False)
    channel = Column(String(50), nullable=False)  # email
    sent_at = Column(DateTime(timezone=True), server_default=func.now())
    success = Column(Boolean, default=True)  # Whether alert was sent successfully
    message = Column(Text, nullable=False)
    
    # Relationships
    build = relationship("Build", back_populates="alerts")

class Settings(Base):
    __tablename__ = "settings"
    
    id = Column(Integer, primary_key=True, default=1)
    alert_email = Column(String(255))  # Email for alerts
    smtp_host = Column(String(255))  # SMTP server host
    smtp_port = Column(Integer)  # SMTP server port
    smtp_username = Column(String(255))  # SMTP username
    smtp_password = Column(String(255))  # SMTP password
    api_write_key = Column(String(255))  # API key for write operations
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# Create indexes for performance
Index('idx_builds_status_started', Build.status, Build.started_at)
Index('idx_builds_provider_finished', Build.provider_id, Build.finished_at)
Index('idx_builds_external_id', Build.external_id)
Index('idx_alerts_build_id', Alert.build_id)
Index('idx_providers_kind', Provider.kind)
