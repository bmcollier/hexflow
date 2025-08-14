#!/usr/bin/env python3
"""Application Confirmation - Library Card Application Final Step"""

import sys
import os
import random
from datetime import datetime, timedelta

# Add the parent directories to the path so we can import local skeletons
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from skeletons.gds_display import GDSDisplayApp


class ApplicationConfirmationApp(GDSDisplayApp):
    """Application confirmation page using GDS styling."""
    
    def __init__(self, name="application-confirmation", host='localhost', port=8004):
        super().__init__(name=name, host=host, port=port, service_name="Apply for a library card")
    
    def setup_display(self, workflow_data=None):
        """Configure the confirmation display."""
        # Generate library card details
        library_card_number = f"LC{datetime.now().strftime('%Y')}{random.randint(100000, 999999)}"
        application_reference = f"APP{datetime.now().strftime('%Y%m%d')}{random.randint(1000, 9999)}"
        
        return {
            'title': 'Library card application submitted',
            'sections': [
                {
                    'title': 'What happens next',
                    'items': [
                        'Your application has been successfully submitted.',
                        'You will receive a confirmation email within 24 hours.',
                        'Your library card will be ready for collection within 3-5 working days.',
                        'You will need to bring photo ID and your proof of address document when collecting your card.'
                    ]
                },
                {
                    'title': 'Your application details',
                    'items': [
                        {'label': 'Application reference', 'value': application_reference},
                        {'label': 'Library card number', 'value': library_card_number},
                        {'label': 'Application date', 'value': datetime.now().strftime('%d %B %Y')},
                        {'label': 'Card ready date', 'value': (datetime.now() + timedelta(days=5)).strftime('%d %B %Y')}
                    ]
                }
            ],
            'show_workflow_data': True,
            'completion_message': 'Thank you for applying for a library card. Save your application reference number for your records. You can contact the library service on 0300 123 4567 if you have any questions about your application.'
        }


if __name__ == "__main__":
    app = ApplicationConfirmationApp()
    app.run(debug=True)