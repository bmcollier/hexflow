"""Simple test to verify the workflow is working."""

import sys
from pathlib import Path

# Import framework
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from hexflow.launcher.app_launcher import AppLauncher
import requests
import time


def test_workflow_starts():
    """Test that the workflow starts successfully."""
    launcher = AppLauncher(str(Path(__file__).parent.parent))
    
    try:
        launcher.launch_all_apps()
        time.sleep(3)  # Give services time to start
        
        # Test health check
        response = requests.get('http://localhost:8000/', timeout=5)
        assert response.status_code == 200
        
        # Test start URL
        response = requests.get('http://localhost:8000/start', timeout=5)
        assert response.status_code in [200, 302]  # 302 for redirect to first app
        
        print("✅ Workflow health checks passed")
        
    finally:
        launcher.stop_all_apps()


def test_personal_details_page_loads():
    """Test that the personal details page loads with form fields."""
    launcher = AppLauncher(str(Path(__file__).parent.parent))
    
    try:
        launcher.launch_all_apps()
        time.sleep(3)
        
        # Get the workflow start URL and follow redirect
        start_response = requests.get('http://localhost:8000/start', timeout=5)
        assert start_response.status_code == 302
        
        # Follow redirect to personal details page
        redirect_url = start_response.headers['Location']
        if not redirect_url.startswith('http'):
            redirect_url = f'http://localhost:8001{redirect_url}'
            
        page_response = requests.get(redirect_url, timeout=5)
        assert page_response.status_code == 200
        
        # Check that it contains form elements
        page_content = page_response.text
        assert 'Apply for a library card' in page_content
        assert 'full_name' in page_content
        assert 'email' in page_content
        assert 'postcode' in page_content
        
        print("✅ Personal details page loads with form fields")
        
    finally:
        launcher.stop_all_apps()


if __name__ == "__main__":
    test_workflow_starts()
    test_personal_details_page_loads()
    print("All tests passed!")