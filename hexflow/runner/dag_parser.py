"""DAG file parser for workflow definitions."""

import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class App:
    """Represents an application in the workflow."""
    name: str
    port: int
    entry_point: bool = False


@dataclass
class FlowStep:
    """Represents a step in the workflow flow."""
    from_app: str
    to_app: str
    trigger: str
    condition: Optional[str] = None


@dataclass
class DAGDefinition:
    """Represents a complete DAG definition."""
    name: str
    description: str
    apps: List[App]
    flow: List[FlowStep]
    data_mapping: List[Dict[str, Any]]
    config: Dict[str, Any]
    
    def get_app_by_name(self, name: str) -> Optional[App]:
        """Get an app by its name."""
        for app in self.apps:
            if app.name == name:
                return app
        return None
    
    def get_entry_point(self) -> Optional[App]:
        """Get the entry point app for the workflow."""
        for app in self.apps:
            if app.entry_point:
                return app
        return None
    
    def get_next_app(self, current_app: str) -> Optional[str]:
        """Get the next app in the flow from the current app."""
        for step in self.flow:
            if step.from_app == current_app:
                # For now, just return the first match (simple linear flow)
                # Future: implement condition evaluation here
                return step.to_app
        return None
    
    def get_app_port(self, app_name: str) -> Optional[int]:
        """Get the port for a given app."""
        app = self.get_app_by_name(app_name)
        return app.port if app else None


class DAGParser:
    """Parser for DAG YAML files."""
    
    @staticmethod
    def parse_file(dag_file_path: str) -> DAGDefinition:
        """Parse a DAG file and return a DAGDefinition."""
        path = Path(dag_file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"DAG file not found: {dag_file_path}")
        
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        
        # Parse apps
        apps = []
        for app_data in data.get('apps', []):
            apps.append(App(
                name=app_data['name'],
                port=app_data['port'],
                entry_point=app_data.get('entry_point', False)
            ))
        
        # Parse flow
        flow = []
        for flow_data in data.get('flow', []):
            flow.append(FlowStep(
                from_app=flow_data['from'],
                to_app=flow_data['to'],
                trigger=flow_data['trigger'],
                condition=flow_data.get('condition')
            ))
        
        return DAGDefinition(
            name=data['name'],
            description=data['description'],
            apps=apps,
            flow=flow,
            data_mapping=data.get('data_mapping', []),
            config=data.get('config', {})
        )
    
    @staticmethod
    def find_dag_file(directory: str) -> Optional[str]:
        """Find a valid .dag file in a directory."""
        path = Path(directory)
        
        dag_files = list(path.glob("*.dag"))
        
        if not dag_files:
            return None
        
        # If only one DAG file, return it
        if len(dag_files) == 1:
            return str(dag_files[0])
        
        # Multiple DAG files - try to find a valid one
        for dag_file in dag_files:
            try:
                # Try to parse each file to see if it's valid
                with open(dag_file, 'r') as f:
                    data = yaml.safe_load(f)
                    
                # Check if it has required fields
                if (data and 
                    isinstance(data, dict) and 
                    'name' in data and 
                    'apps' in data and 
                    data['apps']):  # Must have at least one app
                    return str(dag_file)
                    
            except Exception:
                # Skip invalid files
                continue
        
        # If no valid DAG found, return the first one (fallback)
        return str(dag_files[0])