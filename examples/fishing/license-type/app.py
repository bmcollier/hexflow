from hexflow.skeletons.casa.app import CasaApp
import os

class LicenseTypeApp(CasaApp):
    """Allow users to select their fishing license type and duration."""
    
    def __init__(self, name="license-type", host='localhost', port=8002):
        super().__init__(name=name, host=host, port=port)
        
        # Set up custom template folder 
        custom_template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        if os.path.exists(custom_template_dir):
            self.app.template_folder = custom_template_dir
    
    def setup_form(self):
        """Define form fields for license type selection."""
        return {
            'title': 'Fishing License Application - License Selection',
            'description': 'Please select the type of fishing license you would like to purchase.',
            'fields': [
                {
                    'name': 'license_type',
                    'label': 'License Type',
                    'type': 'select',
                    'required': True,
                    'options': [
                        {'value': 'coarse', 'text': 'Coarse Fishing License (£30/year)'},
                        {'value': 'trout', 'text': 'Trout and Coarse License (£37/year)'},
                        {'value': 'salmon', 'text': 'Salmon and Sea Trout License (£82/year)'},
                        {'value': 'short-term-coarse', 'text': 'Short Term Coarse (1 day - £6)'},
                        {'value': 'short-term-trout', 'text': 'Short Term Trout and Coarse (1 day - £12)'},
                        {'value': 'short-term-salmon', 'text': 'Short Term Salmon (1 day - £27)'}
                    ]
                },
                {
                    'name': 'start_date',
                    'label': 'License Start Date',
                    'type': 'date',
                    'required': True,
                    'help_text': 'When would you like your license to begin?'
                },
                {
                    'name': 'disability_concession',
                    'label': 'Disability Concession',
                    'type': 'checkbox',
                    'value': 'yes',
                    'help_text': 'Check if you qualify for a disability concession (50% discount)'
                },
                {
                    'name': 'senior_concession',
                    'label': 'Senior Concession (65+)',
                    'type': 'checkbox',
                    'value': 'yes',
                    'help_text': 'Check if you are 65 or older (applies to some license types)'
                }
            ],
            'validation': {
                'license_type': {
                    'required': True,
                    'message': 'Please select a license type'
                },
                'start_date': {
                    'required': True,
                    'message': 'Please select a start date for your license'
                }
            }
        }
    
    def render_form(self, errors=None):
        """Override to use custom template name."""
        from flask import render_template, request
        
        form_config = self.form_config
        errors = errors or {}
        
        # Build form fields HTML with custom checkbox styling
        fields_html = []
        for field in form_config.get('fields', []):
            if field['type'] == 'checkbox':
                field_html = self.render_checkbox_field(field, errors.get(field['name'], ''))
            else:
                field_html = self.render_field(field, errors.get(field['name'], ''))
            fields_html.append(field_html)
        
        workflow_token = request.form.get('workflow_token', '') or request.args.get('workflow_token', '')
        
        # Try to use custom template first
        try:
            return render_template('license_form.html',
                                title=form_config.get('title', 'Form'),
                                fields_html=fields_html,
                                submit_text=form_config.get('submit_text', 'Continue'),
                                app_name=self.name,
                                workflow_token=workflow_token)
        except Exception:
            # Fall back to parent class behavior
            return super().render_form(errors)
    
    def render_checkbox_field(self, field, error=''):
        """Render checkbox with custom styling for license form."""
        field_name = field['name']
        field_label = field.get('label', field_name.replace('_', ' ').title())
        field_value = field.get('value', 'yes')
        help_text = field.get('help_text', '')
        
        from flask import request
        is_checked = request.form.get(field_name, '') == field_value or request.args.get(field_name, '') == field_value
        
        error_html = f'<div class="error">{error}</div>' if error else ''
        help_html = f'<div class="help-text">{help_text}</div>' if help_text else ''
        
        return f'''
        <div class="form-group">
            {error_html}
            <div class="checkbox-group">
                <input type="checkbox" name="{field_name}" id="{field_name}" value="{field_value}" {'checked' if is_checked else ''}>
                <label for="{field_name}">{field_label}</label>
            </div>
            {help_html}
        </div>
        '''

if __name__ == "__main__":
    app = LicenseTypeApp(name="license-type", port=8002)
    app.run()