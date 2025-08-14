#!/usr/bin/env python3
"""Library Preferences - Library Card Application Step 2"""

import sys
import os

# Add the parent directories to the path so we can import local skeletons
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from skeletons.gds_casa import GDSCasaApp


class LibraryPreferencesApp(GDSCasaApp):
    """Library preferences selection using GDS styling."""
    
    def __init__(self, name="library-preferences", host='localhost', port=8002):
        super().__init__(name=name, host=host, port=port, service_name="Apply for a library card")
    
    def setup_form(self):
        """Define library preferences form fields."""
        return {
            'title': 'Choose your library preferences',
            'fields': [
                {
                    'name': 'preferred_branch',
                    'label': 'Preferred library branch for collection',
                    'type': 'select',
                    'required': True,
                    'help_text': 'You can use your card at any library, but you need to collect it from one location',
                    'options': [
                        {'value': 'central_library', 'text': 'Central Library - High Street'},
                        {'value': 'north_branch', 'text': 'North Branch Library - Park Road'},
                        {'value': 'south_branch', 'text': 'South Branch Library - Mill Street'},
                        {'value': 'east_branch', 'text': 'East Branch Library - Station Road'},
                        {'value': 'west_branch', 'text': 'West Branch Library - Church Lane'}
                    ]
                },
                {
                    'name': 'comms_pref',
                    'label': 'Communication preference',
                    'type': 'select',
                    'required': True,
                    'help_text': 'We\'ll use this for overdue notices, reservation notifications, and service updates',
                    'options': [
                        {'value': 'email', 'text': 'Email'},
                        {'value': 'sms', 'text': 'SMS'},
                        {'value': 'post', 'text': 'Post'}
                    ]
                },
                {
                    'name': 'interest_categories',
                    'label': 'What are you most interested in? (optional)',
                    'type': 'textarea',
                    'required': False,
                    'help_text': 'For example: crime fiction, local history, children\'s books, digital resources, audiobooks, large print books',
                    'placeholder': 'Tell us about your reading interests so we can recommend books and events',
                    'rows': 3
                },
                {
                    'name': 'digital_services',
                    'label': 'Are you interested in digital library services?',
                    'type': 'select',
                    'required': True,
                    'help_text': 'Digital services include e-books, audiobooks, online magazines, and research databases',
                    'options': [
                        {'value': 'yes_very_interested', 'text': 'Yes, very interested'},
                        {'value': 'yes_somewhat', 'text': 'Yes, somewhat interested'},
                        {'value': 'maybe_future', 'text': 'Maybe in the future'},
                        {'value': 'no_not_interested', 'text': 'No, not interested'},
                        {'value': 'need_help', 'text': 'I\'d need help getting started'}
                    ]
                },
                {
                    'name': 'accessibility_requirements',
                    'label': 'Do you have any accessibility requirements?',
                    'type': 'select',
                    'required': False,
                    'help_text': 'This helps us provide you with the best possible service',
                    'options': [
                        {'value': '', 'text': 'No special requirements'},
                        {'value': 'large_print', 'text': 'Large print books'},
                        {'value': 'audio_books', 'text': 'Audio books and talking books'},
                        {'value': 'wheelchair_access', 'text': 'Wheelchair accessible facilities'},
                        {'value': 'hearing_loop', 'text': 'Hearing loop support'},
                        {'value': 'easy_read', 'text': 'Easy read materials'},
                        {'value': 'multiple', 'text': 'Multiple requirements (please specify in comments)'}
                    ]
                },
                {
                    'name': 'accessibility_details',
                    'label': 'Additional accessibility information (optional)',
                    'type': 'textarea',
                    'required': False,
                    'help_text': 'Please tell us about any specific requirements or adjustments we can make',
                    'placeholder': 'For example, specific formats you need or assistance you might require',
                    'rows': 3
                },
                {
                    'name': 'library_events',
                    'label': 'Would you like to hear about library events?',
                    'type': 'select',
                    'required': True,
                    'help_text': 'We run book clubs, author talks, children\'s activities, and digital skills workshops',
                    'options': [
                        {'value': 'yes_all_events', 'text': 'Yes, tell me about all events'},
                        {'value': 'yes_adult_events', 'text': 'Yes, but only adult events'},
                        {'value': 'yes_family_events', 'text': 'Yes, but only family/children events'},
                        {'value': 'no_events', 'text': 'No, I\'m not interested in events'}
                    ]
                }
            ],
            'validation': {
                'interest_categories': {
                    'max_length': 500,
                    'message': 'Please keep your interests to 500 characters or less'
                },
                'accessibility_details': {
                    'max_length': 500,
                    'message': 'Please keep accessibility details to 500 characters or less'
                }
            },
            'submit_text': 'Continue'
        }


if __name__ == "__main__":
    app = LibraryPreferencesApp()
    app.run(debug=True)