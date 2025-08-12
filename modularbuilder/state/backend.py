"""Abstract base class for state backends."""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from .session import WorkflowSession


class StateBackend(ABC):
    """Abstract base class for pluggable state backends."""
    
    @abstractmethod
    def create_session(self, workflow_name: str, workflow_token: str = None) -> WorkflowSession:
        """Create a new workflow session.
        
        Args:
            workflow_name: Name of the workflow
            workflow_token: Optional custom workflow token
            
        Returns:
            New WorkflowSession instance
        """
        pass
    
    @abstractmethod
    def get_session(self, session_id: str) -> Optional[WorkflowSession]:
        """Get a session by its session ID.
        
        Args:
            session_id: UUID of the session
            
        Returns:
            WorkflowSession if found, None otherwise
        """
        pass
    
    @abstractmethod
    def get_session_by_token(self, workflow_token: str) -> Optional[WorkflowSession]:
        """Get a session by its workflow token.
        
        Args:
            workflow_token: Workflow token string
            
        Returns:
            WorkflowSession if found, None otherwise
        """
        pass
    
    @abstractmethod
    def save_session(self, session: WorkflowSession) -> bool:
        """Save/update a session.
        
        Args:
            session: WorkflowSession to save
            
        Returns:
            True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def delete_session(self, session_id: str) -> bool:
        """Delete a session.
        
        Args:
            session_id: UUID of the session to delete
            
        Returns:
            True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def list_sessions(self, workflow_name: str = None, status: str = None) -> List[WorkflowSession]:
        """List sessions with optional filters.
        
        Args:
            workflow_name: Optional filter by workflow name
            status: Optional filter by status
            
        Returns:
            List of matching WorkflowSession objects
        """
        pass
    
    @abstractmethod
    def cleanup_expired_sessions(self, max_age_days: int = 30) -> int:
        """Clean up old sessions.
        
        Args:
            max_age_days: Delete sessions older than this many days
            
        Returns:
            Number of sessions deleted
        """
        pass