"""Workflow session data model."""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict


@dataclass
class WorkflowSession:
    """Represents a workflow session with all its data."""
    
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    workflow_name: str = ""
    workflow_token: str = field(default_factory=lambda: f"WF-{str(uuid.uuid4())[:8].upper()}")
    current_step: Optional[str] = None
    status: str = "in_progress"  # in_progress, completed, abandoned, processing
    data: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Initialize metadata if not provided."""
        if not self.metadata:
            self.metadata = {
                'completed_steps': [],
                'total_steps': None,
                'progress_percentage': 0
            }
    
    def set_step_data(self, step_name: str, step_data: Dict[str, Any]) -> None:
        """Set data for a specific workflow step.
        
        Args:
            step_name: Name of the workflow step
            step_data: Data dictionary for this step
        """
        self.data[step_name] = step_data
        self.updated_at = datetime.now()
        
        # Mark step as completed if not already
        completed_steps = self.metadata.get('completed_steps', [])
        if step_name not in completed_steps:
            completed_steps.append(step_name)
            self.metadata['completed_steps'] = completed_steps
            
        # Update progress percentage
        total_steps = self.metadata.get('total_steps')
        if total_steps:
            progress = (len(completed_steps) / total_steps) * 100
            self.metadata['progress_percentage'] = min(100, progress)
    
    def get_step_data(self, step_name: str) -> Optional[Dict[str, Any]]:
        """Get data for a specific workflow step.
        
        Args:
            step_name: Name of the workflow step
            
        Returns:
            Data dictionary if step exists, None otherwise
        """
        return self.data.get(step_name)
    
    def has_completed_step(self, step_name: str) -> bool:
        """Check if a step has been completed.
        
        Args:
            step_name: Name of the workflow step
            
        Returns:
            True if step is completed, False otherwise
        """
        completed_steps = self.metadata.get('completed_steps', [])
        return step_name in completed_steps
    
    def get_all_data(self) -> Dict[str, Any]:
        """Get all workflow data flattened into a single dictionary.
        
        Returns:
            Dictionary with all step data combined
        """
        all_data = {}
        for step_name, step_data in self.data.items():
            for key, value in step_data.items():
                # Prefix with step name to avoid conflicts
                all_data[f"{step_name}_{key}"] = value
                # Also add unprefixed for convenience (last step wins)
                all_data[key] = value
        return all_data
    
    def set_status(self, status: str) -> None:
        """Update session status.
        
        Args:
            status: New status (in_progress, completed, abandoned, processing)
        """
        self.status = status
        self.updated_at = datetime.now()
        
        if status == 'completed':
            self.metadata['completed_at'] = datetime.now().isoformat()
            self.metadata['progress_percentage'] = 100
    
    def add_metadata(self, key: str, value: Any) -> None:
        """Add custom metadata to the session.
        
        Args:
            key: Metadata key
            value: Metadata value
        """
        self.metadata[key] = value
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert session to dictionary for serialization.
        
        Returns:
            Dictionary representation of the session
        """
        session_dict = asdict(self)
        # Convert datetime objects to ISO strings
        session_dict['created_at'] = self.created_at.isoformat()
        session_dict['updated_at'] = self.updated_at.isoformat()
        return session_dict
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WorkflowSession':
        """Create session from dictionary.
        
        Args:
            data: Dictionary representation of session
            
        Returns:
            WorkflowSession instance
        """
        # Convert ISO strings back to datetime objects
        if isinstance(data.get('created_at'), str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        if isinstance(data.get('updated_at'), str):
            data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        
        return cls(**data)
    
    def __repr__(self) -> str:
        return f"WorkflowSession(id={self.session_id[:8]}, workflow={self.workflow_name}, token={self.workflow_token}, status={self.status})"