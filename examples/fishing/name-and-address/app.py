from hexflow.skeletons.casa.app import CasaApp
import os

class NameAndAddressApp(CasaApp):
    """Collect name and address information for British fishing license applicants."""
    
    def __init__(self, name="name-and-address", host='localhost', port=8001):
        super().__init__(name=name, host=host, port=port)
        
        # Set up custom template folder 
        custom_template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        if os.path.exists(custom_template_dir):
            self.app.template_folder = custom_template_dir
    
    def setup_form(self):
        """Define form fields for name and address collection."""
        return {
            'title': 'Fishing License Application - Personal Details',
            'description': 'Please provide your full name and address.',
            'fields': [
                {
                    'name': 'full_name',
                    'label': 'Full Name',
                    'type': 'text',
                    'required': True,
                    'placeholder': 'Enter your full legal name'
                },
                {
                    'name': 'address_line1',
                    'label': 'Address Line 1',
                    'type': 'text',
                    'required': True,
                    'placeholder': 'House number and street name'
                },
                {
                    'name': 'address_line2',
                    'label': 'Address Line 2',
                    'type': 'text',
                    'required': False,
                    'placeholder': 'Optional - apartment, suite, etc.'
                },
                {
                    'name': 'city',
                    'label': 'City/Town',
                    'type': 'text',
                    'required': True,
                    'placeholder': 'Enter your city or town'
                },
                {
                    'name': 'postcode',
                    'label': 'Postcode',
                    'type': 'text',
                    'required': True,
                    'placeholder': 'e.g. SW1A 1AA'
                }
            ],
            'validation': {
                'full_name': {
                    'min_length': 2,
                    'message': 'Full name must be at least 2 characters'
                },
                'postcode': {
                    'pattern': r'^[A-Z]{1,2}[0-9][A-Z0-9]?\s?[0-9][A-Z]{2}$',
                    'message': 'Please enter a valid UK postcode'
                }
            }
        }
    
    def render_form(self, errors=None):
        """Override to use custom template name."""
        from flask import render_template, render_template_string, request
        
        form_config = self.form_config
        errors = errors or {}
        
        # Build form fields HTML
        fields_html = []
        for field in form_config.get('fields', []):
            field_html = self.render_field(field, errors.get(field['name'], ''))
            fields_html.append(field_html)
        
        workflow_token = request.form.get('workflow_token', '') or request.args.get('workflow_token', '')
        
        # Try to use custom template first
        try:
            return render_template('custom_form.html',
                                title=form_config.get('title', 'Form'),
                                fields_html=fields_html,
                                submit_text=form_config.get('submit_text', 'Submit'),
                                app_name=self.name,
                                workflow_token=workflow_token)
        except Exception:
            # Fall back to parent class behavior
            return super().render_form(errors)

if __name__ == "__main__":
    app = NameAndAddressApp(name="name-and-address", port=8001)
    app.run()