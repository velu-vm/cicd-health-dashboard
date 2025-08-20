from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .db import Base

class Pipeline(Base):
    __tablename__ = "pipelines"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    provider = Column(String(50), nullable=False)  # github_actions, jenkins
    repository = Column(String(255), nullable=False)
    branch = Column(String(100), default="main")
    status = Column(String(50), default="unknown")  # success, failed, running, unknown
    last_build_number = Column(Integer)
    last_build_url = Column(String(500))
    last_build_time = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    builds = relationship("Build", back_populates="pipeline")

class Build(Base):
    __tablename__ = "builds"
    
    id = Column(Integer, primary_key=True, index=True)
    pipeline_id = Column(Integer, ForeignKey("pipelines.id"))
    build_number = Column(Integer, nullable=False)
    status = Column(String(50), nullable=False)  # success, failed, running, cancelled
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    duration = Column(Integer)  # in seconds
    commit_hash = Column(String(100))
    commit_message = Column(Text)
    author = Column(String(255))
    build_url = Column(String(500))
    metadata = Column(JSON)  # Additional provider-specific data
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    pipeline = relationship("Pipeline", back_populates="builds")

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    pipeline_id = Column(Integer, ForeignKey("pipelines.id"))
    type = Column(String(50), nullable=False)  # build_failed, build_slow, pipeline_down
    message = Column(Text, nullable=False)
    severity = Column(String(20), default="medium")  # low, medium, high, critical
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime(timezone=True))
    
    # Relationships
    pipeline = relationship("Pipeline")
