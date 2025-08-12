#!/usr/bin/env python3
"""Personal Information Collection - Employee Onboarding Step 1"""

import sys
import os

# Add the parent directory to the path so we can import modularbuilder
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from modularbuilder.skeletons.casa.app import CasaApp


class PersonalInfoApp(CasaApp):
    """Personal information collection form for new employees."""
    
    def __init__(self, name="personal-info", host='localhost', port=8001):
        super().__init__(name=name, host=host, port=port)
    
    def setup_form(self):
        """Define personal information form fields."""
        return {
            'title': 'Employee Onboarding - Personal Information',
            'fields': [
                {
                    'name': 'full_name',
                    'label': 'Full Name',
                    'type': 'text',
                    'required': True,
                    'placeholder': 'First Middle Last'
                },
                {
                    'name': 'email',
                    'label': 'Email Address',
                    'type': 'email',
                    'required': True,
                    'placeholder': 'your.email@company.com'
                },
                {
                    'name': 'phone',
                    'label': 'Phone Number',
                    'type': 'tel',
                    'required': True,
                    'placeholder': '+44 7123 456789'
                },
                {
                    'name': 'date_of_birth',
                    'label': 'Date of Birth',
                    'type': 'date',
                    'required': True
                },
                {
                    'name': 'address_line_1',
                    'label': 'Address Line 1',
                    'type': 'text',
                    'required': True,
                    'placeholder': 'Street number and name'
                },
                {
                    'name': 'address_line_2',
                    'label': 'Address Line 2',
                    'type': 'text',
                    'required': False,
                    'placeholder': 'Apartment, suite, etc. (optional)'
                },
                {
                    'name': 'city',
                    'label': 'City',
                    'type': 'text',
                    'required': True
                },
                {
                    'name': 'postcode',
                    'label': 'Postcode',
                    'type': 'text',
                    'required': True,
                    'placeholder': 'SW1A 1AA'
                },
                {
                    'name': 'emergency_contact_name',
                    'label': 'Emergency Contact Name',
                    'type': 'text',
                    'required': True,
                    'placeholder': 'Full name of emergency contact'
                },
                {
                    'name': 'emergency_contact_phone',
                    'label': 'Emergency Contact Phone',
                    'type': 'tel',
                    'required': True,
                    'placeholder': '+44 7123 456789'
                },
                {
                    'name': 'emergency_contact_relationship',
                    'label': 'Relationship to Emergency Contact',
                    'type': 'select',
                    'required': True,
                    'options': [
                        {'value': 'spouse', 'text': 'Spouse/Partner'},
                        {'value': 'parent', 'text': 'Parent'},
                        {'value': 'sibling', 'text': 'Sibling'},
                        {'value': 'child', 'text': 'Child'},
                        {'value': 'friend', 'text': 'Friend'},
                        {'value': 'other', 'text': 'Other'}
                    ]
                }
            ],
            'validation': {
                'email': {
                    'pattern': r'.+@.+\..+',
                    'message': 'Please enter a valid email address'
                },
                'phone': {
                    'pattern': r'^[\+]?[\d\s\-\(\)]{10,}$',
                    'message': 'Please enter a valid phone number'
                },
                'postcode': {
                    'pattern': r'^[A-Z]{1,2}[0-9][A-Z0-9]?\s?[0-9][A-Z]{2}$',
                    'message': 'Please enter a valid UK postcode'
                },
                'emergency_contact_phone': {
                    'pattern': r'^[\+]?[\d\s\-\(\)]{10,}$',
                    'message': 'Please enter a valid emergency contact phone number'
                }
            },
            'submit_text': 'Continue to Job Details'
        }


if __name__ == "__main__":
    app = PersonalInfoApp()
    app.run(debug=True)