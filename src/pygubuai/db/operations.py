"""Database CRUD operations"""

from typing import List, Optional, Dict
from datetime import datetime, timezone

try:
    from sqlalchemy.orm import Session
    from .models import Project, Template, WorkflowEvent, Analytics, SQLALCHEMY_AVAILABLE
except ImportError:
    SQLALCHEMY_AVAILABLE = False
    Session = None
    Project = None  # type: ignore[assignment,misc]
    Template = None  # type: ignore[assignment,misc]
    WorkflowEvent = None  # type: ignore[assignment,misc]
    Analytics = None  # type: ignore[assignment,misc]


def create_project(session: Session, name: str, path: str, description: str = "") -> Optional[Project]:
    """Create new project"""
    if not SQLALCHEMY_AVAILABLE:
        return None

    project = Project(name=name, path=path, description=description)
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


def get_project(session: Session, name: str) -> Optional[Project]:
    """Get project by name"""
    if not SQLALCHEMY_AVAILABLE:
        return None
    return session.query(Project).filter(Project.name == name).first()


def list_projects(session: Session) -> List[Project]:
    """List all projects"""
    if not SQLALCHEMY_AVAILABLE:
        return []
    return session.query(Project).order_by(Project.updated_at.desc()).all()


def update_project(session: Session, name: str, **kwargs) -> bool:
    """Update project"""
    if not SQLALCHEMY_AVAILABLE:
        return False

    project = get_project(session, name)
    if not project:
        return False

    for key, value in kwargs.items():
        if hasattr(project, key):
            setattr(project, key, value)

    project.updated_at = datetime.now(timezone.utc)
    session.commit()
    return True


def delete_project(session: Session, name: str) -> bool:
    """Delete project"""
    if not SQLALCHEMY_AVAILABLE:
        return False

    project = get_project(session, name)
    if not project:
        return False

    session.delete(project)
    session.commit()
    return True


def add_workflow_event(session: Session, project_name: str, action: str, description: str = "") -> bool:
    """Add workflow event"""
    if not SQLALCHEMY_AVAILABLE:
        return False

    project = get_project(session, project_name)
    if not project:
        return False

    event = WorkflowEvent(project_id=project.id, action=action, description=description)
    session.add(event)
    session.commit()
    return True


def get_workflow_events(session: Session, project_name: str, limit: int = 100) -> List[WorkflowEvent]:
    """Get workflow events for project"""
    if not SQLALCHEMY_AVAILABLE:
        return []

    project = get_project(session, project_name)
    if not project:
        return []

    return (
        session.query(WorkflowEvent)
        .filter(WorkflowEvent.project_id == project.id)
        .order_by(WorkflowEvent.timestamp.desc())
        .limit(limit)
        .all()
    )


def create_template(session: Session, name: str, content: str, **kwargs) -> Optional[Template]:
    """Create template"""
    if not SQLALCHEMY_AVAILABLE:
        return None

    template = Template(name=name, content=content, **kwargs)
    session.add(template)
    session.commit()
    session.refresh(template)
    return template


def search_templates(session: Session, query: str) -> List[Template]:
    """Search templates"""
    if not SQLALCHEMY_AVAILABLE:
        return []

    return (
        session.query(Template)
        .filter((Template.name.contains(query)) | (Template.description.contains(query)))
        .order_by(Template.downloads.desc())
        .all()
    )


def record_analytics(
    session: Session,
    metric_name: str,
    metric_value: float,
    project_name: Optional[str] = None,
    metadata: Optional[Dict] = None,
) -> bool:
    """Record analytics metric"""
    if not SQLALCHEMY_AVAILABLE:
        return False

    project_id = None
    if project_name:
        project = get_project(session, project_name)
        if project:
            project_id = project.id

    analytics = Analytics(
        project_id=project_id, metric_name=metric_name, metric_value=metric_value, metadata=metadata or {}
    )
    session.add(analytics)
    session.commit()
    return True
