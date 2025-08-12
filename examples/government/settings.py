"""Configuration settings for the government services workflow."""

import os
from hexflow.state import SQLiteBackend

# State backend configuration
STATE_BACKEND_CLASS = SQLiteBackend
STATE_BACKEND_CONFIG = {
    'db_path': os.path.join(os.path.dirname(__file__), 'government_sessions.db')
}

# Workflow settings
WORKFLOW_TIMEOUT = 1800  # 30 minutes
CLEANUP_SESSIONS_OLDER_THAN = 30  # days
DEBUG = False