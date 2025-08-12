"""Application launcher for discovering and starting modular apps."""

import os
import sys
import importlib.util
import threading
import time
from typing import List, Dict, Any
from pathlib import Path
from ..runner import Router


class AppLauncher:
    """Discovers and launches applications in a given directory."""
    
    def __init__(self, apps_directory: str):
        self.apps_directory = Path(apps_directory)
        self.running_apps: Dict[str, Any] = {}
        self.app_threads: Dict[str, threading.Thread] = {}
        self.router: Router = None
        self.router_thread: threading.Thread = None
        
    def has_dag_file(self) -> bool:
        """Check if the directory contains a .dag file."""
        for file_path in self.apps_directory.glob("*.dag"):
            return True
        return False
    
    def discover_apps(self) -> List[str]:
        """Discover all application directories."""
        if not self.apps_directory.exists():
            print(f"Directory {self.apps_directory} does not exist")
            return []
        
        apps = []
        
        # First, look for apps in the current directory
        for item in self.apps_directory.iterdir():
            if item.is_dir() and (item / "app.py").exists():
                apps.append(item.name)
        
        # Also look for apps in the "apps" subdirectory if it exists
        apps_subdir = self.apps_directory / "apps"
        if apps_subdir.exists() and apps_subdir.is_dir():
            for item in apps_subdir.iterdir():
                if item.is_dir() and (item / "app.py").exists():
                    apps.append(f"apps/{item.name}")
        
        return apps
    
    def load_app_class(self, app_name: str):
        """Load the application class from an app directory."""
        app_path = self.apps_directory / app_name / "app.py"
        
        if not app_path.exists():
            raise FileNotFoundError(f"No app.py found in {app_name}")
        
        # Create module spec and load the module
        # Use just the app name part for the module name (remove apps/ prefix if present)
        module_name = app_name.split('/')[-1] if '/' in app_name else app_name
        spec = importlib.util.spec_from_file_location(f"{module_name}.app", app_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not load module from {app_path}")
        
        module = importlib.util.module_from_spec(spec)
        
        # Add paths for local template discovery
        paths_to_add = [
            str(app_path.parent),  # App directory
            str(self.apps_directory),  # Project root for local templates
            str(self.apps_directory / "templates")  # Local templates directory
        ]
        
        added_paths = []
        for path in paths_to_add:
            if path not in sys.path:
                sys.path.insert(0, path)
                added_paths.append(path)
        
        try:
            spec.loader.exec_module(module)
        finally:
            # Remove added paths from sys.path
            for path in added_paths:
                if path in sys.path:
                    sys.path.remove(path)
        
        # Find the app class (look for classes that inherit from HTTPBaseApp hierarchy)
        # We want the most specific class - the one defined in this module, not imported ones
        app_class = None
        excluded_base_classes = ['HTTPBaseApp', 'CasaApp', 'DisplayApp']
        candidates = []
        
        for name in dir(module):
            obj = getattr(module, name)
            if (isinstance(obj, type) and 
                name not in excluded_base_classes and  # Exclude base classes
                hasattr(obj, '__bases__') and
                any(base_name in str(base) for base_name in ['HTTPBaseApp', 'CasaApp', 'DisplayApp'] for base in obj.__mro__)):
                # Check if this class is defined in this module (not imported)
                if obj.__module__ == module.__name__:
                    candidates.append(obj)
        
        if len(candidates) == 1:
            app_class = candidates[0]
        elif len(candidates) > 1:
            # If multiple candidates, pick the one that doesn't have any subclasses in the candidates
            for candidate in candidates:
                is_base_of_others = any(issubclass(other, candidate) and other != candidate for other in candidates)
                if not is_base_of_others:
                    app_class = candidate
                    break
        
        # Fallback to first candidate if no clear winner
        if app_class is None and candidates:
            app_class = candidates[0]
        
        if app_class is None:
            raise ValueError(f"No suitable app class found in {app_name}")
        
        return app_class
    
    def launch_app(self, app_name: str, port: int = None):
        """Launch a single application."""
        try:
            app_class = self.load_app_class(app_name)
            
            # Use specified port or fallback to auto-assigned
            if port is None:
                port = 8001 + len(self.running_apps)
            
            # Use just the app name part (remove apps/ prefix if present)
            instance_name = app_name.split('/')[-1] if '/' in app_name else app_name
            app_instance = app_class(name=instance_name, host='localhost', port=port)
            
            # Store the app instance
            self.running_apps[app_name] = app_instance
            
            # Start the app in a background thread
            def run_app():
                print(f"Starting {app_name} on port {port}")
                try:
                    app_instance.run(debug=False)
                except Exception as e:
                    print(f"Error running {app_name}: {e}")
            
            thread = threading.Thread(target=run_app, daemon=True)
            thread.start()
            self.app_threads[app_name] = thread
            
            # Give the app a moment to start
            time.sleep(0.5)
            
            print(f"Launched {app_name} at http://localhost:{port}")
            
        except Exception as e:
            print(f"Failed to launch {app_name}: {e}")
    
    def launch_router(self):
        """Launch the router service."""
        try:
            self.router = Router(dag_directory=str(self.apps_directory), port=8000)
            
            def run_router():
                print("Starting router on port 8000")
                try:
                    self.router.run(debug=False)
                except Exception as e:
                    print(f"Error running router: {e}")
            
            self.router_thread = threading.Thread(target=run_router, daemon=True)
            self.router_thread.start()
            
            # Give the router a moment to start
            time.sleep(0.5)
            
            print("Launched router at http://localhost:8000")
            print("Start workflow at: http://localhost:8000/start")
            
        except Exception as e:
            print(f"Failed to launch router: {e}")
    
    def launch_all_apps(self):
        """Discover and launch all applications."""
        # Check for .dag file requirement
        if not self.has_dag_file():
            print(f"Error: No .dag file found in {self.apps_directory}")
            print("A .dag file is required to launch applications")
            return []
        
        # Launch the router first
        self.launch_router()
        
        # Get port mappings from the DAG if router loaded successfully
        port_mapping = {}
        if self.router and self.router.dag:
            for app in self.router.dag.apps:
                port_mapping[app.name] = app.port
            
        apps = self.discover_apps()
        print(f"Discovered apps: {apps}")
        
        for app_name in apps:
            # Use port from DAG if available, otherwise auto-assign
            # Strip "apps/" prefix when looking up in DAG since DAG uses bare names
            dag_app_name = app_name.split('/')[-1] if '/' in app_name else app_name
            port = port_mapping.get(dag_app_name)
            self.launch_app(app_name, port=port)
        
        print(f"Launched {len(apps)} applications")
        return list(self.running_apps.keys())
    
    def stop_all_apps(self):
        """Stop all running applications and router."""
        # Stop router first
        if self.router:
            try:
                print("Stopped router")
            except Exception as e:
                print(f"Error stopping router: {e}")
            self.router = None
            self.router_thread = None
        
        # Stop apps
        for app_name, app_instance in self.running_apps.items():
            try:
                # If the app has a stop method, call it
                if hasattr(app_instance, 'stop'):
                    app_instance.stop()
                print(f"Stopped {app_name}")
            except Exception as e:
                print(f"Error stopping {app_name}: {e}")
        
        self.running_apps.clear()
        self.app_threads.clear()
    
    def get_running_apps(self) -> List[str]:
        """Get list of currently running applications."""
        return list(self.running_apps.keys())


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python app_launcher.py <apps_directory>")
        sys.exit(1)
    
    launcher = AppLauncher(sys.argv[1])
    try:
        launcher.launch_all_apps()
        print("Press Ctrl+C to stop all applications")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping all applications...")
        launcher.stop_all_apps()