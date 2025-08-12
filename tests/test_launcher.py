"""Tests for the hexflow launcher functionality."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch

from hexflow.launcher.app_launcher import AppLauncher


class TestAppLauncher:
    """Test suite for AppLauncher functionality."""
    
    def test_init(self):
        """Test AppLauncher initialization."""
        launcher = AppLauncher("/fake/path")
        assert launcher.apps_directory == Path("/fake/path")
        assert launcher.running_apps == {}
        assert launcher.app_threads == {}
    
    def test_has_dag_file_with_dag(self, tmp_path):
        """Test has_dag_file returns True when DAG file exists."""
        dag_file = tmp_path / "workflow.dag"
        dag_file.write_text("name: test")
        
        launcher = AppLauncher(str(tmp_path))
        assert launcher.has_dag_file() is True
    
    def test_has_dag_file_without_dag(self, tmp_path):
        """Test has_dag_file returns False when no DAG file exists."""
        launcher = AppLauncher(str(tmp_path))
        assert launcher.has_dag_file() is False
    
    def test_discover_apps_empty_directory(self, tmp_path):
        """Test discover_apps with empty directory."""
        launcher = AppLauncher(str(tmp_path))
        apps = launcher.discover_apps()
        assert apps == []
    
    def test_discover_apps_with_apps(self, tmp_path):
        """Test discover_apps finds app directories."""
        # Create app structure
        app_dir = tmp_path / "test-app"
        app_dir.mkdir()
        (app_dir / "app.py").write_text("# test app")
        (app_dir / "__init__.py").write_text("")
        
        launcher = AppLauncher(str(tmp_path))
        apps = launcher.discover_apps()
        assert "test-app" in apps
    
    def test_discover_apps_with_apps_subdirectory(self, tmp_path):
        """Test discover_apps finds apps in apps/ subdirectory."""
        # Create apps subdirectory structure
        apps_dir = tmp_path / "apps"
        apps_dir.mkdir()
        app_dir = apps_dir / "sub-app"
        app_dir.mkdir()
        (app_dir / "app.py").write_text("# test app")
        (app_dir / "__init__.py").write_text("")
        
        launcher = AppLauncher(str(tmp_path))
        apps = launcher.discover_apps()
        assert "apps/sub-app" in apps