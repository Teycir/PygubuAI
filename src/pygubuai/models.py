"""Pydantic models for data validation"""
from typing import Optional, Dict, List
from datetime import datetime, timezone
from pathlib import Path
from pydantic import BaseModel, Field, field_validator

class ProjectConfig(BaseModel):
    """Project configuration model"""
    name: str
    path: str
    ui_file: Optional[str] = None
    py_file: Optional[str] = None
    created: float = Field(default_factory=lambda: datetime.now(timezone.utc).timestamp())
    last_modified: float = Field(default_factory=lambda: datetime.now(timezone.utc).timestamp())
    metadata: Dict = Field(default_factory=dict)
    
    @field_validator('path')
    @classmethod
    def validate_path(cls, v):
        if not Path(v).exists():
            raise ValueError(f"Path does not exist: {v}")
        return str(Path(v).resolve())

class RegistryData(BaseModel):
    """Registry data model"""
    projects: Dict[str, Dict] = Field(default_factory=dict)
    active: Optional[str] = None
    version: str = "1.0"
    
    @field_validator('active')
    @classmethod
    def validate_active(cls, v, info):
        if v and 'projects' in info.data and v not in info.data['projects']:
            raise ValueError(f"Active project '{v}' not in registry")
        return v

class WorkflowHistory(BaseModel):
    """Workflow history entry"""
    timestamp: str
    action: str
    description: str
    user: Optional[str] = None

class WorkflowData(BaseModel):
    """Workflow tracking data"""
    project: str
    history: List[WorkflowHistory] = Field(default_factory=list)
    last_sync: Optional[str] = None
    version: str = "1.0"
    file_hashes: Dict[str, str] = Field(default_factory=dict)
    file_mtimes: Dict[str, float] = Field(default_factory=dict)

class WidgetConfig(BaseModel):
    """Widget configuration"""
    widget_type: str
    widget_id: str
    properties: Dict = Field(default_factory=dict)
    layout: Dict = Field(default_factory=dict)
    
class ExportConfig(BaseModel):
    """Export configuration"""
    project: str
    output_file: str
    standalone: bool = True
    include_comments: bool = True
    minify: bool = False
