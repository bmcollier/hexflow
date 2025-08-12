#!/usr/bin/env python3
"""HR Documentation and Benefits - Employee Onboarding Step 4"""

import sys
import os
from flask import request

# Add the parent directory to the path so we can import hexflow
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from hexflow.skeletons.casa.app import CasaApp


class HRDocumentationApp(CasaApp):
    """HR documentation and benefits enrollment for new employees."""
    
    def __init__(self, name="hr-documentation", host='localhost', port=8004):
        super().__init__(name=name, host=host, port=port)
    
    def setup_form(self):
        """Define HR documentation form fields."""
        return {
            'title': 'Employee Onboarding - HR Documentation',
            'fields': [
                {
                    'name': 'national_insurance',
                    'label': 'National Insurance Number',
                    'type': 'text',
                    'required': True,
                    'placeholder': 'AB 12 34 56 C'
                },
                {
                    'name': 'bank_name',
                    'label': 'Bank Name',
                    'type': 'text',
                    'required': True,
                    'placeholder': 'Name of your bank'
                },
                {
                    'name': 'account_holder_name',
                    'label': 'Account Holder Name',
                    'type': 'text',
                    'required': True,
                    'placeholder': 'Name as it appears on your bank account'
                },
                {
                    'name': 'sort_code',
                    'label': 'Sort Code',
                    'type': 'text',
                    'required': True,
                    'placeholder': '12-34-56'
                },
                {
                    'name': 'account_number',
                    'label': 'Account Number',
                    'type': 'text',
                    'required': True,
                    'placeholder': '12345678'
                },
                {
                    'name': 'tax_code',
                    'label': 'Tax Code (if known)',
                    'type': 'text',
                    'required': False,
                    'placeholder': 'e.g. 1257L'
                },
                {
                    'name': 'pension_scheme',
                    'label': 'Pension Scheme Enrollment',
                    'type': 'select',
                    'required': True,
                    'options': [
                        {'value': 'auto_enroll', 'text': 'Auto-enroll in company pension (recommended)'},
                        {'value': 'opt_out', 'text': 'Opt out of company pension'},
                        {'value': 'existing_scheme', 'text': 'I have an existing scheme to transfer'}
                    ]
                },
                {
                    'name': 'health_insurance',
                    'label': 'Private Health Insurance',
                    'type': 'select',
                    'required': True,
                    'options': [
                        {'value': 'employee_only', 'text': 'Employee only'},
                        {'value': 'employee_partner', 'text': 'Employee + Partner'},
                        {'value': 'family', 'text': 'Family coverage'},
                        {'value': 'decline', 'text': 'Decline private health insurance'}
                    ]
                },
                {
                    'name': 'life_insurance',
                    'label': 'Life Insurance Coverage',
                    'type': 'select',
                    'required': True,
                    'options': [
                        {'value': '2x_salary', 'text': '2x annual salary (standard)'},
                        {'value': '4x_salary', 'text': '4x annual salary (enhanced)'},
                        {'value': '6x_salary', 'text': '6x annual salary (maximum)'},
                        {'value': 'decline', 'text': 'Decline life insurance'}
                    ]
                },
                {
                    'name': 'beneficiary_name',
                    'label': 'Life Insurance Beneficiary',
                    'type': 'text',
                    'required': True,
                    'placeholder': 'Full name of primary beneficiary'
                },
                {
                    'name': 'beneficiary_relationship',
                    'label': 'Relationship to Beneficiary',
                    'type': 'select',
                    'required': True,
                    'options': [
                        {'value': 'spouse', 'text': 'Spouse/Partner'},
                        {'value': 'parent', 'text': 'Parent'},
                        {'value': 'child', 'text': 'Child'},
                        {'value': 'sibling', 'text': 'Sibling'},
                        {'value': 'other', 'text': 'Other'}
                    ]
                },
                {
                    'name': 'holiday_entitlement',
                    'label': 'Additional Holiday Purchase',
                    'type': 'select',
                    'required': True,
                    'options': [
                        {'value': 'none', 'text': 'Standard 25 days + bank holidays'},
                        {'value': 'buy_5', 'text': 'Buy 5 extra days (30 total)'},
                        {'value': 'buy_10', 'text': 'Buy 10 extra days (35 total)'}
                    ]
                },
                {
                    'name': 'work_from_home',
                    'label': 'Work From Home Equipment',
                    'type': 'select',
                    'required': True,
                    'options': [
                        {'value': 'none', 'text': 'No home office setup needed'},
                        {'value': 'basic', 'text': 'Basic setup (desk, chair)'},
                        {'value': 'full', 'text': 'Full setup (desk, chair, monitor, lighting)'}
                    ]
                },
                {
                    'name': 'dietary_requirements',
                    'label': 'Dietary Requirements (for office catering)',
                    'type': 'textarea',
                    'required': False,
                    'placeholder': 'Any allergies, dietary restrictions, or preferences',
                    'rows': 3
                },
                {
                    'name': 'documentation_complete',
                    'label': 'Documentation Acknowledgment',
                    'type': 'select',
                    'required': True,
                    'options': [
                        {'value': '', 'text': 'Please confirm completion'},
                        {'value': 'confirmed', 'text': 'I confirm all information is accurate and complete'}
                    ]
                }
            ],
            'validation': {
                'national_insurance': {
                    'pattern': r'^[A-Z]{2}\s?[0-9]{2}\s?[0-9]{2}\s?[0-9]{2}\s?[A-Z]$',
                    'message': 'Please enter a valid National Insurance number (e.g. AB 12 34 56 C)'
                },
                'sort_code': {
                    'pattern': r'^[0-9]{2}-[0-9]{2}-[0-9]{2}$',
                    'message': 'Please enter sort code in format 12-34-56'
                },
                'account_number': {
                    'pattern': r'^[0-9]{8}$',
                    'message': 'Please enter an 8-digit account number'
                },
                'beneficiary_name': {
                    'min_length': 2,
                    'message': 'Please enter the full name of your beneficiary'
                },
                'documentation_complete': {
                    'pattern': r'^confirmed$',
                    'message': 'Please confirm that all information is accurate and complete'
                }
            },
            'submit_text': 'Complete Onboarding'
        }
    
    def render_form(self, errors=None):
        """Render the form with personalization."""
        # Get employee details from previous steps
        employee_name = request.args.get('full_name', 'New Employee')
        
        # Update the form title with personalization
        form_config = self.form_config.copy()
        form_config['title'] = f'Employee Onboarding - HR Documentation for {employee_name}'
        
        # Temporarily replace the form config for rendering
        original_config = self.form_config
        self.form_config = form_config
        
        # Call the parent render method
        result = super().render_form(errors)
        
        # Restore original config
        self.form_config = original_config
        
        return result


if __name__ == "__main__":
    app = HRDocumentationApp()
    app.run(debug=True)