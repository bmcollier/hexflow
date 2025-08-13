"""Simple test application 1 - subclasses http-base with Next button."""

import sys
import os

# Add the hexflow package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from hexflow.skeletons.casa.app import CasaApp


class AppOne(CasaApp):
    """Test application 1 - with test form and Next button functionality."""
    
    def __init__(self, name="app-one", host='localhost', port=8001):
        super().__init__(name=name, host=host, port=port)
        
        # Set up shared test template folder 
        template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
        if os.path.exists(template_dir):
            self.app.template_folder = template_dir
    
    def setup_form(self):
        """Define a simple test form."""
        return {
            'title': 'Test Application One',
            'fields': [
                {
                    'name': 'user_input',
                    'label': 'Test Input',
                    'type': 'text',
                    'required': True,
                    'placeholder': 'Enter any test data'
                },
                {
                    'name': 'session_id',
                    'label': 'Session ID',
                    'type': 'text',
                    'required': False,
                    'placeholder': 'Optional session identifier'
                }
            ],
            'submit_text': 'Continue to App Two'
        }
    
    def render_form(self, errors=None):
        """Override to use test template."""
        from flask import render_template, request
        
        form_config = self.form_config
        errors = errors or {}
        
        # Build form fields HTML
        fields_html = []
        for field in form_config.get('fields', []):
            field_html = self.render_field(field, errors.get(field['name'], ''))
            fields_html.append(field_html)
        
        workflow_token = request.form.get('workflow_token', '') or request.args.get('workflow_token', '')
        
        # Try to use test template
        try:
            return render_template('test_form.html',
                                title=form_config.get('title', 'Test App'),
                                fields_html=fields_html,
                                submit_text=form_config.get('submit_text', 'Continue'),
                                app_name=self.name,
                                workflow_token=workflow_token)
        except Exception:
            # Fall back to parent class behavior
            return super().render_form(errors)


if __name__ == "__main__":
    app = AppOne(name="app-one", port=8001)
    app.run()