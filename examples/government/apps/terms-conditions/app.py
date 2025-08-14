#!/usr/bin/env python3
"""Terms and Conditions - Library Card Application Step 3"""

import sys
import os

# Add the parent directories to the path so we can import local skeletons
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from skeletons.gds_casa import GDSCasaApp


class TermsConditionsApp(GDSCasaApp):
    """Terms and conditions acceptance using GDS styling."""
    
    def __init__(self, name="terms-conditions", host='localhost', port=8003):
        super().__init__(name=name, host=host, port=port, service_name="Apply for a library card")
    
    def setup_form(self):
        """Define terms and conditions form fields."""
        return {
            'title': 'Terms and conditions',
            'fields': [
                {
                    'name': 'data_protection',
                    'label': 'I agree to the data protection statement',
                    'type': 'checkbox',
                    'required': True,
                    'value': 'accepted'
                },
                {
                    'name': 'code_of_conduct',
                    'label': 'I accept the library code of conduct',
                    'type': 'checkbox',
                    'required': True,
                    'value': 'accepted'
                },
                {
                    'name': 'info_accuracy',
                    'label': 'I confirm my information is accurate',
                    'type': 'checkbox',
                    'required': True,
                    'value': 'accepted'
                },
                {
                    'name': 'marketing_opt_in',
                    'label': 'I would like to receive marketing updates',
                    'type': 'checkbox',
                    'required': False,
                    'value': 'subscribed'
                }
            ],
            'validation': {
                'data_protection': {
                    'pattern': r'^accepted$',
                    'message': 'You must agree to the data protection statement'
                },
                'code_of_conduct': {
                    'pattern': r'^accepted$',
                    'message': 'You must accept the library code of conduct'
                },
                'info_accuracy': {
                    'pattern': r'^accepted$',
                    'message': 'You must confirm your information is accurate'
                }
            },
            'submit_text': 'Submit application'
        }


if __name__ == "__main__":
    app = TermsConditionsApp()
    app.run(debug=True)