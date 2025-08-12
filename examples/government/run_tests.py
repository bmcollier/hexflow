#!/usr/bin/env python3
"""Test runner for library card workflow."""

import sys
import subprocess
from pathlib import Path


def run_tests():
    """Run end-to-end tests for the library card workflow."""
    print("Running library card workflow tests...")
    
    # Install test dependencies if needed
    try:
        import playwright
        import pytest_playwright
    except ImportError:
        print("Installing test dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements-test.txt"], check=True)
        
    # Install Playwright browsers if needed
    try:
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], 
                      check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("Playwright browsers already installed or installation failed")
    
    # Run tests
    result = subprocess.run([
        sys.executable, "-m", "pytest", 
        "tests/",
        "-v",
        "--tb=short"
    ])
    
    return result.returncode == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)