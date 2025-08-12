"""Display application skeleton for read-only confirmation pages."""

from flask import request, render_template_string, has_request_context
from ..http_base.app import HTTPBaseApp
from typing import Dict, List, Any, Optional


class DisplayApp(HTTPBaseApp):
    """Display-only application that shows information without collecting input."""
    
    def __init__(self, name: str = "display-app", host: str = 'localhost', port: int = 8000):
        try:
            super().__init__(name, host, port)
            self.name = name  # Store name for template usage
            # Don't call setup_display() here - it may need request context
        except TypeError as e:
            if "unexpected keyword argument" in str(e):
                raise TypeError(f"DisplayApp constructor requires 'name', 'host', and 'port' parameters. "
                              f"Use: super().__init__(name='app-name', host='localhost', port=8001)") from e
            raise
        
    def get_workflow_data(self) -> Dict[str, Any]:
        """Get workflow data passed from previous steps.
        
        Returns:
            Dict containing workflow data if request context is available, empty dict otherwise.
        """
        if not has_request_context():
            return {}
        
        # Get all workflow data passed from router  
        workflow_params = dict(request.form) if request.method == 'POST' else dict(request.args)
        workflow_params.pop('workflow_token', None)  # Remove token from data
        return workflow_params
    
    def setup_display(self, workflow_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Override this method to define display configuration.
        
        Args:
            workflow_data: Dictionary containing data passed from previous workflow steps
        
        Returns:
            Dict containing display configuration with title, sections, etc.
        """
        workflow_data = workflow_data or {}
        
        return {
            'title': 'Confirmation',
            'sections': [],
            'show_workflow_data': True,
            'completion_message': 'Thank you! Your submission has been completed.'
        }
    
    def setup_routes(self):
        """Setup display routes - override this method in subclasses for custom behavior."""
        
        @self.app.route('/', methods=['GET', 'POST'])
        def display_handler():
            # Get workflow data directly in route handler (like HTTPBaseApp pattern)
            workflow_data = dict(request.form) if request.method == 'POST' else dict(request.args)
            workflow_token = workflow_data.pop('workflow_token', '')
            
            # Call setup_display with direct access to workflow data
            display_config = self.setup_display(workflow_data)
            
            # Build sections HTML
            sections_html = []
            for section in display_config.get('sections', []):
                section_html = self.render_section(section)
                sections_html.append(section_html)
            
            # Get workflow data if requested
            workflow_data_html = ''
            if display_config.get('show_workflow_data', False):
                workflow_data_html = self.render_workflow_data(workflow_data)
            
            template = '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>{{ title }}</title>
                <style>
                    body { font-family: Arial, sans-serif; max-width: 700px; margin: 50px auto; padding: 20px; }
                    .header { text-align: center; margin-bottom: 30px; }
                    .section { background: #f8f9fa; padding: 20px; margin-bottom: 20px; border-radius: 8px; border-left: 4px solid #007cba; }
                    .section h3 { margin-top: 0; color: #007cba; }
                    .data-item { margin-bottom: 10px; }
                    .data-label { font-weight: bold; color: #333; }
                    .data-value { color: #666; margin-left: 10px; }
                    .completion-message { background: #d4edda; color: #155724; padding: 15px; border-radius: 8px; text-align: center; margin-top: 30px; border: 1px solid #c3e6cb; }
                    .workflow-data { background: #fff; border: 1px solid #ddd; padding: 20px; border-radius: 8px; }
                    .workflow-step { margin-bottom: 15px; }
                    .step-title { font-weight: bold; color: #007cba; margin-bottom: 8px; }
                    .empty-data { color: #999; font-style: italic; }
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>{{ title }}</h1>
                </div>
                
                {{ sections_html|safe }}
                {{ workflow_data_html|safe }}
                
                <div class="completion-message">
                    {{ completion_message }}
                </div>
            </body>
            </html>
            '''
            
            return render_template_string(template,
                                        title=display_config.get('title', 'Confirmation'),
                                        sections_html=''.join(sections_html),
                                        workflow_data_html=workflow_data_html,
                                        completion_message=display_config.get('completion_message', 'Thank you!'))
    
    def render_section(self, section: Dict[str, Any]) -> str:
        """Render a display section."""
        section_title = section.get('title', 'Section')
        section_items = section.get('items', [])
        
        items_html = []
        for item in section_items:
            if isinstance(item, dict):
                label = item.get('label', 'Item')
                value = item.get('value', '')
                items_html.append(f'''
                <div class="data-item">
                    <span class="data-label">{label}:</span>
                    <span class="data-value">{value}</span>
                </div>
                ''')
            else:
                items_html.append(f'<div class="data-item">{item}</div>')
        
        return f'''
        <div class="section">
            <h3>{section_title}</h3>
            {''.join(items_html) if items_html else '<div class="empty-data">No data to display</div>'}
        </div>
        '''
    
    def render_workflow_data(self, workflow_data: Dict[str, Any]) -> str:
        """Render workflow data from all previous steps.
        
        Args:
            workflow_data: Dictionary containing data passed from previous workflow steps
        
        Returns:
            HTML string displaying the workflow data
        """
        if not workflow_data:
            return '<div class="workflow-data"><div class="empty-data">No workflow data available</div></div>'
        
        data_html = []
        for key, value in workflow_data.items():
            if isinstance(value, list) and len(value) == 1:
                value = value[0]  # Flatten single-item lists from form data
            
            # Handle list values (like from checkboxes)
            if isinstance(value, list):
                value = ', '.join(str(v) for v in value)
            
            display_key = key.replace('_', ' ').title()
            data_html.append(f'''
            <div class="data-item">
                <span class="data-label">{display_key}:</span>
                <span class="data-value">{value}</span>
            </div>
            ''')
        
        return f'''
        <div class="workflow-data">
            <div class="step-title">Workflow Data</div>
            {''.join(data_html)}
        </div>
        '''


if __name__ == "__main__":
    app = DisplayApp()
    app.run()