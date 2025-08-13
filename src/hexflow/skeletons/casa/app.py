"""Casa application skeleton for form-based applications."""

from flask import request, render_template_string, render_template
from ..http_base.app import HTTPBaseApp
from typing import Dict, List, Any, Optional
import os


class CasaApp(HTTPBaseApp):
    """Form-based application that extends HTTPBaseApp."""
    
    def __init__(self, name: str = "casa-app", host: str = 'localhost', port: int = 8000):
        print(f"INIT DEBUG: CasaApp.__init__ called for {name}")
        try:
            super().__init__(name, host, port)
            self.name = name  # Store name for template usage
            
            # Set up template folder for Jinja2
            template_dir = os.path.join(os.path.dirname(__file__), 'templates')
            if os.path.exists(template_dir):
                self.app.template_folder = template_dir
                
            self.form_config = self.setup_form()
            print(f"INIT DEBUG: CasaApp setup complete for {name}")
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
        print(f"ROUTE DEBUG: CasaApp.setup_routes called")
        
        @self.app.route('/', methods=['GET', 'POST'])
        def form_handler():
            # Form handler for GET and POST requests
            if request.method == 'GET':
                return self.render_form()
            else:
                # Check if this is a workflow navigation POST (from router) or actual form submission
                form_data = dict(request.form)
                
                # The key insight: actual form submissions include an 'action' field from the submit button
                # Workflow navigation from router does not include this field
                is_form_submission = form_data.get('action') == 'submit'
                
                # Debug: print what we found
                # Check if user clicked submit button vs router navigation
                
                if not is_form_submission:
                    # No 'action=submit' present - this is workflow navigation from router
                    # Router navigation - display form without validation errors
                    return self.render_form()  # No errors passed = no validation errors shown
                else:
                    # 'action=submit' present - this is an actual form submission by user
                    # User form submission - validate and process
                    return self.handle_form_submission()  # This will call render_form(errors) if validation fails
    
    def render_form(self, errors: Dict[str, str] = None) -> str:
        """Render the form HTML."""
        form_config = self.form_config
        errors = errors or {}
        
        # Debug logging
        if errors:
            print(f"BASE DEBUG: Showing validation errors: {list(errors.keys())}")

        # Build form fields HTML
        fields_html = []
        for field in form_config.get('fields', []):
            field_html = self.render_field(field, errors.get(field['name'], ''))
            fields_html.append(field_html)
        
        workflow_token = request.form.get('workflow_token', '') or request.args.get('workflow_token', '')
        
        # Try to use Jinja2 template, fall back to inline template if not found
        try:
            return render_template('form.html',
                                title=form_config.get('title', 'Form'),
                                fields_html=fields_html,
                                submit_text=form_config.get('submit_text', 'Submit'),
                                app_name=self.name,
                                workflow_token=workflow_token)
        except Exception as e:
            print(f"Template error: {e}, falling back to inline template for backward compatibility")
            # Fallback to inline template for backward compatibility
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
                    </div>
                </form>
            </body>
            </html>
            '''
            
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
        """Process successfully validated form data and forward to router.
        
        Args:
            form_data: Dictionary of validated form field names and values
            
        Returns:
            HTML response with auto-submitting form to router
        """
        # Build hidden form fields for router (exclude action field)
        hidden_fields = []
        hidden_fields.append(f'<input type="hidden" name="from" value="{self.name}">')
        
        for key, value in form_data.items():
            if key != 'action':  # Don't send the action field to router
                if isinstance(value, list):
                    # Handle multiple values (like checkboxes)
                    for item in value:
                        hidden_fields.append(f'<input type="hidden" name="{key}" value="{item}">')
                else:
                    hidden_fields.append(f'<input type="hidden" name="{key}" value="{value}">')
        
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Processing...</title>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; text-align: center; padding: 50px; }}
                .processing {{ margin: 20px 0; }}
                .fallback {{ margin-top: 30px; padding: 20px; background: #f0f0f0; }}
            </style>
        </head>
        <body>
            <div class="processing">
                <h2>Processing your submission...</h2>
                <p>Please wait while we process your form and continue to the next step.</p>
            </div>
            
            <form id="router-form" action="http://localhost:8000/next" method="post">
                {''.join(hidden_fields)}
                <div class="fallback">
                    <p><strong>If this page doesn't redirect automatically:</strong></p>
                    <button type="submit" style="background: #007cba; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer;">Continue to Next Step</button>
                </div>
            </form>
            
            <script>
                // Auto-submit after a brief delay to show the processing message
                setTimeout(function() {{
                    document.getElementById('router-form').submit();
                }}, 1000);
            </script>
        </body>
        </html>
        '''


if __name__ == "__main__":
    app = CasaApp()
    app.run()