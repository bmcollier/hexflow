"""Router service that coordinates application workflows based on DAG files."""

import os
import sys
from urllib.parse import urlencode
from flask import Flask, request, redirect, jsonify, session
from .dag_parser import DAGParser, DAGDefinition
from ..state import StateBackend, SQLiteBackend, WorkflowSession
from typing import Optional, Dict, Any


class Router:
    """Router service for coordinating application workflows."""
    
    def __init__(self, name: str = "router", host: str = 'localhost', port: int = 8000, dag_directory: str = None, state_backend: Optional[StateBackend] = None):
        self.host = host
        self.port = port
        self.dag_directory = dag_directory or os.getcwd()
        self.dag: Optional[DAGDefinition] = None
        self.app = Flask(name)
        self.app.secret_key = 'modular-builder-router-key'  # For session management
        
        # Initialize state backend
        if state_backend is None:
            self.state_backend = self._load_state_backend()
        else:
            self.state_backend = state_backend
        
        self.load_dag()
        self.setup_routes()
    
    def load_dag(self):
        """Load the DAG file from the specified directory."""
        dag_file = DAGParser.find_dag_file(self.dag_directory)
        if dag_file:
            try:
                self.dag = DAGParser.parse_file(dag_file)
                print(f"Loaded DAG: {self.dag.name} from {dag_file}")
            except Exception as e:
                print(f"Error loading DAG file {dag_file}: {e}")
                print("Please check that the DAG file has valid YAML format and required fields (name, apps)")
                self.dag = None
        else:
            print(f"No valid DAG file found in {self.dag_directory}")
            self.dag = None
    
    def setup_routes(self):
        """Setup runner routes."""
        @self.app.route('/')
        def index():
            if self.dag:
                return f'Modular-Builder Runner: Running workflow "{self.dag.name}"', 200
            else:
                return 'Modular-Builder Runner: No DAG loaded', 200
            
        @self.app.route('/status')
        def status():
            return 'OK', 200
        
        @self.app.route('/start')
        def start_workflow():
            """Start the workflow at the entry point."""
            if not self.dag:
                return 'No DAG loaded', 400
            
            entry_app = self.dag.get_entry_point()
            if not entry_app:
                return 'No entry point defined in DAG', 400
            
            # Create new workflow session
            workflow_session = self.state_backend.create_session(
                workflow_name=self.dag.name
            )
            
            # Store workflow token in browser session for convenience
            session['workflow_token'] = workflow_session.workflow_token
            session['workflow_started'] = True
            
            # Set current step and save
            workflow_session.current_step = entry_app.name
            self.state_backend.save_session(workflow_session)
            
            print(f"Started workflow: {workflow_session.workflow_token}")
            
            # Redirect to the entry point app with workflow token
            params = {'workflow_token': workflow_session.workflow_token}
            return redirect(f'http://localhost:{entry_app.port}?{urlencode(params)}')
        
        @self.app.route('/next', methods=['GET', 'POST'])
        def next_app():
            """Handle transition to the next app in the workflow."""
            if not self.dag:
                return 'No DAG loaded', 400
            
            current_app_name = request.args.get('from') or request.form.get('from')
            workflow_token = request.args.get('workflow_token') or request.form.get('workflow_token') or session.get('workflow_token')
            
            if not current_app_name:
                return 'Missing "from" parameter', 400
            if not workflow_token:
                return 'Missing workflow_token', 400
            
            # Get workflow session
            workflow_session = self.state_backend.get_session_by_token(workflow_token)
            if not workflow_session:
                return f'Workflow session not found: {workflow_token}', 404
            
            # Save any form data from current app
            form_data = dict(request.form) if request.method == 'POST' else {}
            if form_data:
                workflow_session.set_step_data(current_app_name, form_data)
            
            # Get the next app in the flow
            next_app_name = self.dag.get_next_app(current_app_name)
            if not next_app_name:
                # End of workflow
                workflow_session.set_status('completed')
                self.state_backend.save_session(workflow_session)
                return f'Workflow completed! Token: {workflow_token}', 200
            
            # Get the port for the next app
            next_port = self.dag.get_app_port(next_app_name)
            if not next_port:
                return f'App {next_app_name} not found', 400
            
            # Update workflow session
            workflow_session.current_step = next_app_name
            self.state_backend.save_session(workflow_session)
            
            # Prepare data to pass to next app based on data_mapping
            next_app_data = self._get_data_for_app(workflow_session, current_app_name, next_app_name)
            
            # Redirect to the next app with workflow token and data
            params = {'workflow_token': workflow_token}
            params.update(next_app_data)
            
            return redirect(f'http://localhost:{next_port}?{urlencode(params)}')
        
        @self.app.route('/dag')
        def get_dag():
            """Return the current DAG definition."""
            if not self.dag:
                return {'error': 'No DAG loaded'}, 400
            
            return {
                'name': self.dag.name,
                'description': self.dag.description,
                'apps': [{'name': app.name, 'port': app.port, 'entry_point': app.entry_point} 
                        for app in self.dag.apps],
                'flow': [{'from': step.from_app, 'to': step.to_app, 'trigger': step.trigger} 
                        for step in self.dag.flow]
            }
    
    def _get_data_for_app(self, workflow_session: WorkflowSession, from_app: str, to_app: str) -> Dict[str, Any]:
        """Get data to pass from one app to another based on data_mapping in DAG.
        
        Args:
            workflow_session: Current workflow session
            from_app: Name of the source application
            to_app: Name of the target application
            
        Returns:
            Dictionary of data to pass to the target app
        """
        if not self.dag.data_mapping:
            return {}
        
        # Find data mapping for this transition
        for mapping in self.dag.data_mapping:
            if mapping.get('from') == from_app and mapping.get('to') == to_app:
                fields = mapping.get('fields', [])
                
                # Special case: "*" means pass ALL workflow data
                if fields == "*" or (isinstance(fields, list) and len(fields) == 1 and fields[0] == "*"):
                    return self._get_all_workflow_data_flattened(workflow_session)
                
                from_app_data = workflow_session.get_step_data(from_app) or {}
                
                # Extract only specified fields
                filtered_data = {}
                for field in fields:
                    if field in from_app_data:
                        filtered_data[field] = from_app_data[field]
                
                return filtered_data
        
        return {}
    
    def _get_all_workflow_data(self, workflow_session: WorkflowSession) -> Dict[str, Any]:
        """Get all data from workflow session for display purposes.
        
        Args:
            workflow_session: Current workflow session
            
        Returns:
            Dictionary with all workflow data organized by step
        """
        return workflow_session.data
    
    def _get_all_workflow_data_flattened(self, workflow_session: WorkflowSession) -> Dict[str, Any]:
        """Get all workflow data flattened into a single dictionary for URL parameters.
        
        Args:
            workflow_session: Current workflow session
            
        Returns:
            Dictionary with all workflow data flattened (no step organization)
        """
        flattened_data = {}
        all_data = workflow_session.data
        
        # Flatten all step data into a single dictionary
        for step_name, step_data in all_data.items():
            if isinstance(step_data, dict):
                for key, value in step_data.items():
                    # Avoid overwriting keys by prefixing with step name if there's a conflict
                    if key in flattened_data and flattened_data[key] != value:
                        flattened_data[f"{step_name}_{key}"] = value
                    else:
                        flattened_data[key] = value
        
        return flattened_data
    
    def _load_state_backend(self) -> StateBackend:
        """Load state backend from workflow settings or use default."""
        settings_path = os.path.join(self.dag_directory, 'settings.py')
        
        if os.path.exists(settings_path):
            try:
                # Add directory to path temporarily
                if self.dag_directory not in sys.path:
                    sys.path.insert(0, self.dag_directory)
                    
                import settings
                
                # Get backend class and config from settings
                backend_class = getattr(settings, 'STATE_BACKEND_CLASS', SQLiteBackend)
                backend_config = getattr(settings, 'STATE_BACKEND_CONFIG', {})
                
                print(f"Loading state backend from settings: {backend_class.__name__}")
                return backend_class(**backend_config)
                
            except Exception as e:
                print(f"Error loading settings.py: {e}")
                print("Falling back to default SQLite backend")
            finally:
                # Clean up path
                if self.dag_directory in sys.path:
                    sys.path.remove(self.dag_directory)
        
        # Default fallback
        db_path = os.path.join(self.dag_directory, 'workflow_sessions.db')
        return SQLiteBackend(db_path)
    
    def run(self, debug: bool = False):
        """Start the router service."""
        print(f"Starting router on http://{self.host}:{self.port}")
        if self.dag:
            print(f"Managing workflow: {self.dag.name}")
            print(f"Entry point: http://{self.host}:{self.port}/start")
        
        self.app.run(host=self.host, port=self.port, debug=debug)
    
    def get_app(self):
        """Return the Flask app instance for WSGI deployment."""
        return self.app


if __name__ == "__main__":
    router = Router()
    router.run()