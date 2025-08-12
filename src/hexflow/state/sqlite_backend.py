"""SQLite implementation of state backend."""

import sqlite3
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path

from .backend import StateBackend
from .session import WorkflowSession


class SQLiteBackend(StateBackend):
    """SQLite implementation of the state backend."""
    
    def __init__(self, db_path: str = None):
        """Initialize SQLite backend.
        
        Args:
            db_path: Path to SQLite database file. Defaults to 'workflow_sessions.db'
        """
        if db_path is None:
            db_path = os.path.join(os.getcwd(), 'workflow_sessions.db')
        
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize database
        self._init_database()
    
    def _init_database(self) -> None:
        """Initialize the database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS workflow_sessions (
                    session_id TEXT PRIMARY KEY,
                    workflow_name TEXT NOT NULL,
                    workflow_token TEXT UNIQUE NOT NULL,
                    current_step TEXT,
                    status TEXT DEFAULT 'in_progress',
                    data TEXT NOT NULL,  -- JSON
                    metadata TEXT NOT NULL,  -- JSON
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            
            # Create indexes for common queries
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_workflow_token 
                ON workflow_sessions(workflow_token)
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_workflow_name_status 
                ON workflow_sessions(workflow_name, status)
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_created_at 
                ON workflow_sessions(created_at)
            """)
            
            conn.commit()
    
    def create_session(self, workflow_name: str, workflow_token: str = None) -> WorkflowSession:
        """Create a new workflow session."""
        session = WorkflowSession(
            workflow_name=workflow_name,
            workflow_token=workflow_token or f"WF-{WorkflowSession().session_id[:8].upper()}"
        )
        
        if self.save_session(session):
            return session
        else:
            raise RuntimeError("Failed to create session")
    
    def get_session(self, session_id: str) -> Optional[WorkflowSession]:
        """Get a session by its session ID."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM workflow_sessions WHERE session_id = ?",
                (session_id,)
            )
            row = cursor.fetchone()
            
            if row:
                return self._row_to_session(row)
            return None
    
    def get_session_by_token(self, workflow_token: str) -> Optional[WorkflowSession]:
        """Get a session by its workflow token."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM workflow_sessions WHERE workflow_token = ?",
                (workflow_token,)
            )
            row = cursor.fetchone()
            
            if row:
                return self._row_to_session(row)
            return None
    
    def save_session(self, session: WorkflowSession) -> bool:
        """Save/update a session."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Update the updated_at timestamp
                session.updated_at = datetime.now()
                
                conn.execute("""
                    INSERT OR REPLACE INTO workflow_sessions 
                    (session_id, workflow_name, workflow_token, current_step, 
                     status, data, metadata, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    session.session_id,
                    session.workflow_name,
                    session.workflow_token,
                    session.current_step,
                    session.status,
                    json.dumps(session.data),
                    json.dumps(session.metadata),
                    session.created_at.isoformat(),
                    session.updated_at.isoformat()
                ))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error saving session: {e}")
            return False
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "DELETE FROM workflow_sessions WHERE session_id = ?",
                    (session_id,)
                )
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting session: {e}")
            return False
    
    def list_sessions(self, workflow_name: str = None, status: str = None) -> List[WorkflowSession]:
        """List sessions with optional filters."""
        query = "SELECT * FROM workflow_sessions"
        params = []
        conditions = []
        
        if workflow_name:
            conditions.append("workflow_name = ?")
            params.append(workflow_name)
        
        if status:
            conditions.append("status = ?")
            params.append(status)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY updated_at DESC"
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()
            
            return [self._row_to_session(row) for row in rows]
    
    def cleanup_expired_sessions(self, max_age_days: int = 30) -> int:
        """Clean up old sessions."""
        cutoff_date = datetime.now() - timedelta(days=max_age_days)
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "DELETE FROM workflow_sessions WHERE created_at < ?",
                    (cutoff_date.isoformat(),)
                )
                conn.commit()
                return cursor.rowcount
        except Exception as e:
            print(f"Error cleaning up sessions: {e}")
            return 0
    
    def _row_to_session(self, row: sqlite3.Row) -> WorkflowSession:
        """Convert a database row to a WorkflowSession object."""
        return WorkflowSession(
            session_id=row['session_id'],
            workflow_name=row['workflow_name'],
            workflow_token=row['workflow_token'],
            current_step=row['current_step'],
            status=row['status'],
            data=json.loads(row['data']),
            metadata=json.loads(row['metadata']),
            created_at=datetime.fromisoformat(row['created_at']),
            updated_at=datetime.fromisoformat(row['updated_at'])
        )
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        with sqlite3.connect(self.db_path) as conn:
            # Total sessions
            cursor = conn.execute("SELECT COUNT(*) FROM workflow_sessions")
            total_sessions = cursor.fetchone()[0]
            
            # Sessions by status
            cursor = conn.execute("""
                SELECT status, COUNT(*) 
                FROM workflow_sessions 
                GROUP BY status
            """)
            status_counts = dict(cursor.fetchall())
            
            # Sessions by workflow
            cursor = conn.execute("""
                SELECT workflow_name, COUNT(*) 
                FROM workflow_sessions 
                GROUP BY workflow_name
            """)
            workflow_counts = dict(cursor.fetchall())
            
            return {
                'total_sessions': total_sessions,
                'status_counts': status_counts,
                'workflow_counts': workflow_counts,
                'database_path': str(self.db_path)
            }