#!/usr/bin/env python3
"""Demonstration of subclassing DisplayApp with template inheritance."""

import sys
import os

# Add the hexflow package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from hexflow.skeletons.display.app import DisplayApp


class CustomDisplayApp(DisplayApp):
    """
    Custom display app that subclasses DisplayApp.
    
    This demonstrates three approaches to template usage:
    1. Inheriting parent templates automatically
    2. Overriding specific templates 
    3. Customizing template data while using parent templates
    """
    
    def __init__(self, name="custom-display", host='localhost', port=8005):
        # Call parent constructor - this sets up template folder to parent's templates
        super().__init__(name=name, host=host, port=port)
        
        # Option 1: Use parent templates automatically (no additional setup needed)
        # The parent's template_folder is already set to: src/hexflow/skeletons/display/templates
        
        # Option 2: Override with custom templates (uncomment to try)
        # custom_template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        # if os.path.exists(custom_template_dir):
        #     self.app.template_folder = custom_template_dir
    
    def setup_display(self, workflow_data=None):
        """
        Override setup_display to customize the data passed to parent templates.
        The parent's Jinja2 templates will receive this data.
        """
        workflow_data = workflow_data or {}
        
        # Create custom content using parent template structure
        return {
            'title': 'Custom Subclassed Display App',
            'sections': [
                {
                    'title': 'Subclassing Demo',
                    'items': [
                        {'label': 'Parent Class', 'value': 'DisplayApp'},
                        {'label': 'Template Source', 'value': 'Inherited from parent'},
                        {'label': 'Customization', 'value': 'Data customized in subclass'}
                    ]
                },
                {
                    'title': 'Workflow Data',
                    'items': [
                        {'label': key.replace('_', ' ').title(), 'value': value}
                        for key, value in workflow_data.items()
                    ] if workflow_data else [{'label': 'No Data', 'value': 'This is the first step'}]
                }
            ],
            'show_workflow_data': True,
            'completion_message': '✅ Subclassing with template inheritance works perfectly!'
        }


class CustomDisplayAppWithOverride(DisplayApp):
    """
    Alternative approach: subclass with custom template override.
    """
    
    def __init__(self, name="custom-display-override", host='localhost', port=8006):
        super().__init__(name=name, host=host, port=port)
        
        # Override with custom templates if they exist
        custom_template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        if os.path.exists(custom_template_dir):
            self.app.template_folder = custom_template_dir
            print(f"Using custom templates from: {custom_template_dir}")
        else:
            print(f"Using parent templates from: {self.app.template_folder}")
    
    def setup_display(self, workflow_data=None):
        """Custom display configuration."""
        return {
            'title': 'Custom Template Override Demo',
            'sections': [
                {
                    'title': 'Template Override',
                    'items': [
                        {'label': 'Template Strategy', 'value': 'Custom templates with fallback'},
                        {'label': 'Flexibility', 'value': 'Can use parent templates or override completely'}
                    ]
                }
            ],
            'completion_message': 'This shows how template overriding works!'
        }


if __name__ == "__main__":
    print("Testing template inheritance in subclassing...")
    
    # Test 1: Using parent templates
    print("\n1. Testing parent template inheritance:")
    app1 = CustomDisplayApp()
    print(f"Template folder: {app1.app.template_folder}")
    
    # Test 2: Testing template override (will fall back to parent if no custom templates)
    print("\n2. Testing template override:")
    app2 = CustomDisplayAppWithOverride()
    print(f"Template folder: {app2.app.template_folder}")
    
    # Run the first app
    print(f"\nStarting CustomDisplayApp on http://localhost:{app1.port}")
    app1.run()