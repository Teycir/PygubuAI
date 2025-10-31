"""SQLAlchemy ORM models"""
from datetime import datetime
from typing import Optional

try:
    from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, JSON
    from sqlalchemy.orm import declarative_base, relationship
    SQLALCHEMY_AVAILABLE = True
    
    Base = declarative_base()
    
    class Project(Base):
        """Project model"""
        __tablename__ = "projects"
        
        id = Column(Integer, primary_key=True)
        name = Column(String(255), unique=True, nullable=False, index=True)
        path = Column(String(512), nullable=False)
        description = Column(Text, default="")
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        meta_data = Column(JSON, default=dict)
        
        workflow_events = relationship("WorkflowEvent", back_populates="project", cascade="all, delete-orphan")
        analytics = relationship("Analytics", back_populates="project", cascade="all, delete-orphan")
    
    class Template(Base):
        """Template model"""
        __tablename__ = "templates"
        
        id = Column(Integer, primary_key=True)
        name = Column(String(255), unique=True, nullable=False, index=True)
        description = Column(Text, default="")
        author = Column(String(255), default="")
        version = Column(String(50), default="1.0.0")
        downloads = Column(Integer, default=0)
        rating = Column(Float, default=0.0)
        content = Column(Text, nullable=False)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        meta_data = Column(JSON, default=dict)
    
    class WorkflowEvent(Base):
        """Workflow event model"""
        __tablename__ = "workflow_events"
        
        id = Column(Integer, primary_key=True)
        project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
        timestamp = Column(DateTime, default=datetime.utcnow, index=True)
        action = Column(String(100), nullable=False)
        description = Column(Text, default="")
        
        project = relationship("Project", back_populates="workflow_events")
    
    class Analytics(Base):
        """Analytics model"""
        __tablename__ = "analytics"
        
        id = Column(Integer, primary_key=True)
        project_id = Column(Integer, ForeignKey("projects.id"), nullable=True, index=True)
        metric_name = Column(String(100), nullable=False, index=True)
        metric_value = Column(Float, nullable=False)
        recorded_at = Column(DateTime, default=datetime.utcnow, index=True)
        meta_data = Column(JSON, default=dict)
        
        project = relationship("Project", back_populates="analytics")

except ImportError:
    SQLALCHEMY_AVAILABLE = False
    Base = None
    Project = None
    Template = None
    WorkflowEvent = None
    Analytics = None
