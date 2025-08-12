#!/usr/bin/env python3
"""Personal Details Collection - Library Card Application Step 1"""

import sys
import os

# Add the parent directories to the path so we can import local skeletons
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from skeletons.gds_casa import GDSCasaApp


class PersonalDetailsApp(GDSCasaApp):
    """Personal details collection for library card application using GDS styling."""
    
    def __init__(self, name="personal-details", host='localhost', port=8001):
        super().__init__(name=name, host=host, port=port)
    
    def setup_form(self):
        """Define personal details form fields."""
        config = {
            'title': 'Apply for a library card',
            'fields': [
                {
                    'name': 'full_name',
                    'label': 'Full name',
                    'type': 'text',
                    'required': True,
                    'help_text': 'Enter your name as it appears on official documents',
                    'placeholder': 'For example, John Smith'
                },
                {
                    'name': 'date_of_birth',
                    'label': 'Date of birth',
                    'type': 'date',
                    'required': True,
                    'help_text': 'For example, 27 3 1980'
                },
                {
                    'name': 'email',
                    'label': 'Email address',
                    'type': 'email',
                    'required': True,
                    'help_text': 'We\'ll use this to send you library updates and your digital library card',
                    'placeholder': 'name@example.com'
                },
                {
                    'name': 'phone',
                    'label': 'UK telephone number',
                    'type': 'tel',
                    'required': True,
                    'help_text': 'For urgent library notifications and account verification',
                    'placeholder': '07700 900 982'
                },
                {
                    'name': 'street',
                    'label': 'Street',
                    'type': 'text',
                    'required': True,
                    'placeholder': 'Building and street'
                },
                {
                    'name': 'city',
                    'label': 'Town or city',
                    'type': 'text',
                    'required': True
                },
                {
                    'name': 'postcode',
                    'label': 'Postcode',
                    'type': 'text',
                    'required': True,
                    'help_text': 'For example SW1A 1AA',
                    'placeholder': 'SW1A 1AA'
                },
                {
                    'name': 'proof_doc_type',
                    'label': 'Proof of address document type',
                    'type': 'select',
                    'required': True,
                    'help_text': 'You will need to bring this document when you collect your library card',
                    'options': [
                        {'value': 'council_tax', 'text': 'Council tax bill'},
                        {'value': 'utility_bill', 'text': 'Utility bill'},
                        {'value': 'bank_statement', 'text': 'Bank statement'}
                    ]
                }
            ],
            'validation': {
                'email': {
                    'pattern': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                    'message': 'Enter an email address in the correct format, like name@example.com'
                },
                'phone': {
                    'pattern': r'^(\+44\s?7\d{3}|\(?07\d{3}\)?)\s?\d{3}\s?\d{3}$|^(\+44\s?1\d{3}|\(?01\d{3}\)?|\+44\s?2\d{3}|\(?02\d{3}\)?)\s?\d{3}\s?\d{3}$',
                    'message': 'Enter a UK telephone number, like 07700 900 982 or 020 7946 0958'
                },
                'postcode': {
                    'pattern': r'^[A-Z]{1,2}[0-9][A-Z0-9]?\s?[0-9][A-Z]{2}$',
                    'message': 'Enter a real postcode, like SW1A 1AA'
                },
                'full_name': {
                    'min_length': 2,
                    'message': 'Enter your full name'
                }
            },
            'submit_text': 'Continue'
        }
        return config


if __name__ == "__main__":
    app = PersonalDetailsApp()
    app.run(debug=True)