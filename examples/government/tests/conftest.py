"""Pytest configuration for library card workflow tests."""

import pytest
import time
import requests
from pathlib import Path


class LibraryCardWorkflowRunner:
    """Helper class to manage library card workflow lifecycle during tests."""
    
    def __init__(self):
        self.workflow_path = Path(__file__).parent.parent
        self.base_url = "http://localhost:8000"
        
    def start(self):
        """Start the library card workflow launcher."""
        # Import and use the launcher programmatically
        import sys
        sys.path.insert(0, str(self.workflow_path.parent.parent))
        
        from hexflow.launcher.app_launcher import AppLauncher
        
        self.launcher = AppLauncher(str(self.workflow_path))
        self.launcher.launch_all_apps()
        
        # Wait for services to be ready
        self._wait_for_service()
        
    def stop(self):
        """Stop the workflow."""
        if hasattr(self, 'launcher'):
            self.launcher.stop_all_apps()
            
    def _wait_for_service(self, max_attempts=15):
        """Wait for the router service to be ready."""
        print(f"Waiting for service at {self.base_url}")
        for attempt in range(max_attempts):
            try:
                # Try a simple health check first
                response = requests.get(f"{self.base_url}/", timeout=3)
                print(f"Health check attempt {attempt + 1}: Status {response.status_code}")
                if response.status_code in [200, 404]:  # 404 is OK for root, means service is up
                    print("Service is ready!")
                    return True
            except requests.exceptions.RequestException as e:
                print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2)
        raise RuntimeError("Library card workflow service failed to start")
        
    @property 
    def start_url(self):
        """Get the workflow start URL."""
        return f"{self.base_url}/start"


@pytest.fixture(scope="session")
def library_card_workflow():
    """Fixture to manage the library card workflow for testing."""
    runner = LibraryCardWorkflowRunner()
    
    try:
        runner.start()
        yield runner
    finally:
        runner.stop()


@pytest.fixture
def workflow_url(library_card_workflow):
    """Get the library card workflow start URL."""
    return library_card_workflow.start_url