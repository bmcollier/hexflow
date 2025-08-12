"""Casa application skeleton for form-based applications."""

from flask import request, render_template_string
from ..http_base.app import HTTPBaseApp
from typing import Dict, List, Any, Optional


class CasaApp(HTTPBaseApp):
    """Form-based application that extends HTTPBaseApp."""
    
    def __init__(self, name: str = "casa-app", host: str = 'localhost', port: int = 8000):
        try:
            super().__init__(name, host, port)
            self.name = name  # Store name for template usage
            self.form_config = self.setup_form()
        except TypeError as e:
            if "unexpected keyword argument" in str(e):
                raise TypeError(f"CasaApp constructor requires 'name', 'host', and 'port' parameters. "
                              f"Use: super().__init__(name='app-name', host='localhost', port=8001)") from e
            raise
        
    def setup_form(self) -> Dict[str, Any]:
        """Override this method to define form configuration.
        
        Returns:
            Dict containing form configuration with fields, validation, etc.
        """
        return {
            'title': 'Casa Form',
            'fields': [],
            'validation': {},
            'submit_text': 'Submit'
        }
    
    def setup_routes(self):
        """Setup form routes with GET and POST handling."""
        
        @self.app.route('/', methods=['GET', 'POST'])
        def form_handler():
            if request.method == 'GET':
                return self.render_form()
            else:
                return self.handle_form_submission()
    
    def render_form(self, errors: Dict[str, str] = None) -> str:
        """Render the form HTML."""
        form_config = self.form_config
        errors = errors or {}
        
        # Build form fields HTML
        fields_html = []
        for field in form_config.get('fields', []):
            field_html = self.render_field(field, errors.get(field['name'], ''))
            fields_html.append(field_html)
        
        template = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>{{ title }}</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
                .form-group { margin-bottom: 20px; }
                label { display: block; margin-bottom: 5px; font-weight: bold; }
                input, select, textarea { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
                .error { color: red; font-size: 14px; margin-top: 5px; }
                button { background: #007cba; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
                button:hover { background: #005a87; }
                .next-button { background: #28a745; margin-left: 10px; }
                .next-button:hover { background: #218838; }
            </style>
        </head>
        <body>
            <h1>{{ title }}</h1>
            <form action="http://localhost:8000/next" method="post">
                <input type="hidden" name="from" value="{{ app_name }}">
                <input type="hidden" name="workflow_token" value="{{ workflow_token }}">
                {{ fields_html|safe }}
                <div class="form-group">
                    <button type="submit" name="action" value="submit">{{ submit_text }}</button>
                    <button type="submit" name="action" value="next" class="next-button">Next →</button>
                </div>
            </form>
        </body>
        </html>
        '''
        
        workflow_token = request.form.get('workflow_token', '') or request.args.get('workflow_token', '')
        
        return render_template_string(template, 
                                    title=form_config.get('title', 'Form'),
                                    fields_html=''.join(fields_html),
                                    submit_text=form_config.get('submit_text', 'Submit'),
                                    app_name=self.name,
                                    workflow_token=workflow_token)
    
    def render_field(self, field: Dict[str, Any], error: str = '') -> str:
        """Render a single form field."""
        field_type = field.get('type', 'text')
        field_name = field['name']
        field_label = field.get('label', field_name.replace('_', ' ').title())
        field_required = field.get('required', False)
        field_options = field.get('options', [])
        field_value = request.form.get(field_name, '') or request.args.get(field_name, '')
        
        required_attr = 'required' if field_required else ''
        error_html = f'<div class="error">{error}</div>' if error else ''
        
        if field_type == 'select':
            options_html = []
            for option in field_options:
                if isinstance(option, dict):
                    value = option['value']
                    text = option['text']
                else:
                    value = text = option
                
                selected = 'selected' if field_value == value else ''
                options_html.append(f'<option value="{value}" {selected}>{text}</option>')
            
            field_html = f'''
            <div class="form-group">
                <label for="{field_name}">{field_label}:</label>
                <select name="{field_name}" id="{field_name}" {required_attr}>
                    <option value="">Please select...</option>
                    {''.join(options_html)}
                </select>
                {error_html}
            </div>
            '''
        
        elif field_type == 'textarea':
            rows = field.get('rows', 4)
            field_html = f'''
            <div class="form-group">
                <label for="{field_name}">{field_label}:</label>
                <textarea name="{field_name}" id="{field_name}" rows="{rows}" {required_attr}>{field_value}</textarea>
                {error_html}
            </div>
            '''
        
        else:  # text, email, tel, etc.
            placeholder = field.get('placeholder', '')
            placeholder_attr = f'placeholder="{placeholder}"' if placeholder else ''
            
            field_html = f'''
            <div class="form-group">
                <label for="{field_name}">{field_label}:</label>
                <input type="{field_type}" name="{field_name}" id="{field_name}" 
                       value="{field_value}" {required_attr} {placeholder_attr}>
                {error_html}
            </div>
            '''
        
        return field_html
    
    def handle_form_submission(self) -> str:
        """Handle form submission with validation."""
        form_data = dict(request.form)
        errors = self.validate_form(form_data)
        
        if errors:
            # Re-render form with errors
            return self.render_form(errors)
        else:
            # Process successful submission
            return self.process_form(form_data)
    
    def validate_form(self, form_data: Dict[str, str]) -> Dict[str, str]:
        """Validate form data. Override this method for custom validation.
        
        Args:
            form_data: Dictionary of form field names and values
            
        Returns:
            Dictionary of field names to error messages
        """
        errors = {}
        validation_rules = self.form_config.get('validation', {})
        
        # Check required fields
        for field in self.form_config.get('fields', []):
            field_name = field['name']
            field_label = field.get('label', field_name.replace('_', ' ').title())
            
            if field.get('required', False):
                if not form_data.get(field_name, '').strip():
                    errors[field_name] = f"{field_label} is required"
            
            # Check field-specific validation rules
            field_value = form_data.get(field_name, '')
            if field_value and field_name in validation_rules:
                rule = validation_rules[field_name]
                
                if 'pattern' in rule:
                    import re
                    if not re.match(rule['pattern'], field_value):
                        errors[field_name] = rule.get('message', f"{field_label} format is invalid")
                
                if 'min_length' in rule:
                    if len(field_value) < rule['min_length']:
                        errors[field_name] = f"{field_label} must be at least {rule['min_length']} characters"
                
                if 'max_length' in rule:
                    if len(field_value) > rule['max_length']:
                        errors[field_name] = f"{field_label} must be no more than {rule['max_length']} characters"
        
        return errors
    
    def process_form(self, form_data: Dict[str, str]) -> str:
        """Process successfully validated form data. Override this method.
        
        Args:
            form_data: Dictionary of validated form field names and values
            
        Returns:
            HTML response for successful submission
        """
        workflow_token = form_data.get('workflow_token', '')
        return f'''
        <h1>Form Submitted Successfully</h1>
        <p>Thank you for your submission!</p>
        <p><strong>Data received:</strong></p>
        <ul>
        {''.join([f"<li><strong>{key}:</strong> {value}</li>" for key, value in form_data.items() if key not in ['workflow_token', 'from', 'action']])}
        </ul>
        <form action="http://localhost:8000/next" method="post">
            <input type="hidden" name="from" value="{self.name}">
            <input type="hidden" name="workflow_token" value="{workflow_token}">
            <button type="submit">Continue →</button>
        </form>
        '''


if __name__ == "__main__":
    app = CasaApp()
    app.run()