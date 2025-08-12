"""Tests for hexflow skeleton applications."""

import pytest
from unittest.mock import Mock, patch

from hexflow.skeletons.http_base.app import HTTPBaseApp
from hexflow.skeletons.casa.app import CasaApp


class TestHTTPBaseApp:
    """Test suite for HTTPBaseApp skeleton."""
    
    def test_init(self):
        """Test HTTPBaseApp initialization."""
        app = HTTPBaseApp("test-app", "localhost", 8000)
        assert app.name == "test-app"
        assert app.host == "localhost" 
        assert app.port == 8000
        assert app.app is not None
    
    def test_setup_routes_called(self):
        """Test that setup_routes is called during initialization."""
        with patch.object(HTTPBaseApp, 'setup_routes') as mock_setup:
            app = HTTPBaseApp("test-app", "localhost", 8000)
            mock_setup.assert_called_once()


class TestCasaApp:
    """Test suite for CasaApp skeleton."""
    
    def test_init(self):
        """Test CasaApp initialization."""
        app = CasaApp("test-form", "localhost", 8001)
        assert app.name == "test-form"
        assert app.host == "localhost"
        assert app.port == 8001
        assert hasattr(app, 'form_config')
    
    def test_setup_form_returns_default_config(self):
        """Test that setup_form returns default configuration."""
        app = CasaApp("test-form", "localhost", 8001)
        config = app.setup_form()
        
        assert isinstance(config, dict)
        assert 'title' in config
        assert 'fields' in config
        assert 'validation' in config
        assert 'submit_text' in config
    
    def test_form_config_set_from_setup_form(self):
        """Test that form_config is set from setup_form method."""
        class TestCasaApp(CasaApp):
            def setup_form(self):
                return {
                    'title': 'Test Form',
                    'fields': [{'name': 'test', 'type': 'text'}],
                    'validation': {},
                    'submit_text': 'Submit'
                }
        
        app = TestCasaApp("test-form", "localhost", 8001)
        assert app.form_config['title'] == 'Test Form'
        assert len(app.form_config['fields']) == 1
        assert app.form_config['fields'][0]['name'] == 'test'